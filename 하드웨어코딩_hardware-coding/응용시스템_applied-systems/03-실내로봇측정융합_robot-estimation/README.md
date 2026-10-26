# 실내 AGV의 encoder·비콘 위치 추정과 측정 거절

[하드웨어 코딩 목차](../../README.md)

민간 실내 AGV가 직선 통로에서 정지하고 일정한 속도로 움직이는 경우를 직접 구성했습니다. encoder가 알려 주는 이동량으로 위치를 예측하고, 독립 비콘의 절대 위치가 도착하면 보정합니다. Python 표준 라이브러리만 사용하는 선별 수치 실습이며 실제 센서·ROS·로봇 구동기를 연결한 기록은 아닙니다.

## 상태와 센서의 역할

필터 상태는 한 축의 위치 x와 분산 P 두 수입니다. 속도를 상태로 추정하지 않으며 encoder가 제공한 구간 변위 u를 입력으로 받습니다. 이 단순화는 실제 robot_localization의 다차원 EKF·UKF와 구분합니다. 공식 문서의 [예측·보정과 센서 timeout](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/state_estimation_nodes.rst)은 센서가 없을 때 예측만 진행하는 역할을 설명합니다.

단위는 위치·변위 m, 시각 s, 공분산 m²입니다. 1초 구간마다 encoder 오차 분산 Q=0.0025m²를 더하며, 비콘 관측 분산은 R=0.04m²입니다. Q는 이 예제에서 한 구간에 해당하는 분산이며 m²/s 값을 그대로 더한 것이 아닙니다. 초기 위치 추정은 0.3m, P=0.25m²입니다.

두 센서는 같은 고정 실내 축을 사용하고 오차가 독립이라고 가정합니다. 같은 encoder에서 얻은 위치와 속도를 서로 독립인 센서처럼 중복 융합하지 않습니다. [공식 설정 안내](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/configuring_robot_localization.rst)는 좌표계와 같은 원천의 중복 정보를 주의하도록 설명합니다. 여기서는 별도 비콘을 사용한다는 모델 계약입니다.

## 예측과 공분산 보정

예측은 x⁻=x+u, P⁻=P+Q입니다. 측정이 없더라도 이동량은 계속 누적하고 공분산도 증가합니다. 고정 Q를 사용하므로 정지 중에도 P가 증가하며, 이는 선택한 모델의 동작입니다.

관측 z가 현재 시각과 맞으면 잔차 y=z−x⁻, 잔차 분산 S=P⁻+R을 구합니다. 수락한 관측은 K=P⁻/S로 가중하여 x⁺=x⁻+Ky로 반영합니다. 분산은 Joseph 형태 P⁺=(1−K)²P⁻+K²R을 사용합니다. 이 1차원 조건에서는 P⁻R/(P⁻+R)과 같습니다.

직접 만든 작은 손계산 예에서는 이전 x=1m,P=0.25m²에 u=0.5m,Q=0.04m²를 줍니다.

| 단계 | 계산 | 결과 |
| --- | --- | --- |
| 예측 | x⁻=1+0.5,P⁻=0.25+0.04 | 1.5m,0.29m²입니다. |
| 관측 | z=1.2m,R=0.09m² | 잔차는 −0.3m입니다. |
| 게이트 | S=0.38,NIS=0.09/0.38 | 약 0.236842로 수락합니다. |
| 가중치 | K=0.29/0.38 | 29/38입니다. |
| 위치 | 1.5+(29/38)×(−0.3) | 483/380≈1.271053m입니다. |
| 분산 | 0.29×0.09/0.38 | 261/3800≈0.068684m²입니다. |

검사기는 구현의 gain 식을 복사하지 않고, 정밀도 1/P⁻와 1/R의 합으로 평균·분산을 계산해 대조합니다. 작은 손계산은 Fraction의 정확한 유리수와도 비교합니다.

## 시각·누락·이상치 정책

측정의 센서 시각과 현재 추정 시각이 10⁻⁹초의 수치 허용치를 넘어 다르면 보정하지 않습니다. 과거 측정은 rejected_stale, 미래 측정은 rejected_future로 분류합니다. 과거 상태를 되감아 재처리하는 기능은 구현하지 않았습니다. robot_localization의 [smooth_lagged_data·history_length](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/state_estimation_nodes.rst)는 별도 이력 재처리 기능이므로 이 예제의 단순 거절 정책과 구분합니다.

예정한 비콘이 없으면 missing으로 기록하며, 비콘 예약 자체가 없는 시각은 prediction_only로 나눕니다. 어떤 경우든 encoder 예측은 유지합니다. 비유한 측정이나 0 이하 R도 거절합니다. 거절된 관측으로 P를 줄이지 않습니다.

NIS=y²/S가 9보다 크면 이상치로 거절하며 경계 9는 수락합니다. 이는 1차원 잔차의 |y|≤3√S 조건과 같습니다. 위치 오차 전체가 반드시 이 범위 안이라는 보장은 아닙니다. 공식 문서의 [Mahalanobis 거리 기반 측정 거절](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/state_estimation_nodes.rst)은 이 판단을 이해하는 근거입니다. 다차원 측정에 같은 수치 9를 자동 적용한다는 뜻은 아닙니다.

## 직접 구성한 40초 흐름

가상 참값은 1~8초 정지, 9~28초 동안 0.4m/s 등속 이동, 29~40초 정지입니다. 총 이동은 8m입니다. encoder에는 이동 중 구간당 0.01m의 고정 편향과 작은 반복 흔들림을 넣었습니다. 비콘은 5초마다 예정하며 15초에는 13초 측정이 늦게 도착하고, 20초 자료는 누락하며, 25초에는 큰 오차를 넣습니다. 참값은 평가용이며 필터 함수에 전달하지 않습니다.

| 시각 | 관측 처리 | 예측 위치 | 보정 뒤 위치 | 보정 뒤 P |
| --- | --- | --- | --- | --- |
| 5s | accepted | 0.295000m | -0.030413m | 0.034711m² |
| 10s | accepted | 0.789587m | 0.822291m | 0.021654m² |
| 15s | rejected_stale | 2.877291m | 2.877291m | 0.034154m² |
| 20s | missing | 4.922291m | 4.922291m | 0.046654m² |
| 25s | rejected_outlier | 6.972291m | 6.972291m | 0.059154m² |
| 30s | accepted | 8.207291m | 8.055010m | 0.025670m² |
| 40s | accepted | 8.030473m | 7.999134m | 0.017788m² |

15초의 비콘은 위치 2.04m를 측정한 시각이 13초이므로 현재값으로 바꾸어 사용하지 않습니다. 25초 이상치의 NIS는 약 630.656으로 경계를 크게 넘습니다. 두 거절과 누락은 그 시각의 예측값·공분산을 그대로 남깁니다.

이 고정 흐름의 위치 RMSE는 필터 0.134003m, encoder 누적 0.417033m입니다. 임의 환경에서의 성능 우위나 실제 AGV 오차 사양을 검증한 수치가 아닙니다. 오차 목록은 가우스 표본이 아니라 직접 정한 값이며, 편향은 별도 상태로 추정하지 않습니다. 따라서 P가 실제 오차의 신뢰구간과 통계적으로 일치한다고 확인한 기록도 아닙니다.

## 실제 검사와 실행

2026-10-26에 Python 3.12.14로 실제 실행했고 종료 코드 0, stderr 공백을 확인했습니다. 360개 조합의 예측·정밀도 평균·분산·게이트 동치, 정확한 경계와 유리수 예, timestamp·누락·잘못된 입력, 40단계 흐름을 합해 2,342개 비교입니다. 모든 가능한 측정·고장·로봇 동작을 전수 검사한 것은 아닙니다.

```text
PASS robot checks=2342 algebra_cases=360 steps=40 accepted=5 stale=1 missing=1 outlier=1
```

저장소 루트에서 다음 명령을 실행합니다. 패키지 설치는 필요하지 않으며 새 결과는 지정한 임시 경로에 저장합니다. 원본 코드·기존 Python 문제 풀이는 수정하지 않습니다.

```powershell
$py = 'C:/path/to/python.exe'
& $py -B '하드웨어코딩_hardware-coding/응용시스템_applied-systems/03-실내로봇측정융합_robot-estimation/check_estimator.py' --out 'tmp/robot-estimation-validation.json'
```

실제 명령·출력·입력별 판단·소스 SHA는 [example.json](example.json)에 기록합니다. 한 번의 필터 예측·보정은 시간·추가 공간 O(1)이며, T개 시간 기록을 모두 남기는 검사기는 O(T) 저장 공간을 사용합니다.

## 실제 실내 로봇에 필요한 조건

센서 좌표 변환·시계 동기화·보정값의 중복 처리·독립성·바퀴 미끄러짐과 편향·Q/R 추정이 필요합니다. 같은 비콘 자료를 반복해서 독립 관측으로 넣지 않도록 자료 식별과 입력 순서도 관리해야 합니다. 게이트가 나쁜 센서를 항상 알아내는 것은 아니며 잘못 정한 P·Q·R은 정상값을 거절하거나 이상치를 수락하게 할 수 있습니다.

실제 센서·ROS 메시지·TF·제어 명령·경로 계획·장애물 회피를 연결하지 않았습니다. 이 예제는 실내 한 축의 위치 추정이며, 별도 위성 예제의 궤도 계산이나 비행 제어 모델로 사용하지 않습니다.

## 전체 소스와 줄별 메모

### estimator.py

```python
from dataclasses import dataclass  # 입력과 추정 상태의 이름 있는 묶음
import math  # 유한값과 수치 계산 확인

@dataclass(frozen=True)  # 관측 한 건은 생성 뒤 바꾸지 않기
class Beacon:  # 같은 실내 기준축의 절대 위치 관측
    time_s: float  # 센서가 실제로 관측한 시각
    position_m: float  # 비콘이 측정한 위치
    variance_m2: float  # 관측 오차의 가정된 분산

@dataclass  # 현재 위치와 공분산을 함께 보관
class PositionFilter:  # encoder 변위를 입력으로 쓰는 1차원 선형 필터
    position_m: float = 0.3  # 초기 위치 추정값
    variance_m2: float = 0.25  # 초기 위치 불확실성
    time_s: float = 0.0  # 현재 추정값이 대응하는 시각
    def __post_init__(self):  # 유효한 초기 분산에서만 시작
        if not all(math.isfinite(v) for v in (self.position_m, self.variance_m2, self.time_s)) or self.variance_m2 <= 0:  # 유한한 위치·시각과 양의 분산
            raise ValueError("finite state and positive initial variance required")  # 잘못된 초기 조건 거절
    def predict(self, displacement_m, variance_m2, time_s):  # 이번 encoder 구간을 먼저 반영
        if not all(math.isfinite(v) for v in (displacement_m, variance_m2, time_s)) or variance_m2 < 0 or time_s <= self.time_s:  # 뒤로 가는 시각과 음의 Q 방지
            raise ValueError("finite displacement, nonnegative Q, and increasing time required")  # 이전 상태는 그대로 두기
        next_position = self.position_m + displacement_m  # 입력 변위를 위치에 누적
        next_variance = self.variance_m2 + variance_m2  # 독립 encoder 오차의 가정된 분산 누적
        if not math.isfinite(next_position) or not math.isfinite(next_variance):  # 표현 범위를 넘은 덧셈 방지
            raise ValueError("prediction overflow")  # 무한 상태로 진행하지 않기
        self.position_m, self.variance_m2, self.time_s = next_position, next_variance, time_s  # 한 시각의 예측 상태 확정
    def correct(self, measurement):  # 현재 시각의 절대 위치로만 보정
        if measurement is None:  # 예정한 측정이 도착하지 않은 경우
            return {"status": "missing"}  # 예측값과 공분산을 그대로 유지
        if not all(math.isfinite(v) for v in (measurement.time_s, measurement.position_m, measurement.variance_m2)) or measurement.variance_m2 <= 0:  # 잘못된 측정 수치 확인
            return {"status": "rejected_invalid"}  # 유효하지 않은 관측으로 상태를 바꾸지 않기
        age_s = self.time_s - measurement.time_s  # 도착 시각과 실제 측정 시각의 차이
        if abs(age_s) > 1e-9:  # 같은 시각의 계산 오차 수준만 허용
            return {"status": "rejected_stale" if age_s > 0 else "rejected_future", "age_s": age_s}  # 과거 재처리나 미래 예측은 하지 않기
        innovation = measurement.position_m - self.position_m  # 예상 위치와 관측 위치의 차이
        innovation_variance = self.variance_m2 + measurement.variance_m2  # 서로 독립이라고 가정한 잔차 분산
        if not math.isfinite(innovation) or not math.isfinite(innovation_variance):  # 표현 범위를 벗어난 입력 차이 확인
            return {"status": "rejected_invalid"}  # 정상 수치 보정과 구분
        nis = innovation * innovation / innovation_variance  # 잔차를 분산으로 정규화한 제곱 거리
        details = {"innovation_m": innovation, "innovation_variance_m2": innovation_variance, "nis": nis}  # 수락 판단의 근거
        if nis > 9.0:  # 1차원 3-sigma 경계 밖의 관측
            return {"status": "rejected_outlier", **details}  # 이상치는 상태와 분산을 줄이지 않기
        gain = self.variance_m2 / innovation_variance  # 예측보다 신뢰할 관측의 가중치
        self.position_m += gain * innovation  # 수락한 잔차만 반영
        self.variance_m2 = (1 - gain) ** 2 * self.variance_m2 + gain ** 2 * measurement.variance_m2  # Joseph 형태로 두 오차 기여 합산
        return {"status": "accepted", "gain": gain, **details}  # 실제 적용한 보정 근거 반환
```

### check_estimator.py

```python
import argparse  # 결과 JSON 위치 선택
from collections import Counter  # 수락·누락·거절의 실제 건수
from datetime import datetime, timezone  # 실행 시각 기록
from fractions import Fraction  # 손계산 예를 정확한 유리수로 대조
import hashlib  # 실행한 원본 소스 식별
import json  # 수치와 검증 범위를 저장
import math  # 독립 게이트 기준과 RMSE 계산
from pathlib import Path  # 새 결과 파일 경로 처리
from estimator import Beacon, PositionFilter  # 직접 작성한 추정기만 사용

class Checks:  # 실제 실행한 비교를 집계
    def __init__(self):  # 검사 수 초기화
        self.count = 0  # 아직 실행하지 않은 상태
    def verify(self, condition, message):  # -O에도 생략되지 않는 검사
        self.count += 1  # 실제 비교 한 건 집계
        if not condition:  # 불일치가 생기면 바로 실패
            raise AssertionError(message)  # 잘못된 결과의 통과 방지

def algebra_checks(checks):  # 구현의 gain 식과 다른 정보 정밀도 식으로 대조
    cases = 0  # 비교한 입력 조합 수
    for p in (0.01, 0.1, 1.0):  # 세 가지 사전 분산
        for q in (0.0, 0.02):  # 불확실성 증가가 없는 경우도 포함
            for r in (0.04, 0.25):  # 관측 신뢰도의 두 수준
                for displacement in (-0.4, 0.0, 0.4):  # 역방향·정지·전진 변위
                    for initial in (-1.0, 2.0):  # 서로 다른 기준 위치
                        for normalized in (-4.0, -2.5, 0.0, 2.5, 4.0):  # 경계에서 떨어진 수락·거절 잔차
                            prior_x, prior_p = initial + displacement, p + q  # 독립 선형 예측 기준
                            z = prior_x + normalized * math.sqrt(prior_p + r)  # 원하는 크기의 잔차 구성
                            model = PositionFilter(initial, p)  # 매 입력은 독립 초기 상태
                            model.predict(displacement, q, 1.0)  # encoder 예측 실행
                            checks.verify(math.isclose(model.position_m, prior_x, abs_tol=1e-14), "prediction mean")  # 예측 위치 확인
                            checks.verify(math.isclose(model.variance_m2, prior_p, abs_tol=1e-14), "prediction variance")  # 예측 공분산 확인
                            decision = model.correct(Beacon(1.0, z, r))  # 절대 위치 보정 실행
                            accepted = abs(z - prior_x) <= 3 * math.sqrt(prior_p + r)  # NIS 나눗셈과 다른 거리 기준
                            checks.verify((decision["status"] == "accepted") == accepted, "gate equivalence")  # 게이트 결정 대조
                            if accepted:  # 관측이 수락된 경우만 사후 확률 기준 계산
                                information = 1 / prior_p + 1 / r  # 두 독립 가우스의 정밀도 합
                                expected_x = (prior_x / prior_p + z / r) / information  # 정밀도 가중 평균
                                expected_p = 1 / information  # 정밀도의 역수인 사후 분산
                                checks.verify(math.isclose(model.position_m, expected_x, abs_tol=1e-12), "information mean")  # gain 갱신과 독립 대조
                                checks.verify(math.isclose(model.variance_m2, expected_p, rel_tol=1e-12), "information variance")  # Joseph 식과 대수적 동치 대조
                                checks.verify(0 < model.variance_m2 <= prior_p, "accepted covariance contraction")  # 보정에서 분산이 증가하지 않기
                            else:  # 이상치가 거절된 경우
                                checks.verify((model.position_m, model.variance_m2) == (prior_x, prior_p), "outlier preserves prediction")  # 상태와 분산 모두 유지
                            checks.verify(math.isfinite(model.variance_m2) and model.variance_m2 > 0, "finite positive covariance")  # 모든 조합의 수치 상태
                            cases += 1  # 실제 입력 조합 집계
    hand = PositionFilter(1.0, 0.25)  # README의 작은 계산 예
    hand.predict(0.5, 0.04, 1.0)  # 예측값 1.5m·0.29m²
    hand.correct(Beacon(1.0, 1.2, 0.09))  # 같은 시각의 1.2m 측정
    checks.verify(math.isclose(hand.position_m, float(Fraction(483, 380)), abs_tol=1e-14), "rational hand mean")  # 정확한 유리수 평균
    checks.verify(math.isclose(hand.variance_m2, float(Fraction(261, 3800)), abs_tol=1e-14), "rational hand variance")  # 정확한 유리수 분산
    for z, expected in ((3.0, "accepted"), (-3.0, "accepted"), (3.01, "rejected_outlier"), (-3.01, "rejected_outlier")):  # S=1인 정확한 게이트 경계
        model = PositionFilter(0.0, 0.6)  # 잔차 분산이 정확히 1이 되도록 구성
        model.predict(0.0, 0.0, 1.0)  # 정지 상태 예측
        checks.verify(model.correct(Beacon(1.0, z, 0.4))["status"] == expected, "gate boundary")  # 경계는 수락하고 바깥은 거절
    return cases  # 실행한 조합 범위 반환

def rejection_checks(checks):  # timestamp·누락·잘못된 분산의 정책 대조
    model = PositionFilter()  # 독립 기본 상태
    model.predict(0.1, 0.0025, 1.0)  # 현재 시각을 1초로 전진
    before = (model.position_m, model.variance_m2, model.time_s)  # 거절 뒤 유지해야 할 예측
    inputs = [(None, "missing"), (Beacon(0.5, 0.0, 0.04), "rejected_stale"), (Beacon(2.0, 0.0, 0.04), "rejected_future"), (Beacon(1.0, math.nan, 0.04), "rejected_invalid"), (Beacon(1.0, 0.0, 0.0), "rejected_invalid"), (Beacon(1.0, 0.0, -0.1), "rejected_invalid"), (Beacon(math.inf, 0.0, 0.04), "rejected_invalid")]  # 서로 다른 거절 원인
    for measurement, expected in inputs:  # 각 입력은 같은 예측 상태에 적용
        checks.verify(model.correct(measurement)["status"] == expected, "rejection reason")  # 원인별 상태 구분
        checks.verify((model.position_m, model.variance_m2, model.time_s) == before, "rejection preserves state")  # 거절된 값은 반영하지 않기
    for displacement, q, time in ((0.1, -0.01, 2.0), (0.1, 0.01, 0.5)):  # 음의 분산과 과거 예측 시각
        rejected = False  # 예외가 실제로 났는지 확인
        try:  # 예측 입력 검사를 실행
            model.predict(displacement, q, time)  # 잘못된 예측 시도
        except ValueError:  # 지정한 입력 오류만 예상
            rejected = True  # 실제 거절 기록
        checks.verify(rejected, "invalid prediction rejected")  # 아무 오류나 성공으로 세지 않기
        checks.verify((model.position_m, model.variance_m2, model.time_s) == before, "invalid prediction unchanged")  # 실패 전 상태 보존

def scenario(checks):  # 실내 직선 통로의 직접 구성한 정지·등속·정지 흐름
    model = PositionFilter()  # 초기 오차 0.3m의 추정값
    truth = {0: 0.0}  # 비교에만 사용하는 가상 참값
    dead_reckoning = 0.3  # 비콘 없는 encoder 누적 비교값
    records = []  # 실제 입력과 출력의 시간 순서 기록
    statuses = Counter()  # 보정 결정별 개수
    noise = (-0.08, 0.05, 0.04, -0.02, 0.08, -0.03, 0.01, -0.04)  # 고정한 비콘 오차 목록
    for step in range(1, 41):  # 1초 간격 40번 예측
        motion = 0.4 if 9 <= step <= 28 else 0.0  # 20초간 등속 이동하고 앞뒤로 정지
        truth[step] = truth[step - 1] + motion  # 가상 참값은 필터에 전달하지 않기
        displacement = motion + (0.01 if motion else 0.0) + (0.005, -0.005, 0.0)[step % 3]  # 고정 encoder 편향과 작은 흔들림
        dead_reckoning += displacement  # 보정 없는 누적값
        model.predict(displacement, 0.0025, float(step))  # 구간 분산 Q=0.0025m²
        prior_x, prior_p = model.position_m, model.variance_m2  # 보정 이전 값을 별도 기록
        measurement = None  # 기본적으로 이번 에지에는 비콘 예약 없음
        if step % 5 == 0 and step != 20:  # 5초 주기의 비콘 중 20초 자료는 누락
            timestamp = step - 2 if step == 15 else step  # 15초에 도착한 자료는 실제 13초 측정
            z = truth[timestamp] + noise[step // 5 - 1] + (8.0 if step == 25 else 0.0)  # 25초에 큰 이상치 주입
            measurement = Beacon(float(timestamp), z, 0.04)  # 관측 분산 R=0.04m²
        decision = model.correct(measurement) if step % 5 == 0 else {"status": "prediction_only"}  # 예약 없는 시각과 예정 누락 구분
        statuses[decision["status"]] += 1  # 실제 결정 개수 누적
        if decision["status"] == "accepted":  # 수락된 관측의 독립 사후 계산
            information = 1 / prior_p + 1 / measurement.variance_m2  # 정밀도 합
            expected_x = (prior_x / prior_p + measurement.position_m / measurement.variance_m2) / information  # 독립 가중 평균
            checks.verify(math.isclose(model.position_m, expected_x, abs_tol=1e-12), "scenario mean")  # 시나리오의 평균 대조
            checks.verify(math.isclose(model.variance_m2, 1 / information, rel_tol=1e-12), "scenario variance")  # 시나리오의 공분산 대조
        else:  # 누락·이상치·지연에서는 예측만 보존
            checks.verify((model.position_m, model.variance_m2) == (prior_x, prior_p), "scenario prediction-only state")  # 거절의 불변식
        checks.verify(model.variance_m2 > 0 and math.isfinite(model.variance_m2), "scenario covariance")  # 전체 시간 흐름의 공분산
        records.append({"time_s": step, "truth_m": truth[step], "encoder_displacement_m": displacement, "prior_position_m": prior_x, "prior_variance_m2": prior_p, "beacon": None if measurement is None else {"time_s": measurement.time_s, "position_m": measurement.position_m, "variance_m2": measurement.variance_m2}, "decision": decision, "posterior_position_m": model.position_m, "posterior_variance_m2": model.variance_m2, "encoder_only_position_m": dead_reckoning})  # 참값과 추정 입력을 혼동하지 않는 로그
    checks.verify(dict(statuses) == {"prediction_only": 32, "accepted": 5, "rejected_stale": 1, "missing": 1, "rejected_outlier": 1}, "scenario accounting")  # 필수 경계가 실제 실행됨
    rmse = lambda key: math.sqrt(sum((row[key] - row["truth_m"]) ** 2 for row in records) / len(records))  # 이 고정 입력의 설명용 오차
    return {"steps": 40, "statuses": dict(statuses), "filter_rmse_m": rmse("posterior_position_m"), "encoder_only_rmse_m": rmse("encoder_only_position_m"), "trace": records}  # 통계적 성능 보장이 아닌 실행 결과

def main():  # 독립 계산과 시나리오를 실행하고 새 결과 저장
    parser = argparse.ArgumentParser()  # 명령줄 입력 구성
    parser.add_argument("--out", type=Path, required=True)  # 실행 결과는 지정한 임시 JSON으로 저장
    args = parser.parse_args()  # 출력 위치 읽기
    checks = Checks()  # 실제 비교 수 집계기
    cases = algebra_checks(checks)  # 360개 대수 비교와 손계산·경계 검사
    rejection_checks(checks)  # 지연·누락·잘못된 입력 검사
    result = scenario(checks)  # 정지와 등속 이동의 시간 흐름
    result.update(status="passed_local_estimation_checks", checked_at=datetime.now(timezone.utc).isoformat(), checks=checks.count, algebra_cases=cases, source_sha256={name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ("estimator.py", "check_estimator.py")})  # 실제 소스와 결과 연결
    args.out.parent.mkdir(parents=True, exist_ok=True)  # 새 결과의 부모 폴더 준비
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")  # 비유한 수치를 정상 JSON으로 숨기지 않기
    print(f"PASS robot checks={checks.count} algebra_cases={cases} steps=40 accepted=5 stale=1 missing=1 outlier=1")  # 실제 검사 범위 표시

if __name__ == "__main__":  # import만으로 시나리오를 실행하지 않기
    main()  # 명시 실행에서만 검사 시작
```

## 공식 근거와 직접 작성한 범위

- [robot_localization 공식 노드 문서 원문](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/state_estimation_nodes.rst)은 센서 timeout·측정 거절·과정 분산·지연 자료 이력을 구분하는 근거입니다. 이 문서의 다차원 EKF·UKF와 자체 1차원 선형 예제를 동일한 구현으로 표시하지 않습니다.
- [공식 센서 설정 문서](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/doc/configuring_robot_localization.rst)는 좌표와 중복 정보의 조건을 확인하는 근거입니다. ROS 문서 사이트의 접근 제한 때문에 동일 프로젝트의 공식 문서 저장 원문을 확인했습니다.
- 소스·숫자·검사는 직접 작성했습니다. [외부 프로젝트 라이선스](https://raw.githubusercontent.com/cra-ros-pkg/robot_localization/noetic-devel/LICENSE)와 자체 예제를 구분하며 robot_localization 코드를 포함하지 않습니다.

자료 열람과 실제 실행 기준일은 2026-10-26입니다.
