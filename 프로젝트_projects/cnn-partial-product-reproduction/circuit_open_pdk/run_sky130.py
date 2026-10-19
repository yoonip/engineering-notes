"""Official SKY130 TT MOS signed column-mask MAC, with common 32-bit accumulator."""
from pathlib import Path
import sys,re,json,csv,os,time,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'circuit'))
import importlib.util
_spec=importlib.util.spec_from_file_location('_sky130_mac_base',HERE.parent/'circuit/run_circuit.py')
base=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(base)
from arithmetic import column_mask_mul,signed_value

VDD=1.8; PERIOD=100e-9; RISE=200e-12
NAME_PREFIX='sky130';TRACE_FILE=None;MODEL_WRAPPER=None;NGSPICE_PATH=None
base.HERE=HERE;base.VDD=VDD;base.PERIOD=PERIOD;base.RISE=RISE
base.accumulator_width=lambda n,terms:32
original_generate=base.generate


def pwl_bits(name,values,bit):
    points=[(0,0),(2*PERIOD-RISE,0)];previous=0
    for index,value in enumerate(values):
        t=(index+2)*PERIOD;level=((int(value)>>bit)&1)*VDD
        if index==0 or level!=previous:points.extend([(t,previous),(t+RISE,level)])
        previous=level
    points.append(((len(values)+2)*PERIOD,previous))
    return f'V{name} {name} 0 PWL('+' '.join(f'{t:.12g} {v:.12g}' for t,v in points)+')'
base.pwl_bits=pwl_bits


def transistor_replace(match):
    name,d,g,s,b,kind,width=match.groups()
    w={'120':.42,'240':.84,'360':1.26}[width] if kind=='nmos' else 1.26
    device='nfet_01v8' if kind=='nmos' else 'pfet_01v8'
    return f'X{name[1:]} {d} {g} {s} {b} sky130_fd_pr__{device} w={w} l=0.15 nf=1 ad={w*.29:.6g} as={w*.29:.6g} pd={2*(w+.29):.6g} ps={2*(w+.29):.6g}'
base.CELLS=re.sub(r'^(M\S+) (\S+) (\S+) (\S+) (\S+) (nmos|pmos) w=(120|240|360)n l=45n$',transistor_replace,base.CELLS,flags=re.M)


def generate(n,k,count,path,idle=False):
    result=original_generate(n,k,count,path,'mac',idle)
    text=path.read_text()
    text=text.replace('Educational CMOS Level1','Official SKY130 TT 1.8V')
    if MODEL_WRAPPER is None:raise ValueError('Configure an external --model-wrapper')
    text=re.sub(r'^\.include.*$',lambda _:'.include \"'+base.include_reference(MODEL_WRAPPER,path.parent)+'\"',text,flags=re.M)
    text=text.replace('.temp 25','.temp 25\n.option scale=1u')
    text=text.replace('Vdd vdd 0 1\n','Vdd vdd 0 1.8\n')
    text=text.replace('Vclk clk 0 PULSE(0 1 ','Vclk clk 0 PULSE(0 1.8 ')
    text=text.replace('Vmclk mclk 0 PULSE(1 0 ','Vmclk mclk 0 PULSE(1.8 0 ')
    text=re.sub(r'^(Vreset[^\n]*) 1\)$',r'\1 1.8)',text,flags=re.M)
    text=re.sub(r'^(Ven\d+ en\d+ 0) 1$',r'\1 1.8',text,flags=re.M)
    path.write_text(text,encoding='utf8')
    return result


def run_one(n,k,count,idle=False):
    netdir=HERE/'netlists';resdir=HERE/'results';netdir.mkdir(exist_ok=True);resdir.mkdir(exist_ok=True)
    name=f'{NAME_PREFIX}_mac_n{n}_k{k}'+('_idle' if idle else '')
    circuit=netdir/(name+'.cir');vectors,width,gates,transistors=generate(n,k,count,circuit,idle)
    binary=base.resolve_binary(NGSPICE_PATH);logfile=resdir/(name+'.log')
    env=dict(os.environ);env.setdefault('OMP_NUM_THREADS','1')
    start=time.monotonic()
    proc=subprocess.run([str(binary),'-b','-o',str(logfile),str(circuit)],cwd=netdir,env=env,capture_output=True,text=True,timeout=300)
    elapsed=time.monotonic()-start
    if proc.returncode or not (netdir/(name+'.dat')).exists():raise RuntimeError(f'{name}:ngspice failed; see {logfile}')
    data=np.loadtxt(netdir/(name+'.dat'),skiprows=1)
    if 'aborted' in logfile.read_text(errors='replace').lower() or data[-1,0] < (count+2)*PERIOD-RISE:raise RuntimeError(f'{name}:incomplete transient')
    t=data[:,0];records=[];acc=0
    for index,(a,b) in enumerate(vectors):
        rp=int(np.searchsorted(t,(index+2.55)*PERIOD));rq=int(np.searchsorted(t,(index+2.93)*PERIOD))
        pv=data[rp,3:3+2*n];qv=data[rq,3+2*n:3+2*n+32]
        p=signed_value(sum(int(v>VDD/2)<<bit for bit,v in enumerate(pv)),2*n)
        q=signed_value(sum(int(v>VDD/2)<<bit for bit,v in enumerate(qv)),32)
        expected=int(column_mask_mul(a,b,n,k));acc+=expected
        records.append(dict(index=index,a=a,b=b,expected_product=expected,observed_product=p,product_pass=p==expected,expected_accumulator=acc,observed_accumulator=q,accumulator_pass=q==acc))
    t0=2*PERIOD;t1=(count+2)*PERIOD;sel=(t>t0)&(t<t1);tm=np.r_[t0,t[sel],t1];current=data[:,2];im=np.r_[np.interp(t0,t,current),current[sel],np.interp(t1,t,current)]
    energy=float(np.trapezoid(-VDD*im,tm))
    with (resdir/(name+'_checks.csv')).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    r=dict(name=name,n=n,k=k,idle=idle,samples=count,accumulator_bits=32,vdd_V=VDD,temperature_C=25,corner='TT',period_ns=PERIOD*1e9,frequency_MHz=1/PERIOD/1e6,
           average_supply_power_uW=energy/(t1-t0)*1e6,energy_per_operation_fJ=energy/count*1e15,transistors=transistors,
           product_mismatches=sum(not x['product_pass'] for x in records),accumulator_mismatches=sum(not x['accumulator_pass'] for x in records),runtime_seconds=elapsed,
           integration_method='Gear reltol=0.001 maxstep=1ns',netlist=str(circuit.relative_to(HERE)),log=str(logfile.relative_to(HERE)),checks='results/'+name+'_checks.csv')
    r['accepted']=r['product_mismatches']==0 and r['accumulator_mismatches']==0
    r['scenario']='cnn_operand_trace' if TRACE_FILE else 'boundary_vectors'
    if TRACE_FILE:
        import hashlib
        r['trace_csv']=base.include_reference(TRACE_FILE,HERE)
        r['trace_csv_sha256']=hashlib.sha256(TRACE_FILE.read_bytes()).hexdigest()
    print(json.dumps(r),flush=True)
    return r


def main():
    global HERE,NAME_PREFIX,TRACE_FILE,MODEL_WRAPPER,NGSPICE_PATH
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=12);p.add_argument('--jobs',type=int,default=2);p.add_argument('--idle',action='store_true');p.add_argument('--bits',type=int,nargs='+',default=[6,8]);p.add_argument('--masks',type=int,nargs='+');p.add_argument('--cases',nargs='+',help='Exact cases as N:K, e.g. 6:5 8:0');p.add_argument('--vectors-csv',type=Path);p.add_argument('--prefix',default='sky130');p.add_argument('--ngspice');p.add_argument('--model-wrapper',type=Path,default=os.environ.get('SKY130_MODEL_WRAPPER'));p.add_argument('--output-dir',type=Path,default=Path('results/circuit_open_pdk'));p.add_argument('--generate-only',action='store_true')
    args=p.parse_args()
    if args.samples<1 or args.jobs<1:p.error('--samples and --jobs must be positive')
    if not args.model_wrapper:p.error('Supply --model-wrapper or SKY130_MODEL_WRAPPER; vendor models are not bundled')
    MODEL_WRAPPER=Path(args.model_wrapper).expanduser().resolve()
    if not MODEL_WRAPPER.is_file():p.error('External model wrapper was not found')
    NGSPICE_PATH=args.ngspice
    HERE=args.output_dir.expanduser().resolve();base.HERE=HERE
    res=HERE/'results';res.mkdir(parents=True,exist_ok=True);(HERE/'netlists').mkdir(exist_ok=True)
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',args.prefix):raise ValueError('Prefix must be a safe file name')
    NAME_PREFIX=args.prefix
    if args.vectors_csv:
        TRACE_FILE=args.vectors_csv.resolve()
        with TRACE_FILE.open(newline='',encoding='utf-8-sig') as f:pairs=[(int(row['a']),int(row['b'])) for row in csv.DictReader(f)]
        if len(pairs)!=args.samples:raise ValueError('CSV pair count must equal --samples')
        def traced_stimulus(n,count):
            if any(not -(1<<(n-1))<=x<(1<<(n-1)) for pair in pairs for x in pair):raise ValueError('CSV operands outside signed range')
            return pairs[:count]
        base.stimulus=traced_stimulus
    file=res/'summary.json'
    summary={'model':'Official foundry-provided SKY130 TT nfet_01v8/pfet_01v8 BSIM4; unchanged coefficients, selected geometry bins','process_nm':130,'45nm_or_GPDK45_equivalence':False,'scope':'Schematic CMOS estimation; no layout parasitic extraction, custom cells, ideal external input/clock/EN drivers excluded','runs':[],'status':'running'}
    if file.exists():summary['runs']=json.loads(file.read_text()).get('runs',[])
    tasks=[tuple(map(int,x.split(':'))) for x in args.cases] if args.cases else [(n,k) for n in args.bits for k in (args.masks if args.masks is not None else [0,n-1])]
    if any(n not in (6,8) or not 0 <= k < n for n,k in tasks):raise ValueError('Supported: N=6 or 8 and 0 <= K < N')
    if args.generate_only:
        rows=[]
        for n,k in tasks:
            path=HERE/'netlists'/f'{NAME_PREFIX}_mac_n{n}_k{k}.cir'
            pairs,width,gates,count=generate(n,k,args.samples,path,args.idle)
            rows.append({'n':n,'k':k,'samples':len(pairs),'accumulator_bits':width,'transistors':count,'netlist':str(path.relative_to(HERE)).replace('\\','/'),'status':'generated_not_simulated'})
        (res/'generation.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows));return
    import hashlib
    summary['model_wrapper_sha256']=hashlib.sha256(MODEL_WRAPPER.read_bytes()).hexdigest()
    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for future in as_completed([pool.submit(run_one,n,k,args.samples,args.idle) for n,k in tasks]):
                r=future.result();summary['runs']=[x for x in summary['runs'] if x['name']!=r['name']]+[r]
                file.write_text(json.dumps(summary,indent=2),encoding='utf8')
                if not r['accepted']:raise RuntimeError('Functional mismatch, energy rejected')
        summary['status']='complete'
    except Exception as exc:
        summary['status']='failed';summary['failure']=str(exc);file.write_text(json.dumps(summary,indent=2),encoding='utf8');raise
    file.write_text(json.dumps(summary,indent=2),encoding='utf8')
    with (res/'power_metrics.csv').open('w',newline='',encoding='utf8') as f:
        keys=['name','n','k','idle','scenario','samples','accumulator_bits','vdd_V','frequency_MHz','average_supply_power_uW','energy_per_operation_fJ','product_mismatches','accumulator_mismatches','runtime_seconds']
        w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(summary['runs'])
if __name__=='__main__':main()
