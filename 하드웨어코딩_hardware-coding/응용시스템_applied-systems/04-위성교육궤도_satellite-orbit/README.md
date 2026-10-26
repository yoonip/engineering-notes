# 교육용 지구 위성 원운동의 RK4 적분과 보존량

[하드웨어 코딩 목차](../../README.md)

지구 주위를 도는 가벼운 교육용 위성의 무추력 원운동을 평면 중심중력 모델로 계산합니다. Python으로 직접 작성한 RK4 적분을 정확 원운동과 비교하고 에너지·각운동량 오차와 시간 간격 수렴을 확인합니다. 실내 로봇의 측정 융합과 별개인 궤도 수학 실습이며, 실제 위성 관측·운용·비행 제어를 수행한 기록은 아닙니다.

## 중심중력 모델과 단위

상태는 r=(x,y),v=(vx,vy)이며 좌표의 원점은 지구 중심입니다. 위치는 km, 시간은 s, 속도는 km/s입니다. 회전하는 지표 좌표가 아니라 이상적인 관성 평면입니다. 위성의 질량은 중심 천체에 비해 무시하며 다음 식만 적분합니다.

dr/dt=v, dv/dt=−μr/|r|³입니다. 가속도 크기는 μ/|r|²이며 방향은 중심을 향합니다. 역제곱 중력의 개념은 [NASA의 Gravity & Mechanics](https://science.nasa.gov/learn/basics-of-space-flight/chapter3-1/)를 참고합니다. 중심 천체에 대한 질량 무시와 단위 일관성은 [JPL SPICE의 prop2b 설명](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html)에서 확인합니다. 이 예제는 SPICE 함수를 호출하거나 그 코드를 복사하지 않았습니다.

μ=398600.435507km³/s²는 [JPL의 DE440 지구 GM 표](https://ssd.jpl.nasa.gov/astro_par.html)의 값입니다. km와 m를 섞으면 세제곱 길이 단위가 맞지 않습니다. 코드와 정확해는 모두 km·s를 유지합니다. 7000km·9000km는 지구중심 반지름이며 지표 고도로 입력한 수가 아닙니다.

## 정확 원운동과 RK4

반지름 r₀의 시작 상태를 (r₀,0,0,√(μ/r₀))로 둡니다. n=√(μ/r₀³),T=2π/n이면 정확한 위치는 r₀(cos nt,sin nt), 속도는 r₀n(−sin nt,cos nt)입니다. JPL의 [원운동 속도와 반주기 예](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html)를 근거로, 이 실습에서는 별도 삼각함수식으로 정확해를 작성했습니다.

RK4는 구간 시작·두 중간 후보·끝 후보에서 미분을 네 번 계산하고 1·2·2·1의 가중합에 h/6을 곱합니다. 중간 후보를 정확해로 대체하지 않으므로 적분기는 중심중력 미분 함수만 사용합니다. 정확 원운동은 오차 비교에만 사용합니다.

매끄러운 이 조건에서 시간 간격을 절반으로 줄이면 전역 오차가 대략 16배 줄어드는 4차 수렴을 기대합니다. 유한 간격의 실제 감소 비율과 로그 차수는 별도로 기록하며 언제나 정확히 16이라고 가정하지 않습니다. RK4는 장시간의 에너지를 구조적으로 보존하는 symplectic 적분기가 아닙니다.

## 한 주기의 직접 계산 흐름

7000km의 원운동 속력은 약 7.546053231km/s, 주기는 5828.516684s입니다. 가장 작은 시간 간격의 480단계 실행은 아래와 같습니다. 위치는 표에 표시한 자릿수로 반올림한 실제 적분값입니다.

| 주기 지점 | 시각 | RK4 x | RK4 y | 정확 위치와 거리 오차 |
| --- | --- | --- | --- | --- |
| 시작 | 0.000000s | 7000.000000000km | 0.000000000km | 0.000000m |
| 1/4주기 | 1457.129171s | -0.000001001km | 6999.999996728km | 0.003422m |
| 1/2주기 | 2914.258342s | -6999.999993343km | -0.000015123km | 0.016524m |
| 3/4주기 | 4371.387513s | 0.000029746km | -6999.999996381km | 0.029966m |
| 1주기 | 5828.516684s | 6999.999999530km | 0.000031801km | 0.031805m |

에너지는 단위 질량당 ε=|v|²/2−μ/|r|이며 단위는 km²/s²입니다. 평면 비각운동량은 h=xvy−yvx이며 km²/s입니다. 원 궤도의 ε₀=−μ/(2r₀),h₀=√(μr₀)와 초기값부터 대조합니다. 중심 힘의 토크가 0이므로 이상 모델에서는 각운동량이 일정하며, 시간에 명시적으로 의존하지 않는 중력 퍼텐셜에서는 에너지도 일정합니다.

비에너지의 음수 값 자체와 오차는 구분합니다. 오차는 |(ε−ε₀)/ε₀|와 |(h−h₀)/h₀|로 계산합니다. 한 시점의 위치만 맞는 것으로 통과시키지 않고 각 적분 시각의 위치·속도·보존량을 함께 확인합니다.

## 실제 수렴과 보존량 검사

2026-10-26에 Python 3.12.14로 반지름 두 경우를 각각 한 주기씩 120·240·480단계로 적분했습니다. 총 6회·1680단계입니다. 아래 최대값은 저장 시각들의 최대 오차이며 연속 시간의 모든 순간에 대한 증명된 상한은 아닙니다.

| 반지름 | 단계 수 | 시간 간격 | 최대 위치 오차 | 최대 상대 에너지 오차 | 최대 상대 각운동량 오차 |
| --- | --- | --- | --- | --- | --- |
| 7000km | 120 | 48.570972s | 9.838303m | 6.872e-8 | 3.436e-8 |
| 7000km | 240 | 24.285486s | 0.545324m | 2.147e-9 | 1.073e-9 |
| 7000km | 480 | 12.142743s | 0.032197m | 6.708e-11 | 3.354e-11 |
| 9000km | 120 | 70.809822s | 12.649247m | 6.872e-8 | 3.436e-8 |
| 9000km | 240 | 35.404911s | 0.701132m | 2.147e-9 | 1.073e-9 |
| 9000km | 480 | 17.702455s | 0.041396m | 6.708e-11 | 3.354e-11 |

| 반지름 | 단계 변경 | 위치 오차 감소 비율 | 관측 차수 log₂(감소 비율) |
| --- | --- | --- | --- |
| 7000km | 120 → 240 | 18.041193 | 4.173223 |
| 7000km | 240 → 480 | 16.937375 | 4.082138 |
| 9000km | 120 → 240 | 18.041190 | 4.173223 |
| 9000km | 240 → 480 | 16.937311 | 4.082133 |

기준은 각 시각의 상대 위치·속도 오차 2×10⁻⁵ 미만, 상대 에너지·각운동량 오차 10⁻⁵ 미만입니다. 가장 작은 간격에서는 최대 위치 오차 1m 미만, 두 보존량의 상대 오차 10⁻⁷ 미만을 요구합니다. 관측 차수는 이 여섯 실행에서 3.5~4.5 범위여야 합니다. 이 기준을 통과한 것은 선택한 원운동·한 주기의 수치 검사이며 임의 궤도·시간 간격·장기 전파의 정확도 보장이 아닙니다.

초기 에너지·각운동량 공식, 세 방향의 역제곱 힘·중심 방향·토크, 무효 입력 거절도 포함하여 8,435개 비교를 실제 실행했습니다. 종료 코드는 0이며 stderr는 비어 있습니다.

```text
PASS orbit checks=8435 circular_runs=6 integrated_steps=1680 convergence_pairs=4
```

## 재현과 계산량

Python 표준 라이브러리만 사용합니다. 저장소 루트에서 다음 명령으로 같은 선별 실습을 실행하고 새 결과를 임시 경로에 저장합니다.

```powershell
$py = 'C:/path/to/python.exe'
& $py -B '하드웨어코딩_hardware-coding/응용시스템_applied-systems/04-위성교육궤도_satellite-orbit/check_orbit.py' --out 'tmp/satellite-orbit-validation.json'
```

실제 명령·도구·수치·추적·소스 SHA는 [example.json](example.json)에 있습니다. N단계 전파의 시간은 O(N)이며 한 단계에 미분 함수 네 번을 평가합니다. 적분 상태와 최대값만 유지하는 계산은 O(1) 추가 공간이며, 여기서는 실행별 다섯 추적 지점을 따로 저장합니다.

## 교육 모델과 현실 사용 조건

구형 중심중력만 사용하며 지구 비구형 중력·대기 저항·달과 태양의 영향·복사압·추력은 넣지 않았습니다. 달력 시각·실제 좌표 프레임·지구 자세·추정한 관측값도 입력하지 않습니다. 실제 위성 데이터를 예측하거나 임무 요구 정확도를 확인한 결과가 아닙니다.

이 실습은 궤도 운동 방정식과 수치 적분의 관계를 확인하는 데 사용합니다. 상태 추정·자세 제어·명령 생성·운용 절차는 포함하지 않으며, 로봇 추정기의 센서 잔차나 게이트를 위성의 비행 제어 식으로 연결하지 않습니다. 더 긴 전파나 다른 물리 모델에서는 적절한 모델·좌표·적분 방식과 독립 검증 기준을 다시 정해야 합니다.

## 전체 소스와 줄별 메모

### orbit.py

```python
import math  # 거리와 정확 원운동의 삼각함수

EARTH_MU_KM3_S2 = 398600.435507  # JPL DE440 표의 지구 GM, km³/s²

def circular_state(radius_km, time_s, mu=EARTH_MU_KM3_S2):  # 적분기와 독립인 정확 원운동
    if not all(math.isfinite(v) for v in (radius_km, time_s, mu)) or radius_km <= 0 or mu <= 0:  # 양의 반지름과 중심중력 상수
        raise ValueError("positive finite radius and mu, finite time required")  # 무효한 원운동 조건 거절
    frequency = math.sqrt(mu / radius_km ** 3)  # 각속도 rad/s
    angle = frequency * time_s  # 시작점으로부터 회전한 각도
    speed = radius_km * frequency  # 원 궤도의 일정한 속력 km/s
    return (radius_km * math.cos(angle), radius_km * math.sin(angle), -speed * math.sin(angle), speed * math.cos(angle))  # x·y·vx·vy의 정확해

def derivative(state, mu=EARTH_MU_KM3_S2):  # 중심 중력의 위치·속도 미분
    x, y, vx, vy = state  # 평면 관성좌표와 속도
    radius = math.hypot(x, y)  # 지구 중심부터의 거리
    if not all(math.isfinite(v) for v in (*state, mu)) or radius <= 0 or mu <= 0:  # 중심 특이점과 무효 수치 방지
        raise ValueError("finite state, nonzero radius, and positive mu required")  # 유한한 교육 모델 범위 확인
    factor = -mu / radius ** 3  # 좌표에 곱하면 중심을 향하는 가속도
    return (vx, vy, factor * x, factor * y)  # dr/dt=v, dv/dt=−mu r/|r|³

def rk4_step(state, step_s, mu=EARTH_MU_KM3_S2):  # 네 번의 기울기로 한 시간 간격 적분
    if not math.isfinite(step_s) or step_s <= 0:  # 앞을 향하는 양의 유한 간격
        raise ValueError("positive finite step required")  # 0이나 음의 적분 간격 거절
    k1 = derivative(state, mu)  # 구간 시작의 미분
    k2 = derivative(tuple(value + step_s * slope / 2 for value, slope in zip(state, k1)), mu)  # 첫 중간점의 미분
    k3 = derivative(tuple(value + step_s * slope / 2 for value, slope in zip(state, k2)), mu)  # 보정한 중간점의 미분
    k4 = derivative(tuple(value + step_s * slope for value, slope in zip(state, k3)), mu)  # 구간 끝 후보의 미분
    return tuple(value + step_s * (a + 2 * b + 2 * c + d) / 6 for value, a, b, c, d in zip(state, k1, k2, k3, k4))  # 1·2·2·1 가중치의 RK4 갱신

def invariants(state, mu=EARTH_MU_KM3_S2):  # 단위 질량당 에너지와 평면 각운동량
    x, y, vx, vy = state  # 위치와 속도 성분
    energy = (vx * vx + vy * vy) / 2 - mu / math.hypot(x, y)  # km²/s²의 역학적 비에너지
    momentum = x * vy - y * vx  # km²/s의 z방향 비각운동량
    return energy, momentum  # 같은 중심중력에서 일정해야 할 두 양
```

### check_orbit.py

```python
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
```

## 공식 근거와 직접 작성한 범위

- [NASA Gravity & Mechanics](https://science.nasa.gov/learn/basics-of-space-flight/chapter3-1/)는 역제곱 중력과 원·타원 개념의 근거입니다.
- [JPL prop2b 문서](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html)는 중심 천체·무시할 수 있는 위성 질량·단위와 원운동 속도의 근거입니다. SPICE의 universal-variable 알고리즘을 사용하거나 실행한 기록은 아닙니다.
- [JPL astrodynamic parameters](https://ssd.jpl.nasa.gov/astro_par.html)의 DE440 지구 GM 값을 사용합니다. 이것이 전체 DE440 천체력을 불러온다는 뜻은 아닙니다.
- 소스·입력 조건·RK4 계산기·수치 비교는 직접 작성했으며 공식 소스 코드·그림을 복제하지 않았습니다.

자료 열람과 실제 실행 기준일은 2026-10-26입니다.
