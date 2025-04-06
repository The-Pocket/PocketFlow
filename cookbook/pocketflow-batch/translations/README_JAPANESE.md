<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/title.png" width="600"/>
</div>


![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://the-pocket.github.io/PocketFlow/)
 <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

Pocket Flowは[100行](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)のミニマリストLLMフレームワークです

- **軽量**: わずか100行。余分なもの一切なし、依存関係なし、ベンダーロックインなし。
  
- **表現力**: あなたが好きなもの全て—([マルチ-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[エージェント](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[ワークフロー](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)など。

- **[エージェンティックコーディング](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: AIエージェント（例：Cursor AI）にエージェントを構築させる—生産性が10倍に！

- インストールするには、```pip install pocketflow```または[ソースコード](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)をコピーするだけです（わずか100行）。
  
- 詳細については[ドキュメント](https://the-pocket.github.io/PocketFlow/)をご覧ください。動機について学ぶには、[ストーリー](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just)をお読みください。
  
- 🎉 私たちの[Discord](https://discord.gg/hUHHE9Sa6T)に参加してください！

- 🎉 [@zvictor](https://www.github.com/zvictor)、[@jackylee941130](https://www.github.com/jackylee941130)、[@ZebraRoy](https://www.github.com/ZebraRoy)のおかげで、[TypeScriptバージョン](https://github.com/The-Pocket/PocketFlow-Typescript)もできました！

## なぜPocket Flow？

現在のLLMフレームワークは膨大すぎます... LLMフレームワークには100行だけで十分です！

<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/meme.jpg" width="400"/>


  |                | **抽象化**          | **アプリ固有のラッパー**                                      | **ベンダー固有のラッパー**                                    | **行数**       | **サイズ**    |
|----------------|:-----------------------------: |:-----------------------------------------------------------:|:------------------------------------------------------------:|:---------------:|:----------------------------:|
| LangChain  | エージェント、チェーン               | 多数 <br><sup><sub>(例：QA、要約)</sub></sup>              | 多数 <br><sup><sub>(例：OpenAI、Pineconeなど)</sub></sup>                   | 405K          | +166MB                     |
| CrewAI     | エージェント、チェーン            | 多数 <br><sup><sub>(例：FileReadTool、SerperDevTool)</sub></sup>         | 多数 <br><sup><sub>(例：OpenAI、Anthropic、Pineconeなど)</sub></sup>        | 18K           | +173MB                     |
| SmolAgent   | エージェント                      | いくつか <br><sup><sub>(例：CodeAgent、VisitWebTool)</sub></sup>         | いくつか <br><sup><sub>(例：DuckDuckGo、Hugging Faceなど)</sub></sup>           | 8K            | +198MB                     |
| LangGraph   | エージェント、グラフ           | いくつか <br><sup><sub>(例：セマンティック検索)</sub></sup>                     | いくつか <br><sup><sub>(例：PostgresStore、SqliteSaverなど) </sub></sup>        | 37K           | +51MB                      |
| AutoGen    | エージェント                | いくつか <br><sup><sub>(例：ツールエージェント、チャットエージェント)</sub></sup>              | 多数 <sup><sub>[オプション]<br> (例：OpenAI、Pineconeなど)</sub></sup>        | 7K <br><sup><sub>(コアのみ)</sub></sup>    | +26MB <br><sup><sub>(コアのみ)</sub></sup>          |
| **PocketFlow** | **グラフ**                    | **なし**                                                 | **なし**                                                  | **100**       | **+56KB**                  |

</div>

## Pocket Flowはどのように動作しますか？

[100行](https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py)のコードはLLMフレームワークの核となる抽象化を捉えています：グラフ！
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/abstraction.png" width="900"/>
</div>
<br>

そこから、([マルチ-](https://the-pocket.github.io/PocketFlow/design_pattern/multi_agent.html))[エージェント](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)、[ワークフロー](https://the-pocket.github.io/PocketFlow/design_pattern/workflow.html)、[RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)などの人気のあるデザインパターンを簡単に実装できます。
<br>
<div align="center">
  <img src="https://github.com/The-Pocket/.github/raw/main/assets/design.png" width="900"/>
</div>
<br>
✨ 以下は基本的なチュートリアルです：

<div align="center">
  
|  名前  | 難易度    |  説明  |  
| :-------------:  | :-------------: | :--------------------- |  
| [チャット](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat) | ☆☆☆ <br> *超簡単*   | 会話履歴を持つ基本的なチャットボット |
| [構造化出力](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-structured-output) | ☆☆☆ <br> *超簡単* | プロンプトによる履歴書からの構造化データの抽出 |
| [ワークフロー](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-workflow) | ☆☆☆ <br> *超簡単*   | 概要を作成し、コンテンツを書き、スタイルを適用するライティングワークフロー |
| [エージェント](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-agent) | ☆☆☆ <br> *超簡単*   | ウェブを検索して質問に答えることができる研究エージェント |
| [RAG](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-rag) | ☆☆☆ <br> *超簡単*   | シンプルな検索拡張生成プロセス |
| [マップ-リデュース](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-map-reduce) | ☆☆☆ <br> *超簡単* | バッチ評価のためのマップリデュースパターンを使用した履歴書資格処理 |
| [ストリーミング](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-llm-streaming) | ☆☆☆ <br> *超簡単*   | ユーザー中断機能を備えたリアルタイムLLMストリーミングデモ |
| [チャットガードレール](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-guardrail) | ☆☆☆ <br> *超簡単*  | 旅行関連のクエリのみを処理する旅行アドバイザーチャットボット |
| [マルチエージェント](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-multi-agent) | ★☆☆ <br> *初級* | 2つのエージェント間の非同期通信のためのタブーワードゲーム |
| [スーパーバイザー](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-supervisor) | ★☆☆ <br> *初級* | 研究エージェントが信頼性に欠ける場合... 監視プロセスを構築しましょう |
| [並列](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch) | ★☆☆ <br> *初級*   | 3倍の速度向上を示す並列実行デモ |
| [並列フロー](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-parallel-batch-flow) | ★☆☆ <br> *初級*   | 複数のフィルターで8倍の速度向上を示す並列画像処理デモ |
| [多数決](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-majority-vote) | ★☆☆ <br> *初級* | 複数の解決策を集約して推論精度を向上させる |
| [思考](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-thinking) | ★☆☆ <br> *初級*   | 思考連鎖を通じて複雑な推論問題を解決する |
| [メモリ](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-chat-memory) | ★☆☆ <br> *初級* | 短期および長期記憶を持つチャットボット |
| [MCP](https://github.com/The-Pocket/PocketFlow/tree/main/cookbook/pocketflow-mcp) | ★☆☆ <br> *初級* | 数値演算のためのモデルコンテキストプロトコルを使用するエージェント |

</div>

👀 他の超簡単なチュートリアルが見たいですか？[課題を作成してください！](https://github.com/The-Pocket/PocketFlow/issues/new)

## Pocket Flowの使い方は？

🚀 **エージェンティックコーディング**を通じて—最速のLLMアプリ開発パラダイムで、*人間が設計し*、*エージェントがコードを書く*！

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ 以下はより複雑なLLMアプリの例です：

<div align="center">
  
|  アプリ名     |  難易度    | トピック  | 人間による設計 | エージェントによるコード |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Cursorを使ってCursorを構築](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>もうすぐシンギュラリティに到達します...</sup></sub> | ★★★ <br> *上級*   | [エージェント](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html) | [設計書](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [フローコード](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [AI Paul Grahamに質問する](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>もし入れなかった場合は、AI Paul Grahamに聞いてみましょう</sup></sub> | ★★☆ <br> *中級*   | [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html) <br> [マップリデュース](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [TTS](https://the-pocket.github.io/PocketFlow/utility_function/text_to_speech.html) | [設計書](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [フローコード](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtubeサマライザー](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> 5歳児にもわかるようにYouTube動画を説明 </sup></sub> | ★☆☆ <br> *初級*   | [マップリデュース](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) |  [設計書](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [フローコード](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [コールドオープナージェネレーター](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> 冷たいリードを熱くする即席アイスブレーカー </sup></sub> | ★☆☆ <br> *初級*   | [マップリデュース](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html) <br> [Web検索](https://the-pocket.github.io/PocketFlow/utility_function/websearch.html) |  [設計書](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [フローコード](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- **エージェンティックコーディング**を学びたいですか？

  - 上記のアプリがどのように作られたかのビデオチュートリアルについては、[私のYouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)をチェックしてください！

  - 自分のLLMアプリを構築したいですか？この[投稿](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)を読んでください！[このテンプレート](https://github.com/The-Pocket/PocketFlow-Template-Python)から始めましょう！

  - 詳細な手順を学びたいですか？この[ガイド](https://the-pocket.github.io/PocketFlow/guide.html)を読んでください！