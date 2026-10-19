"""MNIST CNN: 학습/검증/최종 시험을 분리하고 실제 loss/정확도를 저장한다."""
import argparse
import csv
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms


class DigitCNN(nn.Module):
    """[N,1,28,28] 영상 -> [N,10] 클래스별 logit(정규화 전 점수)."""
    def __init__(self):
        super().__init__()
        # padding=1로 3x3 합성곱 전후 높이/너비를 유지한다.
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),  # 28 -> 14: 작은 위치 이동에 덜 민감하게 압축.
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),  # 14 -> 7: 결과 [N,32,7,7].
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(32 * 7 * 7, 64), nn.ReLU(),
            nn.Dropout(0.2),  # 학습할 때만 일부 활성값을 지워 과적합을 완화.
            nn.Linear(64, 10),
        )

    def forward(self, x):
        # softmax를 붙이지 않는다: CrossEntropyLoss가 log-softmax까지 계산.
        return self.classifier(self.features(x))


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)


def train_epoch(model, loader, optimizer, criterion, device):
    model.train()  # dropout ON; 이것 자체가 가중치를 변경하는 것은 아니다.
    loss_sum, correct, count = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad(set_to_none=True)  # 이전 batch의 gradient 제거.
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()  # chain rule로 각 파라미터의 loss 미분 계산.
        optimizer.step()  # Adam이 gradient를 이용해 파라미터를 갱신.
        n = labels.numel()
        # 마지막 작은 batch도 동일한 '샘플당 평균'에 기여하도록 n을 곱함.
        loss_sum += loss.item() * n
        correct += (logits.argmax(dim=1) == labels).sum().item()
        count += n
    return loss_sum / count, correct / count


@torch.inference_mode()  # 역전파용 그래프를 만들지 않아 추론 메모리를 줄임.
def evaluate(model, loader, criterion, device):
    model.eval()  # dropout OFF. inference_mode와 목적이 다르다.
    loss_sum, correct, count = 0.0, 0, 0
    confusion = torch.zeros((10, 10), dtype=torch.int64)
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        pred = logits.argmax(dim=1)
        n = labels.numel()
        loss_sum += criterion(logits, labels).item() * n
        correct += (pred == labels).sum().item()
        count += n
        # 행=정답, 열=예측. (정답*10+예측)을 한 번에 세어 10x10으로 복원.
        confusion += torch.bincount(
            (labels * 10 + pred).cpu(), minlength=100
        ).reshape(10, 10)
    return loss_sum / count, correct / count, confusion


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--epochs', type=int, default=5)
    ap.add_argument('--batch-size', type=int, default=128)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--device', choices=['cpu', 'cuda'], default='cpu')
    ap.add_argument('--data', type=Path, default=Path('data'))
    ap.add_argument('--out', type=Path, default=Path('results'))
    args = ap.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        raise ValueError('epochs and batch-size must be positive')
    seed_all(args.seed)
    torch.set_num_threads(args.threads)
    device = torch.device(args.device)
    args.out.mkdir(parents=True, exist_ok=True)
    transform = transforms.Compose([
        transforms.ToTensor(),  # uint8 [0,255] -> float32 [0,1], CHW 배치.
        transforms.Normalize((0.1307,), (0.3081,)),  # (x-평균)/표준편차.
    ])
    full_train = datasets.MNIST(args.data, train=True, download=True,
                                transform=transform)
    test_set = datasets.MNIST(args.data, train=False, download=True,
                              transform=transform)
    # 원래 학습 자료 60,000개만 분리. 시험 10,000개는 모델 선택에 쓰지 않음.
    train_set, val_set = random_split(
        full_train, [55000, 5000], generator=torch.Generator().manual_seed(args.seed)
    )
    shuffle_rng = torch.Generator().manual_seed(args.seed)
    train_loader = DataLoader(train_set, batch_size=args.batch_size,
                              shuffle=True, generator=shuffle_rng, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=256, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_set, batch_size=256, shuffle=False, num_workers=0)
    model = DigitCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    history, best_val = [], float('inf')
    started = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        t0 = time.perf_counter()
        train_loss, train_acc = train_epoch(model, train_loader, optimizer,
                                             criterion, device)
        val_loss, val_acc, _ = evaluate(model, val_loader, criterion, device)
        row = dict(epoch=epoch, train_loss=train_loss, train_accuracy=train_acc,
                   validation_loss=val_loss, validation_accuracy=val_acc,
                   seconds=time.perf_counter()-t0)
        history.append(row)
        print(json.dumps(row), flush=True)
        if val_loss < best_val:
            best_val = val_loss
            torch.save({'state_dict': model.state_dict(), 'epoch': epoch,
                        'validation_loss': val_loss}, args.out / 'best.pt')
    # 검증 loss로 선택한 체크포인트를 복원한 후 시험 세트는 최종 1회 평가.
    checkpoint = torch.load(args.out / 'best.pt', map_location=device,
                            weights_only=True)
    model.load_state_dict(checkpoint['state_dict'])
    test_loss, test_acc, confusion = evaluate(model, test_loader, criterion, device)
    result = dict(torch_version=torch.__version__, device=str(device), seed=args.seed,
                  threads=args.threads, train_samples=55000, validation_samples=5000,
                  test_samples=10000, batch_size=args.batch_size, epochs=args.epochs,
                  best_epoch=checkpoint['epoch'], learning_rate=1e-3,
                  parameters=sum(p.numel() for p in model.parameters()),
                  test_loss=test_loss, test_accuracy=test_acc,
                  correct=int(confusion.diag().sum()),
                  seconds=time.perf_counter()-started, history=history,
                  confusion_matrix=confusion.tolist())
    (args.out / 'metrics.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with (args.out / 'history.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(history[0]))
        writer.writeheader(); writer.writerows(history)
    print('FINAL ' + json.dumps({k:v for k,v in result.items()
                               if k not in ('history', 'confusion_matrix')}), flush=True)


if __name__ == '__main__':
    main()  # Windows에서 DataLoader 시작을 보호하는 표준 진입점.
