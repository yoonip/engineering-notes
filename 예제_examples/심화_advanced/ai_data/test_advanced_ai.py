"""해석적 값·다른 알고리즘·수치 미분으로 심화 예제를 검증한다."""

from dataclasses import asdict
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import random
import sqlite3
import subprocess
import sys
import unittest

import advanced_ai_models as m


class GradientsAndOptimization(unittest.TestCase):
    def test_mlp_all_parameters_finite_difference(self):
        p = [0.07*(i-8) for i in range(17)]
        _, gradient, probability = m.mlp_loss_gradient(p, [0.4, -0.7], 1)
        step = 1e-5
        for j, exact in enumerate(gradient):
            plus, minus = p[:], p[:]
            plus[j] += step
            minus[j] -= step
            numeric = (m.mlp_loss_gradient(plus, [0.4, -0.7], 1)[0]
                       - m.mlp_loss_gradient(minus, [0.4, -0.7], 1)[0])/(2*step)
            self.assertAlmostEqual(exact, numeric, places=9)
        self.assertAlmostEqual(sum(probability), 1)

    def test_mlp_batch_weighting_and_large_logits(self):
        p = [0.0]*17
        p[-2:] = [1000, -1000]
        loss, _, _ = m.mlp_loss_gradient(p, [1, 1], 1)
        self.assertEqual(loss, 2000)
        batch, gradient = m.mlp_batch([0.0]*17, [[1, 2], [3, 4]], [0, 1])
        self.assertAlmostEqual(batch, math.log(2))
        self.assertAlmostEqual(sum(gradient[-2:]), 0)

    def test_adam_first_step_and_second_moments(self):
        optimizer = m.Adam([1.0], rate=0.2, beta1=0.5, beta2=0.5, epsilon=0.1)
        first = optimizer.update([2])[0]
        self.assertAlmostEqual(first, 1-0.2*2/2.1)
        self.assertEqual(optimizer.first, [1])
        self.assertEqual(optimizer.second, [2])
        self.assertEqual(optimizer.update([-1]), [first])
        self.assertEqual(optimizer.first, [0])
        self.assertEqual(optimizer.second, [1.5])

    def test_adam_serialized_resume(self):
        optimizer = m.Adam([0.3, -0.4])
        optimizer.update([2, -1])
        optimizer.update([-0.5, 3])
        resumed = m.Adam(**json.loads(json.dumps(asdict(optimizer))))
        restarted = m.Adam(optimizer.parameters)
        expected = optimizer.update([1.2, 0.7])
        self.assertEqual(resumed.update([1.2, 0.7]), expected)
        self.assertNotEqual(restarted.update([1.2, 0.7]), expected)

    def test_clipping_norm_and_direction(self):
        result, original = m.clip_gradient([3, 4], 2)
        self.assertEqual(original, 5)
        self.assertAlmostEqual(math.hypot(*result), 2)
        self.assertAlmostEqual(result[0]/result[1], 3/4)
        self.assertEqual(m.clip_gradient([0, 0], 2)[0], [0, 0])

    def test_xor_training_real_updates(self):
        rng = random.Random(7)
        p = [rng.uniform(-0.8, 0.8) for _ in range(17)]
        xs, ys = [[-1,-1],[-1,1],[1,-1],[1,1]], [0,1,1,0]
        initial, _ = m.mlp_batch(p, xs, ys)
        optimizer = m.Adam(p, rate=0.03)
        for _ in range(600):
            _, gradient = m.mlp_batch(optimizer.parameters, xs, ys)
            optimizer.update(gradient)
        final, _ = m.mlp_batch(optimizer.parameters, xs, ys)
        self.assertLess(final, initial/20)
        self.assertEqual([max(range(2), key=lambda i:m.mlp_loss_gradient(optimizer.parameters,x,0)[2][i])
                          for x in xs], ys)


class TilingDecodeAndData(unittest.TestCase):
    def test_tiled_traffic_independent_block_enumeration(self):
        for shape in ((3,5,7,2),(16,16,16,16),(17,31,9,8)):
            rows, columns, inner, tile = shape
            reads = 0
            for y in range(0, rows, tile):
                for x in range(0, columns, tile):
                    for k in range(0, inner, tile):
                        a = {(i,p) for i in range(y,min(y+tile,rows)) for p in range(k,min(k+tile,inner))}
                        b = {(p,j) for p in range(k,min(k+tile,inner)) for j in range(x,min(x+tile,columns))}
                        reads += len(a)+len(b)
            self.assertEqual(m.tiled_loads(*shape)["tiled_input_elements"],reads)

    def test_bank_transpose_padding_and_broadcast(self):
        self.assertEqual(m.shared_bank_conflict([32*i for i in range(32)]),32)
        self.assertEqual(m.shared_bank_conflict([33*i for i in range(32)]),1)
        self.assertEqual(m.shared_bank_conflict([5]*32),1)

    def test_matmul_rectangular_exact_rational_reference(self):
        rng = random.Random(4)
        for rows, inner, columns in ((1,1,1),(3,5,2),(17,9,19)):
            a = [[rng.randint(-3,3) for _ in range(inner)] for _ in range(rows)]
            b = [[rng.randint(-3,3) for _ in range(columns)] for _ in range(inner)]
            exact = [[sum(Fraction(a[i][k])*b[k][j] for k in range(inner))
                      for j in range(columns)] for i in range(rows)]
            for tile in (1,2,8,32):
                self.assertEqual(m.matmul_tiled(a,b,tile),exact)

    def test_beam_search_exhaustive_fixed_length(self):
        table={-1:[0.6,0.4],0:[0.5,0.5],1:[0.01,0.99]}
        exact=[]
        for seq in itertools.product(range(2),repeat=4):
            previous,probability=-1,1
            for token in seq:
                probability *= table[previous][token]
                previous=token
            exact.append((seq,probability))
        expected=max(exact,key=lambda item:item[1])
        observed=m.beam_search(table,16,4)[0]
        self.assertEqual(observed[0],expected[0])
        self.assertAlmostEqual(math.exp(observed[1]),expected[1])
        self.assertGreater(m.beam_search(table,2,2)[0][1],m.beam_search(table,1,2)[0][1])

    def test_beam_eos_stops_and_cache_units(self):
        table={-1:[0.2,0.8],0:[0.1,0.9],1:[0.5,0.5]}
        self.assertEqual(m.beam_search(table,2,4,eos=1)[0][0],(1,))
        self.assertEqual(m.kv_bytes(1,2,3,4,5,2),480)

    def test_real_sqlite_wal_and_optimistic_conflict(self):
        result=m.sqlite_wal_snapshot()
        self.assertEqual(result["first"],(0,0))
        self.assertEqual(result["same_snapshot"],(0,0))
        self.assertEqual(result["current"],(1,1))
        self.assertEqual(result["changed_rows"],1)
        self.assertEqual(result["stale_changed_rows"],0)
        self.assertEqual(result["promotion_error"],sqlite3.SQLITE_BUSY_SNAPSHOT)

    def test_lamport_message_causality(self):
        a,b=m.LamportClock(),m.LamportClock()
        local=a.local()
        message=a.send()
        independent=b.local()
        received=b.receive(message)
        after=b.local()
        self.assertLess(local,message)
        self.assertLess(message,received)
        self.assertLess(independent,received)
        self.assertLess(received,after)
        self.assertEqual((m.LamportClock().local(),m.LamportClock().local()),(1,1))


class ScanVisionAttention(unittest.TestCase):
    def test_scan_against_sequential_prefixes(self):
        rng=random.Random(10)
        for size in range(80):
            values=[rng.randrange(-9,10) for _ in range(size)]
            result,meta=m.exclusive_scan(values)
            self.assertEqual(result,[sum(values[:i]) for i in range(size)])
            if size:
                self.assertLessEqual(meta["additions"],4*size-2)
            if size==0:self.assertEqual(meta,{"additions":0,"levels":0})

    def test_scan_stable_compaction(self):
        values=[8,3,4,7,2]
        flags=[int(x%2==0) for x in values]
        positions,_=m.exclusive_scan(flags)
        output=[None]*sum(flags)
        for value,flag,position in zip(values,flags,positions):
            if flag:output[position]=value
        self.assertEqual(output,[8,4,2])

    def test_bilinear_reproduces_affine_plane(self):
        image=[[2*x+3*y+5 for x in range(6)] for y in range(5)]
        for x,y in ((0.25,0.5),(2.7,1.4),(4.8,3.9)):
            self.assertAlmostEqual(m.bilinear(image,x,y),2*x+3*y+5)
        self.assertAlmostEqual(m.bilinear([[10]],-0.25,0),7.5)

    def test_inverse_warp_identity_and_integer_translation(self):
        image=[[1,2,3],[4,5,6]]
        self.assertEqual(m.warp_affine(image,[[1,0,0],[0,1,0]],3,2),image)
        self.assertEqual(m.warp_affine(image,[[1,0,-1],[0,1,0]],3,2),[[0,1,2],[0,4,5]])

    def test_attention_all_inputs_independent_finite_difference(self):
        q=[0.2,-0.3]
        keys=[[0.5,0.1],[-0.4,0.7],[0.2,0.8]]
        values=[[1,2],[-1,0.3],[0.6,-0.5]]
        upstream=[0.7,-0.2]
        _,(dq,dk,dv),_=m.attention_forward_backward(q,keys,values,upstream)
        def objective():
            output=m.attention_forward_backward(q,keys,values,upstream)[0]
            return sum(g*y for g,y in zip(upstream,output))
        h=1e-5
        for vector,gradient in [(q,dq),*zip(keys,dk),*zip(values,dv)]:
            for i,exact in enumerate(gradient):
                original=vector[i]
                vector[i]=original+h;plus=objective()
                vector[i]=original-h;minus=objective()
                vector[i]=original
                self.assertAlmostEqual(exact,(plus-minus)/(2*h),places=9)

    def test_mask_zero_derivative_and_single_key(self):
        q,k,v,g=[0.3],[[1],[2]],[[4],[100]],[2]
        output,(dq,dk,dv),p=m.attention_forward_backward(q,k,v,g,[True,False])
        self.assertEqual(output,[4])
        self.assertEqual(p,[1,0])
        self.assertEqual(dq,[0])
        self.assertEqual(dk,[[0],[0]])
        self.assertEqual(dv,[[2],[0]])
        with self.assertRaises(ValueError):
            m.attention_forward_backward(q,k,v,g,[False,False])

    def test_cached_attention_matches_full_prefix(self):
        cache=m.KVCache()
        for i in range(1,8):
            q=[0.1*i,-0.2]
            key=[0.3,0.2*i]
            value=[float(i),1/i]
            cached=cache.append_and_attend(q,key,value)
            # 작은 입력에서 직접 지수와 가중합을 계산해 별도 기준을 만든다.
            scores=[math.exp(sum(a*b for a,b in zip(q,k))/math.sqrt(2)) for k in cache.keys]
            total=sum(scores)
            expected=[sum(s*v[j] for s,v in zip(scores,cache.values))/total for j in range(2)]
            for a,b in zip(cached,expected):self.assertAlmostEqual(a,b)
        self.assertEqual(len(cache.keys),7)


class MetricsQuantizationRaster(unittest.TestCase):
    def test_macro_micro_and_confusion_counts(self):
        result=m.classification_metrics(["a"]*9+["b"],["a"]*10,["a","b"])
        self.assertAlmostEqual(result["macro_f1"],9/19)
        self.assertEqual(result["micro_f1"],0.9)
        self.assertEqual(result["accuracy"],0.9)
        self.assertEqual(result["per_class"][0]["tp"],9)
        self.assertEqual(result["per_class"][0]["fp"],1)

    def test_wilson_score_inversion_and_extremes(self):
        low,high=m.wilson_interval(7,20)
        z=1.959963984540054
        for p in (low,high):
            self.assertAlmostEqual((7/20-p)**2,z*z*p*(1-p)/20,places=14)
        self.assertEqual(m.wilson_interval(0,20)[0],0)
        self.assertAlmostEqual(m.wilson_interval(0,20)[1],z*z/(20+z*z))
        self.assertAlmostEqual(m.wilson_interval(20,20)[0],1-m.wilson_interval(0,20)[1])

    def test_single_pass_metrics_against_classwise_reference(self):
        generator=random.Random(63)
        for _ in range(100):
            truth=[generator.randrange(5) for _ in range(80)]
            guessed=[generator.randrange(5) for _ in truth]
            result=m.classification_metrics(truth,guessed,list(range(6)))
            for row in result['per_class']:
                label=row['class']
                tp=sum(a==label and b==label for a,b in zip(truth,guessed))
                fp=sum(a!=label and b==label for a,b in zip(truth,guessed))
                fn=sum(a==label and b!=label for a,b in zip(truth,guessed))
                self.assertEqual((row['tp'],row['fp'],row['fn']),(tp,fp,fn))
            self.assertAlmostEqual(result['micro_f1'],result['accuracy'])

    def test_per_channel_quantization_bound_and_zero_row(self):
        x=[0.3,-0.8,1.0,0.01]
        weights=[[0.01,0.002,-0.005,0.001],[3,-2,5,0.1],[0,0,0,0]]
        observed,meta=m.per_channel_linear(x,weights)
        for row,actual,scale in zip(weights,observed,meta["weight_scales"]):
            exact=sum(a*b for a,b in zip(x,row))
            ex,ew=meta["input_scale"]/2,scale/2
            bound=sum(abs(w)*ex+abs(value)*ew+ex*ew for value,w in zip(x,row))
            self.assertLessEqual(abs(exact-actual),bound+1e-14)
        self.assertEqual(observed[-1],0)
        self.assertGreater(meta["weight_scales"][1],100*meta["weight_scales"][0])
        self.assertAlmostEqual(meta["input_scale"],1/127)
        self.assertAlmostEqual(meta["weight_scales"][0],0.01/127)
        zeros,zero_meta=m.per_channel_linear([0,0],[[1,-2],[0,0]])
        self.assertEqual(zeros,[0,0])
        self.assertEqual(zero_meta["input_scale"],1)
        self.assertEqual(zero_meta["weight_scales"][1],1)
        self.assertTrue(all(abs(v)<=len(x)*127**2 for v in meta["accumulators"]))

    def test_perspective_ray_plane_oracle(self):
        # 원본 삼각형과 카메라 광선의 교점에서 얻은 속성은 2/11이다.
        value=m.perspective_interpolate([0.5,0.25,0.25],[0,1,0],[1,2,4])
        self.assertAlmostEqual(value,Fraction(2,11))
        self.assertNotAlmostEqual(value,0.25)
        self.assertAlmostEqual(m.perspective_interpolate([0.5,0.25,0.25],[0,1,0],[3,6,12]),value)

    def test_perspective_equal_depth_and_vertices(self):
        self.assertEqual(m.perspective_interpolate([0.2,0.3,0.5],[1,2,3],[2,2,2]),2.3)
        self.assertEqual(m.perspective_interpolate([0,1,0],[1,2,3],[1,2,3]),2)

    def test_cli_all_has_actual_outputs(self):
        command=[sys.executable,str(Path(__file__).with_name("demo.py")),"all"]
        result=subprocess.run(command,capture_output=True,text=True,encoding="utf-8",check=True)
        report=json.loads(result.stdout)
        self.assertEqual(len(report["results"]),13)
        self.assertEqual(report["results"]["database"]["current"],[1,1])
        self.assertLess(report["results"]["mlp"]["final_loss"],report["results"]["mlp"]["initial_loss"])


if __name__=="__main__":
    unittest.main()
