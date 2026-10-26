import argparse  # 새 실행 결과 위치 선택
from datetime import datetime, timezone  # 확인 시각 기록
import hashlib  # 계산에 사용한 소스 바이트 연결
import json  # 보존량·수렴·추적 결과 저장
import math  # 독립 원 궤도와 오차 계산
from pathlib import Path  # 새 출력 파일 경로
from orbit import EARTH_MU_KM3_S2, circular_state, derivative, invariants, rk4_step  # 직접 작성한 중심중력 계산기

class Checks:  # 실제 실행한 검사의 수 기록
    def __init__(self):  # 집계 초기화
        self.count = 0  # 아직 비교하지 않은 상태
    def verify(self, condition, message):  # Python -O에도 생략되지 않는 비교
        self.count += 1  # 실제 검사 한 건 누적
        if not condition:  # 허용 범위 밖이거나 잘못된 결과
            raise AssertionError(message)  # 확인하지 못한 결과로 중단

def one_period(radius, steps, checks):  # 같은 정확 주기를 서로 다른 간격으로 계산
    mu = EARTH_MU_KM3_S2  # km와 초를 사용하는 지구 중심중력 상수
    period = 2 * math.pi * math.sqrt(radius ** 3 / mu)  # 정확 원운동의 주기
    step_s = period / steps  # 마지막 시각이 같은 한 주기가 되도록 간격 설정
    state = (radius, 0.0, 0.0, math.sqrt(mu / radius))  # 반지름과 접선 속도의 원 궤도 초기값
    initial_energy, initial_momentum = invariants(state)  # 같은 수치 초기값에서 보존량 기준
    checks.verify(math.isclose(initial_energy, -mu / (2 * radius), rel_tol=1e-14), "circular energy")  # 원 궤도 에너지의 별도 공식
    checks.verify(math.isclose(initial_momentum, math.sqrt(mu * radius), rel_tol=1e-14), "circular momentum")  # 원 궤도 각운동량의 별도 공식
    max_position_error = max_velocity_error = max_energy_drift = max_momentum_drift = 0.0  # 실제 경로 전체의 최대 오차
    trace = [{"time_s": 0.0, "state": list(state), "exact_state": list(state), "position_error_km": 0.0}]  # 직접 구성한 시작점
    for index in range(1, steps + 1):  # 한 주기만 전파하는 유한 반복
        state = rk4_step(state, step_s)  # 중심중력 RK4 적분 한 단계
        time_s = index * step_s  # 반복 덧셈 대신 기준 간격으로 관측 시각 계산
        exact = circular_state(radius, time_s)  # 적분 결과를 읽지 않는 정확 원운동
        position_error = math.hypot(state[0] - exact[0], state[1] - exact[1])  # 위치 벡터 오차 km
        velocity_error = math.hypot(state[2] - exact[2], state[3] - exact[3])  # 속도 벡터 오차 km/s
        energy, momentum = invariants(state)  # 이번 상태에서의 두 보존량
        energy_drift = abs((energy - initial_energy) / initial_energy)  # 초기값 대비 상대 에너지 오차
        momentum_drift = abs((momentum - initial_momentum) / initial_momentum)  # 초기값 대비 상대 각운동량 오차
        checks.verify(all(math.isfinite(value) for value in state), "finite propagated state")  # NaN·무한값 방지
        checks.verify(position_error < radius * 2e-5, "sampled circular position")  # 거친 간격도 정확 경로에서 크게 벗어나지 않기
        checks.verify(velocity_error < math.sqrt(mu / radius) * 2e-5, "sampled circular velocity")  # 속도도 독립 원운동과 비교
        checks.verify(energy_drift < 1e-5, "sampled energy drift")  # 역학적 보존량의 상대 오차 한도
        checks.verify(momentum_drift < 1e-5, "sampled angular momentum drift")  # 중심 힘의 각운동량 보존 대조
        max_position_error = max(max_position_error, position_error)  # 위치 최대 오차 갱신
        max_velocity_error = max(max_velocity_error, velocity_error)  # 속도 최대 오차 갱신
        max_energy_drift = max(max_energy_drift, energy_drift)  # 최대 에너지 상대 오차
        max_momentum_drift = max(max_momentum_drift, momentum_drift)  # 최대 각운동량 상대 오차
        if index % (steps // 4) == 0:  # 4분의 1주기마다 실제 수치 상태 기록
            trace.append({"time_s": time_s, "state": list(state), "exact_state": list(exact), "position_error_km": position_error})  # 표시 시각과 정확해를 함께 보존
    return {"radius_km": radius, "steps": steps, "step_s": step_s, "period_s": period, "maximum_position_error_km": max_position_error, "maximum_velocity_error_km_s": max_velocity_error, "maximum_relative_energy_drift": max_energy_drift, "maximum_relative_angular_momentum_drift": max_momentum_drift, "final_position_error_km": position_error, "trace": trace}  # 한 주기의 실제 최대값과 추적

def force_and_input_checks(checks):  # 중심 힘과 잘못된 입력을 작은 수로 확인
    for x, y in ((7000.0, 0.0), (0.0, 7000.0), (-4200.0, 5600.0)):  # 축과 비대칭 방향
        _, _, ax, ay = derivative((x, y, 0.0, 0.0))  # 정지 속도에서도 위치 가속도만 확인
        radius = math.hypot(x, y)  # 별도 거리 기준
        checks.verify(math.isclose(math.hypot(ax, ay), EARTH_MU_KM3_S2 / radius ** 2, rel_tol=1e-14), "inverse square magnitude")  # 가속도 크기의 역제곱 공식
        checks.verify(ax * x + ay * y < 0, "force points inward")  # 위치 벡터와 반대 방향
        checks.verify(math.isclose(x * ay - y * ax, 0.0, abs_tol=1e-12), "zero central torque")  # 중심 힘의 토크가 0
    bad_calls = [lambda: circular_state(0.0, 0.0), lambda: circular_state(7000.0, 0.0, -1.0), lambda: derivative((0.0, 0.0, 1.0, 0.0)), lambda: rk4_step((7000.0, 0.0, 0.0, 7.5), 0.0)]  # 중심 특이점·음의 GM·0 간격
    for call in bad_calls:  # 각각의 무효 입력을 독립 검사
        rejected = False  # 지정한 입력 오류의 실제 발생 표시
        try:  # 잘못된 계산 호출
            call()  # 유효한 궤도로 처리되면 실패해야 함
        except ValueError:  # 입력 조건의 거절만 예상
            rejected = True  # 올바른 거절 기록
        checks.verify(rejected, "invalid orbit input")  # 조용히 진행하지 않았는지 확인

def main():  # 두 반지름·세 시간 간격의 선별 실습
    parser = argparse.ArgumentParser()  # 실행 결과 위치 선택
    parser.add_argument("--out", type=Path, required=True)  # 새 임시 결과 JSON
    args = parser.parse_args()  # 사용자 출력 위치 읽기
    checks = Checks()  # 실제 비교 수 집계
    force_and_input_checks(checks)  # 독립 힘 계산과 입력 경계 확인
    runs = []  # 여섯 개의 유한 전파 결과
    convergence = []  # 시간 간격을 절반으로 줄였을 때의 오차 변화
    for radius in (7000.0, 9000.0):  # 지구중심 반지름 두 경우만 선택
        group = [one_period(radius, steps, checks) for steps in (120, 240, 480)]  # 같은 한 주기의 세 간격
        for coarse, fine in zip(group, group[1:]):  # 인접한 간격 두 개를 대조
            ratio = coarse["maximum_position_error_km"] / fine["maximum_position_error_km"]  # 실제 위치 오차 감소 비율
            order = math.log2(ratio)  # 간격 절반에 대한 관측 수렴 차수
            checks.verify(3.5 < order < 4.5, "observed fourth order convergence")  # 이 매끄러운 원운동에서의 RK4 차수 확인
            convergence.append({"radius_km": radius, "coarse_steps": coarse["steps"], "fine_steps": fine["steps"], "error_ratio": ratio, "observed_order": order})  # 해당 실행 범위만 기록
        checks.verify(group[-1]["maximum_position_error_km"] < 0.001, "fine-grid error below one meter")  # 가장 작은 간격의 1m 위치 오차 한도
        checks.verify(group[-1]["maximum_relative_energy_drift"] < 1e-7, "fine-grid energy drift")  # 미세 간격의 보존량 기준
        checks.verify(group[-1]["maximum_relative_angular_momentum_drift"] < 1e-7, "fine-grid momentum drift")  # 미세 간격의 각운동량 기준
        runs.extend(group)  # 실제 여섯 결과 모으기
    report = {"status": "passed_educational_two_body_checks", "checked_at": datetime.now(timezone.utc).isoformat(), "checks": checks.count, "mu_km3_s2": EARTH_MU_KM3_S2, "runs": runs, "convergence": convergence, "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ("orbit.py", "check_orbit.py")}}  # 수치 실행과 소스 연결
    args.out.parent.mkdir(parents=True, exist_ok=True)  # 새 결과 파일의 부모 폴더
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")  # 비유한 값을 통과 기록으로 쓰지 않기
    print(f"PASS orbit checks={checks.count} circular_runs=6 integrated_steps=1680 convergence_pairs=4")  # 선별한 계산 범위만 완료 표시

if __name__ == "__main__":  # import로 궤도를 전파하지 않기
    main()  # 명시 실행에서만 검증 시작
