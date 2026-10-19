# 비트에서 수까지: 정수, 부동소수점, 고정소수점

[상위 주제](../README.md) · [실행 모델](../../../예제_examples/공학기초_foundations/systems/systems_models.py) · [검증 코드](../../../예제_examples/공학기초_foundations/systems/test_systems_models.py)

## 한국어

### 같은 비트도 약속에 따라 다른 수가 된다

8개의 전구를 켜고 끈다고 생각해 보자. 가능한 상태는 $`2^8=256`$개다. 이 상태를 0부터 255까지로 읽을 수도 있고, 음수를 포함하도록 나눠 읽을 수도 있다. 비트 자체에 소수점이나 부호가 붙어 있는 것은 아니다. 데이터 형식이 그 뜻을 정한다. 이 약속을 정확히 알아야 센서 값, 영상 픽셀, 신경망 가중치, 하드웨어 연산 결과를 서로 비교할 수 있다.

여기서는 $`W`$를 전체 비트 수, $`F`$를 소수 비트 수로 쓴다. 모든 식은 단위 없는 수의 표현을 설명한다. 전압처럼 단위가 있는 값이라면 별도로 V/code 같은 변환 계수를 기록해야 한다.

| 형식 | 이 글에서의 해석 | 주의할 점 |
| --- | --- | --- |
| unsigned 정수 | $`0\le u\le 2^W-1`$ | C의 연산에서는 정수 승격 후 실제 연산 타입도 확인한다 |
| 2의 보수 signed 정수 | $`-2^{W-1}\le q\le2^{W-1}-1`$ | C signed overflow를 자동 순환으로 가정하지 않는다 |
| 고정소수점 | $`x=q2^{-F}`$ | 스케일, 반올림, 포화 규칙을 함께 정한다 |
| binary32 부동소수점 | 부호·지수·유효숫자로 표현 | 모든 실수와 모든 큰 정수를 정확히 담지는 못한다 |

### 정수의 범위와 C의 규칙

2의 보수 비트열에서 최상위 비트의 가중치를 음수로 두면

$$q=-b_{W-1}2^{W-1}+\sum_{i=0}^{W-2}b_i2^i.$$

따라서 8비트 `11111111`은 unsigned로 255, 이 해석의 signed로 -1이다. 반면 C의 `int`가 언제나 32비트인 것은 아니다. `CHAR_BIT`, `sizeof`, `<limits.h>`와 구현 문서를 확인한다. `int32_t` 같은 정확한 폭의 타입도 해당 구현이 제공하는지 확인한다. 이 글의 비트 모델과 C 언어 전체의 타입 규칙을 구분해야 한다. [WG14 C11 초안 N1570, §5.2.4.2.1·§6.2.6.2·§7.20](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)

C에서 일반적인 signed 덧셈의 결과가 타입 범위를 벗어나면 undefined behavior다. 하드웨어가 2의 보수여도 언어 차원에서 결과가 보장되는 것은 아니다. 곱셈은 피연산자를 넓은 타입으로 바꾼 뒤 계산하고, 최종 저장 범위를 확인한다. `wide = a * b`처럼 대입 대상만 넓히면 곱셈 자체는 좁은 타입에서 먼저 일어날 수 있다. [CMU SEI CERT INT32-C](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/)

### 소수점을 고정하면 무엇이 달라질까

$`W=8,F=6`$이면 한 칸의 간격은 $`\Delta=2^{-6}=1/64`$이고 표현 범위는 $`[-2,127/64]`$다. 값 $`x`$를 저장하는 코드를

$$q=\mathrm{clip}\bigl(\mathrm{round}_{\mathrm{ties\ to\ even}}(x2^F),-2^{W-1},2^{W-1}-1\bigr)$$

로 정하자. 가장 가까운 값으로 반올림하고, 정확히 중간이면 짝수 코드를 고른다. 범위를 넘으면 양 끝 값에 붙이는 것이 포화다. 포화가 일어나지 않는 구간에서는 $`\vert q2^{-F}-x\vert \le\Delta/2`$다. 범위 밖에서는 이 오차 한계가 성립하지 않는다. 소수 비트를 늘리면 간격은 줄어들지만 같은 전체 폭에서 정수 범위도 줄어든다.

두 코드의 곱은 $`x_ax_b=(q_aq_b)2^{-2F}`$이므로 원래 스케일의 출력 코드는 $`q_aq_b/2^F`$를 반올림한 값이다. 중간 곱을 충분히 넓게 보관하고 마지막에 한 번 반올림·포화한다. 음수의 오른쪽 시프트가 원하는 반올림과 같다고 가정하면 안 된다. Python 모델은 `Fraction`으로 정확한 유리수 연산을 하여 이 규칙 자체를 확인한다. 실제 MCU·RTL에서는 중간 비트 폭과 연산 비용을 따로 정한다.

### 부동소수점은 소수점이 이동한다

IEEE binary32의 정상수는 $`(-1)^s(1+f/2^{23})2^{e-127}`$이다. 부호 1비트, 지수 8비트, 저장된 소수부 23비트를 쓰며, 0·비정상수·무한대·NaN은 별도의 해석이 있다. [Oracle Numerical Computation Guide, IEEE Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_math.html)

이 식으로부터 $`[2^{24},2^{25})`$ 구간의 binary32 간격은 2임을 알 수 있다. 그래서 $`2^{24}+1`$은 정확히 담기지 않지만 $`2^{24}+2`$는 담긴다. `0.1`도 이진수로 유한하게 끝나지 않는다. 반올림 오차를 비교할 때는 문제의 크기와 단위를 반영한 절대·상대 허용오차를 정하고, NaN은 별도로 다룬다. “실수는 항상 소수 몇 자리까지 정확하다”는 설명은 맞지 않는다.

### 구현과 검증

`quantize()`는 정확한 스케일링, 짝수 쪽 반올림, 포화를 순서대로 수행한다. `fixed_multiply()`는 넓은 Python 정수로 중간 곱을 보관한다. 이 구현의 목적은 수치 규칙의 기준 모델이며 MCU 실행 시간을 예측하는 것은 아니다.

검증은 8비트 전체 256개 패턴을 `int.from_bytes(..., signed=True)`와 비교하고, 2,049개 입력에서 비포화 양자화 오차 한계를 확인한다. 5비트 곱셈 1,024개 조합은 인접 정수까지의 거리를 직접 비교하는 독립 규칙으로 검사한다. 중간값 반올림, 양·음 포화, 잘못된 형식, binary32 간격도 포함한다. 테스트 실행법은 [예제 안내](../../../예제_examples/공학기초_foundations/systems/README.md)에 있다.

## English

### Bits become numbers through an agreed interpretation

Imagine eight lamps, each either on or off. They have $`2^8=256`$ possible states. We can label those states from 0 to 255, or reserve some labels for negative numbers. A bit pattern has no inherent sign or decimal point: its format supplies the meaning. This agreement connects sensor readings, image pixels, neural-network weights, and hardware arithmetic.

Here $`W`$ is total width and $`F`$ is fractional width. The equations describe dimensionless representations. Physical measurements also need a conversion factor such as V/code.

| Format | Interpretation used here | Important condition |
| --- | --- | --- |
| Unsigned integer | $`0\le u\le2^W-1`$ | Check integer promotions and the actual C operation type |
| Two's-complement signed integer | $`-2^{W-1}\le q\le2^{W-1}-1`$ | Do not assume ordinary C signed overflow wraps |
| Fixed point | $`x=q2^{-F}`$ | Specify scale, rounding, and saturation together |
| Binary32 floating point | Sign, exponent, and significand | Not every real number or large integer is exact |

### Integer range and language rules

Giving the top bit a negative weight produces

$$q=-b_{W-1}2^{W-1}+\sum_{i=0}^{W-2}b_i2^i.$$

Thus `11111111` means 255 as an unsigned byte or -1 under this signed interpretation. C does not require `int` to be 32 bits. Check `CHAR_BIT`, `sizeof`, `<limits.h>`, implementation documentation, and availability of exact-width types such as `int32_t`. This bit-level model does not replace the language's complete type rules. [WG14 N1570, §5.2.4.2.1, §6.2.6.2, §7.20](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)

Ordinary signed C addition outside the result type's range has undefined behavior. Two's-complement hardware does not by itself guarantee a language-level result. Widen operands before multiplication and check the final destination range. Merely writing `wide = a * b` can leave the multiplication in the narrower operand type. [CMU SEI CERT INT32-C](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/integers-int/int32-c/)

### Fixing the binary point

With $`W=8,F=6`$, spacing is $`\Delta=2^{-6}=1/64`$ and range is $`[-2,127/64]`$. Define encoding by

$$q=\mathrm{clip}\bigl(\mathrm{round}_{\mathrm{ties\ to\ even}}(x2^F),-2^{W-1},2^{W-1}-1\bigr).$$

Round to the nearest code, choose the even code at a tie, and clamp out-of-range results to an endpoint. Without saturation, $`\vert q2^{-F}-x\vert \le\Delta/2`$. This bound does not hold outside the representable range. More fractional bits improve spacing while reducing integer range at fixed total width.

Since $`x_ax_b=(q_aq_b)2^{-2F}`$, returning to the original scale requires rounding $`q_aq_b/2^F`$. Preserve the intermediate product in sufficient width and round and saturate once at the end. A right shift of a negative value is not automatically the desired rounding rule. The Python model uses exact `Fraction` arithmetic to check the specification. MCU and RTL implementations require separate decisions about intermediate width and operation cost.

### A moving binary point

A normal IEEE binary32 value is $`(-1)^s(1+f/2^{23})2^{e-127}`$, with one sign bit, eight exponent bits, and 23 stored fraction bits. Zero, subnormal values, infinities, and NaNs have special encodings. [Oracle Numerical Computation Guide](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_math.html)

The formula gives a spacing of 2 in $`[2^{24},2^{25})`$. Consequently $`2^{24}+1`$ is not exact, whereas $`2^{24}+2`$ is. Decimal `0.1` has no finite binary expansion either. Choose absolute and relative tolerances from the problem's scale and units, and handle NaN separately. A fixed number of accurate decimal places is not a general floating-point guarantee.

### Implementation and verification

`quantize()` performs exact scaling, ties-to-even rounding, and saturation. `fixed_multiply()` preserves its intermediate product using Python integers. These functions specify numerical behavior; they do not predict MCU timing.

Tests compare all 256 eight-bit words with `int.from_bytes(..., signed=True)`, check the nonsaturating error bound for 2,049 inputs, and compare 1,024 five-bit multiplication pairs against an independent nearest-integer distance rule. They also cover ties, positive and negative saturation, invalid formats, and binary32 spacing. Commands are in the [example guide](../../../예제_examples/공학기초_foundations/systems/README.md).

## 출처와 교차 확인 / Sources and cross-check

- WG14 N1570: C 타입·정수 범위·승격의 기준 / language-level types, ranges, and promotions.
- CMU SEI INT32-C: signed overflow 위험과 피연산자 확장 조건 / overflow hazards and operand widening.
- Oracle IEEE Arithmetic: binary32 구조 / binary32 representation.
- 위 고정소수점 규칙과 오차식은 이 글에서 정의하고 유도했으며, 정확한 유리수 모델과 독립적인 거리 비교로 확인했다. / The fixed-point policy and error bound are defined and derived here, then checked with exact rational arithmetic and an independent distance oracle.
