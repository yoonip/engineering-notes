# 그림과 표의 표기 | Figure and table conventions

[기여 안내 / Contributing](README.md) · [그림 목록과 원본 / Figures and source files](../그림자료_assets/도식_diagrams/그림목록_INDEX.md)

개념도는 구조와 관계를, 수치 도표는 값의 변화와 비교를 보여 주도록 구분했습니다. 회로는 전압원·저항·인덕터·커패시터 기호를 쓰고, 제어계는 합산점·입력 유지·표본화·되먹임 경로를 구분합니다. 상태도는 전이 번호를 본문의 조건표와 연결합니다.

흰 배경과 얇은 선을 기본으로 하고, 색은 필요한 흐름을 구별할 때만 사용했습니다. 상자의 크기보다 글과 연결 관계가 먼저 읽히도록 배치하고, 한국어 라벨 아래에 영어를 덧붙였습니다. 그래프에는 단위와 축 이름을 쓰고, 여러 곡선은 색뿐 아니라 선 모양과 표식으로 구분합니다. 범례가 데이터를 가리지 않도록 따로 공간을 두었습니다.

그림의 편집 원본은 SVG입니다. MMD와 DOT는 개념 관계와 배치를 남긴 구조 원본이며, 회로 기호로 다시 구성한 그림은 SVG에서 세부 위치를 확인할 수 있습니다. 본문에는 글꼴 차이로 글자가 빠지지 않도록 렌더링한 PNG를 사용합니다. 그래프 생성 코드는 [기초 예제](../예제_examples/공학기초_foundations/make_figures.py)에 있습니다.

설계 원칙은 [MIT AeroAstro Communication Lab의 figure design 안내](https://mitcommlab.mit.edu/aeroastro/commkit/figure-design/)와 [IEEE Author Center의 글꼴·출력 안내](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/)를 참고했습니다. 각 그림은 본문의 모델과 연결 관계를 바탕으로 구성했으며, 개념의 근거는 해당 글의 참고 문헌에서 확인할 수 있습니다.

실제 제품 사진, 장비·화면 캡처, 원리 그림도 서로 구분합니다. 사진 설명에는 무엇을 촬영했는지와 글의 어느 원리와 연결되는지를 적고, 제조사 이미지가 렌더링인지 실물 촬영인지 확인되지 않으면 ‘공식 제품 이미지’라고 표시합니다. 원리도에는 특정 제품의 내부 구조를 그대로 그렸다고 오해하지 않도록 일반화한 부분을 밝힙니다. 사진이나 그림의 출처 페이지를 캡션 가까이에 연결하며, 제조사 홍보 이미지는 측정 결과의 증거로 사용하지 않습니다.

외부 공식 사이트의 이미지를 본문에 직접 연결한 경우에는 저장소에 이미지 사본을 만들지 않습니다. 원본 페이지와 이미지 주소를 함께 남기고, 링크가 이동하거나 사라질 수 있음을 전제로 설명을 구성합니다. 이미지 파일을 저장소에 넣을 때에는 출처와 이용 조건을 먼저 확인해 [원본 자료 목록](../반도체설계_semiconductor-design/사진과화면_images/README.md)과 같이 기록합니다.

## English

Actual product photographs, equipment or software screenshots, and principle diagrams are labeled separately. Captions say what was photographed and how it relates to the article. When a manufacturer image cannot be confirmed as a photograph or a rendering, it is labeled an official product image. Diagrams identify any generalized structure so readers do not mistake it for a product's exact internal design. Source pages are linked next to captions, and promotional images are not used as evidence of measured performance.

Images linked directly from official websites are not copied into the repository. The source page and image URL are both retained, with the possibility that an external URL may later move or disappear. Before storing a local image, its source and reuse terms are checked and recorded as in the [source image inventory](../반도체설계_semiconductor-design/사진과화면_images/README.md).

Concept diagrams show structure and relationships; numerical plots show changes in values and comparisons. Circuit schematics use voltage-source, resistor, inductor and capacitor symbols. Control diagrams distinguish summing points, input holds, sampling and feedback. State-diagram transition numbers refer to the conditions in their accompanying tables.

White backgrounds and thin lines provide the basic style, with color reserved for useful distinctions. Layout emphasizes readable labels and relationships, with English below Korean labels. Plots include units and axis names, and curves differ by line styles and markers as well as color. Legends have space separate from the data.

SVG files are the editable drawing originals. MMD and DOT files preserve conceptual relationships and layout; detailed positions in redrawn circuit schematics are defined in SVG. Articles embed rendered PNGs to avoid missing text across font environments. Plot-generation code is included with the [foundation examples](../예제_examples/공학기초_foundations/make_figures.py).

The visual principles draw on the [MIT AeroAstro Communication Lab's figure-design guide](https://mitcommlab.mit.edu/aeroastro/commkit/figure-design/) and [IEEE Author Center guidance on typography and graphic output](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/). Each drawing follows its article's models and relationships, with conceptual references linked in the article.
