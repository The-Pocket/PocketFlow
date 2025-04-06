<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow es un framework minimalista para LLM de [100 líneas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)

- **Ligero**: Solo 100 líneas. Cero redundancia, cero dependencias, cero bloqueo de proveedor.
  
- **Expresivo**: Todo lo que te gusta—([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Flujo de trabajo](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), y más.

- **[Programación Agéntica](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Deja que los Agentes de IA (por ejemplo, Cursor AI) construyan Agentes—¡potencia tu productividad 10 veces!

- Para instalar, ```pip install pocketflow``` o simplemente copia el [código fuente](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (solo 100 líneas).
  
- Para saber más, consulta la [documentación](https://the-pocket.github.io/PocketFlow/). Para conocer la motivación, lee la [historia](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
  
- 🎉 ¡Únete a nuestro [discord](https://discord.gg/hUHHE9Sa6T)!

- 🎉 Gracias a [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) y [@ZebraRoy](https://www.github.com/ZebraRoy), ¡ahora tenemos una [versión TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript)!

## ¿Por qué Pocket Flow?

Los frameworks LLM actuales están sobrecargados... ¡Solo necesitas 100 líneas para un Framework LLM!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Abstracción**          | **Envoltorios específicos de aplicación**                                      | **Envoltorios específicos de proveedor**                                    | **Líneas**       | **Tamaño**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agente, Cadena               | Muchos <br><sup><sub>(p.ej., QA, Resumen)</sub></sup>              | Muchos <br><sup><sub>(p.ej., OpenAI, Pinecone, etc.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agente, Cadena            | Muchos <br><sup><sub>(p.ej., FileReadTool, SerperDevTool)</sub></sup>         | Muchos <br><sup><sub>(p.ej., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agente                      | Algunos <br><sup><sub>(p.ej., CodeAgent, VisitWebTool)</sub></sup>         | Algunos <br><sup><sub>(p.ej., DuckDuckGo, Hugging Face, etc.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agente, Grafo           | Algunos <br><sup><sub>(p.ej., Búsqueda Semántica)</sub></sup>                     | Algunos <br><sup><sub>(p.ej., PostgresStore, SqliteSaver, etc.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agente                | Algunos <br><sup><sub>(p.ej., Tool Agent, Chat Agent)</sub></sup>              | Muchos <sup><sub>[Opcional]<br> (p.ej., OpenAI, Pinecone, etc.)</sub></sup>        | 7K <br><sup><sub>(solo núcleo)</sub></sup>    | +26MB <br><sup><sub>(solo núcleo)</sub></sup>          |
| **PocketFlow** | **Grafo**                    | **Ninguno**                                                 | **Ninguno**                                                  | **100**       | **+56KB**                  |

</div>

## ¿Cómo funciona Pocket Flow?

Las [100 líneas](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) capturan la abstracción central de los frameworks LLM: ¡Grafo!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

A partir de ahí, es fácil implementar patrones de diseño populares como ([Multi-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Agentes](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Flujo de trabajo](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html), etc.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ A continuación se presentan tutoriales básicos:

<div align="center">
  
|  Nombre  | Dificultad    |  Descripción  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Novato*   | Un bot de chat básico con historial de conversación |
| [Salida Estructurada](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Novato* | Extracción de datos estructurados de currículums mediante prompts |
| [Flujo de Trabajo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Novato*   | Un flujo de escritura que esquematiza, escribe contenido y aplica estilo |
| [Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Novato*   | Un agente de investigación que puede buscar en la web y responder preguntas |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Novato*   | Un proceso simple de Generación aumentada por Recuperación |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *Novato* | Un procesador de calificación de currículums usando el patrón map-reduce para evaluación por lotes |
| [Streaming](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Novato*   | Una demo de streaming LLM en tiempo real con capacidad de interrupción por el usuario |
| [Chat con Barreras](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Novato*  | Un chatbot asesor de viajes que solo procesa consultas relacionadas con viajes |
| [Multi-Agente](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Principiante* | Un juego de palabras tabú para comunicación asíncrona entre dos agentes |
| [Supervisor](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Principiante* | El agente de investigación se está volviendo poco fiable... ¡Construyamos un proceso de supervisión! |
| [Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Principiante*   | Una demo de ejecución paralela que muestra una aceleración de 3x |
| [Flujo Paralelo](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Principiante*   | Una demo de procesamiento de imágenes en paralelo que muestra una aceleración de 8x con múltiples filtros |
| [Voto por Mayoría](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Principiante* | Mejora la precisión del razonamiento agregando múltiples intentos de solución |
| [Pensamiento](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Principiante*   | Resuelve problemas de razonamiento complejos a través de Cadena de Pensamiento |
| [Memoria](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Principiante* | Un bot de chat con memoria a corto y largo plazo |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Principiante* | Agente que usa el Protocolo de Contexto de Modelo para operaciones numéricas |

</div>

👀 ¿Quieres ver otros tutoriales para novatos? [¡Crea un issue!](https://github.com/The-Pocket/PocketFlow/issues/new)

## ¿Cómo usar Pocket Flow?

🚀 A través de **Programación Agéntica** — el paradigma de desarrollo de aplicaciones LLM más rápido — donde *los humanos diseñan* y *los agentes programan*!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ A continuación hay ejemplos de aplicaciones LLM más complejas:

<div align="center">
  
|  Nombre de la App     |  Dificultad    | Temas  | Diseño Humano | Código de Agente |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Construir Cursor con Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Pronto llegaremos a la singularidad...</sup></sub> | ★★★ <br> *Avanzado*   | [Agente](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Pregunta a IA Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Pregunta a IA Paul Graham, en caso de que no entres</sup></sub> | ★★☆ <br> *Medio*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Doc de Diseño](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Resumidor de Youtube](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Te explica videos de YouTube como si tuvieras 5 años </sup></sub> | ★☆☆ <br> *Principiante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Generador de Introducción Fría](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Rompehielos instantáneos que calientan contactos fríos </sup></sub> | ★☆☆ <br> *Principiante*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Búsqueda Web](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Doc de Diseño](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Código de Flujo](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- ¿Quieres aprender **Programación Agéntica**?

  - ¡Consulta [mi YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) para tutoriales en video sobre cómo se hicieron algunas aplicaciones anteriores!

  - ¿Quieres construir tu propia aplicación LLM? ¡Lee este [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! ¡Comienza con [esta plantilla](https://github.com/The-Pocket/PocketFlow-Template-Python)!

  - ¿Quieres aprender los pasos detallados? ¡Lee esta [Guía](https://the-pocket.github.io/PocketFlow/guide.html)!