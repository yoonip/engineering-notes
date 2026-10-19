"""Generate and run actual transistor-level signed column-mask MACs in ngspice.

Default: author-created educational Level1 model, NOT a calibrated 45nm process.
External simulator required; no vendor models or simulator binaries are bundled.
All mask settings keep the same transistor topology and stimulus per bitwidth.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, shutil, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
from pathlib import Path
import numpy as np
from arithmetic import column_mask_mul, signed_value, baugh_wooley_mul, accumulator_width

HERE = Path(__file__).resolve().parent
EDUCATIONAL_MODEL = HERE / "models/educational_level1.pm"
VDD = 1.0
PERIOD = 100e-9
RISE = 100e-12

CELLS = '''
.subckt inv a y vdd vss
Mp y a vdd vdd pmos w=240n l=45n
Mn y a vss vss nmos w=120n l=45n
.ends
.subckt nand2 a b y vdd vss
Mp1 y a vdd vdd pmos w=240n l=45n
Mp2 y b vdd vdd pmos w=240n l=45n
Mn1 y a nn vss nmos w=240n l=45n
Mn2 nn b vss vss nmos w=240n l=45n
.ends
.subckt nand3 a b c y vdd vss
Mp1 y a vdd vdd pmos w=240n l=45n
Mp2 y b vdd vdd pmos w=240n l=45n
Mp3 y c vdd vdd pmos w=240n l=45n
Mn1 y a nn1 vss nmos w=360n l=45n
Mn2 nn1 b nn2 vss nmos w=360n l=45n
Mn3 nn2 c vss vss nmos w=360n l=45n
.ends
.subckt and2 a b y vdd vss
Xn a b nb vdd vss nand2
Xi nb y vdd vss inv
.ends
.subckt and3 a b c y vdd vss
Xn a b c nb vdd vss nand3
Xi nb y vdd vss inv
.ends
.subckt xor2 a b y vdd vss
X1 a b t1 vdd vss nand2
X2 a t1 t2 vdd vss nand2
X3 b t1 t3 vdd vss nand2
X4 t2 t3 y vdd vss nand2
.ends
.subckt ha a b s co vdd vss
Xs a b s vdd vss xor2
Xc a b co vdd vss and2
.ends
.subckt fa a b ci s co vdd vss
X1 a b ab vdd vss xor2
X2 ab ci s vdd vss xor2
X3 a b nb1 vdd vss nand2
X4 ab ci nb2 vdd vss nand2
X5 nb1 nb2 co vdd vss nand2
.ends
.subckt tg a y en enb vdd vss
Mn y en a vss nmos w=120n l=45n
Mp y enb a vdd pmos w=240n l=45n
.ends
.subckt dff d mclk mclkb clk clkb q vdd vss
Xmi d m mclk mclkb vdd vss tg
Xmf mq m mclkb mclk vdd vss tg
Xm1 m mb vdd vss inv
Xm2 mb mq vdd vss inv
Xsi mq sl clk clkb vdd vss tg
Xsf q sl clkb clk vdd vss tg
Xs1 sl sb vdd vss inv
Xs2 sb q vdd vss inv
Cm m vss 5f
Cs sl vss 5f
.ends
'''


def stimulus(n, count=24):
    lim = 1 << (n-1)
    # Boundary and mixed-sign tests followed by fixed deterministic switching.
    vectors = [(0,0),(1,1),(-1,1),(1,-1),(-1,-1),(-lim,-lim),
               (lim-1,lim-1),(-lim,lim-1),(lim-1,-lim),(3,3),(-3,5),(5,-3)]
    rng = np.random.default_rng(20261004+n)
    while len(vectors) < count:
        vectors.append(tuple(int(v) for v in rng.integers(-lim,lim,size=2)))
    return vectors[:count]


def pwl_bits(name, values, bit):
    points = [(0,0), (2*PERIOD-RISE,0)]
    previous = 0
    for index,value in enumerate(values):
        t = (index+2)*PERIOD
        level = (int(value)>>bit)&1
        if index == 0 or level != previous:
            points.extend([(t,previous),(t+RISE,level)])
        previous = level
    points.append(((len(values)+2)*PERIOD,previous))
    return f'V{name} {name} 0 PWL('+' '.join(f'{t:.12g} {v}' for t,v in points)+')'


def include_reference(path, directory):
    """Relative SPICE include where possible, absolute only across Windows drives."""
    try:value=os.path.relpath(Path(path).resolve(),Path(directory).resolve())
    except ValueError:value=str(Path(path).resolve())
    if any(c in value for c in ('"','\n','\r')):raise ValueError('Unsupported SPICE include path characters')
    return value.replace('\\','/')


def generate(n, k, count, dest, mode='mac', idle=False):
    if n not in (6,8) or not 0<=k<n or count<1:raise ValueError('Require INT6/INT8, 0<=k<n, and positive sample count')
    vectors = stimulus(n,count)
    if idle:
        vectors = [(0,0)]*count
    width = accumulator_width(n,784)
    lines = [f'Educational CMOS Level1 signed {n}x{n}, mask {k}, mode {mode}, idle {idle}',
             f'.include "{include_reference(EDUCATIONAL_MODEL, dest.parent)}"', CELLS,
             '.temp 25', '.options reltol=0.001 abstol=1p vntol=1u method=gear trtol=3 cshunt=0.05f itl4=100',
             'Vdd vdd 0 1', 'Xclock clk clkb vdd 0 inv', 'Xmclock mclk mclkb vdd 0 inv',
             f'Vclk clk 0 PULSE(0 1 {0.65*PERIOD:.12g} {RISE:.12g} {RISE:.12g} {0.2*PERIOD:.12g} {PERIOD:.12g})',
             f'Vmclk mclk 0 PULSE(1 0 {0.60*PERIOD:.12g} {RISE:.12g} {RISE:.12g} {0.30*PERIOD:.12g} {PERIOD:.12g})',
             f'Vreset resetn 0 PWL(0 0 {2*PERIOD-2*RISE:.12g} 0 {2*PERIOD-RISE:.12g} 1)',]
    for bit in range(n):
        lines.append(pwl_bits(f'a{bit}',[a for a,b in vectors],bit))
        lines.append(pwl_bits(f'b{bit}',[b for a,b in vectors],bit))
    for c in range(n-1):
        lines.append(f'Ven{c} en{c} 0 {int(c >= k)}')
    # 앞의 비트를 계속 꺼내므로 deque를 써서 남은 원소 이동을 피한다.
    columns = [deque() for _ in range(2*n+1)]
    gates = {'and2':0,'and3':0,'nand2':0,'fa':0,'ha':0,'dff':0,'inv':2}
    for i in range(n):
        for j in range(n):
            c = i+j
            node = f'pp{i}_{j}'
            if (i==n-1) != (j==n-1):
                lines.append(f'Xpp{i}_{j} a{i} b{j} {node} vdd 0 nand2')
                gates['nand2'] += 1
            elif c < n-1:
                lines.append(f'Xpp{i}_{j} a{i} b{j} en{c} {node} vdd 0 and3')
                gates['and3'] += 1
            else:
                lines.append(f'Xpp{i}_{j} a{i} b{j} {node} vdd 0 and2')
                gates['and2'] += 1
            columns[c].append(node)
    columns[n].append('vdd')
    columns[2*n-1].append('vdd')
    # Wallace-style column reduction. Carry is sent only to the next column.
    counter = 0
    product_nodes=[]
    for c in range(2*n):
        while len(columns[c]) > 1:
            counter += 1
            s,carry = f'cs{counter}',f'cc{counter}'
            if len(columns[c]) >= 3:
                a,b,ci = [columns[c].popleft() for _ in range(3)]
                lines.append(f'Xreduce{counter} {a} {b} {ci} {s} {carry} vdd 0 fa')
                gates['fa'] += 1
            else:
                a,b = [columns[c].popleft() for _ in range(2)]
                lines.append(f'Xreduce{counter} {a} {b} {s} {carry} vdd 0 ha')
                gates['ha'] += 1
            columns[c].append(s)
            columns[c+1].append(carry)
        src = columns[c][0] if columns[c] else '0'
        lines.extend([f'Xpbuf1_{c} {src} pbar{c} vdd 0 inv',f'Xpbuf2_{c} pbar{c} p{c} vdd 0 inv',f'Cp{c} p{c} 0 1f'])
        gates['inv'] += 2
        product_nodes.append(f'p{c}')
    if mode == 'mac':
        carry = '0'
        for bit in range(width):
            p = f'p{bit}' if bit<2*n else f'p{2*n-1}'
            nxtcarry = f'addc{bit}'
            lines.extend([f'Xaccadd{bit} q{bit} {p} {carry} sum{bit} {nxtcarry} vdd 0 fa',
                          f'Xreset{bit} sum{bit} resetn d{bit} vdd 0 and2',
                          f'Xreg{bit} d{bit} mclk mclkb clk clkb q{bit} vdd 0 dff',f'Cq{bit} q{bit} 0 1f'])
            gates['fa'] += 1; gates['and2'] += 1; gates['dff'] += 1
            carry = nxtcarry
    save = ['v(clk)','i(vdd)']+[f'v(p{bit})' for bit in range(2*n)]
    if mode == 'mac':
        save += [f'v(q{bit})' for bit in range(width)]
    end = (count+2)*PERIOD
    lines += ['.control','set noaskquit','set wr_singlescale','set wr_vecnames',
              'save '+' '.join(save),f'tran {PERIOD/100:.12g} {end:.12g} 0 {PERIOD/100:.12g}',
              'wrdata '+dest.stem+'.dat '+' '.join(save),'quit','.endc','.end']
    dest.write_text('\n'.join(lines)+'\n',encoding='utf8')
    transistors = sum(gates[g]*m for g,m in {'and2':6,'and3':8,'nand2':4,'fa':44,'ha':22,'dff':16,'inv':2}.items())
    return vectors,width,gates,transistors


def resolve_binary(path=None):
    """Resolve a user-installed simulator, without assuming a bundled runtime."""
    selected = path or os.environ.get('NGSPICE_EXECUTABLE')
    if selected:
        candidate = Path(selected).expanduser()
        found = candidate if candidate.is_file() else shutil.which(str(selected))
        if found: return Path(found).resolve()
        raise FileNotFoundError('Configured ngspice executable was not found')
    for name in ('ngspice_con', 'ngspice'):
        found = shutil.which(name)
        if found: return Path(found).resolve()
    raise FileNotFoundError('Install ngspice and use --ngspice, NGSPICE_EXECUTABLE, or PATH')


def run_one(binary,n,k,count,mode,idle=False):
    netdir=HERE/'netlists'; netdir.mkdir(exist_ok=True)
    name=f'{mode}_n{n}_k{k}'+('_idle' if idle else '')
    circuit=netdir/(name+'.cir')
    vectors,width,gates,transistors=generate(n,k,count,circuit,mode,idle)
    logfile=HERE/'results'/f'{name}.log'
    start=time.monotonic()
    env=dict(os.environ); env.setdefault('OMP_NUM_THREADS','1')
    proc=subprocess.run([str(binary),'-b','-o',str(logfile),str(circuit)],cwd=netdir,env=env,capture_output=True,text=True,timeout=900)
    runtime=time.monotonic()-start
    if proc.returncode or not (netdir/f'{name}.dat').exists():
        raise RuntimeError(f'{name} ngspice failure: {proc.stdout} {proc.stderr}; see {logfile}')
    data=np.loadtxt(netdir/f'{name}.dat',skiprows=1)
    if 'aborted' in logfile.read_text(errors='replace').lower() or data[-1,0] < (count+2)*PERIOD-RISE:
        raise RuntimeError(f'{name} incomplete transient; see {logfile}')
    t=data[:,0]; current=data[:,2]
    product_bits=data[:,3:3+2*n]
    records=[]; accumulator=0
    for index,(a,b) in enumerate(vectors):
        # Product checked before clock; register checked after clock and settling.
        tp=(index+2.55)*PERIOD; tq=(index+2.93)*PERIOD
        row=int(np.searchsorted(t,tp)); rq=int(np.searchsorted(t,tq))
        word=sum((int(product_bits[row,bit]>0.5)<<bit) for bit in range(2*n))
        observed=signed_value(word,2*n); expected=int(column_mask_mul(a,b,n,k))
        accumulator+=expected
        record=dict(index=index,a=a,b=b,expected_product=expected,observed_product=observed,product_pass=observed==expected)
        if mode=='mac':
            qb=data[rq,3+2*n:3+2*n+width]
            qword=sum((int(qb[bit]>0.5)<<bit) for bit in range(width))
            q=signed_value(qword,width)
            record.update(expected_accumulator=accumulator,observed_accumulator=q,accumulator_pass=q==accumulator)
        records.append(record)
    # Exclude reset startup. Include every full active period, use boundary interpolation.
    t0=2*PERIOD; t1=(count+2)*PERIOD
    sel=(t>t0)&(t<t1)
    tm=np.r_[t0,t[sel],t1]; im=np.r_[np.interp(t0,t,current),current[sel],np.interp(t1,t,current)]
    energy=float(np.trapezoid(-VDD*im,tm))
    csvpath=HERE/'results'/f'{name}_checks.csv'
    with csvpath.open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0])); writer.writeheader();writer.writerows(records)
    result=dict(name=name,n=n,k=k,mode=mode,idle=idle,vdd_V=VDD,temperature_C=25,period_ns=PERIOD*1e9,
                frequency_MHz=1/PERIOD/1e6,samples=count,measurement_start_ns=t0*1e9,measurement_end_ns=t1*1e9,
                average_supply_power_uW=energy/(t1-t0)*1e6,energy_per_operation_fJ=energy/count*1e15,
                energy_total_J=energy,accumulator_bits=width if mode=='mac' else None,transistors=transistors,gates=gates,
                product_mismatches=sum(not r['product_pass'] for r in records),
                accumulator_mismatches=sum(not r.get('accumulator_pass',True) for r in records),runtime_seconds=runtime,
                integration_method='Gear, reltol=0.001, maxstep=period/100',
                netlist=str(circuit.relative_to(HERE)),log=str(logfile.relative_to(HERE)),checks=str(csvpath.relative_to(HERE)))
    result['accepted_for_power_comparison']=result['product_mismatches']==0 and result['accumulator_mismatches']==0
    print(json.dumps(result),flush=True)
    return result


def exhaustive():
    rows=[]
    for n in (6,8):
        vals=np.arange(-(1<<(n-1)),1<<(n-1),dtype=np.int64)
        a,b=np.meshgrid(vals,vals,indexing='ij')
        for k in range(n):
            expected=column_mask_mul(a,b,n,k)
            actual=np.empty_like(expected)
            for ia,av in enumerate(vals):
                for ib,bv in enumerate(vals):
                    actual[ia,ib]=baugh_wooley_mul(int(av),int(bv),n,k)
            error=expected-a*b
            mismatch=int(np.count_nonzero(expected!=actual))
            rows.append(dict(n=n,k=k,pairs=a.size,hardware_formula_mismatches=mismatch,
                             product_mask_mismatches=int(np.count_nonzero(expected!=((a*b>>k)<<k))),
                             mae=float(np.mean(abs(error))),mean_signed_error=float(np.mean(error)),max_abs_error=int(abs(error).max())))
            assert mismatch==0
    (HERE/'results').mkdir(parents=True,exist_ok=True)
    (HERE/'results/exhaustive_arithmetic.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    return rows


def main():
    global HERE
    parser=argparse.ArgumentParser()
    parser.add_argument('--ngspice');parser.add_argument('--all-masks',action='store_true')
    parser.add_argument('--masks',type=int,nargs='+');parser.add_argument('--jobs',type=int,default=1)
    parser.add_argument('--samples',type=int,default=24);parser.add_argument('--skip-exhaustive',action='store_true')
    parser.add_argument('--bits',type=int,nargs='+',choices=[6,8],default=[6,8])
    parser.add_argument('--mode',choices=['mac','multiplier'],default='mac');parser.add_argument('--idle',action='store_true')
    parser.add_argument('--output-dir',type=Path,default=Path('results/circuit'))
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--generate-only',action='store_true');group.add_argument('--exhaustive-only',action='store_true')
    args=parser.parse_args()
    if args.samples<1 or args.jobs<1:parser.error('--samples and --jobs must be positive')
    HERE=args.output_dir.expanduser().resolve();(HERE/'results').mkdir(parents=True,exist_ok=True);(HERE/'netlists').mkdir(exist_ok=True)
    tasks=[(n,k) for n in args.bits for k in (args.masks if args.masks is not None else (range(n) if args.all_masks else [0,n-1]))]
    if any(not 0<=k<n for n,k in tasks):parser.error('Require 0 <= mask < operand bits')
    if args.exhaustive_only:
        rows=exhaustive();print(json.dumps({'pairs_across_masks':sum(r['pairs'] for r in rows),'mismatches':sum(r['hardware_formula_mismatches'] for r in rows)}));return
    if args.generate_only:
        rows=[]
        for n,k in tasks:
            path=HERE/'netlists'/f'{args.mode}_n{n}_k{k}.cir'
            vectors,width,gates,count=generate(n,k,args.samples,path,args.mode,args.idle)
            rows.append({'n':n,'k':k,'samples':len(vectors),'accumulator_bits':width,'transistors':count,'netlist':str(path.relative_to(HERE)).replace('\\','/'),'status':'generated_not_simulated'})
        (HERE/'results/generation.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows));return
    binary=resolve_binary(args.ngspice)
    report={'model':'Author-created educational Level1; no technology calibration','ngspice_version':subprocess.check_output([str(binary),'-v'],text=True),'model_sha256':hashlib.sha256(EDUCATIONAL_MODEL.read_bytes()).hexdigest(),'runs':[],'status':'running','power_scope':'Total modeled supply includes multiplier, accumulator, register and two clock inverters; excludes ideal external operand/clock/EN drivers and nonoverlap generator. No extracted parasitics.'}
    summary=HERE/'results/summary.json'
    if summary.exists():report['runs']=json.loads(summary.read_text(encoding='utf8')).get('runs',[])
    if not args.skip_exhaustive:report['exhaustive']=exhaustive()
    elif (HERE/'results/exhaustive_arithmetic.json').exists():report['exhaustive']=json.loads((HERE/'results/exhaustive_arithmetic.json').read_text())
    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for future in as_completed([pool.submit(run_one,binary,n,k,args.samples,args.mode,args.idle) for n,k in tasks]):
                result=future.result();report['runs']=[r for r in report['runs'] if r['name']!=result['name']]+[result]
                summary.write_text(json.dumps(report,indent=2),encoding='utf8')
                if not result['accepted_for_power_comparison']:raise RuntimeError('Functional mismatch: reject power comparison')
        report['status']='complete'
    except Exception:
        report['status']='failed';summary.write_text(json.dumps(report,indent=2),encoding='utf8');raise
    summary.write_text(json.dumps(report,indent=2),encoding='utf8')
    with (HERE/'results/power_metrics.csv').open('w',newline='',encoding='utf8') as f:
        keys=['name','n','k','mode','idle','samples','frequency_MHz','average_supply_power_uW','energy_per_operation_fJ','transistors','product_mismatches','accumulator_mismatches','runtime_seconds']
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(report['runs'])

if __name__=='__main__':main()
