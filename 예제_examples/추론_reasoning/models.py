from collections import deque
from fractions import Fraction
from itertools import product, zip_longest


def implies(p, q):
    return not p or q


def check_entailment(names, premises, conclusion):
    """작은 고전 명제논리에서 전제 모형 수와 첫 반례를 구한다."""
    names, premises = tuple(names), tuple(premises)
    if len(set(names)) != len(names) or len(names) > 16:
        raise ValueError("중복 없는 명제 이름을 16개 이하로 지정하세요.")
    premise_models, counterexample = 0, None
    # 진리표 전체를 저장하지 않고 한 행씩 평가한다.
    for bits in product((False, True), repeat=len(names)):
        assignment = dict(zip(names, bits))
        if all(rule(assignment) for rule in premises):
            premise_models += 1
            if not conclusion(assignment) and counterexample is None:
                counterexample = assignment.copy()
    return {"entails": counterexample is None, "premise_models": premise_models,
            "counterexample": counterexample}


def weighted_mean(values, weights):
    """유리수로 비음수 가중평균을 구한다. 소수는 문자열 입력이 정확하다."""
    missing = object()
    total, weighted_sum = Fraction(0), Fraction(0)
    for value, weight in zip_longest(values, weights, fillvalue=missing):
        if value is missing or weight is missing:
            raise ValueError("값과 가중치의 길이가 같아야 합니다.")
        value, weight = Fraction(value), Fraction(weight)
        if weight < 0:
            raise ValueError("비음수 가중치가 필요합니다.")
        total += weight
        weighted_sum += value * weight
    if total == 0:
        raise ValueError("가중치 합은 양수여야 합니다.")
    return weighted_sum / total


def relative_change(old, new):
    old, new = Fraction(old), Fraction(new)
    if old <= 0:
        raise ValueError("이 증가율 모델은 양의 기준값을 사용합니다.")
    return (new-old) / old


def bayes_binary(prior, likelihood, false_positive):
    """P(H), P(E|H), P(E|not H)로 P(H|E)를 구한다."""
    p, hit, false = map(Fraction, (prior, likelihood, false_positive))
    if not all(0 <= x <= 1 for x in (p, hit, false)):
        raise ValueError("확률은 0과 1 사이여야 합니다.")
    evidence = p*hit + (1-p)*false
    if evidence == 0:
        raise ValueError("확률 0인 사건으로는 조건화할 수 없습니다.")
    return p*hit / evidence


def _prepare(domains, constraints):
    current = {}
    for name, values in domains.items():
        values = tuple(values)
        if any(isinstance(v, bool) or not isinstance(v, int) for v in values):
            raise ValueError("이 예제의 도메인 값은 정수여야 합니다.")
        current[name] = tuple(dict.fromkeys(values))
    relations = {}
    neighbors = {name: set() for name in current}
    for x, y, predicate in constraints:
        if x == y or x not in current or y not in current or not callable(predicate):
            raise ValueError("서로 다른 기존 변수 두 개와 판정 함수가 필요합니다.")
        relations.setdefault((x, y), []).append(predicate)
        relations.setdefault((y, x), []).append(lambda b, a, rule=predicate: rule(a, b))
        neighbors[x].add(y)
        neighbors[y].add(x)
    return current, relations, neighbors


def _propagate(domains, relations, neighbors):
    if any(not values for values in domains.values()):
        return False
    queue = deque(relations)
    pending = set(queue)
    while queue:
        x, y = queue.popleft()
        pending.remove((x, y))
        rules = relations[x, y]
        kept = tuple(a for a in domains[x]
                     if any(all(rule(a, b) for rule in rules) for b in domains[y]))
        if len(kept) != len(domains[x]):
            domains[x] = kept
            if not kept:
                return False
            # 도메인이 줄어든 변수를 참고하던 이웃을 다시 검사한다.
            for z in neighbors[x]:
                arc = (z, x)
                if arc not in pending:
                    queue.append(arc)
                    pending.add(arc)
    return True


def iter_solutions(domains, constraints):
    """이항 제약을 모두 만족하는 정수 배정을 중복 없이 순서대로 반환한다."""
    start, relations, neighbors = _prepare(domains, constraints)

    def search(current):
        if not _propagate(current, relations, neighbors):
            return
        undecided = [x for x in current if len(current[x]) > 1]
        if not undecided:
            yield {x: values[0] for x, values in current.items()}
            return
        # 남은 선택지가 가장 적은 변수부터 분기한다.
        variable = min(undecided, key=lambda x: len(current[x]))
        for value in current[variable]:
            child = current.copy()
            child[variable] = (value,)
            yield from search(child)

    yield from search(start)


def minimize_cost(domains, constraints, costs):
    """변수별 비용 합이 최소인 해 하나와 정확한 유리수 비용을 반환한다."""
    start, relations, neighbors = _prepare(domains, constraints)
    if set(costs) != set(start):
        raise ValueError("모든 변수의 비용표가 필요합니다.")
    converted = {}
    for x in start:
        if any(value not in costs[x] for value in start[x]):
            raise ValueError("각 도메인 값에 대한 비용이 필요합니다.")
        converted[x] = {value: Fraction(costs[x][value]) for value in start[x]}
    best_assignment, best_cost = None, None

    def search(current):
        nonlocal best_assignment, best_cost
        if not _propagate(current, relations, neighbors):
            return
        # 제약을 잠시 풀고 각 변수의 최저 비용을 더하면 안전한 하한이다.
        bound = sum(min(converted[x][v] for v in current[x]) for x in current)
        if best_cost is not None and bound >= best_cost:
            return
        undecided = [x for x in current if len(current[x]) > 1]
        if not undecided:
            best_assignment = {x: values[0] for x, values in current.items()}
            best_cost = bound
            return
        variable = min(undecided, key=lambda x: len(current[x]))
        for value in sorted(current[variable], key=lambda v: converted[variable][v]):
            child = current.copy()
            child[variable] = (value,)
            search(child)

    search(start)
    return best_assignment, best_cost
