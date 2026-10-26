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
