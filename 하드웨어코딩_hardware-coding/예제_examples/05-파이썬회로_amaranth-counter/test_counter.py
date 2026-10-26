from amaranth.sim import Simulator  # HDL 회로를 평가하는 시뮬레이터
from counter import Mod10Counter  # 검증할 원본 회로 생성기

async def bench(context):  # 시뮬레이션 시간에 맞춰 실행하는 테스트벤치
    expected = 0  # Python 정수 modulo의 독립 기준
    checks = 0  # 실제로 수행한 assert 수
    for cycle in range(80):  # VHDL과 같은 클록별 자극
        clearing = cycle in (0, 17, 18, 47, 79)  # 초기화와 증가의 우선순위 검사
        enabled = cycle % 5 != 2  # 주기적으로 증가 정지
        context.set(dut.clear, clearing)  # 상승 에지 전에 초기화 입력 변경
        context.set(dut.enable, enabled)  # 상승 에지 전에 enable 변경
        await context.delay(4e-9)  # 5ns 상승 에지보다 앞선 4ns 시각
        assert context.get(dut.count) == expected, "changed before rising edge"  # 에지 없이 입력만 바뀌면 상태 유지
        checks += 1  # 에지 전 유지 검사 집계
        if clearing:  # 기준 모델의 초기화 우선순위
            expected = 0  # 다음 기준 값
        elif enabled:  # 증가가 허용된 클록
            expected = (expected + 1) % 10  # 명시적 if9 대신 정수 나머지로 비교
        await context.tick()  # 상승 에지와 조합 출력 안정화까지 진행
        await context.delay(1e-9)  # VHDL과 같은 상승 뒤 1ns 검사 시각
        assert context.get(dut.count) == expected, "incorrect count after rising edge"  # 회로 다음 상태 비교
        checks += 1  # 기능 검사 집계
        assert 0 <= context.get(dut.count) <= 9, "count outside decimal range"  # 네 비트의 10부터15를 제외
        checks += 1  # 십진 범위 검사 집계
        await context.delay(4e-9)  # 다음 주기의 입력 변경 시점으로 이동
    print(f"PASS mod10_counter cycles=80 checks={checks}")  # 실제 검사 수와 성공 표식

if __name__ == "__main__":  # 독립 시뮬레이션 실행
    dut = Mod10Counter()  # 테스트할 회로 인스턴스
    simulator = Simulator(dut)  # 회로를 시뮬레이터에 전달
    simulator.add_clock(10e-9)  # 주기10ns, 첫 상승 에지5ns
    simulator.add_testbench(bench)  # 입력 생성과 검사 등록
    simulator.run()  # 테스트벤치가 끝날 때까지 실행
