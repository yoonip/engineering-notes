def solution(s):
    words = s.split(' ')
    changed = [word.capitalize() for word in words]
    return ' '.join(changed)

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. s는 대소문자를 바꿀 입력 문자열.
#     words = s.split(' ')  # split(' ')은 공백 한 칸 기준 분리. 인수를 생략한 split()과 달리 연속·앞뒤 공백을 빈 원소로 보존.
#     changed = [word.capitalize() for word in words]  # [] 리스트 내포의 for로 각 단어 변환. capitalize는 첫 문자만 대문자, 나머지는 소문자. 첫 문자가 숫자면 숫자는 그대로.
#     return ' '.join(changed)  # join은 원소 사이에 공백 한 칸을 넣어 연결. 빈 원소 덕분에 원래 공백 수를 보존하며 return으로 반환.

# 풀이 요약
# 공백 한 칸을 구분자로 나누어 빈 단어를 보존하고, 단어마다 첫 문자만 대문자로 만든 뒤 공백으로 다시 연결합니다.
# 예: '3people unFollowed me'→'3people Unfollowed Me'. 연속·앞뒤 공백도 유지합니다. 시간·공간 O(N).
