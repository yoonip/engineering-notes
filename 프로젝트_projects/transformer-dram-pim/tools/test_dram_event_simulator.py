#!/usr/bin/env python3
"""새 DRAM 모델의 손계산 oracle·불변조건·입력/종료 회귀. 기존 RTL 시험과 독립이다.

예상 숫자는 simulate()로 만들지 않는다. 작은 timing 설정에서 ACT/RD/PRE 및
data 구간을 종이에 계산한 정수 literal과 비교한다. 난수 시험은 추가 불변조건
회귀이며 손계산 oracle 또는 실제 DDR 장치 검증을 대신하지 않는다.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import random
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.dram_pim_event_simulator import (MemoryRequest, SimulationLimitError, TimingConfig,
                                              check_invariants, load_legacy_csv, simulate, write_outputs)

TEST_DIR: Path | None = None


def small(**changes) -> TimingConfig:
    """손계산용 작은 정수. 상용 메모리의 timing 표가 아니다."""
    base = TimingConfig(banks=2, queue_depth=2, t_rcd=2, t_rp=2, t_ras=4, t_rc=6,
                        t_ccd=2, t_rrd=1, t_faw=4, read_latency=2, write_latency=1,
                        burst_cycles=2, t_rtp=1, t_wr=1, t_rtw=1, t_wtr=2,
                        refresh_enabled=False, t_refi=30, t_rfc=4)
    return replace(base, **changes)


def requests(items) -> list[MemoryRequest]:
    """(arrival,READ/WRITE,bank,row) 순서를 literal 요청으로 바꿀 뿐 시간을 계산하지 않는다."""
    return [MemoryRequest(f"q{i}", *item) for i, item in enumerate(items)]


def commands(result) -> list[tuple[int, str, int | None]]:
    return [(e["cycle"], e["command"], e["bank"]) for e in result["events"] if e["event"] == "COMMAND"]


def data_ranges(result) -> list[tuple[int, int]]:
    return [(r["data_start_cycle"], r["data_end_cycle"]) for r in result["requests"]]


class HandCalculatedTests(unittest.TestCase):
    """명령/버스 구간/완료 시간을 상수 oracle로 비교하는 별도 작은 경계들."""

    def assertSchedule(self, items, cfg, expected_commands, expected_ranges, finish):
        result = simulate(requests(items), cfg)
        self.assertEqual(commands(result), expected_commands)
        self.assertEqual(data_ranges(result), expected_ranges)
        self.assertEqual(result["finish_cycle"], finish)
        self.assertTrue(result["invariants"]["passed"])
        return result

    def test_single_read(self):
        self.assertSchedule([(0,"READ",0,0)], small(), [(0,"ACT",0),(2,"RD",0)], [(4,6)], 6)

    def test_large_command_spacing_and_minimum_fifo(self):
        result = self.assertSchedule([(0,"READ",0,0),(0,"READ",0,0)], small(t_cmd=5,queue_depth=1),
                                     [(0,"ACT",0),(5,"RD",0),(10,"RD",0)], [(7,9),(12,14)], 14)
        self.assertEqual([r["enqueue_cycle"] for r in result["requests"]],[0,6])
        self.assertEqual(result["fifo_backpressure_cycles"],5)

    def test_large_shared_t_ccd(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",0,0)], small(t_ccd=10),
                            [(0,"ACT",0),(2,"RD",0),(12,"RD",0)], [(4,6),(14,16)], 16)

    def test_same_row_hit_and_shared_data_bus(self):
        result = self.assertSchedule([(0,"READ",0,0),(0,"READ",0,0)], small(),
                                     [(0,"ACT",0),(2,"RD",0),(4,"RD",0)], [(4,6),(6,8)], 8)
        self.assertEqual((result["row_hits"], result["row_misses"], result["row_conflicts"]), (1,1,0))

    def test_row_conflict(self):
        result = self.assertSchedule([(0,"READ",0,0),(0,"READ",0,1)], small(),
                                     [(0,"ACT",0),(2,"RD",0),(6,"PRE",0),(8,"ACT",0),(10,"RD",0)],
                                     [(4,6),(12,14)], 14)
        self.assertEqual((result["row_misses"], result["row_conflicts"]), (2,1))

    def test_t_ras_boundary(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",0,1)], small(t_ras=10,t_rc=12),
                            [(0,"ACT",0),(2,"RD",0),(10,"PRE",0),(12,"ACT",0),(14,"RD",0)],
                            [(4,6),(16,18)], 18)

    def test_t_rc_boundary(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",0,1)], small(t_rc=20),
                            [(0,"ACT",0),(2,"RD",0),(6,"PRE",0),(20,"ACT",0),(22,"RD",0)],
                            [(4,6),(24,26)], 26)

    def test_t_rtp_boundary(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",0,1)], small(t_rtp=10),
                            [(0,"ACT",0),(2,"RD",0),(12,"PRE",0),(14,"ACT",0),(16,"RD",0)],
                            [(4,6),(18,20)], 20)

    def test_write_recovery_after_data_end(self):
        self.assertSchedule([(0,"WRITE",0,0),(0,"READ",0,1)], small(t_wr=5),
                            [(0,"ACT",0),(2,"WR",0),(10,"PRE",0),(12,"ACT",0),(14,"RD",0)],
                            [(3,5),(16,18)], 18)

    def test_write_recovery_before_refresh_independent_oracle(self):
        self.assertSchedule([(0,"WRITE",0,0),(38,"WRITE",0,0)],
                            small(refresh_enabled=True,t_refi=40,t_wr=5),
                            [(0,"ACT",0),(2,"WR",0),(38,"WR",0),(46,"PRE",0),(48,"REF",None)],
                            [(3,5),(39,41)],52)

    def test_bank_act_overlaps_other_bank_data_wait(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",1,0)], small(),
                            [(0,"ACT",0),(2,"RD",0),(3,"ACT",1),(5,"RD",1)], [(4,6),(7,9)], 9)

    def test_read_write_turnaround(self):
        self.assertSchedule([(0,"READ",0,0),(0,"WRITE",0,0)], small(),
                            [(0,"ACT",0),(2,"RD",0),(6,"WR",0)], [(4,6),(7,9)], 9)

    def test_write_read_turnaround(self):
        self.assertSchedule([(0,"WRITE",0,0),(0,"READ",0,0)], small(),
                            [(0,"ACT",0),(2,"WR",0),(5,"RD",0)], [(3,5),(7,9)], 9)

    def test_fifo_next_cycle_acceptance(self):
        result = self.assertSchedule([(0,"READ",0,0),(0,"READ",0,0)], small(queue_depth=1),
                                     [(0,"ACT",0),(2,"RD",0),(4,"RD",0)], [(4,6),(6,8)], 8)
        self.assertEqual([r["enqueue_cycle"] for r in result["requests"]], [0,3])
        self.assertEqual(result["fifo_backpressure_cycles"], 2)

    def test_fifo_records_future_arrival_while_full(self):
        result = simulate(requests([(0,"READ",0,0),(10,"READ",0,0)]), small(queue_depth=1,t_rcd=14))
        self.assertEqual([(e["cycle"],e["event"]) for e in result["events"] if e["event"].startswith("BACKPRESSURE")],
                         [(10,"BACKPRESSURE_START"),(15,"BACKPRESSURE_END")])
        self.assertEqual([r["enqueue_cycle"] for r in result["requests"]], [0,15])
        self.assertEqual(result["fifo_backpressure_cycles"], 5)

    def test_independent_reviewer_bank_fifo_oracle(self):
        cfg = small(queue_depth=1,t_rcd=3,read_latency=4,write_latency=2,
                    t_wr=3,t_rtw=2,t_wtr=3,t_rrd=2,t_faw=8)
        result = self.assertSchedule([(0,"READ",0,0),(0,"READ",1,0),(0,"READ",0,0)], cfg,
                                     [(0,"ACT",0),(3,"RD",0),(4,"ACT",1),(7,"RD",1),(9,"RD",0)],
                                     [(7,9),(11,13),(13,15)], 15)
        self.assertEqual([r["enqueue_cycle"] for r in result["requests"]], [0,4,8])
        self.assertEqual(result["fifo_backpressure_cycles"], 6)

    def test_global_t_rrd(self):
        cfg = small(t_rcd=1,t_rp=1,t_ras=2,t_rc=3,t_ccd=1,read_latency=1,
                    burst_cycles=1,t_rrd=5,t_faw=10)
        self.assertSchedule([(0,"READ",0,0),(0,"READ",1,0)], cfg,
                            [(0,"ACT",0),(1,"RD",0),(5,"ACT",1),(6,"RD",1)], [(2,3),(7,8)], 8)

    def test_rolling_four_act_t_faw(self):
        cfg = small(banks=5,queue_depth=5,t_rcd=1,t_rp=1,t_ras=2,t_rc=3,t_ccd=1,
                    read_latency=1,burst_cycles=1,t_rrd=1,t_faw=10)
        self.assertSchedule([(0,"READ",i,0) for i in range(5)], cfg,
                            [(0,"ACT",0),(1,"RD",0),(2,"ACT",1),(3,"RD",1),
                             (4,"ACT",2),(5,"RD",2),(6,"ACT",3),(7,"RD",3),(10,"ACT",4),(11,"RD",4)],
                            [(2,3),(4,5),(6,7),(8,9),(12,13)], 13)

    def test_due_precedes_act_at_same_arrival(self):
        self.assertSchedule([(30,"READ",0,0)], small(refresh_enabled=True),
                            [(30,"REF",None),(34,"ACT",0),(36,"RD",0)], [(38,40)], 40)

    def test_arrival_and_full_fifo_during_refresh(self):
        result = self.assertSchedule([(31,"READ",0,0),(32,"READ",0,0)],
                                     small(refresh_enabled=True,queue_depth=1),
                                     [(30,"REF",None),(34,"ACT",0),(36,"RD",0),(38,"RD",0)],
                                     [(38,40),(40,42)],42)
        self.assertEqual([r["enqueue_cycle"] for r in result["requests"]],[31,37])
        self.assertEqual(result["fifo_backpressure_cycles"],5)

    def test_very_late_first_arrival_without_refresh(self):
        self.assertSchedule([(1000000,"READ",0,0)],small(),
                            [(1000000,"ACT",0),(1000002,"RD",0)],[(1000004,1000006)],1000006)

    def test_refresh_drains_data_and_restarts_closed_row(self):
        result = self.assertSchedule([(0,"READ",0,0),(28,"READ",0,0),(29,"READ",0,0)],
                                     small(refresh_enabled=True),
                                     [(0,"ACT",0),(2,"RD",0),(28,"RD",0),(32,"PRE",0),
                                      (34,"REF",None),(38,"ACT",0),(40,"RD",0)],
                                     [(4,6),(30,32),(42,44)], 44)
        self.assertEqual(result["max_refresh_lateness_cycles"], 4)
        self.assertEqual([r["row_class"] for r in result["requests"]], ["miss","hit","miss"])

    def test_refresh_closes_two_banks_on_shared_command_bus(self):
        self.assertSchedule([(0,"READ",0,0),(0,"READ",1,0),(28,"READ",0,0)], small(refresh_enabled=True),
                            [(0,"ACT",0),(2,"RD",0),(3,"ACT",1),(5,"RD",1),(28,"RD",0),
                             (30,"PRE",1),(32,"PRE",0),(34,"REF",None)], [(4,6),(7,9),(30,32)], 38)

    def test_refresh_final_tail_and_fixed_calendar(self):
        result = self.assertSchedule([(0,"READ",0,0),(28,"READ",0,0)], small(refresh_enabled=True),
                                     [(0,"ACT",0),(2,"RD",0),(28,"RD",0),(32,"PRE",0),(34,"REF",None)],
                                     [(4,6),(30,32)], 38)
        self.assertEqual(result["last_request_data_end_cycle"], 32)
        result = self.assertSchedule([(70,"READ",0,0)], small(refresh_enabled=True),
                                     [(30,"REF",None),(60,"REF",None),(70,"ACT",0),(72,"RD",0)], [(74,76)], 76)
        self.assertEqual([e["scheduled_cycle"] for e in result["events"] if e["event"]=="REFRESH_DUE"], [30,60])

    def test_due_exactly_at_last_data_end_independent_oracle(self):
        cfg = small(banks=1,queue_depth=1,t_rcd=1,t_rp=1,t_ras=2,t_rc=3,t_ccd=1,
                    read_latency=1,write_latency=1,burst_cycles=1,t_rtw=0,t_wtr=0,
                    refresh_enabled=True,t_refi=20,t_rfc=4)
        self.assertSchedule([(17,"READ",0,0)], cfg,
                            [(17,"ACT",0),(18,"RD",0),(20,"PRE",0),(21,"REF",None)], [(19,20)], 25)

    def test_empty_has_no_periodic_refresh(self):
        result = simulate([], small(refresh_enabled=True))
        self.assertEqual((result["finish_cycle"], result["refresh_count"], result["events"]), (0,0,[]))


class InvalidAndBoundedTests(unittest.TestCase):
    def test_invalid_configuration(self):
        for change in ({"banks":0},{"queue_depth":0},{"t_ras":10,"t_rc":6},
                       {"t_rrd":0},{"t_faw":0},{"read_latency":True},{"t_wr":-1},
                       {"refresh_enabled":1},{"max_events":0}):
            with self.subTest(change=change), self.assertRaises(ValueError): small(**change).validate()

    def test_refresh_saturation_rejected(self):
        cfg = small(refresh_enabled=True)
        with self.assertRaises(ValueError): replace(cfg,t_refi=cfg.refresh_progress_bound()).validate()
        with self.assertRaises(ValueError): replace(cfg,t_refi=cfg.t_rfc).validate()

    def test_invalid_request_fields(self):
        original = MemoryRequest("q",0,"READ",0,0)
        for change in ({"arrival_cycle":-1},{"arrival_cycle":True},{"bank":2},{"row":-1},
                       {"operation":"ACT"},{"byte_count":32},{"request_id":""},
                       {"byte_offset":-1},{"source_trace_cycle":-1},{"tensor":None}):
            with self.subTest(change=change), self.assertRaises(ValueError): simulate([replace(original,**change)],small())

    def test_duplicate_and_nonmonotonic_requests(self):
        with self.assertRaises(ValueError): simulate([MemoryRequest("same",0,"READ",0,0)]*2,small())
        with self.assertRaises(ValueError): simulate(requests([(2,"READ",0,0),(1,"READ",0,0)]),small())
        with self.assertRaises(ValueError): simulate(["not a request"],small())

    def test_infinite_iterable_is_bounded_before_list_materialization(self):
        def forever():
            i = 0
            while True:
                yield MemoryRequest(str(i),0,"READ",0,0); i += 1
        with self.assertRaises(ValueError): simulate(forever(),small(max_requests=3))

    def test_cycle_and_event_guards_terminate(self):
        with self.assertRaises(SimulationLimitError): simulate(requests([(0,"READ",0,0)]),small(max_cycles=3))
        with self.assertRaises(SimulationLimitError): simulate(requests([(0,"READ",0,0)]),small(max_events=2))


class EvidenceAndAdapterTests(unittest.TestCase):
    def fixture_path(self, name):
        assert TEST_DIR is not None
        return TEST_DIR / name

    def make_csv(self, name, rows, header="cycle,scenario,command,bank,row,tensor,byte_offset"):
        path = self.fixture_path(name)
        path.write_text(header+"\n"+"\n".join(rows)+"\n",encoding="utf-8")
        return path

    def test_adapter_preserves_order_bytes_and_reference_cycle(self):
        path = self.make_csv("adapter.csv",["0,A,ACT,0,4,W,0","2,A,READ,0,4,W,0",
                                             "4,A,WRITE,1,7,Y,64","8,A,PRE,0,4,W,0"])
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        groups, meta = load_legacy_csv(path,small(),arrival_gap=3)
        self.assertEqual((meta["source_rows"],meta["ignored_original_ACT_PRE_rows"],meta["input_memory_requests"]),(4,2,2))
        self.assertEqual(meta["scenario_bytes"],{"A":128})
        self.assertEqual([(r.operation,r.bank,r.row,r.arrival_cycle,r.source_trace_cycle,r.byte_offset) for r in groups["A"]],
                         [("READ",0,4,0,2,0),("WRITE",1,7,3,4,64)])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)
        trace, _ = load_legacy_csv(path,small(),arrival_mode="trace_cycles")
        self.assertEqual([r.arrival_cycle for r in trace["A"]],[2,4])

    def test_adapter_empty_and_invalid(self):
        path = self.make_csv("empty.csv",[])
        self.assertEqual(load_legacy_csv(path,small())[0],{})
        for i, rows in enumerate((["0,A,REF,0,0,W,0"],["0,A,READ,3,0,W,0"],["0,A,READ,0,0,W"],
                                  ["0,,READ,0,0,W,0"],["2,A,READ,0,0,W,0","1,A,READ,0,0,W,0"])):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                load_legacy_csv(self.make_csv(f"bad{i}.csv",rows),small(),arrival_mode="trace_cycles")
        with self.assertRaises(ValueError): load_legacy_csv(path,small(),arrival_gap=-1)
        with self.assertRaises(ValueError): load_legacy_csv(path,small(burst_bytes=128))
        with self.assertRaises(ValueError): load_legacy_csv(path,small(),arrival_mode="unknown")
        with self.assertRaises(ValueError): load_legacy_csv(self.make_csv("bad_header.csv",[],"wrong"),small())

    def test_raw_json_csv_roundtrip_and_no_overwrite(self):
        result = simulate(requests([(0,"READ",0,0),(0,"WRITE",1,1)]),small())
        directory = self.fixture_path("serialized")
        write_outputs(result,directory,"hand")
        self.assertEqual(json.loads((directory/"hand.json").read_text(encoding="utf-8")),result)
        with (directory/"hand.events.csv").open(encoding="utf-8",newline="") as handle:
            self.assertEqual([json.loads(r["details_json"]) for r in csv.DictReader(handle)],result["events"])
        with self.assertRaises(FileExistsError): write_outputs(result,directory,"hand")
        with self.assertRaises(ValueError): write_outputs(result,directory,"../unsafe")

    def test_replay_rejects_tampered_bank_and_missing_data(self):
        base = simulate(requests([(0,"READ",0,0),(0,"READ",1,0)]),small())
        for kind in ("ENQUEUE","DATA_START","DATA_END"):
            damaged = copy.deepcopy(base)
            next(e for e in damaged["events"] if e["event"]==kind)["bank"] = 1
            with self.subTest(kind=kind), self.assertRaises(AssertionError): check_invariants(damaged)
        damaged = copy.deepcopy(base)
        next(e for e in damaged["events"] if e.get("command")=="RD")["bank"] = 1
        with self.assertRaises(AssertionError): check_invariants(damaged)
        damaged = copy.deepcopy(base)
        damaged["events"] = [e for e in damaged["events"] if e["event"]!="DATA_START"]
        with self.assertRaises(AssertionError): check_invariants(damaged)

    def test_replay_rejects_tampered_summary_and_refresh_end(self):
        base = simulate(requests([(30,"READ",0,0)]),small(refresh_enabled=True))
        for field in ("finish_cycle","bytes_transferred","completed_requests","row_hits","max_fifo_occupancy"):
            damaged = copy.deepcopy(base); damaged[field] += 1
            with self.subTest(field=field), self.assertRaises(AssertionError): check_invariants(damaged)
        damaged = copy.deepcopy(base)
        damaged["events"] = [e for e in damaged["events"] if e["event"]!="REFRESH_END"]
        with self.assertRaises(AssertionError): check_invariants(damaged)

    def test_replay_rejects_global_act_timing_mutations(self):
        cfg = small(t_rcd=1,t_rp=1,t_ras=2,t_rc=3,t_ccd=1,read_latency=1,
                    burst_cycles=1,t_rrd=5,t_faw=10)
        damaged = simulate(requests([(0,"READ",0,0),(0,"READ",1,0)]),cfg)
        next(e for e in damaged["events"] if e.get("command")=="ACT" and e["bank"]==1)["cycle"] = 4
        with self.assertRaisesRegex(AssertionError,"tRRD"): check_invariants(damaged)
        cfg = replace(cfg,banks=5,queue_depth=5,t_rrd=1)
        damaged = simulate(requests([(0,"READ",i,0) for i in range(5)]),cfg)
        next(e for e in damaged["events"] if e.get("command")=="ACT" and e["bank"]==4)["cycle"] = 8
        ranks = {"DATA_END":0,"REFRESH_END":1,"REFRESH_DUE":2,"BACKPRESSURE_END":3,
                 "ENQUEUE":4,"BACKPRESSURE_START":5,"COMMAND":6,"DATA_START":7}
        damaged["events"].sort(key=lambda e:(e["cycle"],ranks[e["event"]]))
        with self.assertRaisesRegex(AssertionError,"tFAW"): check_invariants(damaged)

    def test_replay_rejects_duplicate_start_and_due(self):
        damaged = simulate(requests([(0,"READ",0,0)]),small())
        index = next(i for i,e in enumerate(damaged["events"]) if e["event"]=="DATA_START")
        damaged["events"].insert(index,copy.deepcopy(damaged["events"][index]))
        with self.assertRaises(AssertionError): check_invariants(damaged)
        damaged = simulate(requests([(30,"READ",0,0)]),small(refresh_enabled=True))
        index = next(i for i,e in enumerate(damaged["events"]) if e["event"]=="REFRESH_DUE")
        damaged["events"].insert(index,copy.deepcopy(damaged["events"][index]))
        with self.assertRaises(AssertionError): check_invariants(damaged)

    def test_small_seeded_regression_is_deterministic(self):
        generator = random.Random(20261005)
        for trial in range(16):
            arrival = 0; items = []
            for _ in range(12):
                arrival += generator.randrange(4)
                items.append((arrival,generator.choice(["READ","WRITE"]),generator.randrange(2),generator.randrange(3)))
            cfg = small(queue_depth=1+trial%3,refresh_enabled=bool(trial%2))
            result = simulate(requests(items),cfg)
            self.assertEqual(result,simulate(requests(items),cfg))
            self.assertEqual(result["completed_requests"],12)


class RecordedResult(unittest.TextTestResult):
    """원시 unittest log와 함께 실제 개별 case의 PASS/FAIL도 JSON으로 남긴다."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.records = []
    def addSuccess(self,test):
        super().addSuccess(test); self.records.append({"test":test.id(),"passed":True})
    def addFailure(self,test,err):
        super().addFailure(test,err); self.records.append({"test":test.id(),"passed":False,"kind":"failure"})
    def addError(self,test,err):
        super().addError(test,err); self.records.append({"test":test.id(),"passed":False,"kind":"error"})


def main():
    global TEST_DIR
    parser = argparse.ArgumentParser(description="독립 DRAM 손계산/입력/불변조건 회귀")
    parser.add_argument("--output-dir",type=Path)
    args = parser.parse_args()
    TEST_DIR = (args.output_dir or ROOT/"build"/"reports"/f"dram_event_simulator_actual_{uuid4().hex}"/"tests").resolve()
    TEST_DIR.mkdir(parents=True,exist_ok=False)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
    report = {"passed":result.wasSuccessful(),"test_count":result.testsRun,"tests":result.records,
              "hand_calculated_oracle":True,"random_scope":"16×12 small invariant/determinism cases only",
              "actual_rtl_vivado_sdf_executed":False,"physical_dram_measured":False}
    (TEST_DIR/"result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__": main()
