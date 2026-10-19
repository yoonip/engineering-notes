# 그림과 표 편집 기준 | Figure and diagram style

개념도는 구조와 관계를, 수치 도표는 값의 변화와 비교를 보여 주도록 구분했다. 회로는 전압원·저항·인덕터·커패시터 기호를 쓰고, 제어계는 합산점·입력 유지·표본화·되먹임 경로를 구분한다. 상태도는 전이 번호를 본문의 조건표와 연결한다.

흰 배경과 얇은 선을 기본으로 하고, 색은 필요한 흐름을 구별할 때만 사용했다. 상자의 크기보다 글과 연결 관계가 먼저 읽히도록 배치하고, 한국어 라벨 아래에 영어를 덧붙였다. 그래프에는 단위와 축 이름을 쓰고, 여러 곡선은 색뿐 아니라 선 모양과 표식으로 구분한다. 범례가 데이터를 가리지 않도록 따로 공간을 두었다.

그림의 편집 원본은 SVG다. MMD와 DOT는 개념 관계와 배치를 남긴 구조 원본이며, 회로 기호로 다시 구성한 그림은 SVG에서 세부 위치를 확인할 수 있다. 본문에는 글꼴 차이로 글자가 빠지지 않도록 렌더링한 PNG를 사용한다. 그래프 생성 코드는 [기초 예제](../예제_examples/공학기초_foundations/make_figures.py)에 있다.

설계 원칙은 [MIT AeroAstro Communication Lab의 figure design 안내](https://mitcommlab.mit.edu/aeroastro/commkit/figure-design/)와 [IEEE Author Center의 글꼴·출력 안내](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/)를 참고했다. 각 그림은 본문의 모델과 연결 관계를 바탕으로 구성했으며, 개념의 근거는 해당 글의 참고 문헌에서 확인할 수 있다.

## English

Concept diagrams show structure and relationships; numerical plots show changes in values and comparisons. Circuit schematics use voltage-source, resistor, inductor and capacitor symbols. Control diagrams distinguish summing points, input holds, sampling and feedback. State-diagram transition numbers refer to the conditions in their accompanying tables.

White backgrounds and thin lines provide the basic style, with color reserved for useful distinctions. Layout emphasizes readable labels and relationships, with English below Korean labels. Plots include units and axis names, and curves differ by line styles and markers as well as color. Legends have space separate from the data.

SVG files are the editable drawing originals. MMD and DOT files preserve conceptual relationships and layout; detailed positions in redrawn circuit schematics are defined in SVG. Articles embed rendered PNGs to avoid missing text across font environments. Plot-generation code is included with the [foundation examples](../예제_examples/공학기초_foundations/make_figures.py).

The visual principles draw on the [MIT AeroAstro Communication Lab's figure-design guide](https://mitcommlab.mit.edu/aeroastro/commkit/figure-design/) and [IEEE Author Center guidance on typography and graphic output](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/). Each drawing follows its article's models and relationships, with conceptual references linked in the article.
