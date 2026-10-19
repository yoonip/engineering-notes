"""AI-assisted independent educational implementation of a reference recipe.

This helper implements explicitly declared training choices, not a missing original
TruncConv2d kernel, checkpoint, quantization metadata or reported accuracy.
The manuscript leaves several implementation choices unspecified; these are
recorded explicitly in recipe_config(). No EMA, SWA, DropPath or integer
quantization is implemented by this module. The caller supplies the model.

Public API:
  build_transform('cifar10' | 'cifar100')
  build_training_transform(mean, std)
  repeat_dataset(dataset, repeats=3)
  mix_batch(x, labels, num_classes) -> (mixed_x, soft_targets)
  sam_step(model, optimizer, mixed_x, soft_targets) -> (loss_float, logits)
  make_optimizer(model), make_scheduler(optimizer, epochs=300)

SAM uses the same already augmented/mixed batch and soft targets for both
passes. BatchNorm continues using batch statistics on pass two, while running
statistics AND num_batches_tracked are updated only on pass one. AMP is disabled
inside sam_step, and model and input parameters should be FP32.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import math
from pathlib import Path
from typing import Sequence

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset
from torchvision import transforms

NORMALIZATION = {
    'cifar10': {'mean': (.491, .482, .446), 'std': (.202, .199, .201)},
    'cifar100': {'mean': (.507, .487, .441), 'std': (.267, .257, .276)},
}


def recipe_config(dataset: str = 'cifar10') -> dict:
    key = dataset.lower().replace('-', '')
    if key not in NORMALIZATION:
        raise ValueError('dataset must be cifar10 or cifar100')
    return {
        'status': 'Independent implementation of the stated recipe; original accuracy unverified',
        'dataset': key,
        'normalization': NORMALIZATION[key],
        'augmentation_order': ['RandomCrop(32, zero padding=4)',
                               'RandomHorizontalFlip(p=0.5)',
                               'RandAugment(num_ops=2, magnitude=9)',
                               'ToTensor', 'Normalize'],
        'randaugment_implementation': 'torchvision RandAugment default nearest interpolation and fill',
        'repeat_augmentation': 3,
        'repeat_implementation': 'Each source item has exactly 3 indices; transform is rerun per access',
        'mixing': {'probability_mixup': .5, 'mixup_alpha': .2, 'cutmix_alpha': 1.,
                   'selection': 'one method per batch, one beta lambda per batch',
                   'cutmix_labels': 'recomputed from actual clipped patch area'},
        'label_smoothing': .1,
        'sam': {'rho': .05, 'adaptive': False, 'passes_per_batch': 2,
                'batch_reused': True, 'bn_running_updates': 'first pass only',
                'amp': False, 'model_randomness': 'independently sampled stochastic model masks'},
        'optimizer': {'type': 'SGD', 'lr': .1, 'momentum': .9, 'weight_decay': 5e-4},
        'scheduler': {'type': 'CosineAnnealingLR', 'T_max': 300, 'eta_min': 0.,
                      'step': 'once after each epoch'},
        'batch_size': 128,
        'not_implemented_here': ['EMA', 'SWA', 'DropPath', 'integer quantizer',
                                 'original truncated convolution kernel', 'automatic k tuner'],
        'sources': ['Recipe hyperparameters are declared above; reference manuscript and slides are not distributed',
                    'SAM algorithm reference: https://github.com/google-research/sam'],
    }


def build_training_transform(mean: Sequence[float], std: Sequence[float]):
    """PIL/uint8 CIFAR image -> normalized floating-point CHW tensor."""
    return transforms.Compose([
        transforms.RandomCrop(32, padding=4, padding_mode='constant', fill=0),
        transforms.RandomHorizontalFlip(p=.5),
        transforms.RandAugment(num_ops=2, magnitude=9),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ])


def build_transform(dataset: str = 'cifar10'):
    key = dataset.lower().replace('-', '')
    if key not in NORMALIZATION:
        raise ValueError('dataset must be cifar10 or cifar100')
    return build_training_transform(**NORMALIZATION[key])


class RepeatedDataset(Dataset):
    """Three independently augmented accesses per underlying source item.

    Wrap an already transformed dataset or transformed training Subset. Shuffle
    this expanded dataset in DataLoader. This is an explicit implementation
    choice rather than a claim to reproduce an unspecified original sampler.
    """
    def __init__(self, dataset: Dataset, repeats: int = 3):
        if not isinstance(repeats, int) or repeats < 1:
            raise ValueError('repeats must be a positive integer')
        self.dataset = dataset
        self.repeats = repeats

    def __len__(self):
        return self.repeats * len(self.dataset)

    def __getitem__(self, index):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return self.dataset[index % len(self.dataset)]


def repeat_dataset(dataset: Dataset, repeats: int = 3) -> RepeatedDataset:
    return RepeatedDataset(dataset, repeats)


def mix_batch(x: torch.Tensor, y: torch.Tensor, num_classes: int,
              mixup_alpha: float = .2, cutmix_alpha: float = 1.,
              mixup_probability: float = .5, *, method: str = 'auto',
              return_info: bool = False):
    """Apply either Mixup or CutMix and return soft class probabilities.

    Default selection has equal 50% probability. 'method' can force a branch for
    implementation smoke tests; it should remain 'auto' for the stated recipe.
    Labels are unsmoothed here; sam_step applies label smoothing once.
    """
    if x.ndim != 4 or x.shape[0] == 0 or y.shape[0] != x.shape[0]:
        raise ValueError('x must be nonempty NCHW; y must have matching batch size')
    if num_classes < 2 or min(mixup_alpha, cutmix_alpha) <= 0:
        raise ValueError('num_classes >= 2 and positive beta alpha are required')
    if not 0 <= mixup_probability <= 1 or method not in ('auto', 'mixup', 'cutmix'):
        raise ValueError('invalid mixing probability or method')
    if y.ndim == 1:
        target = F.one_hot(y.to(device=x.device, dtype=torch.int64), num_classes).float()
    elif y.ndim == 2 and y.shape[1] == num_classes:
        target = y.to(device=x.device, dtype=torch.float32)
    else:
        raise ValueError('labels must be class indices or N x num_classes probabilities')
    if method == 'auto':
        method = 'mixup' if torch.rand(()).item() < mixup_probability else 'cutmix'
    alpha = mixup_alpha if method == 'mixup' else cutmix_alpha
    lam_drawn = float(torch.distributions.Beta(alpha, alpha).sample().item())
    permutation = torch.randperm(x.shape[0], device=x.device)
    box = None
    if method == 'mixup':
        lam = lam_drawn
        mixed_x = x * lam + x[permutation] * (1. - lam)
    else:
        height, width = x.shape[-2:]
        ratio = math.sqrt(1. - lam_drawn)
        box_w, box_h = int(width * ratio), int(height * ratio)
        cx, cy = int(torch.randint(width, ()).item()), int(torch.randint(height, ()).item())
        x0, x1 = max(cx - box_w // 2, 0), min(cx + box_w // 2, width)
        y0, y1 = max(cy - box_h // 2, 0), min(cy + box_h // 2, height)
        mixed_x = x.clone()
        mixed_x[:, :, y0:y1, x0:x1] = x[permutation, :, y0:y1, x0:x1]
        lam = 1. - ((x1 - x0) * (y1 - y0)) / (height * width)
        box = [x0, y0, x1, y1]
    mixed_target = target * lam + target[permutation] * (1. - lam)
    info = {'method': method, 'lambda_drawn': lam_drawn,
            'lambda_actual': lam, 'box_xyxy': box}
    return (mixed_x, mixed_target, info) if return_info else (mixed_x, mixed_target)


def soft_target_cross_entropy(logits: torch.Tensor, target: torch.Tensor,
                              label_smoothing: float = .1):
    if not 0 <= label_smoothing < 1:
        raise ValueError('label_smoothing must be in [0,1)')
    if target.ndim == 1:
        target = F.one_hot(target.long(), logits.shape[-1]).float()
    if target.shape != logits.shape:
        raise ValueError('soft target shape must equal logits shape')
    target = target.to(device=logits.device, dtype=torch.float32)
    target = target * (1. - label_smoothing) + label_smoothing / logits.shape[-1]
    return -(target * F.log_softmax(logits.float(), dim=-1)).sum(dim=-1).mean()


@contextmanager
def _bn_without_running_updates(model):
    settings = [(m, m.track_running_stats) for m in model.modules()
                if isinstance(m, nn.modules.batchnorm._BatchNorm)]
    try:
        for m, _ in settings:
            m.track_running_stats = False
        yield
    finally:
        for m, value in settings:
            m.track_running_stats = value


def sam_step(model: nn.Module, optimizer: torch.optim.Optimizer,
             x: torch.Tensor, soft_targets: torch.Tensor, rho: float = .05,
             label_smoothing: float = .1):
    """One nonadaptive SAM + base-optimizer update; return loss and logits.

    model must be in training mode. Returned logits/loss are from the original
    weights' first pass. Optimizer.step uses second-pass gradients after exact
    restoration of the original weights. This method does not own a scheduler.
    """
    if not model.training:
        raise ValueError('Call model.train() before sam_step')
    if rho < 0:
        raise ValueError('rho must be nonnegative')
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast(device_type=x.device.type, enabled=False):
        logits = model(x.float())
        first_loss = soft_target_cross_entropy(logits, soft_targets, label_smoothing)
    if not torch.isfinite(first_loss):
        raise FloatingPointError('Nonfinite SAM first-pass loss')
    first_loss.backward()
    parameters = [p for group in optimizer.param_groups for p in group['params']
                  if p.grad is not None]
    if not parameters:
        raise RuntimeError('SAM first pass produced no gradients')
    device = parameters[0].device
    norm = torch.linalg.vector_norm(torch.stack([
        torch.linalg.vector_norm(p.grad.detach()).to(device) for p in parameters]))
    if not torch.isfinite(norm):
        optimizer.zero_grad(set_to_none=True)
        raise FloatingPointError('Nonfinite SAM first-pass gradient norm')
    original = []
    try:
        with torch.no_grad():
            scale = rho / (norm + 1e-12)
            for p in parameters:
                original.append((p, p.detach().clone()))
                p.add_(p.grad * scale.to(p.device))
        optimizer.zero_grad(set_to_none=True)
        with _bn_without_running_updates(model), torch.autocast(device_type=x.device.type, enabled=False):
            second_logits = model(x.float())
            second_loss = soft_target_cross_entropy(second_logits, soft_targets, label_smoothing)
        if not torch.isfinite(second_loss):
            raise FloatingPointError('Nonfinite SAM second-pass loss')
        second_loss.backward()
        if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in parameters):
            raise FloatingPointError('Nonfinite SAM second-pass gradient')
    except Exception:
        optimizer.zero_grad(set_to_none=True)
        raise
    finally:
        with torch.no_grad():
            for p, value in original:
                p.copy_(value)
    optimizer.step()
    return float(first_loss.detach().item()), logits.detach()


def make_optimizer(model: nn.Module, lr: float = .1):
    return torch.optim.SGD(model.parameters(), lr=lr, momentum=.9, weight_decay=5e-4)


def make_scheduler(optimizer: torch.optim.Optimizer, epochs: int = 300):
    return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=0.)


def smoke_test(output: Path):
    """Two CPU updates validate implementation only, never research accuracy."""
    from PIL import Image
    import numpy as np
    torch.manual_seed(2026)
    torch.set_num_threads(2)
    model = nn.Sequential(nn.Conv2d(3, 8, 3, padding=1, bias=False), nn.BatchNorm2d(8),
                          nn.ReLU(), nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(8, 10))
    model.train()
    optimizer = make_optimizer(model)
    scheduler = make_scheduler(optimizer)
    bn = model[1]
    image = Image.fromarray(np.random.default_rng(2026).integers(0, 256, (32, 32, 3), dtype=np.uint8))
    transform_checks = {}
    for dataset in ('cifar10', 'cifar100'):
        value = build_transform(dataset)(image)
        assert value.shape == (3, 32, 32) and torch.isfinite(value).all()
        transform_checks[dataset] = {'shape': list(value.shape), 'finite': True}
    base = torch.utils.data.TensorDataset(torch.arange(5))
    repeated = repeat_dataset(base)
    occurrences = [0] * 5
    for idx in range(len(repeated)):
        occurrences[int(repeated[idx][0])] += 1
    assert occurrences == [3] * 5
    rows = []
    for method in ('mixup', 'cutmix'):
        x = torch.randn(8, 3, 8, 8)
        labels = torch.arange(8) % 10
        mixed_x, targets, info = mix_batch(x, labels, 10, method=method, return_info=True)
        assert torch.allclose(targets.sum(-1), torch.ones(8)) and (targets >= 0).all()
        before = [p.detach().clone() for p in model.parameters()]
        counter_before = int(bn.num_batches_tracked)
        loss, logits = sam_step(model, optimizer, mixed_x, targets)
        changed = sum(float((p.detach() - old).abs().sum()) for p, old in zip(model.parameters(), before))
        assert changed > 0 and math.isfinite(loss)
        assert torch.isfinite(logits).all()
        assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
        assert int(bn.num_batches_tracked) == counter_before + 1
        assert bn.track_running_stats
        rows.append({'step': len(rows) + 1, **info, 'loss': loss,
                     'parameter_update_l1': changed, 'finite_gradients': True,
                     'soft_target_rows_sum_to_one': True, 'bn_running_updates': 1})
    initial_lr = optimizer.param_groups[0]['lr']
    scheduler.step()
    assert optimizer.param_groups[0]['lr'] < initial_lr
    result = {'status': 'passed', 'scope': 'Two CPU smoke updates only; no dataset training or accuracy claim',
              'device': 'cpu', 'torch_version': torch.__version__,
              'steps': rows, 'transform_checks': transform_checks,
              'repeat_counts': occurrences, 'cosine_initial_lr': initial_lr,
              'cosine_lr_after_one_epoch': optimizer.param_groups[0]['lr'],
              'recipe_config': recipe_config()}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke', action='store_true', help='Run two CPU implementation smoke steps')
    parser.add_argument('--dataset', choices=['cifar10', 'cifar100'], default='cifar10')
    parser.add_argument('--output', type=Path, default=Path('results/recipe_smoke.json'))
    args = parser.parse_args()
    if args.smoke:
        smoke_test(args.output)
    else:
        print(json.dumps(recipe_config(args.dataset), ensure_ascii=False, indent=2))
