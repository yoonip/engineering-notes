# Web · API · Applications

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

웹 애플리케이션은 브라우저와 서버, 데이터 저장소를 연결한다. 실험 결과 조회, 장치 제어, 모델 추론, 기술 문서 검색도 웹 인터페이스로 제공할 수 있다.

## 통신과 데이터

HTTP는 요청·응답 방식의 프로토콜이다. REST는 자원과 표준적인 인터페이스를 중심으로 하는 설계 스타일이고 WebSocket은 양방향 통신 연결을 제공한다. 인증·권한·입력 검증·오류 형식은 API 계약의 일부다. 오래 걸리는 작업은 요청 처리와 작업 실행을 나누기도 한다.

## 화면과 서버

FastAPI·Flask·Django·Spring·Node.js 생태계는 서버 구성에, React·Vue·Svelte·TypeScript는 웹 UI에 쓰인다. Qt·PySide·Electron은 데스크톱 애플리케이션, Streamlit·Gradio는 데이터·모델 인터페이스 구성에 자주 쓰인다. 사용자가 할 작업과 데이터 흐름을 바탕으로 구조와 framework를 정한다.

장치 제어에서는 화면에 명령을 보낸 시점과 장치가 실제 수행한 시점이 다를 수 있다. 명령 ID·진행 상태·timeout·중복 처리 방식이 필요하다. 대시보드의 시간축·단위·집계 기준은 그래프를 해석하는 기준이 된다.

## 관련 기술

FastAPI, Flask, Django, Node.js, Spring, React, Vue, Svelte, TypeScript, Qt/PySide, Electron, Streamlit, Gradio

## 참고 자료

- [FastAPI documentation](https://fastapi.tiangolo.com/)

## English

### Web, APIs, and applications

Web applications connect browsers, servers, and data stores. A web interface can expose experiment results, device controls, model inference, or technical-document search.

### Communication and data

HTTP is a request-response protocol. REST is an architectural style organized around resources and a uniform interface, while WebSocket provides a bidirectional connection. Authentication, authorization, input validation, and error formats are part of an API contract. Long-running work can be separated from the request that starts it.

### Interfaces and servers

FastAPI, Flask, Django, Spring, and Node.js support server development. React, Vue, Svelte, and TypeScript support web interfaces. Qt, PySide, and Electron support desktop applications, while Streamlit and Gradio are often used for data and model interfaces. User tasks and data flow shape the application structure and framework choice.

In device control, the time a command is sent from the interface can differ from the time the device executes it. Command IDs, progress states, timeouts, and duplicate handling keep those events trackable. A dashboard's time axis, units, and aggregation rules determine how its graphs should be read.
