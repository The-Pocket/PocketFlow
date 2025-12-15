from pocketflow import Node
from utils import call_llm, search_web_duckduckgo
import yaml
import re

class DecideAction(Node):
    def prep(self, shared):
        """Prepare the context and question for the decision-making process."""
        # Get the current context (default to "No previous search" if none exists)
        context = shared.get("context", "No previous search")
        # Get the question from the shared store
        question = shared["question"]
        # Return both for the exec step
        return question, context
        
    def exec(self, inputs):
        """Call the LLM to decide whether to search or answer."""
        question, context = inputs
        
        print(f"🤔 Agent deciding what to do next...")
        
        # Create a prompt to help the LLM decide what to do next with proper yaml formatting
        prompt = f"""
### CONTEXT
You are a research assistant that can search the web.
Question: {question}
Previous Research: {context}

### ACTION SPACE
[1] search
  Description: Look up more information on the web
  Parameters:
    - query (str): What to search for

[2] answer
  Description: Answer the question with current knowledge
  Parameters:
    - answer (str): Final answer to the question

## NEXT ACTION
Decide the next action based on the context and available actions.
Return your response in this format:

```yaml
thinking: |
    <your step-by-step reasoning process>
action: search OR answer
reason: |
    <why you chose this action - always use block scalar>
answer: |
    <if action is answer - always use block scalar, leave empty if searching>
search_query: <specific search query if action is search (plain string)>
```
IMPORTANT: Make sure to:
1. ALWAYS use the | block scalar for thinking, reason and answer so colons or quotes inside the text do not break YAML.
2. Use proper indentation (4 spaces) for all multi-line fields under |.
3. Keep search_query as a single line string without the | character.
"""
        
        # Call the LLM to make a decision
        response = call_llm(prompt)
        
        # Parse the response to get the decision
        def extract_yaml_block(text):
            """Extract YAML from a fenced code block, or fall back to the whole text."""
            match = re.search(r"```yaml(.*?)```", text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return text.strip()

        def parse_yaml_safely(block):
            """Parse YAML, retrying with block scalars if colon characters caused issues."""
            try:
                return yaml.safe_load(block)
            except yaml.YAMLError:
                fixed_lines = []
                for line in block.splitlines():
                    if re.match(r"^(thinking|reason|answer|search_query):", line) and "|" not in line:
                        key, _, val = line.partition(":")
                        fixed_lines.append(f"{key}: |")
                        val = val.strip()
                        if val:
                            fixed_lines.append(f"  {val}")
                    else:
                        fixed_lines.append(line)
                fixed_block = "\n".join(fixed_lines)
                try:
                    return yaml.safe_load(fixed_block)
                except yaml.YAMLError as exc:
                    raise ValueError(f"Unable to parse LLM YAML response:\n{block}") from exc

        yaml_str = extract_yaml_block(response)
        decision = parse_yaml_safely(yaml_str)
        
        return decision
    
    def post(self, shared, prep_res, exec_res):
        """Save the decision and determine the next step in the flow."""
        # If LLM decided to search, save the search query
        if exec_res["action"] == "search":
            shared["search_query"] = exec_res["search_query"]
            print(f"🔍 Agent decided to search for: {exec_res['search_query']}")
        else:
            shared["context"] = exec_res["answer"] #save the context if LLM gives the answer without searching.
            print(f"💡 Agent decided to answer the question")
        
        # Return the action to determine the next node in the flow
        return exec_res["action"]

class SearchWeb(Node):
    def prep(self, shared):
        """Get the search query from the shared store."""
        return shared["search_query"]
        
    def exec(self, search_query):
        """Search the web for the given query."""
        # Call the search utility function
        print(f"🌐 Searching the web for: {search_query}")
        results = search_web_duckduckgo(search_query)
        return results
    
    def post(self, shared, prep_res, exec_res):
        """Save the search results and go back to the decision node."""
        # Add the search results to the context in the shared store
        previous = shared.get("context", "")
        shared["context"] = previous + "\n\nSEARCH: " + shared["search_query"] + "\nRESULTS: " + exec_res
        
        print(f"📚 Found information, analyzing results...")
        
        # Always go back to the decision node after searching
        return "decide"

class AnswerQuestion(Node):
    def prep(self, shared):
        """Get the question and context for answering."""
        return shared["question"], shared.get("context", "")
        
    def exec(self, inputs):
        """Call the LLM to generate a final answer."""
        question, context = inputs
        
        print(f"✍️ Crafting final answer...")
        
        # Create a prompt for the LLM to answer the question
        prompt = f"""
### CONTEXT
Based on the following information, answer the question.
Question: {question}
Research: {context}

## YOUR ANSWER:
Provide a comprehensive answer using the research results.
"""
        # Call the LLM to generate an answer
        answer = call_llm(prompt)
        return answer
    
    def post(self, shared, prep_res, exec_res):
        """Save the final answer and complete the flow."""
        # Save the answer in the shared store
        shared["answer"] = exec_res
        
        print(f"✅ Answer generated successfully")
        
        # We're done - no need to continue the flow
        return "done" 
