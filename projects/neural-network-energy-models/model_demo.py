"""Run numerical energy models without the private source workbooks."""
import argparse
from dataclasses import replace
import json
from pathlib import Path

from energy_analysis import Transformer, BATCHES, decode_energy, paper_sweep, write_csv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('results'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    models = [
        Transformer('tiny', 10, 3, 2, 1, 1, 2, max_positions=3),
        Transformer('GPT175_formula', 50257, 128, 12288, 96, 96, 128),
    ]
    decode = [decode_energy(replace(model, batch=batch))
              for model in models for batch in BATCHES]
    normalized = paper_sweep()
    write_csv(args.out / 'decode_scenarios.csv', decode)
    write_csv(args.out / 'normalized_energy.csv', normalized)
    summary = {
        'kind': 'analytical_model',
        'decode_scenarios': len(decode),
        'normalized_scenarios': len(normalized),
        'measured_power': False,
        'input_workbooks_used': False,
    }
    (args.out / 'summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
