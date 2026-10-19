#!/usr/bin/env python3
"""Independent scalar reference versus a deliberately faulty DUT software model."""
import argparse
import hashlib
import json
from pathlib import Path


def reference(image, weights):
    # Valid cross-correlation: 3x3 input, 2x2 kernel -> 2x2 output.
    # Python integers avoid accidental INT8 accumulator wraparound.
    return [[sum(image[y+ky][x+kx] * weights[ky][kx]
                 for ky in range(2) for kx in range(2))
             for x in range(2)] for y in range(2)]


def device_model(image, weights, fault):
    # A separate flat-buffer indexing path: reference does not call this code.
    memory = [item for row in image for item in row]
    if fault == 'stale':
        memory[4] -= 1  # Device sees an old centre value, although host hash is stable.
    output = []
    for y in range(2):
        row = []
        for x in range(2):
            accumulator = 0
            for ky in range(2):
                for kx in range(2):
                    # Normal row-major address = row * row_stride + column.
                    index = (y+ky)*3 + (x+kx)
                    if fault == 'layout':
                        index = (x+kx)*3 + (y+ky)  # Wrong interpretation: transposed.
                    accumulator += memory[index] * weights[ky][kx]
            if fault == 'overflow':
                # Defined mathematical INT8 wrap, not undefined C signed overflow.
                accumulator = (accumulator + 128) % 256 - 128
            row.append(accumulator)
        output.append(row)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fault', choices=['none','layout','stale','overflow'], default='none')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    contract = {'simulation_only': True, 'image': [[20,-3,4],[5,6,-7],[8,9,10]],
                'weights': [[7,-2],[3,4]], 'operation': 'cross_correlation',
                'layout': 'HW_row_major', 'stride': 1, 'padding': 'valid',
                'input_type': 'signed_int8', 'accumulator_type': 'signed_int32'}
    payload = json.dumps(contract, sort_keys=True).encode()
    (args.out/'input.json').write_bytes(payload)
    expected = reference(contract['image'], contract['weights'])
    actual = device_model(contract['image'], contract['weights'], args.fault)
    errors = [{'y': y, 'x': x, 'expected': expected[y][x], 'actual': actual[y][x]}
              for y in range(2) for x in range(2) if actual[y][x] != expected[y][x]]
    result = {'status': 'FAIL' if errors else 'PASS', 'simulation_only': True,
              'input_sha256': hashlib.sha256(payload).hexdigest(),
              'fault': args.fault, 'expected': expected, 'actual': actual, 'errors': errors}
    (args.out/'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(errors))
