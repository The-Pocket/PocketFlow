import yaml

from pocketflow import BatchNode, Node
from utils.call_llm import call_llm
from utils.code_executor import execute_python


class GenerateTestCases(Node):
    def prep(self, shared):
        return shared["problem"]

    def exec(self, prep_res):
        prompt = f"""Generate 5-7 test cases for this coding problem:

{prep_res}

Output in this YAML format with reasoning:
```yaml
reasoning: |
    The input parameters should be: param1 as a string, and param2 as a number.
    To test the function, I will consider basic cases, edge cases, and corner cases.
    For this problem, I need to test...
test_cases:
  - name: "Basic case"
    input: {{param1: value1, param2: value2}}
    expected: result1
  - name: "Edge case - empty"
    input: {{param1: value3, param2: value4}}
    expected: result2
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        assert "test_cases" in result, "Result must have 'test_cases' field"
        assert isinstance(result["test_cases"], list), "test_cases must be a list"
        
        for i, test_case in enumerate(result["test_cases"]):
            assert "name" in test_case, f"Test case {i} missing 'name' field"
            assert isinstance(test_case["name"], str), f"Test case {i} 'name' must be string"
            assert "input" in test_case, f"Test case {i} missing 'input' field"
            assert isinstance(test_case["input"], dict), f"Test case {i} 'input' must be dict"
            assert "expected" in test_case, f"Test case {i} missing 'expected' field"
        
        return result

    def post(self, shared, prep_res, exec_res):
        shared["test_cases"] = exec_res["test_cases"]
        
        # Print all generated test cases
        print(f"\n=== Generated {len(exec_res['test_cases'])} Test Cases ===")
        for i, test_case in enumerate(exec_res["test_cases"], 1):
            print(f"{i}. {test_case['name']}")
            print(f"   input: {test_case['input']}")
            print(f"   expected: {test_case['expected']}")

class ImplementFunction(Node):
    def prep(self, shared):
        return shared["problem"], shared["test_cases"]

    def exec(self, prep_res):
        problem, test_cases = prep_res
        
        # Format test cases nicely for the prompt
        formatted_tests = ""
        for i, test in enumerate(test_cases, 1):
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
        
        prompt = f"""Implement a solution for this problem:

{problem}

Test cases to consider:
{formatted_tests}

IMPORTANT: The function name must be exactly "run_code"

Output in this YAML format:
```yaml
reasoning: |
    To implement this function, I will...
    My approach is...
function_code: |
    def run_code(...):
        # your implementation
        return result
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        assert "function_code" in result, "Result must have 'function_code' field"
        assert isinstance(result["function_code"], str), "function_code must be string"
        assert "def run_code" in result["function_code"], "Function must be named 'run_code'"
        
        return result["function_code"]

    def post(self, shared, prep_res, exec_res):
        shared["function_code"] = exec_res
        
        # Print the implemented function
        print("\n=== Implemented Function ===")
        print(exec_res)

class RunTests(BatchNode):
    def prep(self, shared):
        function_code = shared["function_code"]
        test_cases = shared["test_cases"]
        # Return list of tuples (function_code, test_case)
        return [(function_code, test_case) for test_case in test_cases]

    def exec(self, prep_res):
        function_code, test_case = prep_res
        output, error = execute_python(function_code, test_case["input"])
        
        if error:
            return {
                "test_case": test_case,
                "passed": False,
                "actual": None,
                "expected": test_case["expected"],
                "error": error
            }
        
        passed = output == test_case["expected"]
        return {
            "test_case": test_case,
            "passed": passed,
            "actual": output,
            "expected": test_case["expected"],
            "error": None if passed else f"Expected {test_case['expected']}, got {output}"
        }

    def post(self, shared, prep_res, exec_res):
        shared["test_results"] = exec_res
        all_passed = all(result["passed"] for result in exec_res)
        shared["iteration_count"] = shared.get("iteration_count", 0) + 1
        
        # Print test results
        passed_count = len([r for r in exec_res if r["passed"]])
        total_count = len(exec_res)
        print(f"\n=== Test Results: {passed_count}/{total_count} Passed ===")
        
        failed_tests = [r for r in exec_res if not r["passed"]]
        if failed_tests:
            print("Failed tests:")
            for i, result in enumerate(failed_tests, 1):
                test_case = result['test_case']
                print(f"{i}. {test_case['name']}:")
                if result['error']:
                    print(f"   error: {result['error']}")
                else:
                    print(f"   output: {result['actual']}")
                print(f"   expected: {result['expected']}")
        
        if all_passed:
            return "success"
        elif shared["iteration_count"] >= shared.get("max_iterations", 5):
            return "max_iterations"
        else:
            return "failure"

class Revise(Node):
    def prep(self, shared):
        failed_tests = [r for r in shared["test_results"] if not r["passed"]]
        return {
            "problem": shared["problem"],
            "test_cases": shared["test_cases"],
            "function_code": shared["function_code"],
            "failed_tests": failed_tests
        }

    def exec(self, prep_res):
        # Format current test cases nicely
        formatted_tests = ""
        for i, test in enumerate(prep_res['test_cases'], 1):
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
        
        # Format failed tests nicely
        formatted_failures = ""
        for i, result in enumerate(prep_res['failed_tests'], 1):
            test_case = result['test_case']
            formatted_failures += f"{i}. {test_case['name']}:\n"
            if result['error']:
                formatted_failures += f"   error: {result['error']}\n"
            else:
                formatted_failures += f"   output: {result['actual']}\n"
            formatted_failures += f"   expected: {result['expected']}\n\n"

        prompt = f"""Problem: {prep_res['problem']}

Current test cases:
{formatted_tests}

Current function:
```python
{prep_res['function_code']}
```

Failed tests:
{formatted_failures}

Analyze the failures and output revisions in YAML. You can revise test cases, function code, or both:

```yaml
reasoning: |
    Looking at the failures, I see that...
    The issue appears to be...
    I will revise...
test_cases:  # Dictionary mapping test case index (1-based) to revised test case
  1:
    name: "Revised test name"
    input: {{...}}
    expected: ...
function_code: |  # Include this if revising function
  def run_code(...):
    return ...
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        if "test_cases" in result:
            assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"
            for index_str, test_case in result["test_cases"].items():
                assert isinstance(index_str, (str, int)), "test_cases keys must be strings or ints"
                assert "name" in test_case, f"Revised test case {index_str} missing 'name' field"
                assert "input" in test_case, f"Revised test case {index_str} missing 'input' field"
                assert "expected" in test_case, f"Revised test case {index_str} missing 'expected' field"
        
        if "function_code" in result:
            assert isinstance(result["function_code"], str), "function_code must be string"
            assert "def run_code" in result["function_code"], "Function must be named 'run_code'"
        
        return result

    def post(self, shared, prep_res, exec_res):
        # Print what is being revised
        print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")
        
        # Handle test case revisions - map indices to actual test cases
        if "test_cases" in exec_res:
            current_tests = shared["test_cases"].copy()
            print("Revising test cases:")
            for index_str, revised_test in exec_res["test_cases"].items():
                index = int(index_str) - 1  # Convert to 0-based
                if 0 <= index < len(current_tests):
                    old_test = current_tests[index]
                    print(f"  Test {index_str}: '{old_test['name']}' -> '{revised_test['name']}'")
                    print(f"    old input: {old_test['input']}")
                    print(f"    new input: {revised_test['input']}")
                    print(f"    old expected: {old_test['expected']}")
                    print(f"    new expected: {revised_test['expected']}")
                    current_tests[index] = revised_test
            shared["test_cases"] = current_tests
            
        if "function_code" in exec_res:
            print("Revising function code:")
            print("New function:")
            print(exec_res["function_code"])
            shared["function_code"] = exec_res["function_code"] 