"""심화 예제와 같은 입력에서 출판용 수치 도표를 만든다."""

from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from models import coupled_verlet, heat_fem, simulate_pi


DESTINATION=Path(__file__).parent/'figures'


def save(name):
    for ax in plt.gcf().axes:
        if ax.get_xscale()=='log':ax.xaxis.set_major_formatter(FuncFormatter(lambda value,position:f'{value:g}'))
        if ax.get_yscale()=='log':ax.yaxis.set_major_formatter(FuncFormatter(lambda value,position:f'{value:g}'))
    DESTINATION.mkdir(parents=True,exist_ok=True)
    plt.tight_layout(pad=1.4)
    for extension in ('png','svg'):
        kwargs={'metadata':{'Date':None}} if extension=='svg' else {}
        plt.savefig(DESTINATION/f'{name}.{extension}',dpi=200,**kwargs)
        if extension=='svg':
            path=DESTINATION/f'{name}.{extension}'
            clean='\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n'
            path.write_bytes(clean.encode('utf-8'))
    plt.close()


def main():
    plt.rcParams.update({'font.family':['Malgun Gothic','DejaVu Sans'],'font.size':10,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'axes.unicode_minus':False,'svg.fonttype':'path',
                         'svg.hashsalt':'engineering-notes-advanced-v15',
                         'axes.grid':True,'grid.alpha':.18,'grid.linewidth':.6,
                         'legend.frameon':False,'lines.linewidth':1.6})
    sigma=[10**(-4+5*i/300) for i in range(301)];lam=.001
    fig,axes=plt.subplots(1,2,figsize=(8.6,3.8))
    axes[0].loglog(sigma,[1/s for s in sigma],color='#777777',linestyle='--',label='최소제곱 / LS')
    axes[0].loglog(sigma,[s/(s*s+lam) for s in sigma],color='#255778',label='Ridge')
    axes[0].set(xlabel='특잇값 / Singular value',ylabel='계수 이득 / Coefficient gain')
    axes[0].legend(loc='lower left')
    axes[1].semilogx(sigma,[s*s/(s*s+lam) for s in sigma],color='#255778')
    axes[1].set(xlabel='특잇값 / Singular value',ylabel='예측 축소 / Prediction factor',ylim=(-.03,1.03))
    fig.suptitle('정규화가 작은 특잇값에 주는 영향 / Ridge filtering, λ=0.001',fontsize=11)
    save('ridge_filter')

    refs=[3]*200+[0]*400
    a=simulate_pi(refs,kaw=0);b=simulate_pi(refs,kaw=4);times=[r[0] for r in a]
    fig,axes=plt.subplots(2,1,figsize=(8.0,5.4),sharex=True)
    axes[0].plot(times,refs,color='#777777',linestyle=':',label='목표 / Reference')
    axes[0].plot(times,[r[2] for r in a],color='#9b5938',linestyle='--',label='일반 PI / Plain PI')
    axes[0].plot(times,[r[2] for r in b],color='#255778',label='포화 보정 / Anti-windup')
    axes[0].set(ylabel='출력 / Output');axes[0].legend(ncol=3,loc='upper right',fontsize=9)
    axes[1].plot(times,[r[3] for r in a],color='#9b5938',linestyle='--')
    axes[1].plot(times,[r[3] for r in b],color='#255778')
    axes[1].set(xlabel='시간 / Time (s)',ylabel='적분 상태 / Integral state')
    for ax in axes:ax.axvline(10,color='#555555',linewidth=.8,linestyle=':')
    fig.suptitle('출력 한계 이후의 적분 기억 / Integral memory during saturation',fontsize=11)
    save('pi_antiwindup')

    fig,axes=plt.subplots(1,2,figsize=(8.6,3.8))
    exact_x=[i/400 for i in range(401)]
    axes[0].plot(exact_x,[x*(1-x) for x in exact_x],color='#555555',label='해석해 / Exact')
    xs=[i/8 for i in range(9)];ys=heat_fem(xs,[2]*8,[4]*8)
    axes[0].plot(xs,ys,color='#255778',marker='o',markersize=3,linestyle='--',label='선형 FEM / Linear FEM')
    axes[0].set(xlabel='위치 / Position (m)',ylabel='온도차 / Temperature rise (K)');axes[0].legend(fontsize=9)
    sizes=[];errors=[]
    for n in (4,8,16,32,64):
        nodes=[i/n for i in range(n+1)];values=heat_fem(nodes,[2]*n,[4]*n);error=0
        for i in range(n):
            for j in range(50):
                t=(j+.5)/50;x=(i+t)/n;u=(1-t)*values[i]+t*values[i+1]
                error+=(u-x*(1-x))**2/(n*50)
        sizes.append(1/n);errors.append(math.sqrt(error))
    axes[1].loglog(sizes,errors,color='#255778',marker='o',markersize=3)
    axes[1].set(xlabel='요소 길이 / Element length (m)',ylabel='L2 오차 / L2 error (K·m½)')
    fig.suptitle('열전도 해와 요소 내 오차 / Conduction and within-element error',fontsize=11)
    save('fem_heat')

    trajectory=coupled_verlet(1000,.02)
    times=[r[0] for r in trajectory]
    fig,axes=plt.subplots(2,1,figsize=(8,5.2),sharex=True)
    axes[0].plot(times,[r[1][0] for r in trajectory],color='#255778',label='질점 1 / Mass 1')
    axes[0].plot(times,[r[1][1] for r in trajectory],color='#9b5938',linestyle='--',label='질점 2 / Mass 2')
    axes[0].set(ylabel='변위 / Displacement (m)');axes[0].legend(ncol=2)
    energy=[.5*sum(z*z for z in v)+.5*sum(z*z for z in x)+.5*(x[0]-x[1])**2 for t,x,v in trajectory]
    axes[1].plot(times,[(e-energy[0])/energy[0] for e in energy],color='#255778')
    axes[1].set(xlabel='시간 / Time (s)',ylabel='상대 에너지 오차\nRelative energy error')
    fig.suptitle('정상 모드의 합과 에너지 / Coupled modes and energy',fontsize=11)
    save('coupled_modes')


if __name__=='__main__':main()
