# Compilers · Languages · Runtimes

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

컴파일러는 프로그램의 의미를 유지하면서 다른 표현으로 변환한다. 보통 구문 분석, 의미 분석, 중간 표현 생성, 최적화, 대상 코드 생성 순서로 진행한다.

## AST에서 machine code로

AST는 소스의 문법 구조를, IR은 분석과 변환에 적합한 표현을 담는다. 최적화는 불필요한 계산 제거·상수 전파·벡터화 등으로 구성된다. CPU·GPU의 명령어와 메모리 구조가 다르면 같은 IR도 다른 코드를 생성한다. Undefined behavior가 있으면 소스에서 예상한 동작과 최적화된 결과가 달라질 수 있다.

## 도구와 실행 방식

Clang은 C 계열 언어의 frontend, LLVM은 IR과 최적화·코드 생성 생태계, MLIR은 여러 추상화 수준의 표현을 다루는 기반이다. GCC도 여러 언어와 대상 아키텍처를 지원하는 컴파일러 모음이다. Interpreter·JIT·AOT는 실행 시점과 변환 방식이 다르며 실제 runtime은 이들을 조합하기도 한다.

JVM·CPython·Julia runtime은 객체·메모리·실행 모델을 제공한다. FFI에서는 ABI, 자료형 크기, 호출 규약, 객체 수명이 언어가 달라도 일치해야 한다. EDA의 Tcl·SKILL 스크립트도 tool runtime과 API에 의존한다.

## 관련 기술

LLVM, MLIR, GCC, Clang, Rust, Go, Java/JVM, CPython, Julia, Tcl, SKILL

## 참고 자료

- [LLVM documentation](https://llvm.org/docs/)
- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)


## 개념·유도·모델·검증

[기초부터 읽기](../../docs/FOUNDATIONS.md)

- [C 코드가 실행되기까지: 컴파일, 링크, 리셋과 main](notes/reset-to-main-and-toolchain.md)

## English

### Compilers, languages, and runtimes

A compiler translates a program into another representation while preserving its meaning. A typical pipeline includes parsing, semantic analysis, intermediate-representation generation, optimization, and target-code generation.

### From an AST to machine code

An abstract syntax tree represents source syntax. An intermediate representation supports analysis and transformation. Optimizations include eliminating redundant work, propagating constants, and vectorization. Differences in CPU and GPU instructions and memory structures lead to different code from the same IR. Undefined behavior can also cause optimized code to behave differently from what a source-level reading suggests.

### Tools and execution models

Clang is a frontend for C-family languages. LLVM provides IR, optimization, and code-generation infrastructure, while MLIR supports representations at multiple abstraction levels. GCC supports many languages and target architectures. Interpreters, JIT compilation, and AOT compilation differ in when and how translation takes place; runtimes can combine them.

The JVM, CPython, and Julia runtimes provide object, memory, and execution models. At an FFI boundary, the ABI, type sizes, calling conventions, and object lifetimes must agree across languages. Tcl and SKILL scripts in EDA also depend on their tools' runtimes and APIs.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../docs/FOUNDATIONS.md#english)

- [From reset to main: ABI, ELF and linking](notes/reset-to-main-and-toolchain.md#english)
