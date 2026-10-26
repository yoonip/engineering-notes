from collections import deque  # 수락 순서만 저장하는 독립 기준 큐
import cocotb  # HDL 시뮬레이터 안의 테스트 등록
import sys  # 내장 Python의 실제 실행 버전 확인
from cocotb.triggers import ReadOnly, Timer  # 시간과 안정된 관측 시점 제어

@cocotb.test()  # 버퍼 한 개의 기능 테스트 등록
async def stalls_replacement_and_reset(dut):  # DUT 내부 full·stored는 읽지 않기
    print(f"RUNTIME python={sys.version.split()[0]}")  # 내장 Python의 실제 런타임 버전 기록
    queue = deque()  # 아직 소비되지 않은 외부 항목
    accepted = consumed = cancelled = stalls = replacements = checks = 0  # 실제 사건 집계
    stimuli = [(1, 1, 255, 1), (0, 1, 17, 0), (0, 0, 17, 0), (0, 1, 34, 0), (0, 1, 34, 1), (0, 0, 0, 1), (0, 1, 51, 0), (1, 1, 68, 1)]  # 직접 구성한 핵심 경계
    stimuli += [(int(i == 31), int(i % 4 != 0), i, int(i % 5 >= 2)) for i in range(64)]  # 속도 차이와 중간 리셋
    stimuli += [(0, 0, 0, 1), (0, 0, 0, 1)]  # 마지막 항목 소비와 가짜 출력 검사
    dut.clk.value = 0  # 첫 클록 전의 기준 수준
    for cycle, (reset, valid, data, ready) in enumerate(stimuli):  # 고정된 74주기 자극
        dut.rst.value = reset  # 리셋은 출력 마스킹과 에지 취소에 사용
        dut.in_valid.value = valid  # 이번에 제시한 입력의 유효 표시
        dut.in_data.value = data  # 8비트 입력 값
        dut.out_ready.value = ready  # 소비자가 받을 수 있는지 표시
        await Timer(4, unit="ns")  # 상승 에지 이전의 관측 위치
        await ReadOnly()  # ready·valid 조합 출력이 안정된 뒤 읽기
        can_accept = not reset and (not queue or ready)  # 빈자리 또는 같은 에지의 소비
        has_output = not reset and bool(queue)  # 리셋 중에는 출력 전송 없음
        assert int(dut.in_ready.value) == can_accept, f"ready cycle={cycle}"  # 수락 가능 여부 대조
        assert int(dut.out_valid.value) == has_output, f"valid-before cycle={cycle}"  # 에지 전 항목 존재 대조
        checks += 2  # 두 제어 신호 비교 집계
        if has_output:  # 유효할 때만 데이터에 의미 부여
            assert int(dut.out_data.value) == queue[0], f"data-before cycle={cycle}"  # 값과 순서 유지
            checks += 1  # 데이터 비교 집계
        stalls += int(has_output and not ready)  # 정체를 실제 관측
        replacements += int(has_output and ready and valid and can_accept)  # 동시 소비와 교체 관측
        if reset:  # 리셋 에지에서는 수락과 소비 대신 취소
            cancelled += len(queue)  # 취소한 항목 개수
            queue.clear()  # 이전 구간의 항목 제거
        else:  # 정상 에지의 외부 전송 계약
            if has_output and ready:  # 이전 출력부터 소비
                queue.popleft()  # 앞 항목 제거
                consumed += 1  # 실제 소비 집계
            if valid and can_accept:  # 수락한 입력만 기대 큐에 추가
                queue.append(data)  # 새 항목의 순서 보관
                accepted += 1  # 실제 수락 집계
        await Timer(1, unit="ns")  # 주기의 5ns 위치
        dut.clk.value = 1  # DUT의 저장 에지 발생
        await Timer(1, unit="ns")  # 순차 갱신이 끝난 6ns 위치
        await ReadOnly()  # 갱신된 출력 관측
        assert len(queue) <= 1, f"capacity cycle={cycle}"  # 한 칸의 기대 점유 상한
        assert int(dut.out_valid.value) == (not reset and bool(queue)), f"valid-after cycle={cycle}"  # 에지 뒤 유효 상태
        checks += 2  # 용량·유효 상태 비교 집계
        if not reset and queue:  # 새 출력 또는 정체로 보존한 항목
            assert int(dut.out_data.value) == queue[0], f"data-after cycle={cycle}"  # 내용이 유실되거나 바뀌지 않기
            checks += 1  # 에지 뒤 데이터 비교 집계
        await Timer(4, unit="ns")  # 다음 주기로 이동
        dut.clk.value = 0  # 다음 상승 에지 준비
    assert not queue  # 마지막 항목이 남지 않아야 종료
    assert accepted == consumed + cancelled  # 수락 항목의 개수 보존
    assert stalls > 0 and replacements > 0 and cancelled > 0  # 핵심 시나리오가 실제로 실행됨
    checks += 3  # 마지막 세 조건도 집계
    print(f"PASS buffer cycles={len(stimuli)} checks={checks} accepted={accepted} consumed={consumed} cancelled={cancelled} stalls={stalls} replacements={replacements}")  # 실제 결과 출력
