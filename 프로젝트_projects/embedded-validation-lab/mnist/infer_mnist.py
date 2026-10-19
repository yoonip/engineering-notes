"""저장된 가중치로 MNIST 실제 영상 한 장을 분류한다."""
import argparse
import json
from pathlib import Path
import torch
from torchvision import datasets, transforms
from train_mnist import DigitCNN


@torch.inference_mode()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--checkpoint', type=Path, default=Path('results/best.pt'))
    ap.add_argument('--data', type=Path, default=Path('data'))
    ap.add_argument('--index', type=int, default=0)
    args = ap.parse_args()
    transform = transforms.Compose([transforms.ToTensor(),
                                     transforms.Normalize((0.1307,), (0.3081,))])
    test = datasets.MNIST(args.data, train=False, download=True, transform=transform)
    if not 0 <= args.index < len(test):
        raise ValueError('index out of range')
    model = DigitCNN()
    checkpoint = torch.load(args.checkpoint, map_location='cpu', weights_only=True)
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    image, truth = test[args.index]
    # CNN의 첫 차원은 batch. 한 장도 [1,1,28,28]로 입력한다.
    logits = model(image.unsqueeze(0))
    probability = torch.softmax(logits, dim=1)[0]
    prediction = int(probability.argmax())
    print(json.dumps({'index': args.index, 'truth': truth, 'prediction': prediction,
                      'correct': prediction == truth,
                      'confidence': float(probability[prediction]),
                      'probabilities': probability.tolist()}, indent=2))
    # confidence는 모델 점수이며 교정된 정답 확률을 보장하는 값은 아니다.


if __name__ == '__main__':
    main()
