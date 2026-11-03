# 로그 탐지와 사고 대응 | Detection and response

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 조사 가능한 사건을 남깁니다

웹 서버의 요청 로그만으로 ‘누가 어느 권한으로 어떤 자료를 읽었는지’를 알 수 없는 경우가 많습니다. 인증·권한 거부·관리 변경·키 사용·자료 접근·배포·보안 기능 변경을 애플리케이션 사건과 연결합니다. 주체·객체·결과·이유·요청 ID·서버 시각을 일관된 구조로 기록합니다. 비밀번호·세션 토큰·원문 개인정보를 조사 편의 때문에 통째로 남기지는 않습니다. [OWASP Logging의 기록할 사건·제외할 자료·로그 보호 절](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

공격자 입력의 줄바꿈·제어문자가 새 로그 행처럼 보이게 할 수 있습니다. 구조화된 직렬화·길이 제한·출력 처리를 적용하고, 로그를 수정·삭제할 권한과 보존 사본도 분리합니다. SIEM은 여러 사건을 모으고 연관 분석하는 체계이며, EDR은 단말의 행위 관측·대응에 초점을 둡니다. 제품 이름보다 필요한 원시 근거가 실제로 수집되는지 확인합니다.

## 시간창 탐지의 정확한 조건

실습은 계정마다 최근 60초 `(현재-60, 현재]` 구간의 실패를 셉니다. 0·10·20초의 실패는 20초에 3회가 되어 경보가 나옵니다. 0·30·60초라면 60초에서 0초는 제외되어 2회입니다. 성공은 실패 수에 더하지 않지만 기존 실패를 지우지도 않습니다. 임계값3과 시간창60초는 학습용 자체 설정입니다.

정렬된 합성 로그를 입력하며 거꾸로 도착한 시각은 예외로 표시합니다. 실제 수집기는 지연·중복·시계 오차·재시작·계정 변경·상태 만료가 필요합니다. 코드는 만료된 계정 키를 전체 상태에서 제거하지 않아 장기 스트리밍 운영용으로 완성된 구현은 아닙니다. 임계값 이후 각 실패마다 경보를 반환하므로 실제 경보 묶기 정책도 별도입니다.

## 경보는 증거를 확인할 시작점입니다

같은 계정의 실패가 많아도 사용자가 비밀번호를 잊었을 수 있습니다. 반대로 많은 계정에 한 번씩 시도하면 이 규칙만으로 놓칠 수 있습니다. 계정·IP·기기·세션·대상 자원·시간을 함께 보되 개인 식별·보존 목적을 정합니다. [ATT&CK](https://attack.mitre.org/matrices/enterprise/)는 관측한 행위를 기술과 연결하는 참고 틀이며 기법 이름 하나가 행위자 귀속의 증거는 아닙니다.

## 사고 대응의 연결

탐지 뒤에는 영향·범위 확인, 격리, 자격증명 폐기, 취약점 수정, 신뢰한 상태 복원, 재발 검사와 관측이 이어집니다. NIST SP 800-61 Rev. 3은 이를 CSF 2.0의 위험관리와 연결합니다. [공식 개요](https://csrc.nist.gov/pubs/sp/800/61/r3/final)

랜섬웨어 상황에서 파일만 복원해도 유출된 계정이나 지속 접근이 남을 수 있습니다. 조사 사본·시각·원본 해시·수집 주체를 남기고 업무 복구와 원인 제거를 함께 진행합니다. 복구 시험에서는 백업 목록 존재보다 실제 내용·버전·권한·복구 시간을 확인합니다. 기존 [백업·RAID·파일시스템 사례](../설계와검증사례_engineering-cases/README.md)는 고장 후 자료 복원의 별도 실행 근거로 읽습니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/login_detection.py) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```python
"""직접 작성한 교육 예제: 합성 로그인 기록에서 이동 시간창의 실패 누적을 찾습니다."""
from collections import defaultdict, deque  # defaultdict는 키별 초기값을, deque는 앞쪽 삭제가 빠른 큐를 제공합니다.

def failure_alerts(events, window=60, threshold=3):  # window초 안에 threshold회 실패한 계정을 찾습니다.
    if window <= 0 or threshold < 1:  # 양수가 아닌 설정을 거부합니다.
        raise ValueError("invalid detector settings")  # 잘못된 설정에 명시적으로 실패합니다.
    pending = defaultdict(deque)  # 계정마다 실패 시각 큐를 만듭니다.
    previous = None  # 이전 이벤트 시각이 아직 없음을 표시합니다.
    alerts = []  # []는 순서가 있는 결과 리스트입니다.
    for event in events:  # for는 입력 이벤트를 순서대로 처리합니다.
        now = event["time"]  # time은 합성 기록의 정수 초입니다.
        if previous is not None and now < previous:  # 시각 역전을 검사합니다.
            raise ValueError("events must be time ordered")  # 조용히 잘못 집계하지 않습니다.
        previous = now  # 다음 이벤트의 순서 검사 기준을 저장합니다.
        queue = pending[event["account"]]  # 요청한 계정의 큐를 가져옵니다.
        while queue and queue[0] <= now - window:  # (now-window, now] 밖의 오래된 실패를 지웁니다.
            queue.popleft()  # deque의 맨 앞 항목을 O(1)에 제거합니다.
        if event["result"] == "failure":  # 이 예제에서 실패한 로그인만 집계합니다.
            queue.append(now)  # 현재 실패 시각을 큐 뒤에 추가합니다.
            if len(queue) >= threshold:  # len은 시간창 안의 실패 횟수입니다.
                alerts.append((event["account"], now, len(queue)))  # 임계값 이상인 사건을 튜플로 기록합니다.
    return alerts  # 입력을 자동 차단하지 않고 경보 후보를 반환합니다.
```

## 사고 대응은 탐지 뒤에도 이어지는 운영 절차입니다

NIST SP 800-61 Rev. 3은 사고 대응을 CSF 2.0 위험관리와 연결합니다. 운영에서는 준비, 분석과 우선순위 판단, 피해 제한, 위협 제거, 신뢰한 상태로 복구, 재발 방지 검토가 맞물립니다. 실제 사건은 단계가 겹칠 수 있으므로 한 번의 분류로 끝났다고 간주하지 않습니다. [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)

| 순서 | 결정 | 보존할 근거 |
| --- | --- | --- |
| 탐지·초기 분류 | 무엇이 언제 관측됐고 어떤 자산이 관련됐나요? | 원본 경보·로그·요청 ID·관측 시간입니다. |
| 범위 확인 | 계정·기기·자료·연결된 서비스 중 어디까지 영향이 있나요? | 로그인·권한·네트워크·배포 이력입니다. |
| 격리 | 계속되는 피해를 막으면서 운영·안전 영향을 어떻게 제한하나요? | 누가 어떤 장비·계정을 언제 격리했는지입니다. |
| 제거·복구 | 취약 경로·자격증명을 제거하고 어떤 신뢰 상태로 복구하나요? | 패치·키 폐기·백업 원본·복구 결과입니다. |
| 검증·사후 분석 | 공격 경로가 닫혔고 정상 기능이 유지되나요? | 재현·수정·회귀 결과와 남은 위험입니다. |

조사에 필요한 로그는 시간 동기·접근 통제·무결성을 고려해 보존합니다. 원본 장치를 급히 재설치하거나 로그를 덮으면 원인 분석 증거가 사라질 수 있습니다. 반대로 산업·의료 환경에서 격리가 안전 기능을 해칠 수 있으므로 보안 담당자만으로 제어 상태를 바꾸지 말고 현장 운영·안전 책임자와 결정합니다. 업무 복구와 공격자 접근 제거는 별도의 완료 조건으로 추적합니다.

## 원문에서 이어 읽기

- [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html): 기록할 사건·민감정보 제외·로그 위변조 대응입니다.
- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/): 전술·기술 행렬과 기법별 탐지 연결입니다.
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final): 공식 초록·CSF 2.0과 연결한 탐지·대응·복구입니다.

## English

Structured audit events support detection and investigation. The toy time-window detector assumes ordered synthetic events and does not implement production streaming state management.
