.section .text # 실행할 함수 코드를 text 영역에 배치
.balign 4 # RV32I 명령 시작을4바이트에 맞추기
.globl update_field # C에서 호출할 함수 이름 공개
.type update_field, @function # ELF 심볼을 함수로 표시
update_field: # a0=원래값,a1=새비트,a2=시작,a3=폭
    beq a3, zero, .Lfield_return # 폭0이면 원래값을 그대로 반환
    addi t0, zero, 32 # 전체 레지스터 폭 비교 상수
    beq a3, t0, .Lfield_full # 폭32의 특별 경로로 shift32 문제 피하기
    addi t0, zero, 1 # 낮은 비트 마스크를 만들 시작값
    sll t0, t0, a3 # 1을 필드 폭만큼 이동
    addi t0, t0, -1 # 낮은 width개 비트가1인 마스크
    sll t1, t0, a2 # 실제 필드 위치로 마스크 이동
    xori t2, t1, -1 # 필드 밖은1이고 안쪽은0인 보존 마스크
    and a0, a0, t2 # 원래값의 필드 부분만 지우기
    and a1, a1, t0 # 새비트에서 필드 폭을 넘는 부분 제거
    sll a1, a1, a2 # 새 필드값을 시작 위치로 이동
    or a0, a0, a1 # 보존한 비트와 새 필드를 결합
.Lfield_return: # a0가 반환값인 공통 경로
    ret # ra로 돌아가는 jalr 의사 명령
.Lfield_full: # 유효 계약상 폭32이면 시작 위치는0
    addi a0, a1, 0 # 전체32비트를 새값으로 교체
    ret # 호출자에게 새값 반환
.size update_field, .-update_field # 함수의 코드 길이 기록

.balign 4 # 두 번째 함수도4바이트 경계에 배치
.globl byte_sum # C에서 호출할 검사합 함수 공개
.type byte_sum, @function # ELF 함수 심볼 표시
byte_sum: # a0=일반RAM 바이트 주소,a1=길이
    addi t0, a0, 0 # 읽기 포인터를 임시 레지스터에 보관
    addi a0, zero, 0 # 반환 레지스터를 합0으로 초기화
    beq a1, zero, .Lsum_return # 길이0이면 주소를 읽지 않고 반환
.Lsum_loop: # 아직 읽지 않은 바이트가 있는 반복
    lbu t1, 0(t0) # 현재 바이트를 부호 없이0~255로 읽기
    add a0, a0, t1 # 32비트 모듈러 합 누적
    addi t0, t0, 1 # 다음 바이트 주소로 전진
    addi a1, a1, -1 # 남은 바이트 수 하나 감소
    bne a1, zero, .Lsum_loop # 남은 바이트가 있으면 계속 읽기
.Lsum_return: # a0에 최종 검사합 보관
    ret # 합을 유지한 채 호출자 복귀
.size byte_sum, .-byte_sum # 검사합 함수 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 가능한 스택을 요청하지 않는 표시
