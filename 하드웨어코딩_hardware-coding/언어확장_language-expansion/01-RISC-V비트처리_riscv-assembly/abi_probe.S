.section .text # ABI 검사 전용 코드 영역
.balign 4 # 함수 시작의4바이트 정렬
.globl abi_probe # C에서 부를 보존 레지스터 검사
.type abi_probe, @function # 함수 심볼 표시
abi_probe: # 호출 뒤 s레지스터 보존과 스택 정렬 확인
    addi sp, sp, -64 #16바이트 정렬을 유지하며 저장 프레임 확보
    sw ra, 0(sp) # 두 함수 호출 전 원래 복귀 주소 보관
    sw s0, 4(sp) # 호출자의 s0 원래값을 스택에 보존
    sw s1, 8(sp) # 호출자의 s1 원래값을 스택에 보존
    sw s2, 12(sp) # 호출자의 s2 원래값을 스택에 보존
    sw s3, 16(sp) # 호출자의 s3 원래값을 스택에 보존
    sw s4, 20(sp) # 호출자의 s4 원래값을 스택에 보존
    sw s5, 24(sp) # 호출자의 s5 원래값을 스택에 보존
    sw s6, 28(sp) # 호출자의 s6 원래값을 스택에 보존
    sw s7, 32(sp) # 호출자의 s7 원래값을 스택에 보존
    sw s8, 36(sp) # 호출자의 s8 원래값을 스택에 보존
    sw s9, 40(sp) # 호출자의 s9 원래값을 스택에 보존
    sw s10, 44(sp) # 호출자의 s10 원래값을 스택에 보존
    sw s11, 48(sp) # 호출자의 s11 원래값을 스택에 보존
    addi s0, zero, 1 # s0에 보존 여부를 확인할 고유값 설정
    addi s1, zero, 2 # s1에 보존 여부를 확인할 고유값 설정
    addi s2, zero, 3 # s2에 보존 여부를 확인할 고유값 설정
    addi s3, zero, 4 # s3에 보존 여부를 확인할 고유값 설정
    addi s4, zero, 5 # s4에 보존 여부를 확인할 고유값 설정
    addi s5, zero, 6 # s5에 보존 여부를 확인할 고유값 설정
    addi s6, zero, 7 # s6에 보존 여부를 확인할 고유값 설정
    addi s7, zero, 8 # s7에 보존 여부를 확인할 고유값 설정
    addi s8, zero, 9 # s8에 보존 여부를 확인할 고유값 설정
    addi s9, zero, 10 # s9에 보존 여부를 확인할 고유값 설정
    addi s10, zero, 11 # s10에 보존 여부를 확인할 고유값 설정
    addi s11, zero, 12 # s11에 보존 여부를 확인할 고유값 설정
    addi a0, zero, 123 # 비트필드 검사의 원래값
    addi a1, zero, 45 # 새 필드 값
    addi a2, zero, 4 # 필드 시작 위치
    addi a3, zero, 5 # 필드 폭
    call update_field # 첫 어셈블리 함수 호출
    addi a0, zero, 0 # 길이0 검사에서는 주소를 읽지 않음
    addi a1, zero, 0 # 빈 검사합 요청
    call byte_sum # 두 번째 어셈블리 함수 호출
    andi t0, sp, 15 # 현재 스택의16바이트 정렬 확인
    bne t0, zero, .Labi_fail # 정렬 위반이면 실패
    addi t0, zero, 1 # s0의 보존 기대값
    bne s0, t0, .Labi_fail # 호출 전 s0 값이 바뀌면 실패
    addi t0, zero, 2 # s1의 보존 기대값
    bne s1, t0, .Labi_fail # 호출 전 s1 값이 바뀌면 실패
    addi t0, zero, 3 # s2의 보존 기대값
    bne s2, t0, .Labi_fail # 호출 전 s2 값이 바뀌면 실패
    addi t0, zero, 4 # s3의 보존 기대값
    bne s3, t0, .Labi_fail # 호출 전 s3 값이 바뀌면 실패
    addi t0, zero, 5 # s4의 보존 기대값
    bne s4, t0, .Labi_fail # 호출 전 s4 값이 바뀌면 실패
    addi t0, zero, 6 # s5의 보존 기대값
    bne s5, t0, .Labi_fail # 호출 전 s5 값이 바뀌면 실패
    addi t0, zero, 7 # s6의 보존 기대값
    bne s6, t0, .Labi_fail # 호출 전 s6 값이 바뀌면 실패
    addi t0, zero, 8 # s7의 보존 기대값
    bne s7, t0, .Labi_fail # 호출 전 s7 값이 바뀌면 실패
    addi t0, zero, 9 # s8의 보존 기대값
    bne s8, t0, .Labi_fail # 호출 전 s8 값이 바뀌면 실패
    addi t0, zero, 10 # s9의 보존 기대값
    bne s9, t0, .Labi_fail # 호출 전 s9 값이 바뀌면 실패
    addi t0, zero, 11 # s10의 보존 기대값
    bne s10, t0, .Labi_fail # 호출 전 s10 값이 바뀌면 실패
    addi t0, zero, 12 # s11의 보존 기대값
    bne s11, t0, .Labi_fail # 호출 전 s11 값이 바뀌면 실패
    addi a0, zero, 0 # 모든 보존 검사가 맞으면 성공0
    j .Labi_restore # 호출자 상태를 복구하는 공통 경로
.Labi_fail: # 보존 또는 정렬 불일치
    addi a0, zero, 1 # 검사 실패1 반환
.Labi_restore: # 검사 결과와 무관하게 원래 저장 상태 복원
    lw s0, 4(sp) # 호출자의 s0 원래값 복원
    lw s1, 8(sp) # 호출자의 s1 원래값 복원
    lw s2, 12(sp) # 호출자의 s2 원래값 복원
    lw s3, 16(sp) # 호출자의 s3 원래값 복원
    lw s4, 20(sp) # 호출자의 s4 원래값 복원
    lw s5, 24(sp) # 호출자의 s5 원래값 복원
    lw s6, 28(sp) # 호출자의 s6 원래값 복원
    lw s7, 32(sp) # 호출자의 s7 원래값 복원
    lw s8, 36(sp) # 호출자의 s8 원래값 복원
    lw s9, 40(sp) # 호출자의 s9 원래값 복원
    lw s10, 44(sp) # 호출자의 s10 원래값 복원
    lw s11, 48(sp) # 호출자의 s11 원래값 복원
    lw ra, 0(sp) # 원래 복귀 주소 복원
    addi sp, sp, 64 # 저장 프레임 반환
    ret # C 검사 드라이버로 복귀
.size abi_probe, .-abi_probe # ABI 검사 코드 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 스택을 요구하지 않는 표시
