"""수학·물리·추론 심화 글에 연결한 실행 모듈."""

from bisect import bisect_right
from collections import Counter
from datetime import date
from fractions import Fraction
import math


def finite(values):
    """유한한 실수 입력만 허용한다."""
    if not all(math.isfinite(x) for x in values):
        raise ValueError('유한한 수가 필요합니다')


def ridge2(rows, targets, penalty):
    """두 계수의 L2 정규화 문제를 Cholesky 분해로 푼다."""
    if not rows or len(rows) != len(targets) or any(len(row) != 2 for row in rows):
        raise ValueError('두 열과 같은 수의 관측값이 필요합니다')
    finite([penalty, *targets, *(x for row in rows for x in row)])
    if penalty <= 0:
        raise ValueError('정규화 계수는 양수여야 합니다')
    aa = math.fsum(row[0] ** 2 for row in rows) + penalty
    ab = math.fsum(row[0] * row[1] for row in rows)
    bb = math.fsum(row[1] ** 2 for row in rows) + penalty
    ay = math.fsum(row[0] * y for row, y in zip(rows, targets))
    by = math.fsum(row[1] * y for row, y in zip(rows, targets))
    l11 = math.sqrt(aa)
    l21 = ab / l11
    pivot = bb - l21 * l21
    if pivot <= 0 or not math.isfinite(pivot):
        raise ValueError('입력 크기와 정규화 계수를 다시 확인해야 합니다')
    l22 = math.sqrt(pivot)
    z1 = ay / l11
    z2 = (by - l21 * z1) / l22
    b = z2 / l22
    return ((z1 - l21 * b) / l11, b)


def pi_linear_coefficients(tau, sample_time, kp, ki, gain=1.0):
    """현재 적분 상태를 출력에 사용하는 PI의 trace와 determinant를 구한다."""
    finite([tau, sample_time, kp, ki, gain])
    if tau <= 0 or sample_time <= 0 or gain <= 0:
        raise ValueError('시정수·표본 주기·플랜트 이득은 양수여야 합니다')
    a = math.exp(-sample_time / tau)
    b = -gain * math.expm1(-sample_time / tau)
    return (1 + a - b * kp, a - b * kp + b * ki * sample_time)


def jury_stable(trace, determinant):
    """실수 계수 2차 다항식의 엄격한 단위원 내부 조건이다."""
    finite([trace, determinant])
    return (1 - trace + determinant > 0 and
            1 + trace + determinant > 0 and 1 - determinant > 0)


def simulate_pi(references, sample_time=0.05, tau=1.0, kp=1.0, ki=2.0,
                kaw=0.0, limit=1.0, initial=0.0):
    """정확한 ZOH 플랜트와 전진 Euler 적분 상태를 시간 순서대로 계산한다."""
    pi_linear_coefficients(tau, sample_time, kp, ki)
    finite([kaw, limit, initial, *references])
    if kaw < 0 or limit <= 0:
        raise ValueError('되먹임 이득은 음이 아니고 출력 한계는 양수여야 합니다')
    a = math.exp(-sample_time / tau)
    b = -math.expm1(-sample_time / tau)
    x, integral = initial, 0.0
    records = []
    for k, reference in enumerate(references):
        error = reference - x
        requested = kp * error + integral
        applied = max(-limit, min(limit, requested))
        records.append((k * sample_time, reference, x, integral, requested, applied))
        x = a * x + b * applied
        integral += sample_time * (ki * error + kaw * (applied - requested))
        finite([x, integral])
    return records


def heat_fem(nodes, conductivities, sources, left=0.0, right=0.0):
    """단면적 1인 1차원 전도 문제를 선형 요소와 삼중대각 소거로 푼다."""
    n = len(nodes)
    if n < 2 or len(conductivities) != n-1 or len(sources) != n-1:
        raise ValueError('절점과 요소 입력의 크기가 맞지 않습니다')
    finite([*nodes, *conductivities, *sources, left, right])
    if any(b <= a for a, b in zip(nodes, nodes[1:])) or any(k <= 0 for k in conductivities):
        raise ValueError('좌표는 증가하고 열전도율은 양수여야 합니다')
    diagonal = [0.0] * n
    off = [0.0] * (n-1)
    rhs = [0.0] * n
    for e, (k, q) in enumerate(zip(conductivities, sources)):
        h = nodes[e+1] - nodes[e]
        stiffness = k / h
        diagonal[e] += stiffness
        diagonal[e+1] += stiffness
        off[e] = -stiffness
        rhs[e] += q * h / 2
        rhs[e+1] += q * h / 2
    if n == 2:
        return [float(left), float(right)]
    rhs[1] -= off[0] * left
    rhs[-2] -= off[-1] * right
    d, r = diagonal[1:-1], rhs[1:-1]
    for i in range(1, n-2):
        factor = off[i] / d[i-1]
        d[i] -= factor * off[i]
        r[i] -= factor * r[i-1]
    answer = [0.0] * (n-2)
    answer[-1] = r[-1] / d[-1]
    for i in range(n-4, -1, -1):
        answer[i] = (r[i] - off[i+1] * answer[i+1]) / d[i]
    return [float(left), *answer, float(right)]


def coupled_exact(t, initial_x, initial_v, mass=1.0, wall_k=1.0, coupling_k=1.0):
    """대칭인 두 질점의 정상 모드를 해석적으로 합친다."""
    finite([t, *initial_x, *initial_v, mass, wall_k, coupling_k])
    if len(initial_x) != 2 or len(initial_v) != 2 or mass <= 0 or wall_k <= 0 or coupling_k < 0:
        raise ValueError('두 질점과 양의 질량·외측 강성이 필요합니다')
    w1, w2 = math.sqrt(wall_k/mass), math.sqrt((wall_k+2*coupling_k)/mass)
    modes_x = ((initial_x[0]+initial_x[1])/2, (initial_x[0]-initial_x[1])/2)
    modes_v = ((initial_v[0]+initial_v[1])/2, (initial_v[0]-initial_v[1])/2)
    q, v = [], []
    for w, x0, v0 in zip((w1, w2), modes_x, modes_v):
        q.append(x0*math.cos(w*t) + v0*math.sin(w*t)/w)
        v.append(-x0*w*math.sin(w*t) + v0*math.cos(w*t))
    return ((q[0]+q[1], q[0]-q[1]), (v[0]+v[1], v[0]-v[1]))


def coupled_verlet(steps, dt, initial_x=(1.0, 0.0), initial_v=(0.0, 0.0),
                   mass=1.0, wall_k=1.0, coupling_k=1.0):
    """안정 한계를 확인한 뒤 두 질점의 위치·속도를 적분한다."""
    coupled_exact(0, initial_x, initial_v, mass, wall_k, coupling_k)
    finite([dt])
    if not isinstance(steps, int) or steps < 0 or dt <= 0 or dt*math.sqrt((wall_k+2*coupling_k)/mass) >= 2:
        raise ValueError('양의 간격과 안정 범위 안의 정수 단계 수가 필요합니다')
    def acceleration(x):
        return (-(wall_k*x[0]+coupling_k*(x[0]-x[1]))/mass,
                -(wall_k*x[1]+coupling_k*(x[1]-x[0]))/mass)
    x, v = tuple(initial_x), tuple(initial_v)
    result = [(0.0, x, v)]
    for i in range(steps):
        a = acceleration(x)
        new_x = tuple(x[j]+dt*v[j]+0.5*dt*dt*a[j] for j in range(2))
        new_a = acceleration(new_x)
        v = tuple(v[j]+0.5*dt*(a[j]+new_a[j]) for j in range(2))
        x = new_x
        result.append(((i+1)*dt, x, v))
    return result


def sat_dpll(clauses, variables):
    """단위 전파 뒤 빈도 높은 변수부터 양쪽을 탐색하는 작은 SAT 풀이기다."""
    if not isinstance(variables, int) or not 0 <= variables <= 24:
        raise ValueError('이 예제는 변수 0~24개를 받습니다')
    normalized=[]
    for clause in clauses:
        c=frozenset(clause)
        if any(type(lit) is not int or lit == 0 or abs(lit) > variables for lit in c):
            raise ValueError('리터럴 번호가 범위를 벗어났습니다')
        if not any(-lit in c for lit in c):normalized.append(c)
    def simplify(cs, lit):
        return [c-{ -lit } for c in cs if lit not in c]
    def search(cs, assigned):
        while True:
            if any(not c for c in cs):return None
            if not cs:return {v:assigned.get(v,False) for v in range(1,variables+1)}
            unit=next((next(iter(c)) for c in cs if len(c)==1),None)
            if unit is None:break
            assigned[abs(unit)]=unit>0
            cs=simplify(cs,unit)
        occurrences=Counter(abs(lit) for c in cs for lit in c)
        var=min(occurrences,key=lambda v:(-occurrences[v],v))
        for lit in (var,-var):
            result=search(simplify(cs,lit),{**assigned,var:lit>0})
            if result is not None:return result
        return None
    return search(normalized,{})


def bayes_coin_models(heads, trials, prior_fair=0.5):
    """공정한 고정 동전과 균등 사전분포의 동전 모형을 비교한다."""
    if type(heads) is not int or type(trials) is not int or not 0 <= heads <= trials:
        raise ValueError('성공 횟수와 전체 횟수를 확인해야 합니다')
    finite([prior_fair])
    if not 0 < prior_fair < 1:
        raise ValueError('모형 사전확률은 0과 1 사이여야 합니다')
    log_fair=-trials*math.log(2)
    log_flexible=math.lgamma(heads+1)+math.lgamma(trials-heads+1)-math.lgamma(trials+2)
    log_bf=log_fair-log_flexible
    log_odds=math.log(prior_fair)-math.log1p(-prior_fair)+log_bf
    posterior=(1/(1+math.exp(-log_odds)) if log_odds>=0 else math.exp(log_odds)/(1+math.exp(log_odds)))
    return {'log_bayes_factor_fair':log_bf,'posterior_fair':posterior,
            'flexible_posterior_mean':(heads+1)/(trials+2)}


def leontief_fixed_point(matrix, demand, tolerance=1e-10, max_steps=10000):
    """최대 행합이 1보다 작은 비음수 투입계수의 총산출을 계산한다."""
    n=len(demand)
    if not n or len(matrix)!=n or any(len(row)!=n for row in matrix):
        raise ValueError('정방행렬과 수요 벡터가 필요합니다')
    finite([*demand,*(x for row in matrix for x in row),tolerance])
    if any(x<0 for row in matrix for x in row) or any(x<0 for x in demand) or tolerance<=0:
        raise ValueError('입력은 음이 아니고 허용 오차는 양수여야 합니다')
    bound=max(math.fsum(row) for row in matrix)
    if bound>=1 or type(max_steps) is not int or max_steps<1:
        raise ValueError('최대 행합은 1 미만이고 반복 한도는 양수여야 합니다')
    x=[0.0]*n
    for step in range(1,max_steps+1):
        x=[demand[i]+math.fsum(a*y for a,y in zip(row,x)) for i,row in enumerate(matrix)]
        residual=max(abs(x[i]-demand[i]-math.fsum(a*y for a,y in zip(row,x))) for i,row in enumerate(matrix))
        certificate=residual/(1-bound)
        if certificate<=tolerance:return {'output':x,'error_bound_inf':certificate,'iterations':step}
    raise RuntimeError('반복 한도 안에서 오차 조건을 만족하지 못했습니다')


def standardized_rates(group_a, group_b, weights):
    """공통 층별 가중치를 적용한 비율과 원시 비율을 유리수로 계산한다."""
    if not group_a or set(group_a)!=set(group_b) or set(group_a)!=set(weights):
        raise ValueError('두 집단과 가중치의 층이 같아야 합니다')
    w={key:Fraction(value) for key,value in weights.items()}
    if any(value<0 for value in w.values()) or sum(w.values())!=1:
        raise ValueError('가중치는 음이 아니며 합이 1이어야 합니다')
    results=[]
    for group in (group_a,group_b):
        for success,total in group.values():
            if type(success) is not int or type(total) is not int or total<=0 or not 0<=success<=total:
                raise ValueError('각 층의 표본 수와 성공 수를 확인해야 합니다')
        crude=Fraction(sum(x[0] for x in group.values()),sum(x[1] for x in group.values()))
        adjusted=sum(w[key]*Fraction(*group[key]) for key in w)
        results.append({'crude':crude,'standardized':adjusted})
    return results


class VersionTimeline:
    """하나의 조항·규칙의 효력 시작일을 정렬해 메타데이터를 조회한다."""
    def __init__(self, records):
        if not records:raise ValueError('한 개 이상의 이력이 필요합니다')
        self.records=sorted((dict(row) for row in records),key=lambda row:date.fromisoformat(row['effective']))
        self.starts=[date.fromisoformat(row['effective']) for row in self.records]
        for row in self.records:
            date.fromisoformat(row['promulgated'])
            if not row['id']:raise ValueError('식별자가 필요합니다')
        if len(set(self.starts))!=len(self.starts):raise ValueError('같은 시행일의 중복 이력입니다')

    def at(self, instant):
        """시행 구간의 식별자만 반환하며 실제 법률관계의 적용은 판단하지 않는다."""
        value=date.fromisoformat(instant)
        i=bisect_right(self.starts,value)-1
        return None if i<0 else dict(self.records[i])
