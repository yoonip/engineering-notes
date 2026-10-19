# 작은 수식 언어 만들기: 우선순위에서 stack bytecode까지

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 문자열을 바로 실행하지 않고 의미를 만든다

`2+3*4`를 왼쪽부터 계산하면 20이지만 곱셈 우선순위를 적용하면 14다. 문자 목록만으로는 연산 구조가 정해지지 않는다. parser는 문법과 우선순위에 따라 그 구조를 결정한다. compiler 입문에서 작은 수식 언어를 만드는 이유는 토큰·구조·실행 단계를 작은 입력으로 연결해 볼 수 있기 때문이다.

예제 언어는 10진 음이 아닌 정수 literal, 괄호, 단항 minus, 이항 `+ - *`만 허용한다. 변수, 함수 호출, 나눗셈과 거듭제곱은 없다. 공백은 토큰 사이에서 무시한다. 허용 문법을 작게 정하면 입력 오류와 실행 의미를 정확하게 검사하기 쉽다. Python의 `eval()`에 이 문자열을 넘기지 않는다.

### binding power로 괄호 없는 구조를 읽는다

tokenizer가 `2`, `+`, `3`, `*`, `4`를 구분한 뒤 parser가 `expression(minimum)`을 호출한다. 먼저 literal·단항 minus·괄호 안 수식 중 하나를 읽는다. 이어지는 이항 연산자의 우선순위가 minimum 이상이면 그 연산자를 소비하고 오른쪽 부분을 더 높은 minimum으로 읽는다. `+ -`는 10, `*`는 20, 단항 minus는 30을 사용한다.

같은 우선순위의 이항 연산을 왼쪽 결합으로 만들기 위해 오른쪽 호출의 minimum을 현재 우선순위+1로 둔다. 따라서 `10-3-2`는 `(10-3)-2`이고, `2+3*4`의 오른쪽에서는 *가 먼저 묶인다. LLVM tutorial은 operator-precedence parsing과 AST를 설명한다. 여기서는 그 원리를 binding-power 방식으로 구현하고 AST를 저장하는 대신 stack code를 바로 만든다. [LLVM parser tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html)

### 후위 순서가 stack 연산이 된다

literal은 `PUSH n`, 단항 minus는 operand code 뒤 `NEG`, binary operator는 왼쪽 code·오른쪽 code·연산 instruction 순으로 출력한다. `2+3*4`는 `PUSH 2, PUSH 3, PUSH 4, MUL, ADD`가 된다. MUL은 오른쪽 4와 왼쪽 3을 꺼내 12를 넣고 ADD가 2와 12를 합친다. SUB에서 pop 순서를 뒤집으면 답이 바뀌므로 right를 먼저 꺼내고 left-right를 계산한다.

stack 높이는 PUSH에서 +1, NEG에서 0, binary operation에서 -1 변한다. NEG 전에는 최소 한 값, 이항 전에는 최소 두 값이 있어야 한다. 완성된 수식은 마지막에 정확히 한 값을 남겨야 한다. 이 조건으로 잘못된 bytecode의 underflow나 남은 operand를 검출한다. Python AST 문서는 syntax tree가 source 구조를 표현하는 별도 단계임을 보여 주며, 테스트에서는 이를 독립적인 구조 해석 경로로 사용한다. [Python ast](https://docs.python.org/3/library/ast.html)

### 입력 크기와 실행 범위를 제한한다

`compile_expression()`는 source 512문자, 재귀 깊이 64를 상한으로 둔다. 알 수 없는 token, 남은 token, 닫히지 않은 괄호를 거부한다. 전체 토큰 수 T에 대한 tokenization·parsing·instruction 생성은 이 문법에서 선형 작업을 한다. 정수는 Python 임의 정밀도이므로 산술 instruction의 비용까지 항상 O(1)이라고 세면 안 된다. 큰 정수 곱셈은 operand의 bit 수에 따라 달라진다.

이 VM은 instruction tuple을 해석하는 작은 계산기이며 실제 CPU instruction이나 ELF를 생성하지 않는다. 허용 operation을 좁혔다고 범용 sandbox가 완성된 것도 아니다. 입력 경계와 자원 한도는 서비스를 붙일 때에도 그대로 유지해야 한다.

### 서로 다른 parser로 결과를 비교한다

테스트는 생성한 500개 수식을 이 parser로 compile·실행한 결과와 Python `ast.parse()`가 만든 tree를 허용 node만 순회해 계산한 결과를 비교한다. 이 참조는 eval을 사용하지 않으며 `Constant`, unary minus와 세 이항 연산만 인정한다. 별도 고정 예시는 우선순위, 왼쪽 결합, 괄호, 음수 곱셈을 확인한다. 빈 입력·함수 호출·지원하지 않는 나눗셈·끊긴 수식과 invalid bytecode도 거부한다. demo는 source, bytecode와 최종 값 1을 보여 준다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" parser
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Build meaning before executing text

Evaluating `2+3*4` strictly left to right gives 20; multiplication precedence gives 14. Tokens alone do not determine structure. A parser applies grammar and binding rules. A small expression language makes tokenization, structure, and execution visible on short examples.

This language accepts nonnegative decimal integer literals, parentheses, unary minus, and binary `+ - *`. It has no variables, calls, division, or exponentiation. Whitespace between tokens is ignored. The input is never passed to Python `eval()`.

### Parse binding power

After tokenization, `expression(minimum)` first reads a literal, unary minus, or parenthesized expression. It then consumes binary operators whose precedence meets the minimum, recursively parsing the right operand at a higher minimum. Addition/subtraction use 10, multiplication 20, and unary minus 30.

Parsing the right operand with current precedence+1 makes equal-precedence binary operators left-associative. Thus `10-3-2` means `(10-3)-2`, while multiplication binds inside the right side of `2+3*4`. LLVM explains operator-precedence parsing and ASTs. This implementation uses binding powers and emits stack code directly rather than retaining an AST. [LLVM parser tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html)

### Postorder becomes stack execution

Literals emit `PUSH n`; unary minus emits operand code then `NEG`; a binary expression emits left code, right code, then its instruction. `2+3*4` becomes `PUSH 2, PUSH 3, PUSH 4, MUL, ADD`. MUL replaces 3 and 4 with 12, then ADD combines 2 and 12. SUB must pop right before left and compute left-right.

PUSH increases stack height by one, NEG preserves it, and binary operations reduce it by one. NEG requires one value, binary operations two, and a complete expression must finish with exactly one. These rules detect underflow and leftover operands. Python AST provides a separate representation of source structure and an independent interpretation path for tests. [Python ast](https://docs.python.org/3/library/ast.html)

### Bound the input and execution model

Source length is capped at 512 characters and recursive depth at 64. Unknown tokens, trailing tokens, and unmatched parentheses are errors. Tokenization, parsing, and instruction generation perform linear work in token count T for this grammar. Python integers have arbitrary precision, so arithmetic instruction cost is not universally constant: multiplication depends on operand bit lengths.

The VM interprets instruction tuples; it emits neither CPU instructions nor ELF. Restricting operations does not establish a general-purpose sandbox. Input and resource limits remain necessary when integrating the calculator into a service.

### Compare different parsers

Tests generate 500 expressions and compare compiled execution against a restricted evaluator over Python `ast.parse()` trees. The reference uses no eval and accepts only integer constants, unary minus, and the three binary operators. Fixed tests exercise precedence, left association, parentheses, and multiplication by a negative value. Empty input, calls, division, incomplete expressions, and invalid bytecode are rejected. The demo prints source, bytecode, and final value one.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" parser
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [LLVM: Parser and AST](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html): operator precedence·구조 표현 / precedence and structure
- [Python: ast](https://docs.python.org/3/library/ast.html): 독립 syntax tree 참조 / independent syntax-tree reference
