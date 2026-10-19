"""Plot only newly generated, functionally accepted SKY130 run summaries."""
from pathlib import Path
import argparse,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=Path('results/circuit_open_pdk'))
    args=parser.parse_args();results=args.output_dir.expanduser().resolve()/'results'
    summary=json.loads((results/'summary.json').read_text(encoding='utf8'))
    accepted=[r for r in summary['runs'] if r.get('accepted') and not r.get('idle')]
    if not accepted:raise ValueError('No functionally accepted active runs to plot')
    fig,ax=plt.subplots(figsize=(8,4.6))
    scenarios=sorted({r.get('scenario','boundary_vectors') for r in accepted})
    for scenario in scenarios:
        for n in (6,8):
            rows=sorted([r for r in accepted if r['n']==n and r.get('scenario','boundary_vectors')==scenario],key=lambda r:r['k'])
            if rows:ax.plot([r['k'] for r in rows],[r['energy_per_operation_fJ']/1000 for r in rows],'o-',label=f'INT{n}: {scenario}')
    ax.set(xlabel='Dropped partial-product columns k',ylabel='Total supply energy (pJ / operation)',title='SKY130 schematic MAC: compare only the same model and operand trace')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(results/'energy_vs_mask.png',dpi=180);plt.close(fig)
if __name__=='__main__':main()
