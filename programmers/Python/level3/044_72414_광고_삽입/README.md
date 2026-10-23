# 광고 삽입

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [72414 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/72414)

## 문제와 조건

동영상에 고정 길이 광고를 한 번 넣어 시청자들의 누적 시청시간을 최대화하는 가장 이른 시작 시각을 구합니다.

시청 로그는 시작 포함·종료 제외이며 중복 시청도 각각 합산합니다. 누적 시청시간 최대, 동점은 가장 이른 광고 시작입니다.

`00:00:01≤adv_time≤play_time≤99:59:59; 1≤logs≤300,000; 0≤start<end≤play_time`

## 풀이를 따라가기

1. 차분 배열로 초별 시청자 수를 만든 후, 누적 합으로 광고 길이만큼의 구간 합을 모두 비교합니다.
2. 예: 광고 구간 [start,end)의 시청 재생 초 T·로그 L개에서 시간 O(T+L), 공간 O(T)
3. 시간 O(시청 기록 수 + 영상의 초 수), 공간 O(영상의 초 수). 최대 영상 길이는 359999초라 초 단위 계산이 가능합니다.

## 왜 이 방법으로 풀 수 있나

차분 배열로 초별 시청자 수를 만든 후, 누적 합으로 광고 길이만큼의 구간 합을 모두 비교합니다.

시간·공간: 재생 초 T·로그 L개에서 시간 O(T+L), 공간 O(T)

## 다른 방법과 비교

모든 광고 시작 초마다 각 시청 구간과 겹치는 길이를 직접 더합니다. 시작 포함·끝 제외 구간과 가장 이른 동점 선택을 독립적으로 확인합니다.

| 항목 | 기본 풀이 | 광고 구간 교집합 직접 합산 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 재생 초 T·로그 L개에서 시간 O(T+L), 공간 O(T) | O(재생 초·로그 수), 짧은 영상 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `["02:03:55", "00:14:15", ["01:20:15-01:45:14", "00:40:31-01:00:00", "00:25:50-00:48:29", "01:30:59-01:53:29", "01:37:44-02:02:30"]]` | `"01:30:59"` |
| `["99:59:59", "25:00:00", ["69:59:59-89:59:59", "01:00:00-21:00:00", "79:59:59-99:59:59", "11:00:00-31:00:00"]]` | `"01:00:00"` |
| `["50:00:00", "50:00:00", ["15:36:51-38:21:49", "10:14:18-15:36:51", "38:21:49-42:51:45"]]` | `"00:00:00"` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the earliest fixed-length advertisement start maximizing total viewer-time.

Viewing intervals include start and exclude end; every viewer contributes separately. Maximize viewer-time and prefer the earliest start on ties.

`00:00:01≤adv_time≤play_time≤99:59:59; 1≤logs≤300,000; 0≤start<end≤play_time`

### Method and correctness

Convert times to seconds and treat viewing logs as half-open intervals. A difference array builds viewers per second; a second prefix sum gives cumulative viewer-seconds. Every advertisement interval is then one prefix subtraction. Update only on strict improvement to keep the earliest start on ties.

Main complexity: O(play seconds+logs) time, O(play seconds) space.

### Alternative and trade-offs

For each advertisement start second, sum its intersection length with every viewing interval. This directly checks half-open endpoints and earliest-start tie breaking.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(play seconds·logs), short-video oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 광고 삽입](https://school.programmers.co.kr/learn/courses/30/lessons/72414) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
