# 컴퓨터공학 기초

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

프로그램은 알고리즘과 자료구조, 운영체제, 메모리, 입출력 방식이 맞물려 동작한다. 같은 계산 복잡도를 가진 구현도 메모리 접근 패턴과 실행 환경에 따라 성능이 달라진다.

## 자료구조와 실행 비용

배열은 인덱스 접근과 연속 순회에 유리하고, 연결 리스트는 노드를 포인터로 연결한다. 해시 테이블은 키를 해시값으로 대응시키며 충돌 처리와 해시 분포가 성능에 영향을 준다. 트리는 계층·정렬·탐색에, 그래프는 일반적인 연결 관계에 쓰인다.

## 운영체제와 동시성

프로세스는 독립된 주소 공간을 갖는 실행 단위이고, 같은 프로세스의 스레드들은 메모리를 공유한다. 가상메모리는 프로그램의 주소를 실제 메모리와 연결한다. 경쟁 상태는 실행 순서에 따라 결과가 달라지는 상황이며, 잠금·원자 연산·메시지 전달은 공유 상태를 다루는 방법이다.

## 저장, 통신, 빌드

파일시스템은 이름과 디렉터리를 저장 장치의 데이터에 연결한다. 데이터베이스는 질의와 동시 접근, 트랜잭션을 다룬다. TCP는 순서 있는 바이트 스트림을 제공하므로 애플리케이션 메시지 경계는 별도로 정의한다. 컴파일러는 소스를 변환하고 링커는 여러 목적 파일과 라이브러리를 결합한다. Linux와 xv6의 소스에서는 운영체제의 내부 구조를 직접 살펴볼 수 있다.

## 관련 기술

Linux, xv6, OSTEP topics, Networking, TCP/IP, Filesystems, Databases, Compilers, Concurrency

## 참고 자료

- [Linux Kernel documentation](https://docs.kernel.org/)
- [LLVM documentation](https://llvm.org/docs/)


## 개념·유도·모델·검증

[기초부터 읽기](../../docs/FOUNDATIONS.md)

- [같은 주소, 다른 메모리: 프로세스·가상 메모리·동시성](notes/processes-memory-concurrency.md)

## English

Program behavior depends on data structures, the operating system, memory, and I/O as well as the algorithm itself. Two implementations with the same asymptotic complexity can perform differently because of memory access patterns and their execution environments.

### Data structures and execution cost

Arrays suit indexed access and contiguous traversal. Linked lists connect nodes through pointers. Hash tables map keys to hash values, with performance affected by collision handling and hash distribution. Trees support hierarchy, ordering, and search; graphs represent more general relationships.

### Operating systems and concurrency

A process has its own address space, while threads within a process share memory. Virtual memory maps a program's addresses to physical storage. A race condition occurs when the result depends on execution order. Locks, atomic operations, and message passing are ways to coordinate shared state.

### Storage, communication, and builds

A filesystem maps names and directories to stored data. A database adds query processing, concurrent access, and transactions. TCP provides an ordered byte stream, so an application must define its own message boundaries. Compilers translate source, and linkers combine object files and libraries. Linux and xv6 provide source code for studying how operating systems are built.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../docs/FOUNDATIONS.md#english)

- [Processes, virtual memory and concurrency](notes/processes-memory-concurrency.md#english)
