# 실무 검증의 오류 재현 코드 | Reproducible engineering fault examples

정상 경로와 의도적으로 잘못 만든 경로를 같은 입력에서 비교합니다. 실행이 끝났는지, 오류가 기대대로 검출됐는지, 해결 경로가 계약을 만족하는지를 따로 확인합니다. 각 코드의 실측·호스트 실행·소프트웨어 모형 범위는 해당 안내에 적었습니다.

| 분야 | 코드와 실행 방법 | 관측과 해설 |
| --- | --- | --- |
| C·C++·펌웨어 | [native_firmware](native_firmware/README.md): C11·C++17 세 프로그램과 빌드 러너 | 프레임 길이 16,496조합, 뷰·소유 복사, 여섯 공개 순서, SPSC 순차 wrap 검사 |
| 칩·시험 데이터 | [chip](chip/README.md): 표준 라이브러리 Python 실행기 | 레이아웃·누산 폭·명시적 wrap, 제품 ID 연결과 오판율, 분리된 통과 구간 |
| AI 학습·배포·평가 | [ai](ai/README.md): 작은 합성 모델 두 실행기 | 특성 순서·저장 scaler·입력 거부, 행/group 분할과 평가 정보 유입 |

[설계와 검증 사례](../../설계와검증사례_engineering-cases/README.md)에서 원인과 해결을 읽고, [현장 계측과 검증](../../현장계측과검증_measurement-validation/README.md)에서 장비·펌웨어·칩 시험 조건으로 연결합니다.

## 기록 보존

실행기는 매번 새로운 결과 폴더를 요구합니다. 입력·소스 해시, 환경, 명령과 종료 상태를 남기며, 제품 FAIL을 재현했다고 실행기 자체가 실패한 것으로 합치지 않습니다. C/C++ 검사는 NDEBUG가 켜진 채라면 빌드를 거부합니다. Python 모형은 장비에 접속하지 않습니다.

## English

Three sets of runnable examples connect deliberately faulty controls with intended fixes: native frame/ownership/publication contracts, chip arithmetic/test-data analysis, and AI serving/group evaluation. New output directories preserve earlier failures. Software models and host checks are explicitly separated from physical measurements.
