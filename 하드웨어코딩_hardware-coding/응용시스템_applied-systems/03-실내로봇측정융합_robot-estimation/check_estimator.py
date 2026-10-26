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
