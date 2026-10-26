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
