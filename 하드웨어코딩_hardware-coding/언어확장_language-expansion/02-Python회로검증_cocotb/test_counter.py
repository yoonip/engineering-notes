import cocotb  # HDL 시뮬레이터 안에서 Python 테스트 등록
import sys  # 내장 Python의 실제 실행 버전 확인
from cocotb.triggers import ReadOnly, Timer  # 시간 이동과 안정된 출력 관측

@cocotb.test()  # 이 코루틴을 실제 시뮬레이션 테스트로 등록
async def counter_boundaries(dut):  # DUT 핸들로 외부 포트만 사용
    print(f"RUNTIME python={sys.version.split()[0]}")  # 도구 빌드 배너와 실제 런타임 버전 구분
    expected = 0  # 첫 clear 뒤부터 사용할 독립 정수 기준
    checks = 0  # 실제 실행한 assert 수
    wraps = 0  # enable이 켜진 9에서 0으로의 전이 수
    dut.clk.value = 0  # 첫 상승 에지 전의 낮은 클록
    for cycle in range(80):  # 재현 가능한 80주기 자극
        clear = int(cycle in (0, 17, 18, 47, 79))  # 시작·연속·중간·마지막 초기화
        enable = int(cycle % 5 != 2)  # 매 다섯 주기마다 한 번 정지
        dut.clear.value = clear  # 초기화 입력 구동
        dut.enable.value = enable  # 증가 허용 입력 구동
        await Timer(4, unit="ns")  # 주기의 4ns 위치로 이동
        await ReadOnly()  # 해당 시각의 HDL 평가가 끝난 뒤 읽기
        if cycle > 0:  # 리셋 전 첫 레지스터 값은 가정하지 않기
            assert int(dut.count.value) == expected, f"pre-edge cycle={cycle}"  # 클록 전 값 유지
            checks += 1  # 실제 비교 한 건 집계
        if clear:  # 모델도 clear 우선
            expected = 0  # 리셋 후 기준값
        elif enable:  # 정지 주기에는 기준도 유지
            wraps += int(expected == 9)  # 실제 순환 경계 집계
            expected = (expected + 1) % 10  # RTL 조건식 대신 정수 나머지 기준
        await Timer(1, unit="ns")  # 주기의 5ns 상승 에지 위치
        dut.clk.value = 1  # 실제 HDL 플립플롭 구동
        await Timer(1, unit="ns")  # nonblocking 갱신 이후의 6ns 위치
        await ReadOnly()  # 안정된 레지스터 출력 읽기
        actual = int(dut.count.value)  # X가 남으면 정수 변환도 실패
        assert actual == expected, f"post-edge cycle={cycle}"  # 계산한 다음 상태와 대조
        assert 0 <= actual <= 9, f"decimal range cycle={cycle}"  # 십진 범위 유지
        checks += 2  # 값·범위 두 비교 집계
        await Timer(4, unit="ns")  # 다음 주기의 0ns 위치
        dut.clk.value = 0  # 다음 상승 에지를 위한 하강
    assert wraps == 5  # 순환 경계를 실제로 다섯 번 통과했는지 확인
    checks += 1  # 시나리오 검사도 실제 개수에 포함
    print(f"PASS counter cycles=80 checks={checks} wraps={wraps}")  # 완료 근거를 로그에 남기기
