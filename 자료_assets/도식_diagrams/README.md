# 개념도 / Concept diagrams

이 폴더의 24개 그림은 각 문서의 설명에 맞춰 직접 구성했습니다. 원리와 조건을 한눈에 보기 위한 그림이며, 실제 회로의 배선도나 장치 측정 결과는 해당 본문에서 별도로 구분합니다. 개념의 참고 문헌은 각 문서에 연결되어 있습니다.

본문에는 한글 글꼴로 렌더링한 PNG를 사용합니다. SVG는 확대하고 편집할 수 있는 벡터 원본입니다. 일반 개념도는 여백과 선 굵기를 통일한 사각형 배치로 정리했으며, RLC 회로·4선식 계측·샘플링 피드백·열확산 격자·전송선 왕복은 각각의 물리적 관계와 시간 순서에 맞춰 SVG로 그렸습니다. MMD와 DOT 파일에는 개념의 연결 구조가 남아 있습니다. 회로 기호와 파형, 상태 전이 등은 같은 모양으로 뭉뚱그리지 않고 대상에 맞는 표현을 사용합니다.

색은 관계를 보조하는 데만 쓰며, 선 모양·화살표·라벨로도 내용을 구분합니다. 자세한 편집 기준과 참고 자료는 [그림과 표의 표기](../../기여안내_contributing/그림과표_FIGURES.md)에 정리했습니다.

상태도 두 개는 화살표에 번호를 붙였습니다. 각 문서의 전이표에서 같은 번호의 출발 상태, 도착 상태, 조건과 동작을 함께 읽습니다. 점선은 일반 흐름과 다른 관계를 구분하며, 구체적인 의미는 본문에서 설명합니다.

- [그림 목록과 연결 관계](그림목록_INDEX.md)
- 배치: [Graphviz](https://graphviz.org/) 14.1.3, [Viz.js](https://viz-js.com/api/) 3.25.0
- PNG 렌더링: [Sharp](https://sharp.pixelplumbing.com/) 0.35.5
- 렌더링 글꼴: Malgun Gothic. 글꼴 파일은 이 저장소에 배포하지 않습니다.

## English

The 24 diagrams in this folder were composed for the corresponding articles. They show principles and conditions at a glance; the articles distinguish them from physical wiring diagrams or device measurements. Conceptual references are linked in each article.

Articles embed PNG images rendered with Korean text. SVG files are scalable, editable vector originals. General concept diagrams use rectangular layouts with consistent spacing and line weights. The RLC circuit, four-wire measurement, sampled feedback, heat-diffusion grid and transmission-line round trip use custom SVG drawings that preserve their physical relationships and time order. MMD and DOT files retain the conceptual connections. Circuit symbols, waveforms and state transitions use representations suited to their subject.

Color supports the relationships; line styles, arrows and labels also distinguish them. See the [figure editing guide](../../기여안내_contributing/그림과표_FIGURES.md) for the design choices and references.

The two state diagrams number their arrows. Read each number with the source state, destination state, condition and action in the article's transition table. Dashed arrows distinguish a different relationship from the ordinary flow; its meaning is explained in the article.

- [Diagram inventory and connections](그림목록_INDEX.md)
- Layout: [Graphviz](https://graphviz.org/) 14.1.3 through [Viz.js](https://viz-js.com/api/) 3.25.0
- PNG rendering: [Sharp](https://sharp.pixelplumbing.com/) 0.35.5
- Rendered font: Malgun Gothic. Font files are not distributed here.
