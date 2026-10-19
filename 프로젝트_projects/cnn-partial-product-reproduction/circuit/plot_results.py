"""Plot measured, functionally accepted ngspice energy and sampled MAC outputs."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=Path('results/circuit'));args=parser.parse_args()
HERE=args.output_dir.expanduser().resolve()
results=HERE/'results'
summary=json.loads((results/'summary.json').read_text(encoding='utf8'))
if (results/'exhaustive_arithmetic.json').exists():summary['exhaustive']=json.loads((results/'exhaustive_arithmetic.json').read_text(encoding='utf8'))
active=[r for r in summary['runs'] if not r['idle'] and r.get('accepted_for_power_comparison',False)]
idle={(r['n'],r['k']):r for r in summary['runs'] if r['idle'] and r.get('accepted_for_power_comparison',False)}
fig,axes=plt.subplots(1,2,figsize=(11,4.5))
for n,color in [(6,'#207db1'),(8,'#ce6537')]:
    rows=sorted([r for r in active if r['n']==n],key=lambda r:r['k'])
    axes[0].plot([r['k'] for r in rows],[r['energy_per_operation_fJ'] for r in rows],'o-',color=color,label=f'INT{n}: registered MAC')
    if not rows:continue
    baseline=rows[0]['energy_per_operation_fJ']
    axes[1].plot([r['k'] for r in rows],[100*(1-r['energy_per_operation_fJ']/baseline) for r in rows],'o-',color=color,label=f'INT{n}')
for ax in axes:
    ax.set_xlabel('Dropped partial-product columns k');ax.grid(alpha=.25);ax.legend()
axes[0].set_ylabel('Total supply energy per operation (fJ)')
axes[1].set_ylabel('Reduction versus same-width full multiplier (%)')
fig.suptitle('ngspice transistor MAC: educational Level1, 1 V, 10 MHz, configured fixed operands\nIllustrative energy only; no foundry or 45 nm calibration',fontsize=11)
fig.tight_layout();fig.savefig(results/'energy_vs_mask.png',dpi=180);plt.close(fig)

for n in (6,8):
    k=n-1;csvpath=results/f'mac_n{n}_k{k}_checks.csv'
    if not csvpath.exists():continue
    rows=list(csv.DictReader(csvpath.open(encoding='utf8')))
    fig,ax=plt.subplots(figsize=(10,4))
    x=np.arange(len(rows))
    ax.plot(x,[int(r['expected_accumulator']) for r in rows],'-',lw=2,label='Exact column-mask software accumulator')
    ax.plot(x,[int(r['observed_accumulator']) for r in rows],'o',ms=5,fillstyle='none',label='Decoded MOS register output')
    ax.set(xlabel='Operand index',ylabel='Signed accumulator',title=f'INT{n}, k={k}: transistor feedback MAC / software comparison')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(results/f'mac_n{n}_k{k}_equivalence.png',dpi=180);plt.close(fig)

raw=HERE/'netlists/mac_n6_k0.dat'
if raw.exists():
    data=np.loadtxt(raw,skiprows=1)
    window=(data[:,0]>4.5e-7)&(data[:,0]<7.5e-7)
    data=data[window]
    fig,axes=plt.subplots(2,1,figsize=(10,5.5),sharex=True)
    for col,label in [(1,'slave clock'),(15,'accumulator q0'),(35,'accumulator sign q20')]:
        axes[0].plot(data[:,0]*1e9,data[:,col],label=label)
    axes[0].set_ylabel('Voltage (V)');axes[0].legend(loc='upper right');axes[0].grid(alpha=.2)
    axes[1].plot(data[:,0]*1e9,-data[:,2]*1e6,color='#207db1')
    axes[1].set(xlabel='Transient time (ns)',ylabel='Supply current (uA)')
    axes[1].grid(alpha=.2)
    fig.suptitle('Actual ngspice CMOS register/current waveform: INT6 full multiplier\nEducational Level1, -1 accumulator +1 product wraps correctly to zero')
    fig.tight_layout();fig.savefig(results/'registered_mac_waveform.png',dpi=180);plt.close(fig)

for r in active:
    match=idle.get((r['n'],r['k']))
    if match:
        r['matched_idle_supply_power_uW']=match['average_supply_power_uW']
        r['nonidle_incremental_power_uW']=r['average_supply_power_uW']-match['average_supply_power_uW']
        r['nonidle_incremental_energy_fJ']=r['energy_per_operation_fJ']-match['energy_per_operation_fJ']
summary['runs']=[next((a for a in active if a['name']==r['name']),r) for r in summary['runs']]
summary['power_reduction_by_width']={}
for n in (6,8):
    rows=sorted([r for r in active if r['n']==n],key=lambda r:r['k'])
    if rows:
        summary['power_reduction_by_width'][str(n)]={'baseline_uW':rows[0]['average_supply_power_uW'],'max_mask_uW':rows[-1]['average_supply_power_uW'],'reduction_percent':100*(1-rows[-1]['energy_per_operation_fJ']/rows[0]['energy_per_operation_fJ'])}
(results/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
with (results/'power_metrics.csv').open('w',newline='',encoding='utf8') as f:
    keys=['name','n','k','mode','idle','samples','frequency_MHz','average_supply_power_uW','energy_per_operation_fJ','nonidle_incremental_power_uW','transistors','product_mismatches','accumulator_mismatches','runtime_seconds']
    writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(summary['runs'])
print(json.dumps(summary['power_reduction_by_width'],indent=2))
