import sqlite3
import time

import yaml  # Import yaml here as nodes use it

from pocketflow import Node
from utils.call_llm import call_llm


class GetSchema(Node):
    def prep(self, shared):
        return shared["db_path"]

    def exec(self, prep_res):
        conn = sqlite3.connect(prep_res)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        schema = []
        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            schema.append(f"Table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                schema.append(f"  - {col[1]} ({col[2]})")
            schema.append("")
        conn.close()
        return "\n".join(schema).strip()

    def post(self, shared, prep_res, exec_res):
        shared["schema"] = exec_res
        print("\n===== DB SCHEMA =====\n")
        print(exec_res)
        print("\n=====================\n")
        # return "default"

class GenerateSQL(Node):
    def prep(self, shared):
        return shared["natural_query"], shared["schema"]

    def exec(self, prep_res):
        natural_query, schema = prep_res
        prompt = f"""
Given SQLite schema:
{schema}

Question: "{natural_query}"

Respond ONLY with a YAML block containing the SQL query under the key 'sql':
```yaml
sql: |
  SELECT ...
```"""
        llm_response = call_llm(prompt)
        yaml_str = llm_response.split("```yaml")[1].split("```")[0].strip()
        structured_result = yaml.safe_load(yaml_str)
        sql_query = structured_result["sql"].strip().rstrip(';')
        return sql_query

    def post(self, shared, prep_res, exec_res):
        # exec_res is now the parsed SQL query string
        shared["generated_sql"] = exec_res
        # Reset debug attempts when *successfully* generating new SQL
        shared["debug_attempts"] = 0
        print(f"\n===== GENERATED SQL (Attempt {shared.get('debug_attempts', 0) + 1}) =====\n")
        print(exec_res)
        print("\n====================================\n")
        # return "default"

class ExecuteSQL(Node):
    def prep(self, shared):
        return shared["db_path"], shared["generated_sql"]

    def exec(self, prep_res):
        db_path, sql_query = prep_res
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            start_time = time.time()
            cursor.execute(sql_query)

            is_select = sql_query.strip().upper().startswith(("SELECT", "WITH"))
            if is_select:
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
            else:
                conn.commit()
                results = f"Query OK. Rows affected: {cursor.rowcount}"
                column_names = []
            conn.close()
            duration = time.time() - start_time
            print(f"SQL executed in {duration:.3f} seconds.")
            return (True, results, column_names)
        except sqlite3.Error as e:
            print(f"SQLite Error during execution: {e}")
            if 'conn' in locals() and conn:
                 try:
                     conn.close()
                 except Exception:
                     pass
            return (False, str(e), [])

    def post(self, shared, prep_res, exec_res):
        success, result_or_error, column_names = exec_res

        if success:
            shared["final_result"] = result_or_error
            shared["result_columns"] = column_names
            print("\n===== SQL EXECUTION SUCCESS =====\n")
            # (Same result printing logic as before)
            if isinstance(result_or_error, list):
                 if column_names: print(" | ".join(column_names)); print("-" * (sum(len(str(c)) for c in column_names) + 3 * (len(column_names) -1)))
                 if not result_or_error: print("(No results found)")
                 else:
                     for row in result_or_error: print(" | ".join(map(str, row)))
            else: print(result_or_error)
            print("\n=================================\n")
            return
        else:
            # Execution failed (SQLite error caught in exec)
            shared["execution_error"] = result_or_error # Store the error message
            shared["debug_attempts"] = shared.get("debug_attempts", 0) + 1
            max_attempts = shared.get("max_debug_attempts", 3) # Get max attempts from shared

            print(f"\n===== SQL EXECUTION FAILED (Attempt {shared['debug_attempts']}) =====\n")
            print(f"Error: {shared['execution_error']}")
            print("=========================================\n")

            if shared["debug_attempts"] >= max_attempts:
                print(f"Max debug attempts ({max_attempts}) reached. Stopping.")
                shared["final_error"] = f"Failed to execute SQL after {max_attempts} attempts. Last error: {shared['execution_error']}"
                return
            else:
                print("Attempting to debug the SQL...")
                return "error_retry" # Signal to go to DebugSQL

class DebugSQL(Node):
    def prep(self, shared):
        return (
            shared.get("natural_query"),
            shared.get("schema"),
            shared.get("generated_sql"),
            shared.get("execution_error")
        )

    def exec(self, prep_res):
        natural_query, schema, failed_sql, error_message = prep_res
        prompt = f"""
The following SQLite SQL query failed:
```sql
{failed_sql}
```
It was generated for: "{natural_query}"
Schema:
{schema}
Error: "{error_message}"

Provide a corrected SQLite query.

Respond ONLY with a YAML block containing the corrected SQL under the key 'sql':
```yaml
sql: |
  SELECT ... -- corrected query
```"""
        llm_response = call_llm(prompt)

        yaml_str = llm_response.split("```yaml")[1].split("```")[0].strip()
        structured_result = yaml.safe_load(yaml_str)
        corrected_sql = structured_result["sql"].strip().rstrip(';')
        return corrected_sql

    def post(self, shared, prep_res, exec_res):
        # exec_res is the corrected SQL string
        shared["generated_sql"] = exec_res # Overwrite with the new attempt
        shared.pop("execution_error", None) # Clear the previous error for the next ExecuteSQL attempt

        print(f"\n===== REVISED SQL (Attempt {shared.get('debug_attempts', 0) + 1}) =====\n")
        print(exec_res)
        print("\n====================================\n")