"""분야별 모델을 선택해 재현 가능한 수치 결과를 출력한다."""
import argparse
import json
import math
import models as m


def demos():
    v,cur=m.mna([1,2],[(1,2,1000),(2,0,2000)],[(1,0,3)])
    ut=m.thermal_voltage()
    wc,pm=m.two_pole_margin()
    war=math.sqrt((1/1e-6+1/1e-7)/(1e-9+1e-9))
    states,transitions=m.explore_queue()
    timing=dict(period=10,cq_max=1,d_max=12,setup=1,cq_min=.3,d_min=.5,hold=.2,skew=.1)
    z=m.line_input_impedance(math.sqrt(5000),100,math.pi/2)
    lsb,dnl,inl=m.adc_linearity([1,2,3,4.25,5,6,7])
    credits=m.credit_simulate(600,capacity=6)
    j,c,out=m.thermal_two_node(2,.001)
    fit=m.fit_line([0,1,2,3,4],[1,3.1,4.9,7.2,8.8])
    x,u=m.inverse_calibrate(5,fit,.1)
    signatures=[m.signature([(value>>bit)&1 for bit in reversed(range(8))]) for value in range(256)]
    levels=[-2,-1,0,1,2]
    fits=[m.fit_line(levels,[g*x+o for x in levels]) for g,o in ((.8,.1),(1.2,-.2))]
    ideal,measured,corrected=m.pim_affine_calibration([[1,-2],[.5,3]],[.2,-.4],[.8,1.2],[.1,-.2],fits)
    return {
        'mna':{'node_voltage_V':v,'source_current_A':cur},
        'subthreshold':{'thermal_voltage_V':ut,'gm_over_id_per_V':1/(1.5*ut),'slope_V_per_decade':1.5*ut*math.log(10)},
        'feedback':{'crossover_Hz':wc/(2*math.pi),'phase_margin_degree':pm},
        'pdn':{'lossless_antiresonance_Hz':war/(2*math.pi),'lossy_magnitude_ohm':abs(m.pdn_impedance(war,[(.01,1e-9,1e-6),(.01,1e-9,1e-7)]))},
        'fixedpoint':{'raw_tie_cases':[m.qmul16(a,128) for a in (1,3,-1,-3)],'saturated_raw':m.qmul16(32767,32767)},
        'modelcheck':{'reachable_states':len(states),'state_input_transitions':transitions},
        'multicycle':{'one_cycle_slacks_ns':m.multicycle_slacks(setup_cycles=1,hold_adjust=0,**timing),'paired_three_cycle_slacks_ns':m.multicycle_slacks(setup_cycles=3,hold_adjust=2,**timing)},
        'vipt':{'safe_64_sets':m.vipt_safe(4096,64,64),'safe_128_sets':m.vipt_safe(4096,64,128),'unsafe_alias_indices':[m.cache_index(a,64,128) for a in (0,4096)]},
        'rf':{'quarter_wave_input_ohm':[z.real,z.imag]},
        'qpsk':{'theoretical_BER_SER_at_0dB':m.qpsk_theory(0),'simulated_BER_SER_at_0dB':m.qpsk_simulate(0)},
        'buck':{'state_A_V_at_0_5ms':m.buck_load_step(.0005,1e-6),'analytic_voltage_V':m.buck_underdamped_voltage(.0005)},
        'adc':{'fitted_LSB_V':lsb,'DNL_LSB':dnl,'transition_INL_LSB':inl},
        'sram':{'low_node_V_at_1ns':m.sram_read_node(1e-9),'assumed_trip_gap_V':.45-m.sram_read_node(1e-9)},
        'credits':{'sent_in_600_cycles':len(credits['sent']),'consumed':len(credits['consumed']),'remaining_credit_account':credits['credits']+credits['data_inflight']+credits['queued']+credits['returns_inflight']},
        'equivalence':{'exhaustive_python_cases':sum(m.counter_behavioral(q,e,r)==m.counter_structural(q,e,r) for q in range(256) for e in (0,1) for r in (0,1))},
        'thermal':{'die_rise_K':j,'case_rise_K':c,'rejected_heat_J':out,'energy_balance_residual_J':.1*j+c+out-4},
        'calibration':{'slope':fit.slope,'intercept':fit.intercept,'estimated_input':x,'input_standard_uncertainty':u},
        'signature':{'nonzero_error_aliases':signatures[1:].count(0),'nonzero_errors':255,'preimages_per_signature':[signatures.count(k) for k in range(8)]},
        'pim':{'normalized_ideal':ideal,'normalized_measured':measured,'normalized_corrected':corrected}
    }


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',default='all',choices=['all','mna','subthreshold','feedback','pdn','fixedpoint','modelcheck','multicycle','vipt','rf','qpsk','buck','adc','sram','credits','equivalence','thermal','calibration','signature','pim'])
    selected=parser.parse_args().case
    results=demos()
    print(json.dumps(results if selected=='all' else {selected:results[selected]},ensure_ascii=False,indent=2))
