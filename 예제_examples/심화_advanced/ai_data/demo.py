"""13개 심화 예제를 실제로 실행하고 JSON 결과를 출력한다."""

import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
import random
import sqlite3
import sys
import time

import advanced_ai_models as m


def initial_parameters():
    generator = random.Random(7)
    return [generator.uniform(-0.8, 0.8) for _ in range(17)]


def run_case(name):
    if name == "mlp":
        xs, ys = [[-1,-1],[-1,1],[1,-1],[1,1]], [0,1,1,0]
        parameters = initial_parameters()
        initial, _ = m.mlp_batch(parameters, xs, ys)
        for _ in range(600):
            _, gradient = m.mlp_batch(parameters, xs, ys)
            parameters = [p-0.2*g for p,g in zip(parameters,gradient)]
        final, _ = m.mlp_batch(parameters, xs, ys)
        return {"initial_loss": initial, "final_loss": final, "updates":600,
                "probabilities":[m.mlp_loss_gradient(parameters,x,0)[2] for x in xs]}
    if name == "tile":
        return {"shape":[37,45,29],"tile":16,"loads":m.tiled_loads(37,45,29,16),
                "transpose_conflict":m.shared_bank_conflict([32*i for i in range(32)]),
                "padded_conflict":m.shared_bank_conflict([33*i for i in range(32)])}
    if name == "matrix":
        rows,inner,columns=37,29,45
        a=[[(i*3+k)%11-5 for k in range(inner)] for i in range(rows)]
        b=[[(k+2*j)%7-3 for j in range(columns)] for k in range(inner)]
        start=time.perf_counter()
        actual=m.matmul_tiled(a,b,16)
        elapsed=time.perf_counter()-start
        reference=[[sum(a[i][k]*b[k][j] for k in range(inner)) for j in range(columns)] for i in range(rows)]
        error=max(abs(actual[i][j]-reference[i][j]) for i in range(rows) for j in range(columns))
        return {"shape":[rows,inner,columns],"cpu_seconds":elapsed,"max_absolute_error":error,
                "checksum":math.fsum(x for row in actual for x in row),"cuda_executed":False}
    if name == "decode":
        table={-1:[0.6,0.4],0:[0.5,0.5],1:[0.01,0.99]}
        return {"greedy":m.beam_search(table,1,4)[0],"beam2":m.beam_search(table,2,4)[0],
                "kv_example_bytes":m.kv_bytes(1,32,8,4096,128,2)}
    if name == "database":
        return m.sqlite_wal_snapshot()
    if name == "clocks":
        first,second=m.LamportClock(),m.LamportClock()
        events=[["A.local",first.local()],["B.local",second.local()]]
        timestamp=first.send()
        events += [["A.send",timestamp],["B.receive",second.receive(timestamp)],["B.local",second.local()]]
        return {"events":events,"physical_time_measured":False}
    if name == "scan":
        values=[3,1,7,0,4,1,6,3,2]
        prefix,meta=m.exclusive_scan(values)
        return {"input":values,"exclusive":prefix,"inclusive":[a+b for a,b in zip(prefix,values)],**meta}
    if name == "warp":
        image=[[10*y+x for x in range(5)] for y in range(4)]
        warped=m.warp_affine(image,[[1,0,-0.5],[0,1,-0.25]],5,4)
        return {"input":image,"inverse_map":[[1,0,-0.5],[0,1,-0.25]],"output":warped}
    if name == "attention":
        query=[0.2,-0.3]
        keys=[[0.5,0.1],[-0.4,0.7],[0.2,0.8]]
        values=[[1,2],[-1,0.3],[0.6,-0.5]]
        output,gradient,p=m.attention_forward_backward(query,keys,values,[0.7,-0.2])
        cache=m.KVCache()
        cached=[cache.append_and_attend(query,key,value) for key,value in zip(keys,values)]
        return {"output":output,"probabilities":p,"dq":gradient[0],"cached_prefix_outputs":cached}
    if name == "adam":
        optimizer=m.Adam([1.0,-2.0],rate=0.05)
        initial=math.fsum(x*x for x in optimizer.parameters)/2
        for _ in range(200):
            gradient,_=m.clip_gradient(optimizer.parameters,1)
            optimizer.update(gradient)
        return {"initial_loss":initial,"final_loss":math.fsum(x*x for x in optimizer.parameters)/2,
                "state":asdict(optimizer)}
    if name == "metrics":
        result=m.classification_metrics(["a"]*9+["b"],["a"]*10,["a","b"])
        result["accuracy_wilson95"]=m.wilson_interval(9,10)
        return result
    if name == "quantization":
        inputs=[0.3,-0.8,1,0.01]
        weights=[[0.01,0.002,-0.005,0.001],[3,-2,5,0.1],[0,0,0,0]]
        output,metadata=m.per_channel_linear(inputs,weights)
        reference=[math.fsum(x*w for x,w in zip(inputs,row)) for row in weights]
        return {"integer_outputs_dequantized":output,"float_reference":reference,
                "absolute_errors":[abs(a-b) for a,b in zip(output,reference)],**metadata}
    if name == "raster":
        weights,attributes,clip_w=[0.5,0.25,0.25],[0,1,0],[1,2,4]
        return {"screen_weights":weights,"affine":sum(a*b for a,b in zip(weights,attributes)),
                "perspective_correct":m.perspective_interpolate(weights,attributes,clip_w),
                "ray_plane_reference":2/11}
    raise ValueError("알 수 없는 예제입니다")


CASES=("mlp","tile","matrix","decode","database","clocks","scan","warp",
       "attention","adam","metrics","quantization","raster")


def main():
    parser=argparse.ArgumentParser(description="AI·데이터 심화 예제를 실행합니다")
    parser.add_argument("case",choices=(*CASES,"all"))
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    cases=CASES if args.case=="all" else (args.case,)
    start=time.perf_counter()
    result={"python":sys.version.split()[0],"sqlite":sqlite3.sqlite_version,
            "results":{name:run_case(name) for name in cases},
            "elapsed_seconds":time.perf_counter()-start}
    rendered=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered,encoding="utf-8")
    print(rendered,end="")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
