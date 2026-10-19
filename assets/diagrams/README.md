# 개념도 / Concept diagrams

이 폴더의 24개 도식은 각 문서의 설명에 맞춰 직접 구성했다. 원리와 조건을 한눈에 보기 위한 그림이며, 실제 회로의 배선도나 장치 측정 결과는 해당 본문에서 별도로 구분한다. 개념의 참고 문헌은 각 문서에 연결되어 있다.

본문에는 한글 글꼴을 포함해 렌더링한 PNG를 사용한다. SVG는 확대해서 읽을 수 있는 벡터 원본이며, MMD 파일에는 노드·화살표·라벨을 정의한 도식 원문이 있다. DOT 파일은 배치에 사용한 소스다. 전송선의 왕복 그림은 시간 순서가 유지되도록 SVG로 직접 구성했다.

상태도 두 개는 화살표에 번호를 붙였다. 각 문서의 전이표에서 같은 번호의 출발 상태, 도착 상태, 조건과 동작을 함께 읽는다. 점선은 일반 흐름과 다른 관계를 구분하며, 구체적인 의미는 본문에서 설명한다.

- [도식 목록과 연결 관계](manifest.json)
- 배치: [Graphviz](https://graphviz.org/) 14.1.3, [Viz.js](https://viz-js.com/api/) 3.25.0
- PNG 렌더링: [Sharp](https://sharp.pixelplumbing.com/) 0.35.5
- 렌더링 글꼴: Malgun Gothic. 글꼴 파일은 이 저장소에 배포하지 않는다.

## English

The 24 diagrams in this folder were composed for the corresponding articles. They show principles and conditions at a glance; the articles distinguish them from physical wiring diagrams or device measurements. Conceptual references are linked in each article.

Articles embed PNG images rendered with Korean text. SVG files provide scalable vector versions, MMD files preserve the nodes, arrows and labels, and DOT files contain layout sources. The transmission-line round-trip diagram was composed directly as SVG to preserve message order in time.

The two state diagrams number their arrows. Read each number with the source state, destination state, condition and action in the article's transition table. Dashed arrows distinguish a different relationship from the ordinary flow; its meaning is explained in the article.

- [Diagram inventory and connections](manifest.json)
- Layout: [Graphviz](https://graphviz.org/) 14.1.3 through [Viz.js](https://viz-js.com/api/) 3.25.0
- PNG rendering: [Sharp](https://sharp.pixelplumbing.com/) 0.35.5
- Rendered font: Malgun Gothic. Font files are not distributed here.
