.section .text.start,"ax",@progbits # ELF 시작 코드를 먼저 배치
.balign 4 # 첫 RV32I 명령의4바이트 정렬
.globl _start # 링커가 찾을 진입점 공개
.type _start, @function # 진입점을 함수 심볼로 표시
_start: # QEMU의 부트 ROM에서 넘어올 시작 위치
    la sp, __stack_top # 16바이트로 정렬한 스택 최상단 설정
    .option push # 현재 어셈블러 옵션 보관
    .option norelax # gp 자체 초기화가 완화로 생략되지 않게 설정
    la gp, __global_pointer$ # ABI의 전역 포인터 기준값 설정
    .option pop # 이전 어셈블러 옵션 복원
    la t0, __bss_start # 0으로 지울 영역의 시작
    la t1, __bss_end # 0으로 지울 영역의 끝
.Lzero_bss: # 4바이트씩 BSS 초기화
    bgeu t0, t1, .Lcall_main # 빈 영역이나 끝에 도달하면 초기화 종료
    sw zero, 0(t0) # 정렬된 RAM 한 워드를0으로 저장
    addi t0, t0, 4 # 다음 워드 주소로 이동
    j .Lzero_bss # 남은 BSS 초기화 반복
.Lcall_main: # C 실행 환경의 최소 저장 영역 초기화 완료
    call main # C 검사 드라이버 진입
.Lhalt: # main이 예기치 않게 반환한 경우
    j .Lhalt # 실행을 다른 데이터 영역으로 흘려보내지 않기
.size _start, .-_start # 진입 코드의 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 스택을 요구하지 않는 표시
