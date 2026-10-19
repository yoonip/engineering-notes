"""주제별 입력과 관찰 결과를 JSON으로 출력한다."""

import argparse
import json
from dataclasses import asdict

import advanced_models as m


def demo(name):
    if name == "pipe":
        stream = m.BoundedStream(4)
        first = stream.write(b"abcdef")
        data = stream.read(2)
        second = stream.write(b"abcdef"[first:])
        stream.close_writer()
        return {"accepted": [first, second], "received": (data+stream.read(8)).decode(), "eof": stream.read(1).hex()}
    if name == "build":
        key = m.action_key({"main.c":b"int main(void){return 0;}"},["cc","main.c"],"example-cc-v1",{"LANG":"C"})
        cache = m.ArtifactCache()
        cache.put(key,b"conceptual artifact")
        return {"action_key":key,"hit_digest":m.digest(cache.get(key))}
    if name == "data":
        raw = b"id,value\na,1\nb,2\nc,3\n"
        rows = m.load_measurements(raw)
        train,test = m.split_ids(rows,17,1)
        return {"raw_sha256":m.digest(raw),"rows":rows,"train_ids":train,"test_ids":test}
    if name == "ring":
        ring = m.ByteRing(3)
        accepted = [ring.push(v) for v in [10,20,30,40]]
        return {"accepted":accepted,"popped":[ring.pop() for _ in range(4)]}
    if name == "root":
        return asdict(m.bracketed_newton(lambda x:x*x-2,lambda x:2*x,0,2))
    if name == "cache":
        return {"aos_misses":m.cache_trace([i*16 for i in range(64)],64,2),
                "soa_misses":m.cache_trace([i*4 for i in range(64)],64,2),"model":"fully associative LRU"}
    if name == "astar":
        graph = m.grid_graph(6,6,{(2,0),(2,1),(2,2),(2,3)})
        cost,path,expanded = m.astar(graph,(0,0),(5,5),lambda p:10-p[0]-p[1])
        return {"cost":cost,"path":path,"expanded":expanded}
    if name == "rtos":
        return {"without_inheritance":m.inversion_trace(False),"with_inheritance":m.inversion_trace(True)}
    if name == "poll":
        return {"records":[r.decode() for r in m.socket_records(b"alpha\n\nbeta\n")],"transport":"local socketpair"}
    if name == "watch":
        events = [("write",10,b"a",b"b"),("write",10,b"b",b"b"),("read",10,b"b",b"b")]
        return {"access_write_hits":m.watch_hits(events,10,1),
                "changed_value_hits":m.watch_hits(events,10,1,detect_same=False)}
    if name == "i2c":
        return {"trace":m.i2c_register_read(0x50,0x12,b"\xab\xcd"),"clocked_bits_without_start_stop":45}
    if name == "pi":
        history = m.simulate_speed(m.PIController(.8,2,-1,1))
        return {"final_speed":history[-1][0],"max_speed":max(x for x,_ in history),"last_command":history[-1][1]}
    if name == "experiment":
        mean,se,differences = m.paired_summary([100,200,300,400],[102,201,304,403])
        return {"differences":differences,"mean_b_minus_a":mean,"standard_error":se,"data_kind":"constructed numerical example"}
    if name == "ci":
        return {"affected":m.affected_targets({"compile-a":["a.c","a.h"],"compile-b":["b.c"],"link":["compile-a","compile-b"]},["a.h"])}
    if name == "replay":
        receiver = m.ReplayReceiver(b"public-test-key-32-bytes-long!!!!")
        tag = receiver.tag(1,b"status")
        return {"first":receiver.accept(1,b"status",tag),"repeat":receiver.accept(1,b"status",tag),"highest":receiver.highest}
    if name == "parser":
        source = "10-3*2-(1+2)"
        code = m.compile_expression(source)
        return {"source":source,"bytecode":code,"result":m.execute(code)}
    if name == "property":
        original = [10,0,7,-8,4,-2]
        return {"original":original,"one_deletion_minimal":m.shrink_failure(original,lambda xs:0 in xs and any(x<0 for x in xs))}
    if name == "api":
        resource = m.VersionedResource("initial")
        _,tag = resource.read()
        return {"first_status":resource.put("A",tag),"stale_status":resource.put("B",tag),"current":resource.read()}
    if name == "ui":
        state,effect_a = m.reduce_ui(m.UIState(),("search","a"))
        state,effect_b = m.reduce_ui(state,("search","ab"))
        state,_ = m.reduce_ui(state,("success",effect_b[1],["new result"]))
        state,_ = m.reduce_ui(state,("success",effect_a[1],["stale result"]))
        return {"state":asdict(state),"effects":[effect_a,effect_b]}
    raise ValueError(name)


NAMES = ["pipe","build","data","ring","root","cache","astar","rtos","poll","watch",
         "i2c","pi","experiment","ci","replay","parser","property","api","ui"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name",choices=[*NAMES,"all"])
    args = parser.parse_args()
    result = {n:demo(n) for n in NAMES} if args.name == "all" else demo(args.name)
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
