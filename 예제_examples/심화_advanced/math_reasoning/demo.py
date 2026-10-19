"""심화 계산을 실행하고 JSON 요약과 CSV 결과를 저장한다."""

import argparse
import csv
from fractions import Fraction
import json
import math
from pathlib import Path

from models import (VersionTimeline, bayes_coin_models, coupled_exact,
                    coupled_verlet, heat_fem, leontief_fixed_point,
                    pi_linear_coefficients, ridge2, sat_dpll,
                    simulate_pi, standardized_rates)


def main():
    parser=argparse.ArgumentParser(description='심화 모델의 계산 결과를 생성한다.')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.output:args.output.mkdir(parents=True,exist_ok=True)
    def write(name,header,rows):
        if args.output:
            with (args.output/name).open('w',encoding='utf-8',newline='') as file:
                writer=csv.writer(file);writer.writerow(header);writer.writerows(rows)
    refs=[3]*200+[0]*400
    pi_plain=simulate_pi(refs,kaw=0);pi_aw=simulate_pi(refs,kaw=4)
    write('pi_control.csv',['time_s','reference','plain_x','antiwindup_x','plain_integral','antiwindup_integral'],
          ((a[0],a[1],a[2],b[2],a[3],b[3]) for a,b in zip(pi_plain,pi_aw)))
    xs=[i/32 for i in range(33)];ys=heat_fem(xs,[2]*32,[4]*32)
    write('fem_heat.csv',['x_m','temperature_model','exact'],((x,y,x*(1-x)) for x,y in zip(xs,ys)))
    trajectory=coupled_verlet(500,.02)
    write('coupled_oscillators.csv',['time_s','x1','x2','exact_x1','exact_x2'],
          ((t,*x,*coupled_exact(t,(1,0),(0,0))[0]) for t,x,v in trajectory))
    a={'easy':(9,10),'hard':(20,100)};b={'easy':(80,100),'hard':(1,10)}
    rates=standardized_rates(a,b,{'easy':Fraction(1,2),'hard':Fraction(1,2)})
    timeline=VersionTimeline([{'id':'v1','promulgated':'2024-01-01','effective':'2024-02-01'},
                              {'id':'v2','promulgated':'2024-11-01','effective':'2025-01-01'}])
    report={'ridge':ridge2([[1,0],[0,.001]],[1,.002],.001),
            'pi_characteristic_trace_determinant':pi_linear_coefficients(1,.05,1,2),
            'pi_release_integrals':{'plain':pi_plain[200][3],'antiwindup':pi_aw[200][3]},
            'fem_max_nodal_error':max(abs(y-x*(1-x)) for x,y in zip(xs,ys)),
            'coupled_final_error':max(abs(x-y) for x,y in zip(trajectory[-1][1],coupled_exact(10,(1,0),(0,0))[0])),
            'modus_ponens_negated_conclusion_sat':sat_dpll([[-1,2],[1],[-2]],2),
            'bayes_models':bayes_coin_models(10,20),
            'leontief':leontief_fixed_point([[.2,.1],[.3,.2]],[70,50]),
            'rates':rates,'version_on_2024_12_01':timeline.at('2024-12-01')}
    text=json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n'
    if args.output:(args.output/'summary.json').write_text(text,encoding='utf-8',newline='\n')
    print(text,end='')


if __name__=='__main__':main()
