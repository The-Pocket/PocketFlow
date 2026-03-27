from pocketflow import Node
from utils import call_llm, DOCS
import yaml

class DecideAction(Node):
    def prep(self, shared):
        """Read the question, accumulated context, and available doc names."""
        return shared["question"], shared.get("context", ""), list(DOCS.keys())

    def exec(self, inputs):
        """Ask the LLM whether to read another doc or answer the question."""
        question, context, available = inputs

        prompt = f"""You are an agentic RAG assistant. You have access to a set of documents about PocketFlow.
Your job is to decide whether you have enough context to answer the question, or if you need to read another document.

Question: {question}
Available documents: {available}
Context already gathered: {context if context else 'nothing yet'}

If you have enough information to answer the question, set action to 'answer'.
Otherwise, pick one document to read next. Output ONLY valid yaml:

```yaml
action: read
doc: document_name
```

OR

```yaml
action: answer
```"""
        resp = call_llm(prompt)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        return yaml.safe_load(yaml_str)

    def post(self, shared, prep_res, exec_res):
        """Route to 'read' or 'answer' based on the LLM decision."""
        if exec_res["action"] == "read":
            shared["doc_to_read"] = exec_res.get("doc", "")
            print(f"  🔍 Agent decides to read '{shared['doc_to_read']}'")
        else:
            print(f"  💡 Agent decides it has enough context to answer")
        return exec_res["action"]


class ReadDoc(Node):
    def prep(self, shared):
        """Get the document name to read."""
        return shared["doc_to_read"]

    def exec(self, doc_name):
        """Retrieve the document content from the store."""
        print(f"  📄 Reading document: {doc_name}")
        return DOCS.get(doc_name, "Document not found.")

    def post(self, shared, prep_res, exec_res):
        """Append the document content to the accumulated context."""
        shared["context"] = shared.get("context", "") + f"\n[{prep_res}]: {exec_res}"
        print(f"  ✅ Added '{prep_res}' to context")
        return "decide"


class Answer(Node):
    def prep(self, shared):
        """Get the question and accumulated context."""
        return shared["question"], shared.get("context", "")

    def exec(self, inputs):
        """Generate the final answer using the accumulated context."""
        question, context = inputs
        print(f"  ✍️ Generating answer...")
        return call_llm(
            f"Based on this context:\n{context}\n\nAnswer the following question concisely and accurately: {question}"
        )

    def post(self, shared, prep_res, exec_res):
        """Store the final answer."""
        shared["answer"] = exec_res
