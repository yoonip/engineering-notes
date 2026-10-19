# 컴파일러·언어·런타임 | Compilers, Languages & Runtimes

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

컴파일러는 프로그램의 의미를 유지하면서 다른 표현으로 변환합니다. 보통 구문 분석, 의미 분석, 중간 표현 생성, 최적화, 대상 코드 생성 순서로 진행합니다.

## AST에서 machine code로

AST는 소스의 문법 구조를, IR은 분석과 변환에 적합한 표현을 담습니다. 최적화는 불필요한 계산 제거·상수 전파·벡터화 등으로 구성됩니다. CPU·GPU의 명령어와 메모리 구조가 다르면 같은 IR도 다른 코드를 생성합니다. Undefined behavior가 있으면 소스에서 예상한 동작과 최적화된 결과가 달라질 수 있습니다.

## 도구와 실행 방식

Clang은 C 계열 언어의 frontend, LLVM은 IR과 최적화·코드 생성 생태계, MLIR은 여러 추상화 수준의 표현을 다루는 기반입니다. GCC도 여러 언어와 대상 아키텍처를 지원하는 컴파일러 모음입니다. Interpreter·JIT·AOT는 실행 시점과 변환 방식이 다르며 실제 runtime은 이들을 조합하기도 합니다.

JVM·CPython·Julia runtime은 객체·메모리·실행 모델을 제공합니다. FFI에서는 ABI, 자료형 크기, 호출 규약, 객체 수명이 언어가 달라도 일치해야 합니다. EDA의 Tcl·SKILL 스크립트도 tool runtime과 API에 의존합니다.

## 관련 기술

LLVM, MLIR, GCC, Clang, Rust, Go, Java/JVM, CPython, Julia, Tcl, SKILL

## 참고 자료

- [LLVM documentation](https://llvm.org/docs/)
- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [C 코드가 실행되기까지: 컴파일, 링크, 리셋과 main](해설_notes/C코드가실행되기까지_reset-to-main-and-toolchain.md)

## English

### Compilers, languages, and runtimes

A compiler translates a program into another representation while preserving its meaning. A typical pipeline includes parsing, semantic analysis, intermediate-representation generation, optimization, and target-code generation.

### From an AST to machine code

An abstract syntax tree represents source syntax. An intermediate representation supports analysis and transformation. Optimizations include eliminating redundant work, propagating constants, and vectorization. Differences in CPU and GPU instructions and memory structures lead to different code from the same IR. Undefined behavior can also cause optimized code to behave differently from what a source-level reading suggests.

### Tools and execution models

Clang is a frontend for C-family languages. LLVM provides IR, optimization, and code-generation infrastructure, while MLIR supports representations at multiple abstraction levels. GCC supports many languages and target architectures. Interpreters, JIT compilation, and AOT compilation differ in when and how translation takes place; runtimes can combine them.

The JVM, CPython, and Julia runtimes provide object, memory, and execution models. At an FFI boundary, the ABI, type sizes, calling conventions, and object lifetimes must agree across languages. Tcl and SKILL scripts in EDA also depend on their tools' runtimes and APIs.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [From reset to main: ABI, ELF and linking](해설_notes/C코드가실행되기까지_reset-to-main-and-toolchain.md#english)


## 심화 해설 | Advanced article

- [작은 수식 언어 만들기: 우선순위에서 stack bytecode까지](해설_notes/수식에서바이트코드_expression-bytecode.md) · [English](해설_notes/수식에서바이트코드_expression-bytecode.md#english)
