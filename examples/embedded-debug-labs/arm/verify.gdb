set pagination off
set confirm off
set remotetimeout 20
target remote 127.0.0.1:3341
monitor start
set $pc=(unsigned long)&Reset_Handler
break main
break lesson_done
continue
printf "AT_MAIN: input_a=%u input_b=%u result=%u trace=%u,%u\n", input_a,input_b,result,trace[0],trace[1]
disassemble /m main
info registers
continue
printf "AT_DONE: input_a=%u input_b=%u result=%u trace=%u,%u\n", input_a,input_b,result,trace[0],trace[1]
x/2wx &input_a
x/wx &result
x/2wx &trace
if input_a != 1 || input_b != 3 || result != 4 || trace[0] != 4 || trace[1] != 5
  echo VERIFICATION_FAILED\n
  quit 1
end
echo VERIFICATION_PASSED\n
detach
quit
