# nodes.py

import yaml

from pocketflow import Node
from utils import call_llm


class ThinkNode(Node):
    def prep(self, shared):
        """Prepare the context needed for thinking"""
        query = shared.get("query", "")
        observations = shared.get("observations", [])
        thoughts = shared.get("thoughts", [])
        current_thought_number = shared.get("current_thought_number", 0)
        
        # Update thought count
        shared["current_thought_number"] = current_thought_number + 1
        
        # Format previous observations
        observations_text = "\n".join([f"Observation {i+1}: {obs}" for i, obs in enumerate(observations)])
        if not observations_text:
            observations_text = "No observations yet."
            
        return {
            "query": query,
            "observations_text": observations_text,
            "thoughts": thoughts,
            "current_thought_number": current_thought_number + 1
        }
    
    def exec(self, prep_res):
        """Execute the thinking process, decide the next action"""
        query = prep_res["query"]
        observations_text = prep_res["observations_text"]
        current_thought_number = prep_res["current_thought_number"]
        
        # Build the prompt
        prompt = f"""
        You are an AI assistant solving a problem. Based on the user's query and previous observations, think about what action to take next.
        
        User query: {query}
        
        Previous observations:
        {observations_text}
        
        Please think about the next action and return your thinking process and decision in YAML format:
        ```yaml
        thinking: |
            <detailed thinking process>
        action: <action name, such as 'search' or 'answer'>
        action_input: <input parameters for the action>
        is_final: <set to true if this is the final answer, otherwise false>
        ```
        """
        
        # Call LLM to get thinking result
        response = call_llm(prompt)
        
        # Parse YAML response
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        thought_data = yaml.safe_load(yaml_str)
        
        # Add thought number
        thought_data["thought_number"] = current_thought_number
        
        return thought_data
    
    def post(self, shared, prep_res, exec_res):
        """Save the thinking result and decide the next step in the flow"""
        # Save thinking result
        if "thoughts" not in shared:
            shared["thoughts"] = []
        shared["thoughts"].append(exec_res)
        
        # Save action information
        shared["current_action"] = exec_res["action"]
        shared["current_action_input"] = exec_res["action_input"]
        
        # If it's the final answer, end the flow
        if exec_res.get("is_final", False):
            shared["final_answer"] = exec_res["action_input"]
            print(f"🎯 Final Answer: {exec_res['action_input']}")
            return "end"
        
        # Otherwise continue with the action
        print(f"🤔 Thought {exec_res['thought_number']}: Decided to execute {exec_res['action']}")
        return "action"

class ActionNode(Node):
    def prep(self, shared):
        """Prepare to execute action"""
        action = shared["current_action"]
        action_input = shared["current_action_input"]
        return action, action_input
    
    def exec(self, prep_res):
        """Execute action and return result"""
        action, action_input = prep_res
        
        print(f"🚀 Executing action: {action}, input: {action_input}")
        
        # Execute different operations based on action type
        if action == "search":
            # Simulate search operation
            result = self.search_web(action_input)
        elif action == "calculate":
            # Simulate calculation operation
            result = self.calculate(action_input)
        elif action == "answer":
            # Direct return answer
            result = action_input
        else:
            # Unknown action type
            result = f"Unknown action type: {action}"
        
        return result
    
    def post(self, shared, prep_res, exec_res):
        """Save action result"""
        # Save the current action result
        shared["current_action_result"] = exec_res
        print("✅ Action completed, result obtained")
        
        # Continue to observation node
        return "observe"
    
    # Simulated tool functions
    def search_web(self, query):
        # This should be actual search logic
        return f"Search results: Information about '{query}'..."
    
    def calculate(self, expression):
        # This should be actual calculation logic
        try:
            return f"Calculation result: {eval(expression)}"
        except:
            return f"Unable to calculate expression: {expression}"

class ObserveNode(Node):
    def prep(self, shared):
        """Prepare observation data"""
        action = shared["current_action"]
        action_input = shared["current_action_input"]
        action_result = shared["current_action_result"]
        return action, action_input, action_result
    
    def exec(self, prep_res):
        """Analyze action results, generate observation"""
        action, action_input, action_result = prep_res
        
        # Build prompt
        prompt = f"""
        You are an observer, needing to analyze action results and provide objective observations.
        
        Action: {action}
        Action input: {action_input}
        Action result: {action_result}
        
        Please provide a concise observation of this result. Don't make decisions, just describe what you see.
        """
        
        # Call LLM to get observation result
        observation = call_llm(prompt)
        
        print(f"👁️ Observation: {observation[:50]}...")
        return observation
    
    def post(self, shared, prep_res, exec_res):
        """Save observation result and decide next flow step"""
        # Save observation result
        if "observations" not in shared:
            shared["observations"] = []
        shared["observations"].append(exec_res)
        
        # Continue thinking
        return "think"
    

    
class EndNode(Node):
    def prep(self, shared):
        """Prepare end node"""
        
        return {}
    def exec(self, prep_res):
        """Execute end operation"""
        print("Flow ended, thank you for using!")
        return None
    def post(self, shared, prep_res, exec_res):
        """End flow"""
        return None