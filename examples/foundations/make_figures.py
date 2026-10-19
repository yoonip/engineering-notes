"""검증 예제의 수치로 원본 도표를 생성한다. Matplotlib이 필요하다."""

from pathlib import Path
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from signals_ai.models import (adc_midrise, feedback_response, first_order_zoh,
                               roofline, sample_cosine)


DESTINATION = Path(__file__).parent / 'figures'


def save(name):
    plt.tight_layout()
    for extension in ('png', 'svg'):
        path = DESTINATION / f'{name}.{extension}'
        metadata = {'Date': None} if extension == 'svg' else None
        plt.savefig(path, dpi=160, metadata=metadata)
        if extension == 'svg':
            # 경로 좌표의 의미를 유지하며 줄 끝 공백과 생성 시각을 없앤다.
            normalized = '\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n'
            path.write_text(normalized, encoding='utf-8', newline='\n')
    plt.close()


def main():
    DESTINATION.mkdir(exist_ok=True)
    plt.rcParams.update({'figure.figsize': (8.4, 4.5), 'font.size': 11,
                         'axes.grid': True, 'grid.alpha': 0.25,
                         'svg.hashsalt': 'engineering-foundations'})
    # 다른 연속 주파수가 같은 표본을 만든다는 사실을 그린다.
    times = [n / 100000 for n in range(1001)]
    fig, ax = plt.subplots()
    ax.plot([t * 1000 for t in times], [math.cos(2 * math.pi * 900 * t) for t in times],
            alpha=.65, label='900 Hz continuous')
    ax.plot([t * 1000 for t in times], [math.cos(2 * math.pi * 100 * t) for t in times],
            label='100 Hz continuous', linewidth=2)
    ax.scatter(list(range(11)), sample_cosine(900, 1000, 11), color='#111827',
               label='Shared samples at 1 kS/s', zorder=5)
    ax.set(xlabel='Time (ms)', ylabel='Normalized amplitude', title='Different signals, identical samples')
    ax.legend(loc='lower right', fontsize=9)
    save('sampling_aliasing')

    # 코드 구간 중앙을 복원값으로 쓰는 모델과 오차 경계를 그린다.
    xs = [i / 1600 for i in range(1601)]
    ys = [adc_midrise(x, 3)[1] for x in xs]
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.5), sharex=True)
    axes[0].plot(xs, xs, '--', label='Ideal identity')
    axes[0].plot(xs, ys, label='3-bit mid-rise reconstruction')
    axes[0].set(ylabel='Reconstructed value', title='Quantization is an amplitude mapping')
    axes[0].legend(fontsize=9)
    axes[1].plot(xs, [y-x for x, y in zip(xs, ys)], linewidth=1)
    axes[1].axhline(1/16, linestyle='--', color='#dc2626', label='Half-step bounds')
    axes[1].axhline(-1/16, linestyle='--', color='#dc2626')
    axes[1].set(xlabel='Input (normalized)', ylabel='Error')
    axes[1].legend(fontsize=9)
    save('adc_quantization')

    a, b = first_order_zoh(1, .1)
    fig, ax = plt.subplots()
    for gain in (0.5, 2, 15):
        values = feedback_response(a, b, gain, 1, 80)
        ax.plot([i*.1 for i in range(81)], values,
                label=f'K={gain:g}, pole={a-b*gain:.3f}')
    ax.axhline(1, color='#111827', linestyle='--', label='Reference')
    ax.set(xlabel='Time (s)', ylabel='Normalized output', title='Stable gain choices can have different responses')
    ax.legend(fontsize=9)
    save('feedback_response')

    # 특정 GPU 사양이 아닌 가상의 장치로 상한의 모양을 그린다.
    intensities = [10 ** (-2 + 4*i/400) for i in range(401)]
    ceilings = [roofline(i, 1, 1e12, 1e11)['ceiling_flop_s']/1e9 for i in intensities]
    fig, ax = plt.subplots()
    ax.loglog(intensities, ceilings, linewidth=2, label='Model ceiling')
    ax.loglog(intensities, [1e11*i/1e9 for i in intensities], '--', alpha=.7, label='100 GB/s bandwidth line')
    ax.axhline(1000, linestyle=':', color='#dc2626', label='1 TFLOP/s compute ceiling')
    ax.scatter([.25], [25], color='#111827', zorder=5, label='Worked example (upper bound)')
    ax.set(xlabel='Arithmetic intensity (FLOP/byte)', ylabel='Throughput ceiling (GFLOP/s)',
           title='Hypothetical Roofline model — not a hardware benchmark', ylim=(.7, 2000))
    ax.legend(fontsize=9)
    save('roofline')


if __name__ == '__main__':
    main()
