from pocketflow import Node, Flow
from utils import TOOL_LIBRARY, TOOL_SEARCH_DEFINITION, handle_tool_search, handle_tool_exec, call_llm, create_all_tools_embedding, run_user_code
import yaml
import sys
from datetime import datetime

class ToolsNode(Node):
    def prep(self, shared):
        """Initialize and get tools"""
        # The question is now passed from main via shared
        tool_embeddings = create_all_tools_embedding()
        return shared["query"], shared["top_k"], tool_embeddings

    def exec(self, inputs):
        """Retrieve tools from the MCP server"""
        tool_query, top_k, tool_embeddings = inputs
        res = handle_tool_search(tool_query, top_k, tool_embeddings)
        return res

    def post(self, shared, prep_res, exec_res):
        """Store tools and process to decision node"""
        tools_search_result = exec_res
        shared["tools_search_result"] = tools_search_result
        return "reason"

class ReasonNode(Node):
    def prep(self, shared):
        """Prepare the prompt for LLM to process the question"""
        question = shared["question"]
        tools_search_result = shared.get("tools_search_result","no tool list")
        tools_exec_result = shared.get("tools_exec_result","no tool execute result")
        date = datetime.now().strftime("%Y-%m-%d")

        # Now is the time to combine with PocketFlow
        # refer from #77 of https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb
        prompt = f"""
#### PROMPT START

#### CONTEXT
You are a reasoning assistant.
CURRENT DATE:{date}
Question: {question}
Tool Recall List: {tools_search_result}
Tool Execute Result : {tools_exec_result}

#### ACTION SPACE
[1] tool_search
{TOOL_SEARCH_DEFINITION}

[2] tool_execute
Based on Tool Recall List and Question, use tool with proper parameters to answer Question.

[3] tool_execute_coding
When single tool calling is not enough to answer the Question, follow provided tool input schema to generate python code.
All your generated python code will be executed within single python file.
ONLY ALLOW to call provided tool, tool calling result will be provided with Tool Execute Result of next round.

[4] answer
Answer Question with proper reason

#### NEXT ACTION
Decide the next action based on the context and available actions.
Return your response in this format:

```yaml
thinking: |
    <your step-by-step reasoning process>
action: tool_search or tool_execute or tool_execute_coding or answer
reason: <why you chose this action>
query: <your_query_string if action is tool_search>
top_k: <your_top_k if action is tool_search>
tool_name: <your chosen tool name if action is tool_execute>
tool_param: <your chosen tool parameters if action is tool_execute>
code_block: <your generated tool calling python code if action is tool_execute_coding>
conclusion: <your answer content if action is answer>
```
IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character

#### END OF PROMPT
"""
        return prompt

    def exec(self, prompt):
        """Call LLM to process the question and decide which tool to use"""
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        return response

    def post(self, shared, prep_res, exec_res):
        """Extract decision from YAML and save to shared context"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            decision = yaml.safe_load(yaml_str)
            shared["action"] = decision["action"]
        except Exception as e:
            print(f"❌ Error parsing LLM response: {e}")
            print("Raw response:", exec_res)
            exit(1)
        if decision["action"] == "tool_search":
            shared["reason"] = decision["reason"]
            shared["query"] = decision["query"]
            shared["top_k"] = decision["top_k"]
            print(f"💡 Reason Node Decide to query tool with string: {decision['query']}")
            return "tool_search"
        elif decision["action"] == "tool_execute":
            shared["tool_name"] = decision["tool_name"]
            shared["tool_param"] = decision["tool_param"]
            print(f"💡 Reason Node Decide to use tool. \n 💡NAME: {decision['tool_name']} , PARAMS : {decision['tool_param']}")
            return "tool_execute"
        elif decision["action"] == "tool_execute_coding":
            shared["code_block"] = decision["code_block"]
            print(f"💡 Reason Node Decide to use tool coding \n 💡CODE : {decision['code_block']}")
            return "tool_execute_coding"
        elif decision["action"] == "answer":
            print(" 🟢 Reason Node Decide to answer ")
            shared["context"] = "Latest Reasonning : \n" + decision["thinking"] + "\n Tool Calling Result : \n" + decision["conclusion"]
            return "answer"
        else :
            print("Action NOT DEFINED !! ")
            exit(1)

class ExecuteToolNode(Node):
    def prep(self, shared):
        """Prepare tool execution parameters"""
        if shared["action"] == "tool_execute" :
            return shared["action"], shared["tool_name"], shared["tool_param"]
        elif shared["action"] == "tool_execute_coding" :
            print(" exec node : coding ")
            return shared["action"], shared["code_block"]
        else:
            print("  WRONG INPUT FOR EXEC NODE ")
            exit(1)

    def exec(self, inputs):
        """Execute the chosen tool"""
        if inputs[0] == "tool_execute" :
            intent, tool_name, parameters = inputs
            result = handle_tool_exec(tool_name, parameters)
        elif inputs[0] == "tool_execute_coding" :
            intent, code_block = inputs
            result = run_user_code(code_block)
        else :
            print("❌ no tool chosen or code generated")
            exit(1)

        return result

    def post(self, shared, prep_res, exec_res):
        print(f"\n✅ Tool Execution Result is : {exec_res}")
        shared["tools_exec_result"] = exec_res
        return "reason"


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
Conclusion: {context}

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

if __name__ == "__main__":
    # Default question
    default_question = "I want to know the latest price of NVDA/MSFT/QCOM"
    
    # Get question from command line if provided with --
    question = default_question
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            question = arg[2:]
            break
    
    print(f"🤔 Processing question: {question}")
    
    # Create nodes
    reason_node = ReasonNode()
    tools_node = ToolsNode()
    exec_node = ExecuteToolNode()
    answer_node = AnswerQuestion()
    
    # Connect nodes
    reason_node - "tool_search" >> tools_node
    tools_node - "reason" >> reason_node
    reason_node - "tool_execute" >> exec_node
    reason_node - "tool_execute_coding" >> exec_node
    exec_node - "reason" >> reason_node
    reason_node - "answer" >> answer_node
    
    # Create and run flow
    flow = Flow(start=reason_node)
    shared = {"question": question}
    flow.run(shared)
