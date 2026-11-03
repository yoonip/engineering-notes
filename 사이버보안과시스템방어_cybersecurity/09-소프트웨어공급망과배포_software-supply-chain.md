# 소프트웨어 공급망과 배포 | Software supply chain

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 소스가 맞아도 배포물이 달라질 수 있습니다

의존성·컴파일러·빌드 스크립트·CI 계정·패키지 저장소·배포 키가 결과물을 바꿀 수 있습니다. 공급망 보안은 ‘라이브러리에 CVE가 있는가’뿐 아니라 누가 어떤 소스로 무엇을 만들고 누가 배포를 승인했는지 연결하는 일입니다. [NIST SSDF 1.1의 SDLC 보안 개발 목적](https://csrc.nist.gov/pubs/sp/800/218/final)

SBOM은 구성요소 목록이고 provenance는 빌드 출처·과정의 근거입니다. 서명은 특정 키의 인증이며 서명된 코드가 무해하다는 증명은 아닙니다. 재현 가능한 빌드는 같은 조건의 결과물 일치를 확인하는 데 도움을 주지만, 신뢰하지 않는 소스가 정확히 재현될 수도 있습니다.

## SHA를 고정하는 이유와 한계

패키지 이름이나 변경 가능한 태그만 사용하면 같은 명령의 결과가 시간이 지나 바뀔 수 있습니다. 버전·해시·실제 가져온 출처를 기록하고 교체는 검토된 변경으로 수행합니다. 해시가 맞는지는 [digest 실습](실습_labs/artifact_digest.py)으로 확인할 수 있습니다. 받은 파일과 같은 곳에서 받은 해시를 모두 공격자가 바꿀 수 있다면 검사는 통과합니다. 따라서 신뢰 경로·서명 키·배포 정책이 먼저 필요합니다.

## CI에 입력이 명령으로 들어가는 경로

PR 제목·브랜치명·issue 본문은 외부 입력입니다. 이를 shell 코드에 직접 끼워 넣으면 워크플로가 의도하지 않은 문법을 실행할 수 있습니다. 비밀이 있는 작업과 신뢰하지 않는 코드를 실행하는 작업을 분리하고, GITHUB_TOKEN 기본 권한을 줄이며 외부 action을 검토한 전체 commit SHA로 고정하는 방법을 사용합니다. [GitHub Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

외부 PR을 테스트했다고 운영 배포 자격증명을 제공할 이유는 없습니다. self-hosted runner는 작업 종료 뒤 남는 상태·네트워크 권한·호스트 자료까지 고려해야 합니다. 일회용 runner도 이미 작업 중 유출한 비밀을 되돌리지는 못합니다.

## 배포 전후에 남길 근거

| 단계 | 남길 내용 |
| --- | --- |
| 소스 선택 | 저장소·commit·검토자·의존성 잠금 파일입니다. |
| 빌드 | 도구 판본·환경·명령·입력 해시·산출물 digest입니다. |
| 검사 | 정상·오류 재현·권한·정적 분석의 실제 결과입니다. |
| 승인 | 대상 환경·산출물·권한·승인 시점의 결합입니다. |
| 배포 | 설치한 digest·서비스 상태·되돌릴 조건입니다. |

secret이 공개되면 파일을 삭제하는 것만으로 충분하지 않습니다. 기존 값을 폐기·교체하고 사용 흔적을 확인합니다. 서명 키 유출과 일반 문서 오타는 대응 범위가 다르므로 같은 절차로 처리하지 않습니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/artifact_digest.py) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```python
"""직접 작성한 교육 예제: 신뢰한 기준 해시와 받은 바이트의 일치 여부를 검사합니다."""
import hashlib  # hashlib는 표준 해시 알고리즘을 제공합니다.
import hmac  # compare_digest로 동일 자료형의 digest를 비교합니다.

def matches_pinned_digest(data, expected_hex):  # expected_hex는 별도 신뢰 경로에서 받은 64자리 SHA-256입니다.
    if not isinstance(expected_hex, str) or len(expected_hex) != 64:  # 기준 해시의 자료형과 길이를 확인합니다.
        return False  # 형식이 잘못됐으면 검사에 실패합니다.
    try:  # 잘못된 16진수 문자열 변환의 예외를 처리합니다.
        expected = bytes.fromhex(expected_hex)  # 클래스 메서드로 16진수 문자열을 바이트로 바꿉니다.
    except ValueError:  # 변환할 수 없는 문자가 있으면 이 분기를 실행합니다.
        return False  # 잘못된 기준을 정상 값으로 취급하지 않습니다.
    return len(expected) == 32 and hmac.compare_digest(hashlib.sha256(data).digest(), expected)  # and는 두 조건이 모두 맞아야 True를 반환합니다.
```

## 원문에서 이어 읽기

- [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final): 공식 초록·SDLC에 보안 개발 활동을 넣는 목적입니다.
- [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): 최소 토큰 권한·외부 입력·SHA 고정·신뢰하지 않는 코드 checkout입니다.

## English

Supply-chain evidence connects source, dependencies, builders, artifacts and deployment authority. A matching digest requires a trusted reference.
