# 오름차순 자연수 분할을 직접 만들고 곱이 가장 큰 분할을 찾습니다. 몫·나머지로 균등하게 나누는 교환 논리를 작은 합에서
# 확인합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n,s):
    best_product=-1;best=None
    def search(left,remaining,minimum,chosen,product):
        nonlocal best_product,best
        if left==0:
            if remaining==0 and product>best_product:best_product=product;best=chosen
            return
        for value in range(minimum,remaining//left+1):
            search(left-1,remaining-value,value,chosen+[value],product*value)
    search(n,s,1,[],1)
    return best if best is not None else [-1]
