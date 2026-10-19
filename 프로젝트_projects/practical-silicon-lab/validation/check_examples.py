#!/usr/bin/env python3
"""Meaningful executable checks for expected success and injected failure paths."""
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import bench
import training_ber


def main():
    source = Path(__file__).parent
    with tempfile.TemporaryDirectory(prefix='validation-check-') as temp:
        for fault, wanted in [('none',0),('droop',1),('mismatch',1),('timeout',2),('malformed',2)]:
            out = Path(temp) / fault
            run = subprocess.run([sys.executable, str(source/'bench.py'), '--fault', fault,
                                  '--out', str(out)], capture_output=True, text=True)
            assert run.returncode == wanted, (fault, run.stderr, run.stdout)
            result = json.loads((out/'result.json').read_text())
            assert result['model_output_disabled'] is True
            manifest = json.loads((out/'manifest.json').read_text())
            for name, wanted_hash in manifest.items():
                file = source/'bench.py' if name.startswith('source:') else out/name
                assert bench.sha256(file) == wanted_hash
            if fault == 'none':
                assert math.isclose(result['energy_j'],0.016, rel_tol=1e-12)
                assert math.isclose(result['energy_per_inference_j'],0.008, rel_tol=1e-12)
            if fault == 'droop':
                assert result['reasons'] == ['RAIL_UNDERVOLTAGE']
        assert training_ber.longest_window([1,2,3,9,10])['chosen_tap'] == 2
        assert training_ber.longest_window([])['pass'] is False
        assert training_ber.longest_window(range(20,25))['margin_steps'] == 2
        assert 9.98e-13 < training_ber.zero_error_upper(3e12) < 1e-12
    print('PASS: 5 harness outcomes, cleanup, hashes, energy, training and BER')


if __name__ == '__main__':
    main()
