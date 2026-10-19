"""경계값, 독립 계산과 상태 순열로 확인하는 심화 예제."""

import ast
import hashlib
import itertools
import math
import random
import unittest
from collections import deque
from decimal import Decimal, localcontext
from fractions import Fraction

import advanced_models as m


class StreamTests(unittest.TestCase):
    def test_backpressure_preserves_order(self):
        stream = m.BoundedStream(7)
        source, accepted, received = bytes(range(250)), 0, bytearray()
        while accepted < len(source):
            accepted += stream.write(source[accepted:accepted+11])
            received.extend(stream.read(3))
            self.assertLessEqual(len(stream.data), 7)
        stream.close_writer()
        while chunk := stream.read(4):
            received.extend(chunk)
        self.assertEqual(received, source)

    def test_empty_is_not_eof(self):
        stream = m.BoundedStream(2)
        with self.assertRaises(BlockingIOError):
            stream.read(1)
        self.assertEqual(stream.write(b"abc"), 2)
        self.assertEqual(stream.write(b"d"), 0)
        stream.close_writer()
        self.assertEqual(stream.read(8), b"ab")
        self.assertEqual(stream.read(8), b"")
        with self.assertRaises(ValueError):
            stream.write(b"x")


class BuildTests(unittest.TestCase):
    def test_key_covers_inputs_and_environment(self):
        args = ({"a": b"1", "b": b"2"}, ["cc", "a"], "cc-v1", {"LANG": "C"})
        key = m.action_key(*args)
        self.assertEqual(key, m.action_key({"b": b"2", "a": b"1"}, *args[1:]))
        for changed in [({"a": b"2", "b": b"2"}, *args[1:]),
                        (args[0], ["cc", "-O2", "a"], *args[2:]),
                        (*args[:2], "cc-v2", args[3]),
                        (*args[:3], {"LANG": "ko_KR"})]:
            self.assertNotEqual(key, m.action_key(*changed))

    def test_cache_corruption_and_miss(self):
        cache = m.ArtifactCache()
        self.assertIsNone(cache.get("absent"))
        cache.put("key", b"artifact")
        self.assertEqual(cache.get("key"), b"artifact")
        expected, _ = cache.entries["key"]
        cache.entries["key"] = (expected, b"corrupted")
        with self.assertRaises(ValueError):
            cache.get("key")


class DataTests(unittest.TestCase):
    def test_order_independent_partition(self):
        rows = m.load_measurements(b"id,value\r\nb,2\r\na,1\r\nc,3\r\n")
        train, test = m.split_ids(rows, 17, 1)
        self.assertEqual((train, test), m.split_ids(list(reversed(rows)), 17, 1))
        self.assertEqual(set(train) | set(test), {"a", "b", "c"})
        self.assertFalse(set(train) & set(test))
        ranking = sorted(["a", "b", "c"], key=lambda s: hashlib.sha256(f'[17,"{s}"]'.encode()).hexdigest())
        self.assertEqual(test, ranking[:1])

    def test_reject_schema_duplicates_and_nonfinite(self):
        for raw in [b"id,value\na,1\na,2\n", b"id,value\na,nan\n", b"id,value\na,1,2\n",
                    b"value,id\n1,a\n", b"id,value\na\n"]:
            with self.assertRaises((ValueError, TypeError)):
                m.load_measurements(raw)


class RingTests(unittest.TestCase):
    def test_random_operations_against_deque(self):
        rng = random.Random(4)
        for capacity in [1, 2, 7, 64]:
            ring, reference = m.ByteRing(capacity), deque()
            for _ in range(4000):
                if rng.randrange(2):
                    byte = rng.randrange(256)
                    success = len(reference) < capacity
                    self.assertEqual(ring.push(byte), success)
                    if success:
                        reference.append(byte)
                else:
                    self.assertEqual(ring.pop(), reference.popleft() if reference else None)
                self.assertEqual(ring.used, len(reference))
                self.assertTrue(0 <= ring.head < capacity and 0 <= ring.tail < capacity)

    def test_boundaries(self):
        with self.assertRaises(ValueError):
            m.ByteRing(0)
        ring = m.ByteRing(1)
        for value in [-1, 256, True]:
            with self.assertRaises(ValueError):
                ring.push(value)
        self.assertIsNone(ring.pop())


class RootTests(unittest.TestCase):
    def test_sqrt_against_decimal(self):
        with localcontext() as ctx:
            ctx.prec = 70
            for n in [2, 3, 7, 20, 1000]:
                result = m.bracketed_newton(lambda x: x*x-n, lambda x: 2*x, 0, n+1)
                expected = float(Decimal(n).sqrt())
                self.assertLessEqual(abs(result.x - expected), 1.1e-10)
                self.assertLessEqual(result.lo, expected + 1e-13)
                self.assertGreaterEqual(result.hi, expected - 1e-13)

    def test_bisection_fallback_and_failures(self):
        result = m.bracketed_newton(lambda x: x-0.3, lambda x: 0.0, 0, 1)
        self.assertAlmostEqual(result.x, 0.3, places=9)
        for f in [lambda x: x*x+1, lambda x: math.nan]:
            with self.assertRaises(ValueError):
                m.bracketed_newton(f, lambda x: 1, -1, 1)
        with self.assertRaises(ArithmeticError):
            m.bracketed_newton(lambda x: x*x-2, lambda x: 2*x, 0, 2, max_steps=1)


class LocalityTests(unittest.TestCase):
    def test_trace_against_list_lru(self):
        rng = random.Random(7)
        for _ in range(100):
            addresses = [rng.randrange(256) for _ in range(100)]
            resident, misses = [], 0
            for address in addresses:
                block = address // 16
                if block in resident:
                    resident.remove(block)
                else:
                    misses += 1
                resident.append(block)
                resident = resident[-3:]
            self.assertEqual(m.cache_trace(addresses, 16, 3), misses)

    def test_aos_vs_soa_one_field(self):
        self.assertEqual(m.cache_trace([i*16 for i in range(64)], 64, 2), 16)
        self.assertEqual(m.cache_trace([i*4 for i in range(64)], 64, 2), 4)


class SearchTests(unittest.TestCase):
    def test_grid_against_breadth_first_search(self):
        rng = random.Random(8)
        for _ in range(150):
            blocked = {(x, y) for x in range(6) for y in range(6)
                       if (x, y) not in {(0,0), (5,5)} and rng.random() < .25}
            graph = m.grid_graph(6, 6, blocked)
            queue, distance = deque([(0, 0)]), {(0, 0): 0}
            while queue:
                node = queue.popleft()
                for other, _ in graph[node]:
                    if other not in distance:
                        distance[other] = distance[node] + 1
                        queue.append(other)
            cost, path, _ = m.astar(graph, (0,0), (5,5), lambda v: 10-v[0]-v[1])
            self.assertEqual(cost, distance.get((5,5), math.inf))
            if path:
                self.assertEqual(len(path)-1, cost)
                self.assertTrue(all(b in dict(graph[a]) for a,b in zip(path,path[1:])))

    def test_reopening_with_inconsistent_admissible_heuristic(self):
        graph = {"s": [("a", 3), ("b", 1)], "b": [("a", 1)], "a": [("g", 3)], "g": []}
        h = {"s": 5, "a": 0, "b": 4, "g": 0}
        self.assertEqual(m.astar(graph, "s", "g", h.__getitem__)[:2], (5, ["s","b","a","g"]))

    def test_negative_edge_rejected(self):
        with self.assertRaises(ValueError):
            m.astar({0: [(1, -1)], 1: []}, 0, 1, lambda _: 0)


class PriorityTests(unittest.TestCase):
    def test_transitive_inheritance(self):
        base = {"L": 1, "M": 3, "H": 9}
        effective = m.inherited_priorities(base, {"A": "L", "B": "M"}, {"H": "B", "M": "A"})
        self.assertEqual(effective, {"L": 9, "M": 9, "H": 9})
        self.assertEqual(base["L"], 1)
        self.assertEqual(m.inherited_priorities(base, {"A":"L"}, {}), base)

    def test_interference_removal(self):
        self.assertEqual(m.inversion_trace(False), list("MMMMLLLH"))
        self.assertEqual(m.inversion_trace(True), list("LLLHMMMM"))


class PollTests(unittest.TestCase):
    def test_real_socket_readiness_and_eof(self):
        self.assertEqual(m.socket_records(b"alpha\n\nbeta\n"),[b"alpha",b"",b"beta"])

    def test_every_split_preserves_records(self):
        raw = b"alpha\n\nbeta\n"
        for split in range(len(raw)+1):
            receiver = m.LineReceiver()
            records = receiver.feed(raw[:split]) + receiver.feed(raw[split:])
            receiver.eof()
            self.assertEqual(records, [b"alpha", b"", b"beta"])

    def test_truncation_and_bounds(self):
        receiver = m.LineReceiver(2)
        with self.assertRaises(ValueError):
            receiver.feed(b"abc")
        receiver = m.LineReceiver()
        receiver.feed(b"unfinished")
        with self.assertRaises(ValueError):
            receiver.eof()


class WatchTests(unittest.TestCase):
    def test_access_and_value_change_are_different(self):
        events = [("write", 9, b"ab", b"ac"), ("write",10,b"c",b"c"),
                  ("read",10,b"c",b"c"), ("write",11,b"z",b"x")]
        self.assertEqual(m.watch_hits(events, 10, 1), [0,1])
        self.assertEqual(m.watch_hits(events, 10, 1, detect_same=False), [0])
        self.assertEqual(m.watch_hits(events, 10, 1, access="read"), [2])

    def test_change_outside_region_does_not_change_watched_value(self):
        events = [("write", 9, b"ab", b"zb")]
        self.assertEqual(m.watch_hits(events,10,1,detect_same=False), [])


class I2CTests(unittest.TestCase):
    def test_known_register_read(self):
        trace = m.i2c_register_read(0x50, 0x12, b"\xab\xcd")
        self.assertEqual([e for e in trace if e[0] == "TX"], [("TX",0xA0),("TX",0x12),("TX",0xA1)])
        self.assertEqual(trace[-5:], [("RX",0xAB),("ACK",),("RX",0xCD),("NACK",),("STOP",)])
        self.assertEqual(sum(e[0] in {"TX","RX"} for e in trace)*9, 45)

    def test_one_byte_and_invalid_address(self):
        self.assertEqual(m.i2c_register_read(1,0,b"x")[-2], ("NACK",))
        for address in [-1,128]:
            with self.assertRaises(ValueError):
                m.i2c_register_read(address,0,b"x")


class ControlTests(unittest.TestCase):
    def test_saturation_does_not_accumulate_outward_integral(self):
        controller = m.PIController(2,4,-1,1)
        for _ in range(1000):
            self.assertEqual(controller.update(100,0,.01), 1)
        self.assertEqual(controller.integral, 0)
        self.assertEqual(controller.update(-1,0,.01), -1)

    def test_reachable_speed_converges(self):
        history = m.simulate_speed(m.PIController(.8,2,-1,1))
        self.assertLess(abs(history[-1][0] - 1), 1e-6)
        self.assertTrue(all(-1 <= u <= 1 for _,u in history))
        self.assertLess(max(speed for speed,_ in history), 1.2)

    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            m.PIController(1,1,-1,1).update(1,0,0)


class ExperimentTests(unittest.TestCase):
    def test_paired_statistics_against_rational_arithmetic(self):
        a, b = [100,200,300,400], [102,201,304,403]
        mean, se, differences = m.paired_summary(a,b)
        exact = sum(map(Fraction,differences))/4
        variance = sum((Fraction(x)-exact)**2 for x in differences)/3
        self.assertEqual(mean, float(exact))
        self.assertAlmostEqual(se*se, float(variance/4))
        self.assertEqual(m.paired_summary([x+5000 for x in a],[x+5000 for x in b])[:2],(mean,se))

    def test_no_invented_precision_with_one_pair(self):
        with self.assertRaises(ValueError):
            m.paired_summary([1],[2])


class IncrementalTests(unittest.TestCase):
    def test_reverse_closure_against_recursive_dependency(self):
        deps = {"a": ["x"], "b": ["y"], "c": ["a","b"], "d": ["a"]}
        def needs(node, changed):
            return node in changed or any(needs(d,changed) for d in deps.get(node,()))
        for size in range(4):
            for changed in itertools.combinations(["x","y","a"],size):
                expected = sorted(n for n in deps if needs(n,changed))
                self.assertEqual(m.affected_targets(deps,changed), expected)

    def test_cycle_rejected(self):
        with self.assertRaises(ValueError):
            m.affected_targets({"a":["b"],"b":["a"]},["a"])


class ReplayTests(unittest.TestCase):
    def test_window_against_set_oracle(self):
        receiver, seen, highest = m.ReplayReceiver(b"k"*32,width=8), set(), 0
        rng = random.Random(38)
        for sequence in [*range(1,50), *[rng.randrange(1,100) for _ in range(500)]]:
            expected = sequence not in seen and sequence > highest-8
            self.assertEqual(receiver.accept(sequence,b"data",receiver.tag(sequence,b"data")), expected)
            if expected:
                seen.add(sequence)
                highest = max(highest, sequence)

    def test_forgery_cannot_advance_window(self):
        receiver = m.ReplayReceiver(b"k"*32)
        self.assertFalse(receiver.accept(2**63,b"data",b"x"*32))
        self.assertEqual((receiver.highest,receiver.bitmap),(0,0))
        tag = receiver.tag(1,b"data")
        self.assertTrue(receiver.accept(1,b"data",tag))
        self.assertFalse(receiver.accept(1,b"data",tag))
        self.assertTrue(m.ReplayReceiver(b"k"*32).accept(1,b"data",tag))


class CompilerTests(unittest.TestCase):
    @staticmethod
    def oracle(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op,ast.USub):
            return -CompilerTests.oracle(node.operand)
        if isinstance(node,ast.BinOp):
            a,b = CompilerTests.oracle(node.left),CompilerTests.oracle(node.right)
            if isinstance(node.op,ast.Add): return a+b
            if isinstance(node.op,ast.Sub): return a-b
            if isinstance(node.op,ast.Mult): return a*b
        raise ValueError("oracle grammar")

    def test_random_expressions_against_python_ast(self):
        rng = random.Random(39)
        def generate(depth):
            if depth == 0 or rng.random() < .3:
                return str(rng.randrange(20))
            if rng.random() < .2:
                return "-("+generate(depth-1)+")"
            return "("+generate(depth-1)+rng.choice(["+","-","*"])+generate(depth-1)+")"
        for _ in range(500):
            source = generate(4)
            self.assertEqual(m.execute(m.compile_expression(source)),self.oracle(ast.parse(source,mode="eval").body))

    def test_precedence_and_associativity(self):
        for source,expected in [("2+3*4",14),("10-3-2",5),("-(2+3)*4",-20),("2*-3",-6)]:
            self.assertEqual(m.execute(m.compile_expression(source)),expected)

    def test_bad_source_and_bytecode(self):
        for source in ["", "1 2", "a+1", "1/2", "(2+3", "2+", "x()"]:
            with self.assertRaises(ValueError):
                m.compile_expression(source)
        for code in [[("ADD",)],[("PUSH",1),("PUSH",2)],[("CALL",)]]:
            with self.assertRaises(ValueError):
                m.execute(code)


class PropertyTests(unittest.TestCase):
    def test_shrink_preserves_failure_and_is_one_deletion_minimal(self):
        fails = lambda xs: 0 in xs and any(x < 0 for x in xs)
        result = m.shrink_failure([10,0,7,-8,4,-2],fails)
        self.assertTrue(fails(result))
        self.assertEqual(len(result),2)
        self.assertTrue(all(not fails(result[:i]+result[i+1:]) for i in range(len(result))))

    def test_nonfailure_rejected(self):
        with self.assertRaises(ValueError):
            m.shrink_failure([1,2],lambda xs: 0 in xs)


class ApiTests(unittest.TestCase):
    def test_two_writers_do_not_lose_first_update(self):
        for first,second in [("A","B"),("B","A")]:
            resource = m.VersionedResource("initial")
            _,tag_a = resource.read()
            _,tag_b = resource.read()
            self.assertEqual(resource.put(first,tag_a),200)
            self.assertEqual(resource.put(second,tag_b),412)
            self.assertEqual(resource.value,first)
            _,fresh = resource.read()
            self.assertEqual(resource.put(second,fresh),200)

    def test_precondition_and_validation_are_nonmutating(self):
        resource = m.VersionedResource("initial")
        for value,tag,status in [("new",None,428),("new",'W/"v1"',412),("",'"v1"',400)]:
            self.assertEqual(resource.put(value,tag),status)
            self.assertEqual(resource.read(),("initial",'"v1"'))


class UITests(unittest.TestCase):
    def test_completion_permutations(self):
        state = m.UIState()
        effects = []
        for query in ["a","ab","abc"]:
            state,effect = m.reduce_ui(state,("search",query))
            effects.append(effect)
        for order in itertools.permutations(effects):
            current = state
            for _,generation,query in order:
                current,_ = m.reduce_ui(current,("success",generation,[query]))
            self.assertEqual(current.result,("abc",))
            self.assertFalse(current.loading)

    def test_stop_restart_and_duplicate(self):
        state,_ = m.reduce_ui(m.UIState(),("search","a"))
        stopped,_ = m.reduce_ui(state,("stop",))
        ignored,_ = m.reduce_ui(stopped,("success",state.generation,["old"]))
        self.assertEqual(ignored,stopped)
        restarted,_ = m.reduce_ui(stopped,("start",))
        current,_ = m.reduce_ui(restarted,("search","b"))
        done,_ = m.reduce_ui(current,("success",current.generation,["new"]))
        again,_ = m.reduce_ui(done,("failure",current.generation,"late"))
        self.assertEqual(done,again)


if __name__ == "__main__":
    unittest.main(verbosity=2)
