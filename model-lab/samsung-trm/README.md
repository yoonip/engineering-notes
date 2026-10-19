# Tiny Recursive Models

Samsung SAIL Montréal의 TRM은 작은 신경망을 반복 적용해 답을 개선하는 추론 연구다. 논문 제목은 “Less is More: Recursive Reasoning with Tiny Networks”다. 대규모 대화형 언어 모델을 그대로 축소한 구조와는 다르다.

## 구조

입력 표현 x, 현재 답의 표현 y, 내부 상태 z를 사용한다. 입력과 답을 바탕으로 z를 여러 번 갱신한 뒤 y를 갱신하며 이 과정을 반복한다. 파라미터를 공유하는 반복 계산으로 네트워크 크기와 계산 깊이를 다른 축으로 다룬다.

## 코드와 과제

공식 저장소에는 모델 코드, 학습 진입점, 데이터 생성·변환 코드, 설정 파일이 있다. Sudoku·maze·ARC 계열 과제가 포함되며, 입력·정답의 표현과 평가 분할이 과제마다 다르다. 재귀 횟수와 상태 갱신, loss와 gradient 흐름이 구조를 이해하는 핵심이다.

모델의 파라미터 수가 작아도 학습의 메모리·시간이 자동으로 작아지지는 않는다. 반복 횟수·batch·데이터 증강이 계산량을 바꾼다. 원본 저장소는 2026년 4월 1일 archive 상태로 전환되었다.

[공식 코드와 논문 링크](https://github.com/SamsungSAILMontreal/TinyRecursiveModels) · [AI 기업과 모델](../PROVIDERS.md)
