<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" alt="Pocket Flow – 100-line minimalist LLM framework" width="600"/>
</div>

<!-- [English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) -->

[English](https://github.com/The-Pocket/PocketFlow/blob/main/README.md) | [中文](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_CHINESE.md) | Español | [日本語](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_JAPANESE.md) | [Deutsch](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_GERMAN.md) | [Русский](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_RUSSIAN.md) | [Português](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_PORTUGUESE.md) | [Français](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_FRENCH.md) | [한국어](https://github.com/The-Pocket/PocketFlow/blob/main/cookbook/pocketflow-batch/translations/README_KOREAN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow es un framework minimalista de LLM de [100 líneas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)

- **Ligero**: Solo 100 líneas. Cero hinchazón, cero dependencias, cero vinculación a proveedores.
  
- **Expresivo**: Todo lo que amas—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Flujo de Trabajo](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), y más.

- **[Programación mediante Agentes](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Permite que los Agentes de IA (por ejemplo, Cursor AI) construyan Agentes—¡multiplicando la productividad por 10!

Comienza con Pocket Flow:
- Para instalar, ```pip install pocketflow``` o simplemente copia el [código fuente](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (solo 100 líneas).
- Para aprender más, consulta la [documentación](https://the-pocket.github.io/PocketFlow/). Para conocer la motivación, lee la [historia](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- ¿Tienes preguntas? Consulta este [Asistente de IA](https://chatgpt.com/g/g-677464af36588191b9eba4901946557b-pocket-flow-assistant), o [¡crea un issue!](https://github.com/The-Pocket/PocketFlow/issues/new)
- 🎉 ¡Únete a nuestro [Discord](https://discord.gg/hUHHE9Sa6T) para conectar con otros desarrolladores construyendo con Pocket Flow!
- 🎉 Pocket Flow inicialmente está en Python, ¡pero ahora tenemos versiones en [Typescript](https://github.com/The-Pocket/PocketFlow-Typescript), [Java](https://github.com/The-Pocket/PocketFlow-Java), [C++](https://github.com/The-Pocket/PocketFlow-CPP), [Go](https://github.com/The-Pocket/PocketFlow-Go), [Rust](https://github.com/The-Pocket/PocketFlow-Rust), [PHP](https://github.com/The-Pocket/PocketFlow-PHP) y [Dart](https://github.com/rag-wtf/PocketFlow-Dart)!

## ¿Por qué Pocket Flow?

Los frameworks actuales de LLM están sobrecargados... ¡Solo necesitas 100 líneas para un framework de LLM!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Abstracción**          | **Envolturas Específicas de Aplicación**                                      | **Envolturas Específicas de Proveedor**                                    | **Líneas**       | **Tamaño**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agente, Cadena               | Muchas <br><sup><sub>(p.ej., QA, Resumen)</sub></sup>              | Muchas <br><sup><sub>(p.ej., OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agente, Cadena            | Muchas <br><sup><sub>(p.ej., FileReadTool, SerperDevTool)</sub></sup>         | Muchas <br><sup><sub>(p.ej., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agente                      | Algunas <br><sup><sub>(p.ej., CodeAgent, VisitWebTool)</sub></sup>         | Algunas <br><sup><sub>(p.ej., DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agente, Grafo           | Algunas <br><sup><sub>(p.ej., Búsqueda Semántica)</sub></sup>                     | Algunas <br><sup><sub>(p.ej., PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agente                | Algunas <br><sup><sub>(p.ej., Tool Agent, Chat Agent)</sub></sup>              | Muchas <sup><sub>[Opcional]<br> (p.ej., OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(solo-núcleo)</sub></sup>    | +26MB <br><sup><sub>(solo-núcleo)</sub></sup>          |
| **PocketFlow** | **Grafo**                    | **Ninguna**                                                 | **Ninguna**                                                  | **100**       | **+56KB**                  |

</div>

## ¿Cómo funciona Pocket Flow?

Las [100 líneas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) capturan la abstracción principal de los frameworks de LLM: ¡el Grafo!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

A partir de ahí, es fácil implementar patrones de diseño populares como ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Flujo de Trabajo](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ A continuación se presentan tutoriales básicos:

<div align="center">
  
|  Nombre  | Dificultad    |  Descripción  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Principiante*   | Un chatbot básico con historial de conversación |
| [Salida Estructurada](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Principiante* | Extracción de datos estructurados de currículums mediante prompts |
| [Flujo de Trabajo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Principiante*   | Un flujo de escritura que esquematiza, escribe contenido y aplica estilo |
| [Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Principiante*   | Un agente de investigación que puede buscar en la web y responder preguntas |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Principiante*   | Un simple proceso de Generación aumentada por Recuperación |
| [Procesamiento por Lotes](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-batch) | ☆☆☆ <br> *Principiante* | Un procesador por lotes que traduce contenido markdown a múltiples idiomas |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Principiante*   | Una demostración de streaming LLM en tiempo real con capacidad de interrupción del usuario |
| [Protección de Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Principiante*  | Un chatbot asesor de viajes que solo procesa consultas relacionadas con viajes |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ★☆☆ <br> *Inicial* | Un procesador de calificación de currículums que utiliza el patrón map-reduce para evaluación por lotes |
| [Multi-Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Inicial* | Un juego de palabras Tabú para comunicación asíncrona entre dos agentes |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Inicial* | El agente de investigación se vuelve poco fiable... Construyamos un proceso de supervisión|
| [Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Inicial*   | Una demostración de ejecución paralela que muestra una aceleración de 3x |
| [Flujo Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Inicial*   | Una demostración de procesamiento de imágenes en paralelo que muestra una aceleración de 8x con múltiples filtros |
| [Voto por Mayoría](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Inicial* | Mejora de la precisión del razonamiento mediante la agregación de múltiples intentos de solución |
| [Pensamiento](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Inicial*   | Resolver problemas de razonamiento complejos a través de Cadena de Pensamiento |
| [Memoria](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Inicial* | Un chatbot con memoria a corto y largo plazo |
| [Text2SQL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-text2sql) | ★☆☆ <br> *Inicial* | Convertir lenguaje natural a consultas SQL con un bucle de auto-depuración |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Inicial* | Agente que utiliza el Protocolo de Contexto de Modelo para operaciones numéricas |
| [A2A](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-a2a) | ★☆☆ <br> *Inicial* | Agente envuelto con protocolo Agente-a-Agente para comunicación entre agentes |
| [Web HITL](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-web-hitl) | ★☆☆ <br> *Inicial* | Un servicio web mínimo para un bucle de revisión humana con actualizaciones SSE |

</div>

👀 ¿Quieres ver otros tutoriales para principiantes? [¡Crea un issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## ¿Cómo usar Pocket Flow?

🚀 A través de la **Programación mediante Agentes**—el paradigma de desarrollo de aplicaciones LLM más rápido- donde *los humanos diseñan* y *los agentes programan*!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ A continuación hay ejemplos de aplicaciones LLM más complejas:

<div align="center">
  
|  Nombre de la App     |  Dificultad    | Temas  | Diseño Humano | Código del Agente |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Construir Cursor con Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Pronto alcanzaremos la singularidad ...</sup></sub> | ★★★ <br> *Avanzado*   | [Agente](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Constructor de Conocimiento de Código Base](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge) <br> <sup><sub>La vida es demasiado corta para mirar el código de otros con confusión</sup></sub> |  ★★☆ <br> *Medio* | [Flujo de Trabajo](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html) | [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/flow.py)
| [Pregunta a AI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Pregunta a AI Paul Graham, en caso de que no entres</sup></sub> | ★★☆ <br> *Medio*  | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Doc de Diseño](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Resumidor de Youtube](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Explica videos de YouTube como si tuvieras 5 años </sup></sub> | ★☆☆ <br> *Principiante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Generador de Introducción para Email Frío](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Rompehielos instantáneos que convierten leads fríos en calientes </sup></sub> | ★☆☆ <br> *Principiante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Búsqueda Web](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- ¿Quieres aprender **Programación mediante Agentes**?

  - ¡Consulta [mi YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) para ver tutoriales en video sobre cómo se crearon algunas de las aplicaciones anteriores!

  - ¿Quieres construir tu propia aplicación LLM? ¡Lee este [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! ¡Comienza con [esta plantilla](https://github.com/The-Pocket/PocketFlow-Template-Python)!