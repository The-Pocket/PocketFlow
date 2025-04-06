<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow는 [100줄](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)의 미니멀리스트 LLM 프레임워크입니다

- **경량화**: 단 100줄. 불필요한 요소 없음, 종속성 없음, 벤더 락인 없음.
  
- **표현력**: 당신이 좋아하는 모든 것—([다중-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[에이전트](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [워크플로우](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) 등.

- **[에이전틱 코딩](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: AI 에이전트(예: Cursor AI)가 에이전트를 구축하도록—생산성 10배 향상!

- 설치하려면, ```pip install pocketflow```또는 [소스 코드](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)(단 100줄)를 복사하세요.
  
- 더 알아보려면, [문서](https://the-pocket.github.io/PocketFlow/)를 확인하세요. 개발 동기를 알아보려면, [이야기](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just)를 읽어보세요.
  
- 🎉 우리의 [디스코드](https://discord.gg/hUHHE9Sa6T)에 참여하세요!

- 🎉 [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130), [@ZebraRoy](https://www.github.com/ZebraRoy) 덕분에 이제 [TypeScript 버전](https://github.com/The-Pocket/PocketFlow-Typescript)이 있습니다!

## 왜 Pocket Flow인가?

현재 LLM 프레임워크들은 너무 비대합니다... LLM 프레임워크는 100줄만 필요합니다!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **추상화**          | **앱 특화 래퍼**                                      | **벤더 특화 래퍼**                                    | **코드 줄 수**       | **크기**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | 에이전트, 체인               | 다수 <br><sup><sub>(예: QA, 요약)</sub></sup>              | 다수 <br><sup><sub>(예: OpenAI, Pinecone 등)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | 에이전트, 체인            | 다수 <br><sup><sub>(예: FileReadTool, SerperDevTool)</sub></sup>         | 다수 <br><sup><sub>(예: OpenAI, Anthropic, Pinecone 등)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | 에이전트                      | 일부 <br><sup><sub>(예: CodeAgent, VisitWebTool)</sub></sup>         | 일부 <br><sup><sub>(예: DuckDuckGo, Hugging Face 등)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | 에이전트, 그래프           | 일부 <br><sup><sub>(예: 시맨틱 검색)</sub></sup>                     | 일부 <br><sup><sub>(예: PostgresStore, SqliteSaver 등) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | 에이전트                | 일부 <br><sup><sub>(예: Tool Agent, Chat Agent)</sub></sup>              | 다수 <sup><sub>[선택사항]<br> (예: OpenAI, Pinecone 등)</sub></sup>        | 7K <br><sup><sub>(핵심만)</sub></sup>    | +26MB <br><sup><sub>(핵심만)</sub></sup>          |
| **PocketFlow** | **그래프**                    | **없음**                                                 | **없음**                                                  | **100**       | **+56KB**                  |

</div>

## Pocket Flow는 어떻게 작동하나요?

[100줄](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)은 LLM 프레임워크의 핵심 추상화를 담고 있습니다: 그래프!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

이를 기반으로 ([다중-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[에이전트](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [워크플로우](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) 등과 같은 인기 있는 디자인 패턴을 쉽게 구현할 수 있습니다.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ 아래는 기본 튜토리얼입니다:

<div align="center">
  
|  이름  | 난이도    |  설명  |  
| :-------------:  | :-------------: | :--------------------- |  
| [채팅](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *초보*   | 대화 기록이 있는 기본 채팅 봇 |
| [구조화된 출력](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *초보* | 프롬프트를 통해 이력서에서 구조화된 데이터 추출 |
| [워크플로우](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *초보*   | 개요 작성, 콘텐츠 작성, 스타일 적용을 수행하는 글쓰기 워크플로우 |
| [에이전트](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *초보*   | 웹을 검색하고 질문에 답할 수 있는 연구 에이전트 |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *초보*   | 간단한 검색 증강 생성 프로세스 |
| [맵-리듀스](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *초보* | 배치 평가를 위한 맵-리듀스 패턴을 사용하는 이력서 자격 처리기 |
| [스트리밍](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *초보*   | 사용자 중단 기능이 있는 실시간 LLM 스트리밍 데모 |
| [채팅 가드레일](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *초보*  | 여행 관련 쿼리만 처리하는 여행 어드바이저 챗봇 |
| [다중 에이전트](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *초급* | 두 에이전트 간의 비동기 통신을 위한 금기어 게임 |
| [감독자](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *초급* | 연구 에이전트가 신뢰할 수 없게 되었습니다... 감독 프로세스를 구축해 봅시다 |
| [병렬](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *초급*   | 3배 속도 향상을 보여주는 병렬 실행 데모 |
| [병렬 플로우](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *초급*   | 여러 필터로 8배 속도 향상을 보여주는 병렬 이미지 처리 데모 |
| [다수결 투표](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *초급* | 여러 솔루션 시도를 집계하여 추론 정확도 향상 |
| [사고](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *초급*   | 사고 체인을 통한 복잡한 추론 문제 해결 |
| [메모리](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *초급* | 단기 및 장기 메모리가 있는 채팅 봇 |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *초급* | 수치 연산을 위한 모델 컨텍스트 프로토콜을 사용하는 에이전트 |

</div>

👀 초보자를 위한 다른 튜토리얼을 보고 싶으신가요? [이슈를 생성하세요!](https://github.com/The-Pocket/PocketFlow/issues/new)

## Pocket Flow를 어떻게 사용하나요?

🚀 **에이전틱 코딩**을 통해—가장 빠른 LLM 앱 개발 패러다임-*인간이 설계*하고 *에이전트가 코딩*합니다!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ 아래는 더 복잡한 LLM 앱의 예시입니다:

<div align="center">
  
|  앱 이름     |  난이도    | 주제  | 인간 설계 | 에이전트 코드 |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Cursor로 Cursor 만들기](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>우리는 곧 특이점에 도달할 것입니다...</sup></sub> | ★★★ <br> *고급*   | [에이전트](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [설계 문서](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [플로우 코드](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [AI Paul Graham에게 물어보기](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>입학하지 못한 경우를 대비해 AI Paul Graham에게 물어보세요</sup></sub> | ★★☆ <br> *중급*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [맵 리듀스](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [설계 문서](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [플로우 코드](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [유튜브 요약기](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> 유튜브 비디오를 5세 아이에게 설명하듯이 설명해 줍니다 </sup></sub> | ★☆☆ <br> *초급*   | [맵 리듀스](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [설계 문서](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [플로우 코드](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [콜드 오프너 생성기](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> 차가운 리드를 뜨겁게 만드는 즉각적인 아이스브레이커 </sup></sub> | ★☆☆ <br> *초급*   | [맵 리듀스](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [웹 검색](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [설계 문서](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [플로우 코드](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- **에이전틱 코딩**을 배우고 싶으신가요?

  - 위의 앱 중 일부가 어떻게 만들어졌는지 비디오 튜토리얼을 보려면 [내 YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)를 확인하세요!

  - 자신만의 LLM 앱을 만들고 싶으신가요? 이 [포스트](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)를 읽어보세요! [이 템플릿](https://github.com/The-Pocket/PocketFlow-Template-Python)으로 시작하세요!

  - 자세한 단계를 배우고 싶으신가요? 이 [가이드](https://the-pocket.github.io/PocketFlow/guide.html)를 읽어보세요!