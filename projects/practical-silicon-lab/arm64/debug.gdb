set pagination off
set confirm off
file build/bringup.elf
target remote 127.0.0.1:1234
info registers pc sp
x/8i $pc
break main
continue
info registers pc sp
print/x phase
# Use next/step/continue interactively from here.
