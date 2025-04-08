<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flow — это минималистичный фреймворк для LLM, состоящий всего из [100 строк](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)

- **Легкий**: Всего 100 строк. Никакого избыточного кода, никаких зависимостей, никакой привязки к поставщикам.
  
- **Выразительный**: Всё, что вы любите — ([Мульти-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Агенты](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Рабочие процессы](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) и многое другое.

- **[Агентное программирование](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Позвольте ИИ-агентам (например, Cursor AI) создавать других агентов — повышение продуктивности в 10 раз!

- Для установки выполните ```pip install pocketflow``` или просто скопируйте [исходный код](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) (всего 100 строк).
  
- Чтобы узнать больше, ознакомьтесь с [документацией](https://the-pocket.github.io/PocketFlow/). Чтобы понять мотивацию, прочитайте [историю создания](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
  
- 🎉 Присоединяйтесь к нашему [Discord-серверу](https://discord.gg/hUHHE9Sa6T)!

- 🎉 Благодаря [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) и [@ZebraRoy](https://www.github.com/ZebraRoy), у нас теперь есть [версия на TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript)!

## Почему Pocket Flow?

Текущие фреймворки для LLM перегружены... Для фреймворка LLM вам нужно всего 100 строк!

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **Абстракция**          | **Специфичные обертки для приложений**                                      | **Специфичные обертки для вендоров**                                    | **Строк кода**       | **Размер**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | Agent, Chain               | Много <br><sup><sub>(напр., QA, Summarization)</sub></sup>              | Много <br><sup><sub>(напр., OpenAI, Pinecone и т.д.)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | Agent, Chain            | Много <br><sup><sub>(напр., FileReadTool, SerperDevTool)</sub></sup>         | Много <br><sup><sub>(напр., OpenAI, Anthropic, Pinecone и т.д.)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | Agent                      | Несколько <br><sup><sub>(напр., CodeAgent, VisitWebTool)</sub></sup>         | Несколько <br><sup><sub>(напр., DuckDuckGo, Hugging Face и т.д.)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | Agent, Graph           | Несколько <br><sup><sub>(напр., Semantic Search)</sub></sup>                     | Несколько <br><sup><sub>(напр., PostgresStore, SqliteSaver и т.д.) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | Agent                | Несколько <br><sup><sub>(напр., Tool Agent, Chat Agent)</sub></sup>              | Много <sup><sub>[Опционально]<br> (напр., OpenAI, Pinecone и т.д.)</sub></sup>        | 7K <br><sup><sub>(только ядро)</sub></sup>    | +26MB <br><sup><sub>(только ядро)</sub></sup>          |
| **PocketFlow** | **Graph**                    | **Нет**                                                 | **Нет**                                                  | **100**       | **+56KB**                  |

</div>

## Как работает Pocket Flow?

[100 строк](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py) охватывают основную абстракцию фреймворков LLM: Граф!
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

Отсюда легко реализовать популярные шаблоны проектирования, такие как ([Мульти-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[Агенты](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html), [Рабочие процессы](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html), [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) и т.д.
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ Ниже представлены базовые руководства:

<div align="center">
  
|  Название  | Сложность    |  Описание  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Чат](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *Простейший*   | Базовый чат-бот с историей разговора |
| [Структурированный вывод](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *Простейший* | Извлечение структурированных данных из резюме с помощью промптов |
| [Рабочий процесс](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *Простейший*   | Рабочий процесс создания текста, который составляет план, пишет контент и применяет стилистику |
| [Агент](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *Простейший*   | Исследовательский агент, который может искать в интернете и отвечать на вопросы |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *Простейший*   | Простой процесс генерации с извлечением (Retrieval-augmented Generation) |
| [Map-Reduce](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *Простейший* | Обработчик квалификаций резюме с использованием паттерна map-reduce для пакетной оценки |
| [Потоковая обработка](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *Простейший*   | Демонстрация потоковой обработки LLM в реальном времени с возможностью прерывания |
| [Ограничения чата](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *Простейший*  | Чат-бот для путешествий, обрабатывающий только запросы, связанные с путешествиями |
| [Мульти-агент](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *Начальный* | Игра в Табу для асинхронного общения между двумя агентами |
| [Супервизор](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *Начальный* | Исследовательский агент становится ненадежным... Построим процесс надзора |
| [Параллельное выполнение](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *Начальный*   | Демонстрация параллельного выполнения с ускорением в 3 раза |
| [Параллельный поток](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *Начальный*   | Демонстрация параллельной обработки изображений с ускорением в 8 раз при использовании нескольких фильтров |
| [Голосование большинством](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *Начальный* | Повышение точности рассуждений путем объединения нескольких попыток решения |
| [Мышление](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *Начальный*   | Решение сложных задач рассуждения с помощью цепочки мыслей (Chain-of-Thought) |
| [Память](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *Начальный* | Чат-бот с краткосрочной и долгосрочной памятью |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *Начальный* | Агент с использованием протокола контекста модели (Model Context Protocol) для числовых операций |

</div>

👀 Хотите увидеть другие руководства для начинающих? [Создайте задачу!](https://github.com/The-Pocket/PocketFlow/issues/new)

## Как использовать Pocket Flow?

🚀 Через **Агентное программирование** — самую быструю парадигму разработки LLM-приложений, где *люди проектируют*, а *агенты программируют*!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Ниже представлены примеры более сложных LLM-приложений:

<div align="center">
  
|  Название приложения     |  Сложность    | Темы  | Дизайн от человека | Код от агента |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Создаем Cursor с помощью Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Скоро достигнем сингулярности ...</sup></sub> | ★★★ <br> *Продвинутый*   | [Агент](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Спроси AI Пола Грэма](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Спроси AI Пола Грэма, если не попал в программу</sup></sub> | ★★☆ <br> *Средний*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [Дизайн-документ](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Объясняет YouTube-видео так, как будто вам 5 лет </sup></sub> | ★☆☆ <br> *Начальный*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Генератор "холодных" открытий](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Мгновенные ледоколы, превращающие холодные контакты в горячие </sup></sub> | ★☆☆ <br> *Начальный*   | [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Веб-поиск](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Хотите изучить **Агентное программирование**?

  - Посмотрите [мой YouTube-канал](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) для видеоуроков о том, как были созданы некоторые вышеуказанные приложения!

  - Хотите создать свое собственное LLM-приложение? Прочитайте эту [статью](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Начните с [этого шаблона](https://github.com/The-Pocket/PocketFlow-Template-Python)!

  - Хотите узнать подробные шаги? Прочитайте это [Руководство](https://the-pocket.github.io/PocketFlow/guide.html)!