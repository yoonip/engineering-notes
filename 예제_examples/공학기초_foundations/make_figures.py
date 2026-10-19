"""검증 예제의 수치로 원본 도표를 생성한다. Matplotlib이 필요하다."""

from pathlib import Path
import math

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from cycler import cycler

from signals_ai.models import (adc_midrise, feedback_response, first_order_zoh,
                               roofline, sample_cosine)


DESTINATION = Path(__file__).parent / 'figures'


def save(name):
    plt.tight_layout()
    for extension in ('png', 'svg'):
        path = DESTINATION / f'{name}.{extension}'
        metadata = {'Date': None} if extension == 'svg' else None
        plt.savefig(path, dpi=200, metadata=metadata)
        if extension == 'svg':
            # 경로 좌표의 의미를 유지하며 줄 끝 공백과 생성 시각을 없앤다.
            normalized = '\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n'
            path.write_text(normalized, encoding='utf-8', newline='\n')
    plt.close()


def main():
    DESTINATION.mkdir(exist_ok=True)
    plt.rcParams.update({'figure.figsize': (8.4, 4.5), 'font.size': 10,
                         'font.family': ['Malgun Gothic', 'DejaVu Sans'],
                         'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.linewidth': 0.8, 'axes.grid': False,
                         'axes.titleweight': 'medium', 'axes.titlesize': 11,
                         'axes.titlepad': 14, 'legend.frameon': False,
                         'lines.linewidth': 1.5, 'xtick.direction': 'out',
                         'ytick.direction': 'out',
                         'axes.prop_cycle': cycler(color=['#315f78', '#986b3a', '#4b5055']),
                         'svg.hashsalt': 'engineering-foundations'})
    # 다른 연속 주파수가 같은 표본을 만든다는 사실을 그린다.
    times = [n / 100000 for n in range(1001)]
    fig, ax = plt.subplots()
    ax.plot([t * 1000 for t in times], [math.cos(2 * math.pi * 900 * t) for t in times],
            alpha=.75, linestyle='--', label='900 Hz 연속 신호 / Continuous')
    ax.plot([t * 1000 for t in times], [math.cos(2 * math.pi * 100 * t) for t in times],
            label='100 Hz 연속 신호 / Continuous', linewidth=1.5)
    ax.scatter(list(range(11)), sample_cosine(900, 1000, 11), color='#111827',
               s=18, label='1 kS/s 공통 표본 / Shared samples', zorder=5)
    ax.set(xlabel='시간 / Time (ms)', ylabel='정규화 진폭 / Normalized amplitude', title='주파수가 달라도 같은 표본을 얻을 수 있다\nDifferent signals can produce identical samples')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), ncol=3, fontsize=8)
    save('sampling_aliasing')

    # 코드 구간 중앙을 복원값으로 쓰는 모델과 오차 경계를 그린다.
    xs = [i / 1600 for i in range(1601)]
    ys = [adc_midrise(x, 3)[1] for x in xs]
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.1), sharex=True)
    axes[0].plot(xs, xs, '--', label='이상적인 항등 사상 / Identity')
    axes[0].step(xs, ys, where='post', label='3-bit mid-rise 복원 / Reconstruction')
    axes[0].set(ylabel='복원값 / Reconstructed value', title='양자화는 진폭을 유한한 값으로 대응시킨다\nQuantization maps amplitudes to finite values')
    axes[0].legend(fontsize=9)
    axes[1].plot(xs, [y-x for x, y in zip(xs, ys)], linewidth=1)
    axes[1].axhline(1/16, linestyle='--', color='#986b3a', label='반 스텝 경계 / Half-step bounds')
    axes[1].axhline(-1/16, linestyle='--', color='#986b3a')
    axes[1].set(xlabel='정규화 입력 / Normalized input', ylabel='오차 / Error')
    axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.28), fontsize=8)
    save('adc_quantization')

    a, b = first_order_zoh(1, .1)
    fig, ax = plt.subplots()
    for gain in (0.5, 2, 15):
        values = feedback_response(a, b, gain, 1, 80)
        ax.plot([i*.1 for i in range(81)], values,
                linestyle={0.5:'-',2:'--',15:'-.'}[gain],
                label=f'K={gain:g}, 극점 / pole={a-b*gain:.3f}')
    ax.axhline(1, color='#111827', linestyle=':', linewidth=1, label='목표값 / Reference')
    ax.set(xlabel='시간 / Time (s)', ylabel='정규화 출력 / Normalized output', title='안정한 이득에서도 과도 응답은 서로 다르다\nStable gains can produce different transient responses')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), ncol=2, fontsize=8)
    save('feedback_response')

    # 특정 GPU 사양이 아닌 가상의 장치로 상한의 모양을 그린다.
    intensities = [10 ** (-2 + 4*i/400) for i in range(401)]
    ceilings = [roofline(i, 1, 1e12, 1e11)['ceiling_flop_s']/1e9 for i in intensities]
    fig, ax = plt.subplots()
    ax.loglog(intensities, ceilings, linewidth=1.8, label='모델 상한 / Model ceiling')
    ax.loglog(intensities, [1e11*i/1e9 for i in intensities], '--', alpha=.7, label='100 GB/s 대역폭 / Bandwidth line')
    ax.axhline(1000, linestyle=':', color='#4b5055', label='1 TFLOP/s 연산 상한 / Compute ceiling')
    ax.scatter([.25], [25], color='#111827', s=22, zorder=5, label='계산 예제의 상한 / Example bound')
    ax.set(xlabel='연산 집약도 / Arithmetic intensity (FLOP/byte)', ylabel='처리량 상한 / Throughput ceiling (GFLOP/s)',
           title='가상 장치의 Roofline 상한 모델\nHypothetical Roofline model; no measured hardware data', ylim=(.7, 2000))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, position: f'{value:g}'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, position: f'{value:g}'))
    ax.legend(fontsize=9)
    save('roofline')


if __name__ == '__main__':
    main()
