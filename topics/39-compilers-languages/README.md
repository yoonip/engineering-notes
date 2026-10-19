# Compilers · Languages · Runtimes

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

컴파일러는 프로그램의 의미를 유지하면서 다른 표현으로 변환한다. 일반적인 흐름은 parsing, 의미 분석, 중간 표현 생성, 최적화, 대상 코드 생성으로 이어진다.

## AST에서 machine code로

AST는 소스의 문법 구조를, IR은 분석과 변환에 적합한 표현을 담는다. 최적화는 불필요한 계산 제거·상수 전파·벡터화 등으로 구성된다. CPU·GPU의 명령어와 메모리 구조가 다르면 같은 IR도 다른 코드를 생성한다. Undefined behavior가 있으면 소스에서 예상한 동작과 최적화된 결과가 달라질 수 있다.

## 도구와 실행 방식

Clang은 C 계열 언어의 frontend, LLVM은 IR과 최적화·코드 생성 생태계, MLIR은 여러 추상화 수준의 표현을 다루는 기반이다. GCC도 다양한 언어와 대상 아키텍처를 지원하는 컴파일러 모음이다. Interpreter·JIT·AOT는 실행 시점과 변환 방식이 다르며 실제 runtime은 이들을 조합하기도 한다.

JVM·CPython·Julia runtime은 객체·메모리·실행 모델을 제공한다. FFI에서는 ABI, 자료형 크기, 호출 규약, 객체 수명이 언어 경계를 넘어 맞아야 한다. EDA의 Tcl·SKILL 스크립트도 tool runtime과 API에 의존한다.

## 관련 기술

LLVM, MLIR, GCC, Clang, Rust, Go, Java/JVM, CPython, Julia, Tcl, SKILL

## 참고 자료

- [LLVM documentation](https://llvm.org/docs/)
- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)
