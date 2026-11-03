"""직접 작성한 교육 예제: 일반 텍스트를 HTML 본문에 출력합니다."""
from html import escape  # from ... import는 HTML 문자 이스케이프 함수를 가져옵니다.

def render_message(text):  # def는 한 문자열을 HTML 문단으로 만드는 함수를 정의합니다.
    return "<p>" + escape(text, quote=True) + "</p>"  # +는 문자열을 연결하며 입력의 태그 문자는 문자 표현으로 바꿉니다.
