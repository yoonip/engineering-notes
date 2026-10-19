"""해석해·정확한 유리수·전수 열거로 심화 구현을 검증한다."""

import cmath
from datetime import date, timedelta
from fractions import Fraction as F
from itertools import product
import math
import random
import unittest

from models import (VersionTimeline, bayes_coin_models, coupled_exact,
                    coupled_verlet, heat_fem, jury_stable,
                    leontief_fixed_point, pi_linear_coefficients, ridge2,
                    sat_dpll, simulate_pi, standardized_rates)


class RidgeTests(unittest.TestCase):
    def test_exact_fraction_reference(self):
        rng=random.Random(1506)
        for _ in range(100):
            rows=[[rng.randrange(-5,6),rng.randrange(-5,6)] for _ in range(6)]
            ys=[rng.randrange(-8,9) for _ in rows]; lam=F(3,10)
            a=sum(F(x*x) for x,y in rows)+lam
            b=sum(F(x*y) for x,y in rows)
            c=sum(F(y*y) for x,y in rows)+lam
            d=sum(F(row[0]*y) for row,y in zip(rows,ys))
            e=sum(F(row[1]*y) for row,y in zip(rows,ys))
            exact=((c*d-b*e)/(a*c-b*b),(a*e-b*d)/(a*c-b*b))
            for actual,expected in zip(ridge2(rows,ys,float(lam)),exact):
                self.assertAlmostEqual(actual,float(expected),places=10)

    def test_diagonal_spectral_filter(self):
        rows=[[1,0],[0,0.001]];y=[1,0.002];lam=0.001
        actual=ridge2(rows,y,lam)
        self.assertAlmostEqual(actual[0],1/(1+lam))
        self.assertAlmostEqual(actual[1],0.001*0.002/(0.001**2+lam))
        self.assertLess(abs(actual[1]),0.01)

    def test_gradient_and_positive_curvature(self):
        a=[[1,2],[2,1],[3,-1]];y=[4,3,-1];lam=0.7
        theta=ridge2(a,y,lam)
        def loss(v):return sum((sum(x*z for x,z in zip(row,v))-yy)**2 for row,yy in zip(a,y))+lam*sum(x*x for x in v)
        for i in range(2):
            p=list(theta);m=list(theta);p[i]+=1e-5;m[i]-=1e-5
            self.assertAlmostEqual((loss(p)-loss(m))/2e-5,0,places=7)
            self.assertGreater(loss(p)+loss(m)-2*loss(theta),0)

    def test_invalid(self):
        for args in (([],[],1),([[1,2]],[3],0),([[1,2]],[math.inf],1),([[1]],[3],1)):
            with self.assertRaises(ValueError):ridge2(*args)


class ControlTests(unittest.TestCase):
    def test_jury_against_independent_roots(self):
        for kp,ki in product((0,0.5,3,20),(.1,2,100)):
            t,d=pi_linear_coefficients(1,.1,kp,ki)
            roots=((t+cmath.sqrt(t*t-4*d))/2,(t-cmath.sqrt(t*t-4*d))/2)
            self.assertEqual(jury_stable(t,d),max(abs(x) for x in roots)<1)
        self.assertFalse(jury_stable(2,1))

    def test_zoh_plant_constant_input(self):
        refs=[100]*80
        result=simulate_pi(refs,.05,kp=10,ki=0,limit=1)
        for time,ref,x,integ,requested,u in result:
            self.assertEqual(u,1)
            self.assertAlmostEqual(x,1-math.exp(-time),places=12)

    def test_antiwindup_recovers_from_saturation(self):
        refs=[3]*200+[0]*400
        plain=simulate_pi(refs,kaw=0)
        corrected=simulate_pi(refs,kaw=4)
        self.assertLess(abs(corrected[200][3]),abs(plain[200][3]))
        self.assertLess(sum(abs(r[2]) for r in corrected[200:260]),sum(abs(r[2]) for r in plain[200:260]))
        self.assertTrue(all(abs(row[-1])<=1 for row in corrected))

    def test_unsaturated_zero_error_and_validation(self):
        self.assertTrue(all(row[2]==row[3]==0 for row in simulate_pi([0]*20)))
        with self.assertRaises(ValueError):simulate_pi([0],sample_time=0)
        with self.assertRaises(ValueError):simulate_pi([0],kaw=-1)


class FemTests(unittest.TestCase):
    def test_linear_constant_flux_nonuniform_material(self):
        nodes=[0,.2,.5,.9,1];ks=[1,2,4,3]
        resistances=[(b-a)/k for a,b,k in zip(nodes,nodes[1:],ks)]
        total=sum(resistances)
        expected=[0]+[10*sum(resistances[:i])/total for i in range(1,len(nodes))]
        got=heat_fem(nodes,ks,[0]*4,0,10)
        for a,b in zip(got,expected):self.assertAlmostEqual(a,b,places=11)
        fluxes=[-k*(b-a)/h for a,b,k,h in zip(got,got[1:],ks,[nodes[i+1]-nodes[i] for i in range(4)])]
        self.assertLess(max(fluxes)-min(fluxes),1e-10)

    def test_manufactured_quadratic_and_source_balance(self):
        for n in (4,8,16,32):
            nodes=[i/n for i in range(n+1)]
            values=heat_fem(nodes,[2]*n,[4]*n)
            for x,y in zip(nodes,values):self.assertAlmostEqual(y,x*(1-x),places=11)
            outward=-2*(values[0]-values[1])/(1/n)-2*(values[-1]-values[-2])/(1/n)
            self.assertAlmostEqual(outward+4/n,4,places=10)

    def test_l2_interpolation_convergence(self):
        errors=[]
        for n in (8,16,32):
            xs=[i/n for i in range(n+1)];ys=heat_fem(xs,[1]*n,[2]*n)
            error=0.0
            for i in range(n):
                for j in range(50):
                    t=(j+.5)/50;x=(i+t)/n;u=(1-t)*ys[i]+t*ys[i+1]
                    error+=(u-x*(1-x))**2/(n*50)
            errors.append(math.sqrt(error))
        self.assertAlmostEqual(errors[0]/errors[1],4,places=7)
        self.assertAlmostEqual(errors[1]/errors[2],4,places=7)

    def test_boundary_only_and_invalid(self):
        self.assertEqual(heat_fem([0,1],[2],[0],3,7),[3.,7.])
        with self.assertRaises(ValueError):heat_fem([0,0],[1],[0])
        with self.assertRaises(ValueError):heat_fem([0,1],[-1],[0])


class OscillatorTests(unittest.TestCase):
    def test_pure_modes(self):
        for sign,w in ((1,1),(-1,math.sqrt(3))):
            x,v=coupled_exact(.7,(1,sign),(0,0))
            self.assertAlmostEqual(x[0],math.cos(w*.7))
            self.assertAlmostEqual(x[1],sign*math.cos(w*.7))

    def test_time_convergence(self):
        exact=coupled_exact(4,(1,.2),(.3,-.2))[0]
        errors=[]
        for dt in (.04,.02,.01):
            last=coupled_verlet(round(4/dt),dt,(1,.2),(.3,-.2))[-1][1]
            errors.append(max(abs(a-b) for a,b in zip(last,exact)))
        self.assertTrue(3.9<errors[0]/errors[1]<4.1)
        self.assertTrue(3.9<errors[1]/errors[2]<4.1)

    def test_bounded_energy_and_initial_state(self):
        series=coupled_verlet(10000,.02)
        energies=[.5*sum(z*z for z in v)+.5*sum(z*z for z in x)+.5*(x[0]-x[1])**2 for t,x,v in series]
        self.assertEqual(series[0],(0.0,(1.0,0.0),(0.0,0.0)))
        self.assertLess(max(abs(e-energies[0]) for e in energies),0.0004)

    def test_unstable_step_rejected(self):
        with self.assertRaises(ValueError):coupled_verlet(2,2/math.sqrt(3))
        with self.assertRaises(ValueError):coupled_verlet(-1,.1)


class LogicTests(unittest.TestCase):
    @staticmethod
    def holds(clauses,model):return all(any(model[abs(lit)]==(lit>0) for lit in c) for c in clauses)

    def test_exhaustive_small_models(self):
        rng=random.Random(1557)
        for n in range(1,7):
            for _ in range(70):
                cs=[[rng.choice((-1,1))*rng.randint(1,n) for j in range(rng.randrange(4))] for i in range(rng.randrange(12))]
                expected=any(self.holds(cs,dict(zip(range(1,n+1),v))) for v in product((False,True),repeat=n))
                result=sat_dpll(cs,n)
                self.assertEqual(result is not None,expected)
                if result is not None:self.assertTrue(self.holds(cs,result))

    def test_entailment_and_counterexample(self):
        self.assertIsNone(sat_dpll([[-1,2],[1],[-2]],2))
        result=sat_dpll([[-1,2],[2],[-1]],2)
        self.assertIsNotNone(result)
        self.assertFalse(result[1])

    def test_tautology_empty_formula_and_reject(self):
        self.assertEqual(sat_dpll([],0),{})
        self.assertIsNotNone(sat_dpll([[1,-1]],1))
        self.assertIsNone(sat_dpll([[]],0))
        with self.assertRaises(ValueError):sat_dpll([[0]],1)
        with self.assertRaises(ValueError):sat_dpll([[2]],1)


class EpistemologyTests(unittest.TestCase):
    def test_exact_integrated_likelihood(self):
        for n in range(16):
            for k in range(n+1):
                bf=F((n+1)*math.comb(n,k),2**n)
                expected=bf/(1+bf)
                got=bayes_coin_models(k,n)
                self.assertAlmostEqual(got['posterior_fair'],float(expected),places=12)

    def test_empty_evidence_and_prior_odds(self):
        self.assertAlmostEqual(bayes_coin_models(0,0,.8)['posterior_fair'],.8)
        self.assertGreater(bayes_coin_models(10,20,.9)['posterior_fair'],bayes_coin_models(10,20,.1)['posterior_fair'])

    def test_log_domain_and_invalid(self):
        result=bayes_coin_models(0,100000)
        self.assertTrue(math.isfinite(result['log_bayes_factor_fair']))
        self.assertEqual(result['posterior_fair'],0.)
        with self.assertRaises(ValueError):bayes_coin_models(3,2)


class EconomicsTests(unittest.TestCase):
    def test_known_output_and_residual_certificate(self):
        got=leontief_fixed_point([[.2,.1],[.3,.2]],[70,50])
        self.assertLessEqual(max(abs(x-100) for x in got['output']),got['error_bound_inf']+1e-12)

    def test_fraction_inverse_reference(self):
        a,b,c,d=F(1,5),F(1,10),F(3,10),F(1,5)
        determinant=(1-a)*(1-d)-b*c
        exact=[((1-d)*70+b*50)/determinant,(c*70+(1-a)*50)/determinant]
        got=leontief_fixed_point([[float(a),float(b)],[float(c),float(d)]],[70,50],1e-9)
        self.assertLessEqual(max(abs(float(x)-y) for x,y in zip(exact,got['output'])),got['error_bound_inf']+1e-12)

    def test_zero_coefficients_and_invalid_bound(self):
        self.assertEqual(leontief_fixed_point([[0]],[3])['output'],[3])
        with self.assertRaises(ValueError):leontief_fixed_point([[1]],[3])
        with self.assertRaises(RuntimeError):leontief_fixed_point([[.99]],[3],max_steps=1)


class SocietyTests(unittest.TestCase):
    def test_reversal_and_common_population(self):
        a={'easy':(9,10),'hard':(20,100)};b={'easy':(80,100),'hard':(1,10)}
        aa,bb=standardized_rates(a,b,{'easy':F(1,2),'hard':F(1,2)})
        self.assertLess(aa['crude'],bb['crude'])
        self.assertEqual(aa['standardized']-bb['standardized'],F(1,10))

    def test_weighted_population_replication(self):
        a={'a':(1,2),'b':(3,4)};b={'a':(1,4),'b':(1,2)}
        rates=standardized_rates(a,b,{'a':F(1,3),'b':F(2,3)})
        self.assertEqual(rates[0]['standardized'],F(2*1+2*3,12))

    def test_missing_zero_and_bad_weights(self):
        with self.assertRaises(ValueError):standardized_rates({'x':(0,0)},{'x':(1,2)},{'x':1})
        with self.assertRaises(ValueError):standardized_rates({'x':(0,1)},{'y':(1,2)},{'x':1})
        with self.assertRaises(ValueError):standardized_rates({'x':(0,1)},{'x':(1,2)},{'x':F(1,2)})


class TimelineTests(unittest.TestCase):
    def test_boundary_and_announcement_distinction(self):
        data=[{'id':'v1','promulgated':'2024-01-01','effective':'2024-02-01'},
              {'id':'v2','promulgated':'2024-11-01','effective':'2025-01-01'}]
        timeline=VersionTimeline(data)
        self.assertIsNone(timeline.at('2024-01-31'))
        self.assertEqual(timeline.at('2024-02-01')['id'],'v1')
        self.assertEqual(timeline.at('2024-12-31')['id'],'v1')
        self.assertEqual(timeline.at('2025-01-01')['id'],'v2')
        timeline.at('2025-01-01')['id']='changed'
        self.assertEqual(timeline.at('2025-01-02')['id'],'v2')

    def test_binary_lookup_matches_linear_oracle(self):
        start=date(2020,1,1)
        records=[{'id':str(i),'promulgated':'2019-01-01','effective':str(start+timedelta(days=7*i))} for i in range(50)]
        timeline=VersionTimeline(records[::-1])
        for delta in range(-1,360):
            instant=str(start+timedelta(days=delta))
            applicable=[r for r in records if r['effective']<=instant]
            self.assertEqual(timeline.at(instant),applicable[-1] if applicable else None)

    def test_duplicate_and_malformed_rejected(self):
        row={'id':'a','promulgated':'2024-01-01','effective':'2024-02-01'}
        with self.assertRaises(ValueError):VersionTimeline([row,row])
        with self.assertRaises(ValueError):VersionTimeline([])

    def test_mixed_iso_forms_sort_by_calendar_date(self):
        rows=[{'id':'feb','promulgated':'2024-01-01','effective':'20240201'},
              {'id':'dec','promulgated':'2024-11-01','effective':'2024-12-01'}]
        timeline=VersionTimeline(rows)
        self.assertEqual(timeline.at('2024-03-01')['id'],'feb')
        self.assertEqual(timeline.at('20241215')['id'],'dec')
        duplicate=dict(rows[0],effective='2024-02-01')
        with self.assertRaises(ValueError):VersionTimeline([rows[0],duplicate])


if __name__=='__main__':unittest.main()
