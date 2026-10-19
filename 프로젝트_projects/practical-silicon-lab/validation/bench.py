#!/usr/bin/env python3
"""Local, deterministic bench model. No instrument or rail is controlled."""
import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def energy_j(samples):
    """Trapezoidal integral of synchronized V/I samples; t is seconds."""
    total = 0.0
    for left, right in zip(samples, samples[1:]):
        dt = right['time_s'] - left['time_s']
        if dt <= 0:
            raise ValueError('timestamps must be strictly increasing')
        p0 = left['voltage_v'] * left['current_a']
        p1 = right['voltage_v'] * right['current_a']
        total += 0.5 * (p0 + p1) * dt
    if len(samples) < 2 or not math.isfinite(total):
        raise ValueError('invalid capture')
    return total


class FakeBench:
    """A software model, including deliberately injected failure modes."""
    def __init__(self, fault):
        self.fault = fault
        self.output = False
        self.transcript = []

    def setup(self, voltage_v, frequency_mhz):
        # These are educational limits, not a specification for a real SoC.
        if not 0.75 <= voltage_v <= 0.85 or not 400 <= frequency_mhz <= 800:
            raise ValueError('outside the educational model envelope')
        self.voltage_v, self.frequency_mhz = voltage_v, frequency_mhz
        self.output = True
        self.transcript.append(f'MODEL setup V={voltage_v} F={frequency_mhz}')

    def capture(self):
        if self.fault == 'timeout':
            raise TimeoutError('simulated instrument communication timeout')
        if self.fault == 'malformed':
            raise ValueError('simulated instrument response is not numeric')
        # A deterministic synchronized 10 ms trace; no wall-clock timing claim.
        # The rectangular load is 2 A; voltage is nominal or a 120 mV droop.
        rail = self.voltage_v - (0.12 if self.fault == 'droop' else 0.0)
        return [{'time_s': k * 0.001, 'voltage_v': rail, 'current_a': 2.0}
                for k in range(11)]

    def run_workload(self):
        # Pretend two inferences completed within the capture interval.
        mismatches = 1 if self.fault == 'mismatch' else 0
        return {'completed_inferences': 2, 'mismatches': mismatches,
                'ecc_corrected_delta': 0, 'ecc_uncorrected_delta': 0}

    def close(self):
        self.output = False
        self.transcript.append('MODEL output disabled; session closed')


def run_case(out, fault):
    # Refuse overwrite: a failed run is evidence, not temporary clutter.
    out.mkdir(parents=True, exist_ok=False)
    config = {'simulation_only': True, 'serial': 'SIM-SOC-0001',
              'board_revision': 'MODEL-A', 'test_revision': 'bench-v2',
              'firmware': 'software-model-no-firmware',
              'voltage_command_v': 0.80, 'frequency_command_mhz': 600,
              'temperature_command_c': 25, 'fault': fault,
              'limits': {'voltage_min_v': 0.76, 'voltage_max_v': 0.84,
                         'energy_per_inference_max_j': 0.010,
                         'mismatches_max': 0, 'ecc_uncorrected_max': 0}}
    (out / 'config.json').write_text(json.dumps(config, indent=2), encoding='utf-8')
    bench = FakeBench(fault)
    started = time.monotonic()
    result = {'serial': config['serial'], 'status': 'INFRA_ERROR',
              'simulation_only': True, 'reasons': [], 'retry_of': None}
    try:
        bench.setup(config['voltage_command_v'], config['frequency_command_mhz'])
        trace = bench.capture()
        work = bench.run_workload()
        with (out / 'waveform.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(trace[0]))
            writer.writeheader()
            writer.writerows(trace)
        joules = energy_j(trace)
        count = work['completed_inferences']
        if count <= 0:
            raise ValueError('cannot divide by zero completed inferences')
        result.update(work, energy_j=joules, energy_per_inference_j=joules/count,
                      voltage_measured_min_v=min(p['voltage_v'] for p in trace),
                      voltage_measured_max_v=max(p['voltage_v'] for p in trace))
        limits = config['limits']
        if result['voltage_measured_min_v'] < limits['voltage_min_v']:
            result['reasons'].append('RAIL_UNDERVOLTAGE')
        if result['voltage_measured_max_v'] > limits['voltage_max_v']:
            result['reasons'].append('RAIL_OVERVOLTAGE')
        if result['energy_per_inference_j'] > limits['energy_per_inference_max_j']:
            result['reasons'].append('ENERGY_LIMIT')
        if work['mismatches'] > limits['mismatches_max']:
            result['reasons'].append('DATA_MISMATCH')
        if work['ecc_uncorrected_delta'] > limits['ecc_uncorrected_max']:
            result['reasons'].append('ECC_UNCORRECTED')
        result['status'] = 'FAIL' if result['reasons'] else 'PASS'
    except (TimeoutError, ValueError) as exc:
        # Transport/parser errors are not evidence of silicon failure.
        result['error_type'] = type(exc).__name__
        result['reasons'] = [str(exc)]
    finally:
        # Real power-off/reset policy must follow the board's sequencing contract.
        bench.close()
        result['model_output_disabled'] = not bench.output
        result['host_elapsed_s'] = time.monotonic() - started
        result['python'] = platform.python_version()
        (out / 'instrument.log').write_text('\n'.join(bench.transcript)+'\n', encoding='utf-8')
    (out / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    with (out / 'summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['serial', 'status', 'simulation_only'])
        writer.writeheader()
        writer.writerow({k: result[k] for k in writer.fieldnames})
    # Hash raw files and the exact source so a report can be reproduced later.
    manifest = {p.name: sha256(p) for p in sorted(out.iterdir()) if p.is_file()}
    manifest['source:bench.py'] = sha256(Path(__file__))
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return {'PASS': 0, 'FAIL': 1, 'INFRA_ERROR': 2}[result['status']]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fault', choices=['none','droop','mismatch','timeout','malformed'], default='none')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    sys.exit(run_case(args.out, args.fault))
