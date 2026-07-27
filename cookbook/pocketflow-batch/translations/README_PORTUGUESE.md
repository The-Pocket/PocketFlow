<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" alt="Pocket Flow – 100-line minimalist LLM framework" width="600"/>
</div>

<!-- [English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) -->

[English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) | [中文](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_CHINESE.md) | [Español](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_SPANISH.md) | [日本語](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_JAPANESE.md) | [Deutsch](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_GERMAN.md) | [Русский](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_RUSSIAN.md) | Português | [Français](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_FRENCH.md) | [한국어](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_KOREAN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow é um framework minimalista para LLM com [apenas 100 linhas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)

- **Leve**: Apenas 100 linhas. Zero inchaço, zero dependências, zero aprisionamento a fornecedores.
  
- **Expressivo**: Tudo o que você adora—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Fluxo de Trabalho](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), e mais.

- **[Codificação Agêntica](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Deixe que Agentes de IA (ex: Cursor AI) construam Agentes—aumento de produtividade de 10x!

Comece com o Pocket Flow:
- Para instalar, ```pip install pocketflow``` ou apenas copie o [código-fonte](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (apenas 100 linhas).
- Para saber mais, consulte a [documentação](https://the-pocket.github.io/PocketFlow/). Para entender a motivação, leia a [história](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- Tem perguntas? Consulte este [Assistente de IA](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant), ou [crie uma issue!](https://github.com/The-Pocket/PocketFlow/issues/new)
- 🎉 Junte-se ao nosso [Discord](https://discord.gg/hUHHE9Sa6T) para se conectar com outros desenvolvedores construindo com o Pocket Flow!
- 🎉 O Pocket Flow é inicialmente em Python, mas agora temos versões em [Typescript](https://github.com/The-Pocket/PocketFlow-Typescript), [Java](https://github.com/The-Pocket/PocketFlow-Java), [C++](https://github.com/The-Pocket/PocketFlow-CPP), [Go](https://github.com/The-Pocket/PocketFlow-Go), [Rust](https://github.com/The-Pocket/PocketFlow-Rust), [PHP](https://github.com/The-Pocket/PocketFlow-PHP) e [Dart](https://github.com/rag-wtf/PocketFlow-Dart)!

## Por que Pocket Flow?

Os frameworks LLM atuais são pesados... Você só precisa de 100 linhas para um Framework LLM!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Abstração**          | **Wrappers Específicos para Aplicações**                                      | **Wrappers Específicos para Fornecedores**                                    | **Linhas**       | **Tamanho**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agente, Cadeia               | Muitos <br><sup><sub>(ex: QA, Summarization)</sub></sup>              | Muitos <br><sup><sub>(ex: OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agente, Cadeia            | Muitos <br><sup><sub>(ex: FileReadTool, SerperDevTool)</sub></sup>         | Muitos <br><sup><sub>(ex: OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agente                      | Alguns <br><sup><sub>(ex: CodeAgent, VisitWebTool)</sub></sup>         | Alguns <br><sup><sub>(ex: DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agente, Grafo           | Alguns <br><sup><sub>(ex: Semantic Search)</sub></sup>                     | Alguns <br><sup><sub>(ex: PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agente                | Alguns <br><sup><sub>(ex: Tool Agent, Chat Agent)</sub></sup>              | Muitos <sup><sub>[Opcional]<br> (ex: OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(somente core)</sub></sup>    | +26MB <br><sup><sub>(somente core)</sub></sup>          |
| **PocketFlow** | **Grafo**                    | **Nenhum**                                                 | **Nenhum**                                                  | **100**       | **+56KB**                  |

</div>

## Como funciona o Pocket Flow?

As [100 linhas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) capturam a abstração central dos frameworks LLM: o Grafo!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

A partir daí, é fácil implementar padrões de design populares como ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Fluxo de Trabalho](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ Abaixo estão tutoriais básicos:

<div align="center">
  
|  Nome  | Dificuldade    |  Descrição  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Básico*   | Um chatbot básico com histórico de conversação |
| [Saída Estruturada](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Básico* | Extraindo dados estruturados de currículos por prompt |
| [Fluxo de Trabalho](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Básico*   | Um fluxo de escrita que esboça, escreve conteúdo e aplica estilo |
| [Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Básico*   | Um agente de pesquisa que pode buscar na web e responder perguntas |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Básico*   | Um processo simples de Geração Aumentada por Recuperação |
| [Processamento em Lote](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-batch) | ☆☆☆ <br> *Básico* | Um processador em lote que traduz conteúdo markdown para vários idiomas |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Básico*   | Uma demonstração de streaming LLM em tempo real com capacidade de interrupção pelo usuário |
| [Guardrail de Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Básico*  | Um chatbot de consultoria de viagens que processa apenas consultas relacionadas a viagens |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ★☆☆ <br> *Iniciante* | Um processador de qualificação de currículos usando o padrão map-reduce para avaliação em lote |
| [Multi-Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Iniciante* | Um jogo de Tabu para comunicação assíncrona entre dois agentes |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Iniciante* | O agente de pesquisa está ficando pouco confiável... Vamos criar um processo de supervisão |
| [Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Iniciante*   | Uma demonstração de execução paralela que mostra um aumento de velocidade de 3x |
| [Fluxo Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Iniciante*   | Uma demonstração de processamento de imagem paralelo mostrando um aumento de velocidade de 8x com múltiplos filtros |
| [Voto Majoritário](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Iniciante* | Melhore a precisão de raciocínio agregando múltiplas tentativas de solução |
| [Pensamento](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Iniciante*   | Resolva problemas complexos de raciocínio através de Cadeia-de-Pensamento |
| [Memória](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Iniciante* | Um chatbot com memória de curto e longo prazo |
| [Text2SQL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-text2sql) | ★☆☆ <br> *Iniciante* | Converta linguagem natural para consultas SQL com um loop de autodepuração |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Iniciante* | Agente usando o Protocolo de Contexto de Modelo para operações numéricas |
| [A2A](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-a2a) | ★☆☆ <br> *Iniciante* | Agente envolvido com o protocolo Agente-para-Agente para comunicação entre agentes |
| [Web HITL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-web-hitl) | ★☆☆ <br> *Iniciante* | Um serviço web mínimo para um loop de revisão humana com atualizações SSE |

</div>

👀 Quer ver outros tutoriais para iniciantes? [Crie uma issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## Como usar o Pocket Flow?

🚀 Através da **Codificação Agêntica**—o paradigma mais rápido de desenvolvimento de aplicativos LLM—onde *humanos projetam* e *agentes codificam*!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Abaixo estão exemplos de aplicativos LLM mais complexos:

<div align="center">
  
|  Nome do Aplicativo     |  Dificuldade    | Tópicos  | Design Humano | Código do Agente |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Construir Cursor com Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Logo chegaremos à singularidade ...</sup></sub> | ★★★ <br> *Avançado*   | [Agente](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Doc de Design](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Código de Fluxo](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Construtor de Conhecimento de Base de Código](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge) <br> <sup><sub>A vida é curta demais para ficar olhando o código dos outros em confusão</sup></sub> |  ★★☆ <br> *Médio* | [Fluxo de Trabalho](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html) | [Doc de Design](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/docs/design.md) | [Código de Fluxo](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/flow.py)
| [Pergunte à IA Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Pergunte à IA Paul Graham, caso você não consiga entrar</sup></sub> | ★★☆ <br> *Médio*  | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Doc de Design](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Código de Fluxo](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Resumidor de Youtube](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Explica vídeos do YouTube para você como se você tivesse 5 anos </sup></sub> | ★☆☆ <br> *Iniciante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Doc de Design](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Código de Fluxo](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Gerador de Abertura a Frio](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Quebra-gelos instantâneos que transformam leads frios em quentes </sup></sub> | ★☆☆ <br> *Iniciante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Busca Web](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Doc de Design](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Código de Fluxo](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Quer aprender **Codificação Agêntica**?

  - Confira [meu YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) para tutoriais em vídeo sobre como alguns dos aplicativos acima são feitos!

  - Quer construir seu próprio aplicativo LLM? Leia este [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Comece com [este modelo](https://github.com/The-Pocket/PocketFlow-Template-Python)!