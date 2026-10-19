"""순수 Python RV32I ISA reference: RTL의 cycle/상태와 독립적인 명령 단위 모델."""
import json
from pathlib import Path

MASK = 0xffffffff
def signed(v): return v if v < 0x80000000 else v - 0x100000000
def sext(v, bits): return v - (1 << bits) if v & (1 << (bits-1)) else v


def run_reference(binary: bytes, out: Path):
    ram = bytearray(65536); ram[:len(binary)] = binary
    x = [0]*32; pc = 0; trace = []; mailbox = {}; counts = {}
    cause = None
    for step in range(1000000):
        if pc & 3: cause=0; break
        if pc >= len(ram): cause=1; break
        ins = int.from_bytes(ram[pc:pc+4], 'little')
        op=ins&127; rd=(ins>>7)&31; f=(ins>>12)&7
        ra=(ins>>15)&31; rb=(ins>>20)&31; hi=ins>>25
        a,b=x[ra],x[rb]; npc=pc+4; value=None
        ii=sext(ins>>20,12)
        si=sext(((ins>>25)<<5)|((ins>>7)&31),12)
        bi=sext(((ins>>31)<<12)|(((ins>>7)&1)<<11)|
                (((ins>>25)&63)<<5)|(((ins>>8)&15)<<1),13)
        ji=sext(((ins>>31)<<20)|(((ins>>12)&255)<<12)|
                (((ins>>20)&1)<<11)|(((ins>>21)&1023)<<1),21)
        if op==0x37: value=ins&0xfffff000
        elif op==0x17: value=pc+(ins&0xfffff000)
        elif op==0x6f: value=pc+4; npc=(pc+ji)&MASK
        elif op==0x67:
            if f: cause=2; break
            value=pc+4; npc=((a+ii)&MASK)&~1
        elif op==0x63:
            predicates={0:a==b,1:a!=b,4:signed(a)<signed(b),
                        5:signed(a)>=signed(b),6:a<b,7:a>=b}
            if f not in predicates: cause=2; break
            if predicates[f]: npc=(pc+bi)&MASK
        elif op==0x13:
            if f==0: value=a+ii
            elif f==2: value=int(signed(a)<ii)
            elif f==3: value=int(a<(ii&MASK))
            elif f==4: value=a^(ii&MASK)
            elif f==6: value=a|(ii&MASK)
            elif f==7: value=a&(ii&MASK)
            elif f==1 and hi==0: value=a<<((ins>>20)&31)
            elif f==5 and hi==0: value=a>>((ins>>20)&31)
            elif f==5 and hi==32: value=signed(a)>>((ins>>20)&31)
            else: cause=2; break
        elif op==0x33:
            if f==0 and hi in (0,32): value=a+b if hi==0 else a-b
            elif f==1 and hi==0: value=a<<(b&31)
            elif f==2 and hi==0: value=int(signed(a)<signed(b))
            elif f==3 and hi==0: value=int(a<b)
            elif f==4 and hi==0: value=a^b
            elif f==5 and hi in (0,32): value=a>>(b&31) if hi==0 else signed(a)>>(b&31)
            elif f==6 and hi==0: value=a|b
            elif f==7 and hi==0: value=a&b
            else: cause=2; break
        elif op in (3,0x23):
            allowed=(0,1,2,4,5) if op==3 else (0,1,2)
            if f not in allowed: cause=2; break
            n={0:1,1:2,2:4,4:1,5:2}[f]
            address=(a+(ii if op==3 else si))&MASK
            if address%n: cause=4 if op==3 else 6; break
            if address+n>len(ram):
                if op==0x23 and n==4 and 0x10000<=address<0x10010:
                    mailbox[address]=b
                else: cause=5 if op==3 else 7; break
            elif op==3:
                raw=int.from_bytes(ram[address:address+n],'little')
                value=sext(raw,n*8) if f in (0,1) else raw
            else: ram[address:address+n]=(b&((1<<(8*n))-1)).to_bytes(n,'little')
        elif op==0x0f and f==0: pass
        elif op==0x73:
            cause=3 if ins==0x00100073 else 11 if ins==0x73 else 2; break
        else: cause=2; break
        if npc&3: cause=0; break
        actual_rd=rd if value is not None else 0
        if actual_rd: x[actual_rd]=value&MASK
        trace.append(f'{pc:08x} {ins:08x} {actual_rd:02x} {x[actual_rd]:08x}')
        counts[f'{op:02x}']=counts.get(f'{op:02x}',0)+1
        x[0]=0; pc=npc
    else: raise TimeoutError('reference did not halt')
    out.write_text('\n'.join(trace)+'\n',encoding='ascii')
    report=dict(retired=len(trace),trap_cause=cause,trap_pc=pc,
                opcode_counts=counts,mailbox=mailbox)
    out.with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
