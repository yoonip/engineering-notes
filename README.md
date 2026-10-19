# 공학 노트 | Engineering Notes

회로와 반도체부터 RTL·펌웨어, 시스템 소프트웨어, GPU와 AI까지 다루는 기술 기록입니다. 개념을 정리하고, 수식을 코드로 옮기고, 직접 실행한 결과를 함께 모았습니다. 논증과 자료를 읽는 추론, 철학·경제·사회·법의 기초도 함께 다룹니다.

각 주제에서는 무엇에 쓰이는지, 왜 그 방식으로 구현하는지부터 살펴봅니다. 설명은 한국어와 영어로 나누고, 코드 주석은 한국어로 적었습니다. Linux·Bash 같은 기술명은 익숙한 표기를 그대로 씁니다.

- [심화 해설·구현·검증 | Advanced explanations and implementations](문서_docs/심화해설_ADVANCED.md)
- [기초 개념·유도·모델·검증 | Engineering foundations](문서_docs/공학기초_FOUNDATIONS.md)
- [분야별 기초 해설 | Technical foundations by topic](문서_docs/분야별기초해설_EXTENDED_FOUNDATIONS.md)
- [추론·인문사회 | Reasoning & humanities](문서_docs/추론과인문사회_REASONING_AND_HUMANITIES.md)
- [연구·프로젝트·논문·수상 | Research & publications](연구_research/README.md)
- [분야별 목차 | Topic index](분야별목차_CATALOG.md)
- [AI 기업과 모델 | AI providers & models](AI모델실험_model-lab/PROVIDERS.md)
- [도구 목록 | Tools](문서_docs/도구목록_TOOLS_INDEX.md)
- [구현 프로젝트 | Projects](프로젝트_projects/README.md) · [코드 예제 | Code examples](예제_examples/README.md)
- [알고리즘과 코딩테스트 | Algorithms](분야_topics/08-알고리즘_problem-solving/README.md) · [프로그래머스 학습 기록 | Programmers](programmers/README.md)
- [지원·시험·면접 | Applications & interviews](분야_topics/55-지원시험면접_applications-assessments/README.md)
- [작성자와 연락처 | Author & contact](문서_docs/작성자소개_PROFILE_TEMPLATE.md) · [참고 자료 | References](문서_docs/참고자료_SOURCES.md)

## 공학과 지식 공유

사람에게 주어진 시간은 유한하지만, 지식은 세대를 건너 이어지고 더 나아질 수 있습니다. 오늘의 기술도 이름이 널리 알려진 연구자뿐 아니라 원리를 설명하고, 도구를 고치고, 실패를 기록해 온 많은 사람의 작업 위에 서 있습니다. 저도 그 흐름에 보탬이 되고 싶습니다. 제가 이해한 원리와 확인한 방법을 다른 사람이 다시 살펴보고 활용할 수 있도록 남기는 것이 이 기록의 출발점입니다.

공학의 가치는 사람의 삶에서 드러난다고 생각합니다. 일상의 번거로운 일을 줄이고 시간을 아껴 주는 기술, 장애나 나이에 따른 제약을 낮추어 스스로 선택하고 활동할 수 있게 하는 기술 모두 중요합니다. 의료 기기와 진단·재활 기술은 치료와 회복을 돕고, 로봇과 원격 제어는 사람이 위험한 환경에 직접 들어가야 하는 일을 줄일 수 있습니다. 작은 편의부터 생명과 안전에 관계된 문제까지, 기술이 실제로 누구에게 어떤 도움을 주는지 생각하며 공학을 바라봅니다.

효율도 같은 관점에서 봅니다. 계산을 빠르게 하는 일은 더 적은 시간과 자원으로 문제를 해결하는 데 의미가 있습니다. 반복 작업을 자동화하면 사람은 판단과 창의성이 필요한 일에 더 집중할 수 있습니다. 에너지를 효율적으로 생산하고 사용하며, 자원 낭비를 줄이고 수리와 유지보수가 가능한 시스템을 만드는 일은 환경과 지속가능성으로 이어집니다. 성능 수치와 함께 사용자의 부담, 운용 비용, 신뢰성과 오래 사용할 수 있는지도 살피고 싶습니다.

도움이 되는 기술은 믿을 수 있어야 합니다. 어떤 조건에서 성립하는 결과인지, 무엇을 측정했고 무엇을 가정했는지, 다른 방법으로 확인할 수 있는지를 함께 기록하려 합니다. 잘못 이해한 부분이 드러나면 근거를 따라 수정하고, 설계와 검증의 과정을 다른 사람도 이해할 수 있게 설명하는 태도를 중요하게 생각합니다. 지식을 공유하는 일에는 읽는 사람의 시간을 존중하고, 잘못된 설명이 다음 작업으로 이어지지 않도록 살피는 책임도 있다고 봅니다.

이러한 작업이 국가의 과학기술 기반과 산업 경쟁력을 튼튼하게 하는 데 기여하기를 바랍니다. 한국의 국가 기술 역량과 국가경쟁력을 높이는 일 역시, 더 좋은 기술을 만들고 세계와 지식을 나누는 과정 속에서 의미를 갖는다고 생각합니다. 궁극적으로는 어느 한 나라의 성과에 머무르지 않고, 서로 다른 지역과 환경에 있는 사람들에게 도움이 되며 전 세계 인류의 삶을 더 낫게 만드는 공학을 지향합니다.

이 저장소가 완성된 답을 보관하는 곳에 그치지 않았으면 합니다. 누군가는 개념을 처음 이해하는 데 쓰고, 누군가는 코드를 고치거나 새로운 연구를 시작하는 데 활용할 수 있기를 바랍니다. 훗날 제 아이와 조카를 비롯한 다음 세대가 보더라도, 무엇을 만들었는지뿐 아니라 왜 그렇게 생각하고 확인했는지 따라갈 수 있는 기록을 남기고 싶습니다. 도구와 기술이 바뀌어도 배움과 개선이 이어질 수 있도록, 지식을 읽기 쉽고 다시 사용할 수 있는 형태로 공유하겠습니다.

## English

These notes connect circuits and semiconductors with RTL, firmware, systems software, GPU computing, and AI. They bring together technical explanations, equations translated into code, and results from the implementations. The collection also covers reasoning about arguments and data, alongside foundations of philosophy, economics, society and law.

Each topic starts with what it is used for and why the implementation works that way. Explanations are available in Korean and English, while code comments stay in Korean. Familiar technical names such as Linux and Bash keep their usual spelling.

- [60 advanced explanations and executable examples](문서_docs/심화해설_ADVANCED.md#english)
- [Foundations: concepts, derivations, models, and verification](문서_docs/공학기초_FOUNDATIONS.md#english)
- [Technical foundations by topic](문서_docs/분야별기초해설_EXTENDED_FOUNDATIONS.md)
- [Reasoning, assessments, philosophy, economics, society and law](문서_docs/추론과인문사회_REASONING_AND_HUMANITIES.md#english)
- [Research, papers, and awards](연구_research/README.md)
- [Topic index](분야별목차_CATALOG.md) · [AI companies and models](AI모델실험_model-lab/PROVIDERS.md)
- [Tools](문서_docs/도구목록_TOOLS_INDEX.md) · [Implemented projects](프로젝트_projects/README.md) · [Code examples](예제_examples/README.md)
- [Algorithms and coding tests](분야_topics/08-알고리즘_problem-solving/README.md) · [309 Programmers solutions](programmers/README.md)
- [Applications, assessments, and interviews](분야_topics/55-지원시험면접_applications-assessments/README.md)
- [Author and contact](문서_docs/작성자소개_PROFILE_TEMPLATE.md) · [References](문서_docs/참고자료_SOURCES.md)

### Engineering and shared knowledge

Our time is finite, but knowledge can travel across generations and continue to improve. Today's technology rests on the work of many people: not only widely recognized researchers, but also those who explain principles, repair tools and document failures. I want to contribute to that continuing work by leaving the principles I understand and the methods I have checked in a form that others can examine and use.

I see the value of engineering in people's lives. Technologies that remove everyday inconvenience and save time matter, as do those that reduce barriers associated with disability or age and support independent choices. Medical devices, diagnostic tools and rehabilitation technologies can support treatment and recovery. Robotics and remote operation can reduce the need for people to enter hazardous environments. From modest conveniences to questions of life and safety, I care about who benefits from a technology and how it helps them.

I view efficiency through the same lens. Faster computation matters when it solves problems with less time and fewer resources. Automating repetitive work can leave people more room for judgment and creativity. Efficient energy production and use, reduced material waste, and systems that can be repaired and maintained connect engineering with environmental responsibility and sustainability. Alongside performance, I want to consider users' effort, operating costs, reliability and useful lifetime.

Useful technology must also be trustworthy. I aim to record the conditions under which a result holds, what was measured, what was assumed, and how the result can be checked independently. When an explanation proves wrong, I value correcting it through evidence and making the design and verification process understandable to others. Sharing knowledge also means respecting readers' time and taking care that a mistaken explanation does not propagate into their work.

I hope this work can strengthen scientific and technological capacity and industrial competitiveness. Those contributions have their greatest value when they help build better technology and support an exchange of knowledge across borders. My wider purpose is to contribute to humanity: engineering that benefits people living in different regions and circumstances, rather than ending with the achievements of any single country.

I hope this repository will be more than a store of finished answers. One reader may use it to understand a concept for the first time; another may improve a program or begin a new research project. I want future generations, including my children and nieces or nephews, to be able to follow not only what was built but also why it was designed and checked that way. By sharing knowledge in a readable, reusable form, I hope learning and improvement can continue as tools and technologies change.

[English topic list](README.en.md)
