<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow é um framework LLM minimalista de [100 linhas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)

- **Leve**: Apenas 100 linhas. Zero inchaço, zero dependências, zero bloqueio de fornecedor.
  
- **Expressivo**: Tudo o que você ama—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Fluxo de Trabalho](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), e mais.

- **[Codificação Agêntica](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Deixe os Agentes de IA (por exemplo, Cursor AI) construírem Agentes—aumento de produtividade de 10x!

- Para instalar, ```pip install pocketflow``` ou apenas copie o [código-fonte](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (apenas 100 linhas).
  
- Para saber mais, consulte a [documentação](https://the-pocket.github.io/PocketFlow/). Para entender a motivação, leia a [história](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
  
- 🎉 Junte-se ao nosso [discord](https://discord.gg/hUHHE9Sa6T)!

- 🎉 Graças a [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) e [@ZebraRoy](https://www.github.com/ZebraRoy), agora temos uma [versão TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript)!

## Por que Pocket Flow?

Os frameworks LLM atuais são inchados... Você só precisa de 100 linhas para um Framework LLM!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Abstração**          | **Wrappers Específicos de App**                                      | **Wrappers Específicos de Fornecedor**                                    | **Linhas**       | **Tamanho**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agente, Cadeia               | Muitos <br><sup><sub>(ex., QA, Sumarização)</sub></sup>              | Muitos <br><sup><sub>(ex., OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agente, Cadeia            | Muitos <br><sup><sub>(ex., FileReadTool, SerperDevTool)</sub></sup>         | Muitos <br><sup><sub>(ex., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agente                      | Alguns <br><sup><sub>(ex., CodeAgent, VisitWebTool)</sub></sup>         | Alguns <br><sup><sub>(ex., DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agente, Grafo           | Alguns <br><sup><sub>(ex., Busca Semântica)</sub></sup>                     | Alguns <br><sup><sub>(ex., PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agente                | Alguns <br><sup><sub>(ex., Agente de Ferramentas, Agente de Chat)</sub></sup>              | Muitos <sup><sub>[Opcional]<br> (ex., OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(apenas núcleo)</sub></sup>    | +26MB <br><sup><sub>(apenas núcleo)</sub></sup>          |
| **PocketFlow** | **Grafo**                    | **Nenhum**                                                 | **Nenhum**                                                  | **100**       | **+56KB**                  |

</div>

## Como funciona o Pocket Flow?

As [100 linhas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) capturam a abstração central dos frameworks LLM: Grafo!
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
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Iniciante*   | Um chatbot básico com histórico de conversas |
| [Saída Estruturada](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Iniciante* | Extraindo dados estruturados de currículos por prompt |
| [Fluxo de Trabalho](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Iniciante*   | Um fluxo de escrita que esboça, escreve conteúdo e aplica estilo |
| [Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Iniciante*   | Um agente de pesquisa que pode buscar na web e responder perguntas |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Iniciante*   | Um processo simples de Geração Aumentada por Recuperação |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *Iniciante* | Um processador de qualificação de currículo usando o padrão map-reduce para avaliação em lote |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Iniciante*   | Uma demonstração de streaming LLM em tempo real com capacidade de interrupção pelo usuário |
| [Guarda-rail de Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Iniciante*  | Um chatbot de consultoria de viagens que processa apenas consultas relacionadas a viagens |
| [Multi-Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Intermediário* | Um jogo de palavras Tabu para comunicação assíncrona entre dois agentes |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Intermediário* | O agente de pesquisa está ficando não confiável... Vamos construir um processo de supervisão|
| [Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Intermediário*   | Uma demonstração de execução paralela que mostra aceleração de 3x |
| [Fluxo Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Intermediário*   | Uma demonstração de processamento de imagem paralela mostrando aceleração de 8x com múltiplos filtros |
| [Voto por Maioria](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Intermediário* | Melhore a precisão do raciocínio agregando múltiplas tentativas de solução |
| [Pensamento](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Intermediário*   | Resolva problemas de raciocínio complexos através da Cadeia de Pensamento |
| [Memória](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Intermediário* | Um chatbot com memória de curto e longo prazo |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Intermediário* |  Agente usando Protocolo de Contexto de Modelo para operações numéricas |

</div>

👀 Quer ver outros tutoriais para iniciantes? [Crie uma issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## Como Usar Pocket Flow?

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
  
|  Nome do App     |  Dificuldade    | Tópicos  | Design Humano | Código do Agente |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Construir Cursor com Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Logo chegaremos à singularidade ...</sup></sub> | ★★★ <br> *Avançado*   | [Agente](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Doc de Design](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Código Flow](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Pergunte ao AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Pergunte ao AI Paul Graham, caso você não seja aceito</sup></sub> | ★★☆ <br> *Médio*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Doc de Design](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Código Flow](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Resumidor de Youtube](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Explica vídeos do YouTube como se você tivesse 5 anos </sup></sub> | ★☆☆ <br> *Iniciante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Doc de Design](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Código Flow](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Gerador de Aberturas Frias](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Quebra-gelos instantâneos que transformam leads frios em quentes </sup></sub> | ★☆☆ <br> *Iniciante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Busca Web](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Doc de Design](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Código Flow](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Quer aprender **Codificação Agêntica**?

  - Confira [meu YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) para tutorial em vídeo sobre como alguns aplicativos acima são feitos!

  - Quer construir seu próprio aplicativo LLM? Leia este [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Comece com [este modelo](https://github.com/The-Pocket/PocketFlow-Template-Python)!

  - Quer aprender os passos detalhados? Leia este [Guia](https://the-pocket.github.io/PocketFlow/guide.html)!