import argparse  # RTLIL 출력 모드의 명령줄 선택
from amaranth import ClockDomain, ClockSignal, Elaboratable, Module, Signal  # 하드웨어 신호와 회로 구성
from amaranth.back import rtlil  # 외부 합성 도구 없이 RTLIL 생성

class Mod10Counter(Elaboratable):  # Python으로 정의하는 회로 생성기
    def __init__(self):  # 회로의 포트와 상태 신호 생성
        self.clear = Signal(name="clear")  # enable보다 우선하는 동기 초기화
        self.enable = Signal(name="enable")  # 1인 클록에서만 증가
        self.count = Signal(range(10), name="count", init=0)  # 표현 폭은 네 비트이며 순환은 직접 정의
    def elaborate(self, platform):  # 회로 구조를 구성하는 단계
        module = Module()  # 동시 회로와 동기 회로를 담는 객체
        module.domains += ClockDomain("sync", reset_less=True)  # 별도 숨은 reset 대신 clear 입력 사용
        with module.If(self.clear):  # 하드웨어 우선순위 선택 회로
            module.d.sync += self.count.eq(0)  # 상승 에지의 초기화 값
        with module.Elif(self.enable):  # clear가 0이고 증가가 허용된 경우
            with module.If(self.count == 9):  # 십진 순환 경계
                module.d.sync += self.count.eq(0)  # 9 다음을 0으로 지정
            with module.Else():  # 0부터 8인 상태
                module.d.sync += self.count.eq(self.count + 1)  # 레지스터의 다음 값
        return module  # 완성한 하드웨어 구조 반환

def main():  # 회로를 파일로 내보내는 독립 실행
    parser = argparse.ArgumentParser()  # 명령줄 도움말 구성
    parser.add_argument("--rtlil", action="store_true", help="emit RTLIL to stdout")  # RTLIL 생성 선택
    arguments = parser.parse_args()  # 실행 옵션 읽기
    if arguments.rtlil:  # 명시적으로 요청한 출력 모드
        dut = Mod10Counter()  # 변환할 회로 구성
        print(rtlil.convert(dut, name="mod10_counter", ports=[ClockSignal("sync"), dut.clear, dut.enable, dut.count], emit_src=False), end="")  # 기계별 소스 경로를 빼고 클록과 세 포트의 RTLIL 출력
    else:  # 시험 실행 명령 안내
        parser.error("use --rtlil; run test_counter.py for simulation")  # 모드 없는 실행은 명확히 구분

if __name__ == "__main__":  # 직접 실행할 때만 변환 시작
    main()  # 입력과 회로 변환 처리
