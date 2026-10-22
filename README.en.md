# Engineering Notes

Technical notes on electronics, computer engineering, and AI by [yoonip](https://github.com/yoonip). The collection connects circuits and semiconductors with RTL, firmware, systems software, GPU computing, and AI. It includes explanations, equations, implementations and recorded results. The paper studies explain the methods in Korean with original English terms; many technical notes also provide English summaries.

## Engineering and shared knowledge

Our time is finite, but knowledge can travel across generations and continue to improve. Today's technology rests on the work of many people: not only widely recognized researchers, but also those who explain principles, repair tools and document failures. I want to contribute to that continuing work by leaving the principles I understand and the methods I have checked in a form that others can examine and use.

I see the value of engineering in people's lives. Technologies that remove everyday inconvenience and save time matter, as do those that reduce barriers associated with disability or age and support independent choices. Medical devices, diagnostic tools and rehabilitation technologies can support treatment and recovery. Robotics and remote operation can reduce the need for people to enter hazardous environments. From modest conveniences to questions of life and safety, I care about who benefits from a technology and how it helps them.

I view efficiency through the same lens. Faster computation matters when it solves problems with less time and fewer resources. Automating repetitive work can leave people more room for judgment and creativity. Efficient energy production and use, reduced material waste, and systems that can be repaired and maintained connect engineering with environmental responsibility and sustainability. Alongside performance, I want to consider users' effort, operating costs, reliability and useful lifetime.

Useful technology must also be trustworthy. I aim to record the conditions under which a result holds, what was measured, what was assumed, and how the result can be checked independently. When an explanation proves wrong, I value correcting it through evidence and making the design and verification process understandable to others. Sharing knowledge also means respecting readers' time and taking care that a mistaken explanation does not propagate into their work.

I hope this work can strengthen scientific and technological capacity and industrial competitiveness. Those contributions have their greatest value when they help build better technology and support an exchange of knowledge across borders. My wider purpose is to contribute to humanity: engineering that benefits people living in different regions and circumstances, rather than ending with the achievements of any single country.

I hope this repository will be more than a store of finished answers. One reader may use it to understand a concept for the first time; another may improve a program or begin a new research project. I want future generations, including my children and nieces or nephews, to be able to follow not only what was built but also why it was designed and checked that way. By sharing knowledge in a readable, reusable form, I hope learning and improvement can continue as tools and technologies change.

## Contents

| Section | Coverage |
| --- | --- |
| [Measurement, debugging and validation](현장계측과검증_measurement-validation/README.md) | Instrument guides, DMA/cache, fault tracing, PVT, industrial communications and SCPI automation |
| [Engineering decisions and checks](설계와검증사례_engineering-cases/README.md) | C/C++, RTOS, interrupt/DMA, CAN/SPI/I2C/UART/Ethernet, watchdog/reset, USB/PCIe, firmware updates, NVMe/eMMC/SD, journal recovery, NAND management, FTL mapping, filesystem repair, backups, RAID parity recovery, I/O retries, ECC, DDR, RTL/CDC, chip, AI and data cases with runnable faults, fixes and dated execution evidence |
| [Learning sites and channels](학습사이트와채널_learning-resources/README.md) | Korean and international open courses, research resources, technical documentation and educational video channels |
| [Engineering foundations](공학기초_foundations/README.md) | Foundational and advanced derivations, calculations and checks |
| [Technical topics](분야_topics/README.md) | Development, circuits, digital design, embedded systems, GPUs, AI and services |
| [Reading comprehension and argument reasoning](언어이해와추리논증_reading-reasoning/README.md) | CSAT/LEET past questions, choice-by-choice reasoning and original practice |
| [Foreign languages and technical English](외국어와기술영어_foreign-languages/README.md) | English foundations and exercises, study methods and technical reading |
| [Humanities](인문사회_humanities/README.md) | [Philosophy concepts](인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/개념_concepts/README.md), economics, society, legal rights, facts, procedure and judgments |
| [Music foundations and listening](인문사회_humanities/63-음악기초와듣기_music-foundations-listening/README.md) | Learn beats, rhythm, intervals, tuning, melody, harmony and form through original examples and calculations. |
| [History and historical sources](인문사회_humanities/64-역사와사료_history-sources/README.md) | Read sources in context, then compare trade, industrialization and Korean modern history through evidence and causal questions. |
| [Literature and close reading](인문사회_humanities/65-문학과작품읽기_literature-reading/README.md) | Study voice, poetic lines, narrative time and dramatic action through short original texts and evidence for interpretations. |
| [Art, expression and society](인문사회_humanities/66-예술과감상_arts-aesthetics/README.md) | Compare reasons for interpretations, choices of medium, performance spaces, audiences and arts institutions. |
| [Visual form and art analysis](인문사회_humanities/67-미술과조형_visual-arts/README.md) | Observe line, colour, space and materials, then compare style, context and interpretive evidence in drawings and artworks. |
| [Paper studies](논문해설_papers/README.md) | Korean explanations of research across computing, AI, electronics, life sciences, industry, philosophy of mind, free will and personal identity |
| [Technology landscape](기술동향_technology/README.md) | Dated analysis of benchmarks and technical developments |
| [Product and technology reviews](제품리뷰_reviews/README.md) | Analyses of principles, competing technologies, evidence, supply chains, standards, business models and switching costs |
| [AI model references](AI모델실험_model-lab/README.md) | Official model descriptions and separately documented educational numerical examples |
| [Projects](프로젝트_projects/README.md) · [examples](예제_examples/README.md) | Implementations, execution steps and recorded checks |
| [Programmers](programmers/README.md) | Submitted solutions, study notes and incomplete-attempt analysis |
| [Research](연구_research/README.md) · [author](소개_about/README.md) | Research participation, publications and background |

[Tools and environments](도구와환경_tools/README.md) · [References](참고자료_references/README.md) · [Full subject index](분야별목차_CATALOG.md) · [Contributing](기여안내_contributing/README.md) · [한국어](README.md)

[Philosophy concepts](인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/개념_concepts/README.md) introduces reality, knowledge, ethics, mind, freedom, identity, political legitimacy, and cultivation and action through worked cases. [Recent AI evidence and classical questions](인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/해설_notes/AI연구와고전개념_ai-evidence-and-classical-concepts.md) compares experiments and arguments while separating measured functions from claims about experience and identity.

[Biomedical engineering and medical AI](분야_topics/62-의공학의료AI_medical-engineering/README.md) connects imaging, diagnostic support, neuroprosthetics and AI-assisted drug discovery through mechanisms and clinical evidence.
