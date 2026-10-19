"""해석해, 보존법칙, 전수검사와 독립 계산으로 참조모델을 확인한다."""
import math
import random
import unittest
from fractions import Fraction
import models as m


class HardwareModels(unittest.TestCase):
    def test_mna_divider_and_power(self):
        v, current = m.mna([1, 2], [(1, 2, 1000), (2, 0, 2000)], [(1, 0, 3)])
        self.assertAlmostEqual(v[2], 2)
        self.assertAlmostEqual((v[1]-v[2])/1000, v[2]/2000)
        self.assertAlmostEqual((v[1]-v[2])**2/1000 + v[2]**2/2000 + 3*current[0], 0)

    def test_mna_floating_source(self):
        v, _ = m.mna([1, 2], [(1, 0, 1000), (2, 0, 1000)], [(1, 2, 2)])
        self.assertAlmostEqual(v[1], 1)
        self.assertAlmostEqual(v[2], -1)

    def test_mna_current_and_singular(self):
        v, _ = m.mna([1], [(1, 0, 1000)], current_sources=[(0, 1, .001)])
        self.assertAlmostEqual(v[1], 1)
        with self.assertRaises(ValueError):
            m.mna([1, 2], [(1, 2, 1000)])

    def test_weak_inversion_gm_derivative(self):
        vg, dv = .3, 1e-6
        i = m.weak_inversion(vg, .2)
        gm = (m.weak_inversion(vg+dv, .2)-m.weak_inversion(vg-dv, .2))/(2*dv)
        self.assertAlmostEqual(gm/i, 1/(1.5*m.thermal_voltage()), places=6)

    def test_subthreshold_decade_and_drain_zero(self):
        slope = 1.5*m.thermal_voltage()*math.log(10)
        self.assertAlmostEqual(m.weak_inversion(.3+slope,.2)/m.weak_inversion(.3,.2),10)
        self.assertEqual(m.weak_inversion(.3,0),0)
        self.assertGreater(m.thermal_voltage(400),m.thermal_voltage(300))

    def test_feedback_closed_form(self):
        for w in (0,10,1000,1e7):
            expected=1e5/(1+1e4+1j*w/(2*math.pi*10))
            self.assertAlmostEqual(abs(m.feedback_one_pole(w)-expected),0,places=11)

    def test_feedback_crossover_and_pole_separation(self):
        wc,pm=m.two_pole_margin()
        loop=1e4/((1+1j*wc/(2*math.pi*10))*(1+1j*wc/(2*math.pi*1e5)))
        self.assertAlmostEqual(abs(loop),1)
        self.assertGreater(m.two_pole_margin(pole2=2*math.pi*1e6)[1],pm)

    def test_pdn_antiresonance_and_loss(self):
        c1,c2,l1,l2=1e-6,100e-9,1e-9,1e-9
        w=math.sqrt((1/c1+1/c2)/(l1+l2))
        susceptance=sum(1/(1j*(w*l-1/(w*c))) for l,c in ((l1,c1),(l2,c2)))
        self.assertLess(abs(susceptance),1e-10)
        z=m.pdn_impedance(w,[(.01,l1,c1),(.01,l2,c2)])
        self.assertTrue(math.isfinite(abs(z)))
        self.assertGreater(z.real,0)

    def test_pdn_branch_kcl(self):
        w=2*math.pi*1e6
        branches=[(.02,1e-9,1e-6),(.05,2e-9,1e-7)]
        z=m.pdn_impedance(w,branches)
        total=sum(z/complex(r,w*l-1/(w*c)) for r,l,c in branches)
        self.assertAlmostEqual(abs(total-1),0,places=12)

    def test_qmul_fraction_oracle(self):
        rng=random.Random(22)
        for _ in range(10000):
            a,b=rng.randint(-32768,32767),rng.randint(-32768,32767)
            expected=max(-32768,min(32767,round(Fraction(a*b,256))))
            self.assertEqual(m.qmul16(a,b),expected)

    def test_qmul_ties_and_saturation(self):
        for a,b,want in [(1,128,0),(3,128,2),(-1,128,0),(-3,128,-2),
                         (32767,32767,32767),(-32768,32767,-32768),(-32768,-32768,32767)]:
            self.assertEqual(m.qmul16(a,b),want)

    def test_queue_complete_state_space(self):
        states,transitions=m.explore_queue()
        self.assertEqual(len(states),7)
        self.assertEqual(transitions,56)

    def test_queue_mutant_escapes_occupancy(self):
        good=bad=()
        for data in (0,1):
            good,*_=m.queue_transition(good,True,data,False)
            bad,*_=m.queue_transition(bad,True,data,False,mutant=True)
        self.assertEqual(len(good),len(bad))
        self.assertNotEqual(m.queue_transition(good,False,0,True)[3],
                            m.queue_transition(bad,False,0,True)[3])

    def test_multicycle_setup_and_hold(self):
        args=dict(period=10,cq_max=1,d_max=12,setup=1,cq_min=.3,d_min=.5,hold=.2,skew=.1)
        one=m.multicycle_slacks(setup_cycles=1,hold_adjust=0,**args)
        paired=m.multicycle_slacks(setup_cycles=3,hold_adjust=2,**args)
        unpaired=m.multicycle_slacks(setup_cycles=3,hold_adjust=0,**args)
        self.assertAlmostEqual(paired[0]-one[0],20)
        self.assertAlmostEqual(paired[1],one[1])
        self.assertAlmostEqual(unpaired[1],one[1]-20)

    def test_vipt_safe_synonyms(self):
        self.assertTrue(m.vipt_safe(4096,64,64))
        for offset in (0,64,2048,4032):
            self.assertEqual(m.cache_index(offset,64,64),m.cache_index(4096+offset,64,64))

    def test_vipt_unsafe_counterexample(self):
        self.assertFalse(m.vipt_safe(4096,64,128))
        self.assertNotEqual(m.cache_index(0,64,128),m.cache_index(4096,64,128))

    def test_quarter_and_half_wave(self):
        zt=math.sqrt(50*100)
        self.assertAlmostEqual(abs(m.line_input_impedance(zt,100,math.pi/2)-50),0,places=11)
        self.assertAlmostEqual(abs(m.line_input_impedance(zt,100,math.pi)-100),0,places=11)

    def test_line_passivity_and_quarter_involution(self):
        for load in (25+5j,100-20j,50+0j):
            transformed=m.line_input_impedance(70,load,math.pi/2)
            back=m.line_input_impedance(70,transformed,math.pi/2)
            self.assertLess(abs(back-load),1e-10)
            self.assertLessEqual(abs((transformed-50)/(transformed+50)),1+1e-12)

    def test_qpsk_energy_and_symbol_relation(self):
        for length in (1,4,16):
            self.assertAlmostEqual(sum((1/math.sqrt(length))**2 for _ in range(length)),1)
        p,ps=m.qpsk_theory(0)
        self.assertAlmostEqual(p,.07864960352514257)
        self.assertAlmostEqual(ps,1-(1-p)**2)

    def test_qpsk_monte_carlo(self):
        for db in (0,4):
            p,ps=m.qpsk_theory(db)
            empirical,es=m.qpsk_simulate(db,symbols=20000,seed=31)
            # 독립 표본의 표준오차보다 넓은 고정 경계로 난수 검산을 한다.
            self.assertLess(abs(empirical-p),6*math.sqrt(p*(1-p)/40000))
            self.assertLess(abs(es-ps),6*math.sqrt(ps*(1-ps)/20000))

    def test_buck_analytic_rk4(self):
        for time in (0,1e-4,5e-4,2e-3):
            self.assertAlmostEqual(m.buck_load_step(time,1e-6)[1],m.buck_underdamped_voltage(time),places=7)

    def test_buck_initial_slope_and_energy(self):
        h=1e-9
        state=m.buck_load_step(h,h)
        self.assertAlmostEqual((state[1]-6)/h,-5000,delta=1)
        i,v=m.buck_load_step(.0002,1e-6)
        di,dv=i-1,v-6
        rate=1e-4*di*((6-v)/1e-4)+1e-4*dv*((i-v/6)/1e-4)
        self.assertAlmostEqual(rate,-dv*dv/6)

    def test_adc_transition_error_pair(self):
        lsb,dnl,inl=m.adc_linearity([1,2,3,4.25,5,6,7])
        self.assertEqual(lsb,1)
        self.assertEqual(dnl,[0,0,.25,-.25,0,0])
        self.assertEqual(inl,[0,0,0,.25,0,0,0])

    def test_adc_missing_code_and_endpoint_sum(self):
        _,dnl,inl=m.adc_linearity([1,2,3,3,5,6,7])
        self.assertIn(-1,dnl)
        self.assertAlmostEqual(sum(dnl),0)
        self.assertEqual((inl[0],inl[-1]),(0,0))
        with self.assertRaises(ValueError):
            m.adc_linearity([1,2,3,2,5,6,7])

    def test_sram_kcl_and_time_constant(self):
        r1,r2,c=2e4,1e4,1e-15
        equilibrium=1/3
        self.assertAlmostEqual((1-equilibrium)/r1,equilibrium/r2)
        tau=r1*r2/(r1+r2)*c
        self.assertAlmostEqual(m.sram_read_node(tau),equilibrium*(1-math.exp(-1)))

    def test_sram_strength_and_ode(self):
        self.assertLess(m.sram_read_node(1e-9,pull_down_r=5000),m.sram_read_node(1e-9))
        t,h=5e-12,1e-16
        derivative=(m.sram_read_node(t+h)-m.sram_read_node(t-h))/(2*h)
        v=m.sram_read_node(t)
        expected=((1-v)/20000-v/10000)/1e-15
        self.assertTrue(math.isclose(derivative,expected,rel_tol=1e-9))

    def test_credit_conservation_order_stalls(self):
        r=m.credit_simulate(1000,capacity=5,seed=91,stalls=True)
        self.assertEqual(r['consumed'],r['sent'][:len(r['consumed'])])
        self.assertEqual(r['credits']+r['data_inflight']+r['queued']+r['returns_inflight'],5)
        self.assertLessEqual(r['max_queue'],5)

    def test_credit_round_trip_throughput(self):
        fast=m.credit_simulate(600,capacity=6)
        small=m.credit_simulate(600,capacity=3)
        self.assertEqual(len(fast['sent']),600)
        self.assertEqual(len(small['sent']),300)

    def test_counter_all_states_inputs(self):
        for q in range(256):
            for enable in (0,1):
                for reset in (0,1):
                    self.assertEqual(m.counter_behavioral(q,enable,reset),m.counter_structural(q,enable,reset))

    def test_counter_reset_and_wrap(self):
        self.assertEqual(m.counter_structural(255,1,0),0)
        self.assertEqual(m.counter_structural(99,1,1),0)
        self.assertEqual(m.counter_structural(99,0,0),99)

    def test_thermal_energy_balance(self):
        j,c,out=m.thermal_two_node(2,.001)
        self.assertAlmostEqual(.1*j+c+out,4,places=10)
        self.assertGreater(j,c)

    def test_thermal_steady_and_timestep(self):
        j,c,_=m.thermal_two_node(200,.02)
        self.assertAlmostEqual(j,20,places=6)
        self.assertAlmostEqual(c,16,places=6)
        a=m.thermal_two_node(1,.01)
        b=m.thermal_two_node(1,.005)
        self.assertLess(max(abs(x-y) for x,y in zip(a,b)),1e-6)

    def test_calibration_normal_equations(self):
        xs=[0,1,2,3,4]
        ys=[1,3.1,4.9,7.2,8.8]
        fit=m.fit_line(xs,ys)
        residual=[y-fit.slope*x-fit.intercept for x,y in zip(xs,ys)]
        self.assertAlmostEqual(sum(residual),0)
        self.assertAlmostEqual(sum(x*r for x,r in zip(xs,residual)),0)

    def test_calibration_inverse_and_covariance(self):
        fit=m.fit_line([0,1,2,3,4],[1,3.1,4.9,7.2,8.8])
        x,u=m.inverse_calibrate(fit.slope*2+fit.intercept,fit,.1)
        self.assertAlmostEqual(x,2)
        expected=(.1**2+fit.residual_variance/5)/fit.slope**2
        self.assertAlmostEqual(u*u,expected)
        self.assertGreater(m.inverse_calibrate(fit.intercept,fit,.1)[1],u)

    def test_signature_independent_polynomial_division(self):
        for value in range(256):
            bits=[(value>>bit)&1 for bit in reversed(range(8))]
            self.assertEqual(m.signature(bits),m.gf2_remainder(value<<3,0b1011))

    def test_signature_alias_count_linearity(self):
        def sig(value):
            return m.signature([(value>>bit)&1 for bit in reversed(range(8))])
        aliases=sum(sig(error)==0 for error in range(1,256))
        self.assertEqual(aliases,31)
        for a,b in ((1,33),(14,55),(128,255)):
            self.assertEqual(sig(a^b),sig(a)^sig(b))

    def test_signature_full_rank_by_preimages(self):
        counts=[0]*8
        for value in range(256):
            counts[m.signature([(value>>bit)&1 for bit in reversed(range(8))])]+=1
        self.assertEqual(counts,[32]*8)

    def test_pim_heldout_affine_recovery(self):
        gains,offsets=[.8,1.2],[.1,-.2]
        xs=[-2,-1,0,1,2]
        fits=[m.fit_line(xs,[g*x+o for x in xs]) for g,o in zip(gains,offsets)]
        ideal,_,corrected=m.pim_affine_calibration([[1,-2],[.5,3]],[.2,-.4],gains,offsets,fits)
        for a,b in zip(ideal,corrected):
            self.assertAlmostEqual(a,b)

    def test_pim_nonlinearity_not_repaired(self):
        xs=[-1,0,1]
        fit=m.fit_line(xs,[2*x+.4*x**3 for x in xs])
        corrected,_=m.inverse_calibrate(2*.5+.4*.5**3,fit)
        self.assertAlmostEqual(corrected,.4375)
        self.assertNotAlmostEqual(corrected,.5)


if __name__ == '__main__':
    unittest.main()
