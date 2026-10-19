# Databases & Data Engineering

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

데이터베이스는 데이터를 저장하는 기능과 함께 질의·동시 접근·무결성·복구를 제공한다. 데이터 엔지니어링은 수집부터 변환·검증·저장·전달까지 이어지는 흐름을 만든다.

## SQL과 실행 계획

관계형 모델은 표와 관계를 사용한다. Index는 조회를 빠르게 할 수 있지만 저장 공간과 쓰기 비용이 추가된다. Transaction은 여러 연산을 하나의 논리 작업으로 다루며 isolation 수준에 따라 동시 실행에서 관찰되는 현상이 달라진다. Query plan은 데이터 접근과 join이 어떤 순서와 방식으로 실행되는지 보여준다.

SQLite는 파일 기반의 내장형 데이터베이스, PostgreSQL·MySQL은 서버형 관계형 데이터베이스, DuckDB는 분석 질의, Redis는 메모리 기반 데이터 구조에 자주 쓰인다. CSV는 단순 교환, Parquet는 columnar 저장, Arrow는 메모리 내 데이터 교환과 관련된다.

## 파이프라인과 검색

Batch는 모인 데이터를 묶어 처리하고 streaming은 계속 들어오는 이벤트를 다룬다. Spark·Kafka는 대규모 데이터 처리와 이벤트 전달에 쓰인다. 결측·중복·단위·시간대·schema 변화가 분석 결과에 영향을 준다. FAISS·pgvector는 벡터 유사도 검색에 쓰이며 유사도 점수 자체가 내용의 사실성을 보장하지는 않는다.

## 관련 기술

SQLite, PostgreSQL, MySQL, DuckDB, Redis, Parquet, Arrow, Spark, Kafka, FAISS, pgvector

## 참고 자료

- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)

## English

### Databases and data engineering

Databases provide queries, concurrent access, integrity, and recovery alongside data storage. Data engineering connects collection, transformation, validation, storage, and delivery into a pipeline.

### SQL and query plans

The relational model represents data through tables and relationships. An index can speed up reads at the cost of storage and additional work on writes. A transaction groups operations into a logical unit; its isolation level affects what concurrent transactions can observe. A query plan shows how data access and joins will execute.

SQLite is an embedded, file-based database. PostgreSQL and MySQL are server-based relational databases, DuckDB supports analytical queries, and Redis provides in-memory data structures. CSV is used for simple data exchange, Parquet for columnar storage, and Arrow for in-memory data interchange.

### Pipelines and search

Batch processing works on accumulated data, while streaming handles incoming events continuously. Spark and Kafka support large-scale processing and event delivery. Missing values, duplicates, units, time zones, and schema changes affect analysis. FAISS and pgvector support vector-similarity search, but a similarity score does not establish whether the retrieved content is factually correct.
