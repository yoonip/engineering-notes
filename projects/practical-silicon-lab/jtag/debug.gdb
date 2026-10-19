# Run from jtag/ after building. OpenOCD must already be listening.
set pagination off
set confirm off
file build/blink.elf
target extended-remote 127.0.0.1:3333
# The following load changes the lab board's application flash.
monitor reset halt
load
monitor verify_image build/blink.elf
monitor reset halt
# Stop at C entry before GPIO writes; source symbols come from the ELF.
break main
continue
info registers pc sp xpsr
print/x magic
print/x blink_count
print/x phase
x/2wx 0x08000000
x/wx 0x40023830
# Inspect execution with next, step, continue, Ctrl-C, and x/wx.
