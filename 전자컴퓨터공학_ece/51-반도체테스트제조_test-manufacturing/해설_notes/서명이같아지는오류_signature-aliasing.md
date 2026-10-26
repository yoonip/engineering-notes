# 다른 출력이 같은 signature가 될 때: aliasing을 계산하기

[반도체 테스트 목차](../README.md) · [signature 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 긴 답안을 짧은 숫자로 요약하면

테스트 출력 수백만 비트를 모두 저장하는 대신 작은 signature register로 압축하면 저장·전송 비용이 줄어듭니다. 하지만 서로 다른 출력이 같은 signature로 압축될 수 있습니다. 정상 출력과 고장 출력이 같은 최종 값이 되는 aliasing입니다. signature가 같다는 사실만으로 원래 출력 전체가 같다고 결론내릴 수 없는 이유입니다.

[TI의 boundary-scan BIST 자료](https://www.ti.com/lit/pdf/scta043)는 signature 압축과 programmable polynomial tap을 설명합니다. [Verimag 저자들의 signature 효율 연구](https://www-verimag.imag.fr/~caspi/PAPIERS/ieeetc91.html)는 오류열 분포 가정·sequence 길이와 보장 범위의 관계를 설명합니다. 아래에서는 그 일반 문제를 작은 GF(2) 선형 map으로 직접 계산합니다.

### 생성 다항식과 비트 순서

width m=3, 생성다항식 $`g(x)=x^3+x+1`$을 씁니다. register 초기값은 0, 입력은 MSB-first, final XOR와 reflection은 없습니다. 매 bit b에서 feedback은 최상위 state bit XOR b입니다. register를 왼쪽으로 한 칸 밀어 3비트로 자르고, feedback=1이면 low polynomial 011을 XOR합니다.

이 규약에서 n비트 정수 메시지 M의 signature는 다음과 같습니다.

```math
S(M)=\mathrm{rem}_{g(x)}\left(M(x)x^m\right).
```

입력에 x^m을 곱한 augmented remainder라는 점이 중요합니다. CRC 이름이 같아도 bit order, initialization, augmentation, final XOR가 다르면 숫자가 달라집니다. 여기의 함수는 단일 입력 serial signature의 교육용 예이며 실제 병렬 MISR의 각 입력 tap 연결을 구현하지 않습니다.

### 선형성에서 검출 불가능한 오류까지

GF(2)에서는 덧셈이 XOR입니다. 초기값 0인 이 signature map은 선형이므로 다음이 성립합니다.

```math
S(M\oplus E)=S(M)\oplus S(E).
```

따라서 정상과 오류 출력의 signature가 같을 조건은 $`S(E)=0`$입니다. 모든 오류 패턴 중 kernel에 들어가는 오류가 검출되지 않습니다. map의 rank가 r이면 kernel 차원은 n−r이고 원소 수는 $`2^{n-r}`$입니다. 0 오류를 제외한 모든 n비트 오류가 같은 확률이라고 가정하면 다음을 얻습니다.

```math
P_{alias}=\frac{2^{n-r}-1}{2^n-1}.
```

full rank r=m이고 n이 충분히 크면 약 $`2^{-m}`$입니다. 이 근사는 모든 physical fault의 미검출 확률을 보장하는 식이 아닙니다. 실제 고장은 특정 bit·시간·관측 경로에 편중되어 균일 오류 가정을 만족하지 않을 수 있습니다. 극단적으로 가능한 오류가 kernel의 특정 원소 하나라면 그 오류는 항상 alias합니다.

### 8비트에서 전부 세어 보기

n=8, m=3의 위 polynomial에서 rank는 3입니다. 가능한 255개 nonzero error 중 31개가 zero signature를 만듭니다. 따라서 정확한 균일 오류 alias 비율은 31/255≈0.12157이고 근사 1/8과 약간 다릅니다. 256개의 메시지를 8개 signature로 보내는 map의 각 묶음 크기가 32임을 직접 세어 rank 조건도 확인할 수 있습니다.

```bash
python demo.py --case signature
python -m unittest -v test_models.HardwareModels.test_signature_independent_polynomial_division test_models.HardwareModels.test_signature_alias_count_linearity
```

한 구현은 register shift/XOR이고, 독립 oracle은 정수 비트 다항식의 긴 나눗셈입니다. 256개 입력 전부에서 일치하는지 확인하고, 255개 오류의 alias 개수를 셉니다. 여러 입력쌍에서 linearity도 확인합니다. 이것은 오류 공간의 전수검사이며 ATE에서 실제 결함을 넣어 fault coverage를 측정한 결과가 아닙니다.

### 테스트 설계에서 남는 조건

scan response의 X값을 어떻게 mask하는지, 여러 출력이 어떻게 MISR로 들어가는지, signature를 중간에 관찰하는지, polynomial·test length·seed가 무엇인지에 따라 결과가 달라집니다. X를 0으로 임의 치환하면 실제 검출성을 과장할 수 있습니다. fault coverage는 고장을 활성화·전파·관측하는 문제이며 signature compaction의 aliasing과 구분해야 합니다. 큰 register만 붙이는 것으로 모든 종류의 테스트 한계가 사라지지는 않습니다.

## English

### A short summary cannot preserve every long response

Signature compaction reduces storage and transfer of long test responses, but different responses can map to the same final register. Aliasing occurs when faulty and fault-free responses share that signature. Equality of signatures therefore does not prove equality of the complete responses.

[TI's boundary-scan BIST report](https://www.ti.com/lit/pdf/scta043) explains signature compaction and programmable polynomial taps. [The Verimag authors' study](https://www-verimag.imag.fr/~caspi/PAPIERS/ieeetc91.html) independently addresses error-distribution assumptions, sequence length and guarantees. The example derives a small linear-map result directly.

### Fixing the exact bit convention

Use width three, polynomial $`x^3+x+1`$, zero initialization, MSB-first input, no reflection and no final XOR. Each bit XORs the top register bit to form feedback; shift left, keep three bits and XOR low polynomial 011 when feedback is one. Under this convention the signature equals the polynomial remainder of M(x)x^m divided by g(x).

Augmentation by x^m matters. Different ordering, initialization or final transforms can change numerical results despite similar CRC labels. This is a serial single-input model, not an implementation of a particular parallel MISR tap network.

### Deriving the alias count

The zero-initialized map is linear over GF(2), so $`S(M\oplus E)=S(M)\oplus S(E)`$. Undetected errors are exactly the nonzero E in its kernel. A rank-r map from n bits has a kernel of size 2^(n−r). If all nonzero n-bit error patterns are equally likely, alias probability is $`(2^{n-r}-1)/(2^n-1)`$.

For full rank r=m and long inputs, this approaches 2^−m. It is not a universal miss probability for physical faults. Structured errors may have a very different distribution; an error confined to one nonzero kernel element aliases with certainty.

### Exhaustive executable example

For eight input bits and this three-bit signature, the map has rank three. Exactly 31 of 255 nonzero error patterns produce zero signature, giving 31/255≈0.12157 rather than exactly 1/8. Each of the eight signatures has 32 preimages, independently confirming full rank.

The commands above compare a shift/XOR implementation with an independent polynomial long-division oracle for all 256 inputs, count all nonzero aliases and check linearity on input pairs. This exhausts the mathematical error space; it is not measured ATE fault coverage.

### Physical test boundaries

X masking, parallel input taps, intermediate signatures, polynomial, length and seed all affect an actual compactor. Arbitrarily replacing X with zero can exaggerate observability. Fault activation, propagation and observation coverage must also be distinguished from compaction aliasing. Increasing signature width alone does not remove every test limitation.

## 출처 / Sources

- Texas Instruments, *SCTA043A Built-In Self-Test Using Boundary Scan*, 1996: signature register and programmable polynomial taps.
- Caspi, Priotrowski and Velazco, *An a priori approach to the evaluation of signature analysis efficiency*, IEEE TC 1991: distribution assumptions and guarantees. Links appear above.
