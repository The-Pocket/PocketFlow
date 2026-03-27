"""
Setup script that creates a mini SQL database project with skeleton code and tests.
The coding agent's task is to implement the skeleton functions to make all tests pass.
"""

import os

WORKDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_project")

# ─── CSV Data ────────────────────────────────────────────────────────────────

EMPLOYEES_CSV = """\
id,name,department_id,salary,hire_date,manager_id
1,Alice Johnson,1,95000,2019-03-15,
2,Bob Smith,1,87000,2020-06-01,1
3,Carol Williams,2,72000,2021-01-10,4
4,David Brown,2,91000,2018-11-20,
5,Eve Davis,3,68000,2022-04-05,6
6,Frank Miller,3,105000,2017-08-30,
7,Grace Lee,1,78000,2023-02-14,1
8,Henry Wilson,2,83000,2020-09-22,4
9,Ivy Chen,3,71000,2021-07-18,6
10,Jack Taylor,1,92000,2019-12-01,1
"""

DEPARTMENTS_CSV = """\
id,name,budget,location
1,Engineering,500000,Building A
2,Marketing,300000,Building B
3,Sales,250000,Building C
4,HR,150000,Building A
"""

PROJECTS_CSV = """\
id,name,department_id,status,start_date
1,Project Alpha,1,active,2023-01-15
2,Project Beta,1,completed,2022-06-01
3,Campaign X,2,active,2023-03-20
4,Campaign Y,2,paused,2023-05-10
5,Sales Push,3,active,2023-02-28
6,Onboarding,4,active,2023-04-01
"""

# ─── database.py (CSV loader — working, no TODOs) ──────────────────────────

DATABASE_PY = '''\
"""Simple CSV-based database loader."""

import csv
import os

_tables = {}

def load_csv(name, filepath):
    """Load a CSV file as a named table."""
    rows = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Auto-convert numeric fields
            converted = {}
            for k, v in row.items():
                if v == "":
                    converted[k] = None
                else:
                    try:
                        converted[k] = int(v)
                    except ValueError:
                        try:
                            converted[k] = float(v)
                        except ValueError:
                            converted[k] = v
            rows.append(converted)
    _tables[name] = rows
    return rows

def get_table(name):
    """Return loaded table by name."""
    if name not in _tables:
        raise ValueError(f"Table \\'{name}\\' not loaded. Call load_csv first.")
    return [dict(r) for r in _tables[name]]

def init_db(data_dir=None):
    """Load all CSV files from data_dir (defaults to script directory)."""
    if data_dir is None:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in os.listdir(data_dir):
        if fname.endswith(".csv"):
            table_name = fname[:-4]
            load_csv(table_name, os.path.join(data_dir, fname))
    return list(_tables.keys())

def reset():
    """Clear all loaded tables."""
    _tables.clear()
'''

# ─── db.py (tokenizer + parser + executor skeleton) ────────────────────────

DB_PY = '''\
"""
Mini SQL Engine — tokenizer, parser, and executor for a subset of SQL.

Supports: SELECT, FROM, WHERE, JOIN, LEFT JOIN, GROUP BY, HAVING,
          ORDER BY, LIMIT, DISTINCT, aliases, aggregates (COUNT, SUM, AVG, MIN, MAX),
          comparison operators (=, !=, <, >, <=, >=),
          logical operators (AND, OR, NOT), IN, BETWEEN, LIKE, IS NULL, IS NOT NULL.

The tokenizer is fully implemented. The parser and executor contain skeleton
functions marked with TODO that need to be implemented.
"""

import re
from database import get_table

# ═══════════════════════════════════════════════════════════════════════════════
# TOKENIZER (fully implemented)
# ═══════════════════════════════════════════════════════════════════════════════

KEYWORDS = {
    "SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "JOIN", "LEFT", "RIGHT",
    "INNER", "ON", "GROUP", "BY", "HAVING", "ORDER", "ASC", "DESC", "LIMIT",
    "AS", "DISTINCT", "IN", "BETWEEN", "LIKE", "IS", "NULL", "COUNT", "SUM",
    "AVG", "MIN", "MAX",
}

TOKEN_PATTERNS = [
    ("WHITESPACE", r"\\s+"),
    ("NUMBER",     r"\\d+(?:\\.\\d+)?"),
    ("STRING",     r"\'[^\']*\'"),
    ("CMP",        r"!=|<=|>=|<>"),
    ("SYMBOL",     r"[=<>(),.*]"),
    ("KEYWORD",    None),  # handled in tokenize()
    ("IDENT",      r"[a-zA-Z_][a-zA-Z0-9_]*"),
]

def tokenize(sql):
    """
    Tokenize a SQL string into a list of (type, value) tuples.
    Whitespace tokens are filtered out. Identifiers matching keywords
    are re-tagged as KEYWORD tokens.
    """
    tokens = []
    pos = 0
    while pos < len(sql):
        match = None
        for ttype, pattern in TOKEN_PATTERNS:
            if pattern is None:
                continue
            m = re.match(pattern, sql[pos:])
            if m:
                val = m.group(0)
                if ttype == "IDENT" and val.upper() in KEYWORDS:
                    ttype = "KEYWORD"
                    val = val.upper()
                if ttype != "WHITESPACE":
                    tokens.append((ttype, val))
                pos += len(m.group(0))
                match = True
                break
        if not match:
            raise SyntaxError(f"Unexpected character at position {pos}: {sql[pos]!r}")
    return tokens


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER (skeleton — implement the TODO functions)
# ═══════════════════════════════════════════════════════════════════════════════

class Stream:
    """Token stream with peek/consume helpers."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def consume(self, expected_type=None, expected_value=None):
        t = self.peek()
        if expected_type and t[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type} but got {t[0]} ({t[1]!r}) at pos {self.pos}")
        if expected_value and t[1] != expected_value:
            raise SyntaxError(f"Expected {expected_value!r} but got {t[1]!r} at pos {self.pos}")
        self.pos += 1
        return t

    def match(self, ttype, value=None):
        t = self.peek()
        if t[0] == ttype and (value is None or t[1] == value):
            return True
        return False

    def match_keyword(self, *values):
        t = self.peek()
        return t[0] == "KEYWORD" and t[1] in values

    def at_end(self):
        return self.pos >= len(self.tokens)


def parse(sql):
    """Parse a SQL string into an AST dict."""
    tokens = tokenize(sql)
    stream = Stream(tokens)
    ast = parse_select(stream)
    return ast


# ── Provided helper: parse a dotted name like "employees.name" ──────────────

def _parse_dotted_name(stream):
    """Parse an identifier, possibly with a dot (table.column)."""
    name = stream.consume("IDENT")[1]
    if stream.match("SYMBOL", "."):
        stream.consume()
        right = stream.consume("IDENT")[1]
        return f"{name}.{right}"
    return name


def parse_select(stream):
    """
    Parse a full SELECT statement and return an AST dict.

    TODO: Implement this function.

    The returned AST should be a dict with these keys:
      - "type": "select"
      - "distinct": bool
      - "columns": list from parse_select_columns()
      - "from": table name (string)
      - "alias": table alias or None
      - "joins": list of join dicts from parse_join()
      - "where": condition AST or None, from parse_condition()
      - "group_by": list of column name strings, or None
      - "having": condition AST or None
      - "order_by": list of {"column": str, "direction": "ASC"/"DESC"} or None
      - "limit": int or None

    Parsing order:
      1. Consume SELECT keyword
      2. Check for DISTINCT keyword
      3. Parse columns with parse_select_columns()
      4. Consume FROM keyword and table name (IDENT)
      5. Check for optional alias (AS keyword + IDENT, or just bare IDENT that
         is not a keyword)
      6. Parse any JOINs with parse_join() (loop while next is JOIN/LEFT/INNER/RIGHT)
      7. If WHERE keyword, consume it and parse_condition()
      8. If GROUP keyword, consume GROUP, BY, then parse_column_list()
      9. If HAVING keyword, consume it and parse_condition()
     10. If ORDER keyword, consume ORDER, BY, then parse_order_by()
     11. If LIMIT keyword, consume it and parse the NUMBER
     12. Return the AST dict
    """
    # TODO: Implement this function
    pass


def parse_select_columns(stream):
    """
    Parse the column list after SELECT (before FROM).

    TODO: Implement this function.

    Returns a list of column dicts from parse_select_column().
    Columns are separated by commas (SYMBOL ',').
    Keep parsing columns while the next token is a comma.
    """
    # TODO: Implement this function
    pass


def parse_select_column(stream):
    """
    Parse a single column expression in a SELECT clause.

    TODO: Implement this function.

    Returns a dict with keys:
      - "expr": the expression (string like "name", "e.name", or "*")
      - "alias": alias string or None
      - "aggregate": aggregate function name ("COUNT","SUM","AVG","MIN","MAX") or None

    Cases to handle (in order):
      1. Star (*): SYMBOL "*" -> {"expr": "*", "alias": None, "aggregate": None}
      2. Aggregate: KEYWORD(COUNT/SUM/AVG/MIN/MAX), SYMBOL "(",
         then either SYMBOL "*" or a dotted_name, SYMBOL ")",
         optional alias (AS + IDENT).
         -> {"expr": inner_expr, "alias": alias_or_None, "aggregate": func_name}
      3. Regular column: a dotted_name, optional alias (AS + IDENT).
         -> {"expr": name, "alias": alias_or_None, "aggregate": None}
    """
    # TODO: Implement this function
    pass


def parse_join(stream):
    """
    Parse a single JOIN clause.

    TODO: Implement this function.

    Returns a dict with keys:
      - "type": "JOIN" or "LEFT JOIN"
      - "table": table name string
      - "alias": table alias or None
      - "on": condition AST from parse_condition()

    Steps:
      1. Determine join type: if LEFT keyword, consume it -> "LEFT JOIN",
         if INNER keyword, consume it -> "JOIN", else "JOIN"
      2. Consume JOIN keyword
      3. Consume table name (IDENT)
      4. Check for optional alias (AS + IDENT, or bare IDENT that is not a keyword)
      5. Consume ON keyword
      6. Parse condition with parse_condition()
    """
    # TODO: Implement this function
    pass


# ── Provided helpers for parsing ────────────────────────────────────────────

def parse_value(stream):
    """Parse a literal value (number or string)."""
    t = stream.peek()
    if t[0] == "NUMBER":
        stream.consume()
        return int(t[1]) if "." not in t[1] else float(t[1])
    if t[0] == "STRING":
        stream.consume()
        return t[1].strip("\'")
    raise SyntaxError(f"Expected value but got {t}")


def parse_column_list(stream):
    """Parse a comma-separated list of column names (for GROUP BY)."""
    cols = [_parse_dotted_name(stream)]
    while stream.match("SYMBOL", ","):
        stream.consume()
        cols.append(_parse_dotted_name(stream))
    return cols


def parse_order_by(stream):
    """Parse ORDER BY clause entries."""
    result = []
    while True:
        col = _parse_dotted_name(stream)
        direction = "ASC"
        if stream.match_keyword("ASC"):
            stream.consume()
        elif stream.match_keyword("DESC"):
            stream.consume()
            direction = "DESC"
        result.append({"column": col, "direction": direction})
        if stream.match("SYMBOL", ","):
            stream.consume()
        else:
            break
    return result


def parse_condition(stream):
    """
    Parse a WHERE/ON/HAVING condition expression.

    TODO: Implement this function.

    Returns an AST node (dict) representing the condition.

    This function handles OR-level precedence:
      - Parse left side with _parse_and(stream)
      - While next token is OR keyword, consume it, parse right with _parse_and(),
        and combine: {"type": "or", "left": left, "right": right}
      - Return the result

    You also need to implement _parse_and(stream):
      - Parse left side with parse_comparison(stream)
      - While next token is AND keyword, consume it, parse right with parse_comparison(),
        and combine: {"type": "and", "left": left, "right": right}
      - Return the result
    """
    # TODO: Implement this function (and _parse_and helper)
    pass


def parse_comparison(stream):
    """
    Parse a single comparison expression.

    TODO: Implement this function.

    Returns a condition AST dict.

    Cases to handle (in order of checking):

    1. Parenthesized expression: SYMBOL "(" -> consume, parse_condition(), consume SYMBOL ")"
    2. NOT: KEYWORD "NOT" -> consume, parse_comparison(), return {"type": "not", "expr": inner}
    3. Column-based comparisons - parse left side as _parse_dotted_name(stream), then:
       a. IS NULL: KEYWORD "IS", KEYWORD "NULL"
          -> {"type": "is_null", "column": left}
       b. IS NOT NULL: KEYWORD "IS", KEYWORD "NOT", KEYWORD "NULL"
          -> {"type": "is_not_null", "column": left}
       c. IN: KEYWORD "IN", SYMBOL "(", list of parse_value() separated by commas, SYMBOL ")"
          -> {"type": "in", "column": left, "values": [...]}
       d. BETWEEN: KEYWORD "BETWEEN", parse_value(), KEYWORD "AND", parse_value()
          -> {"type": "between", "column": left, "low": val1, "high": val2}
       e. LIKE: KEYWORD "LIKE", parse_value()
          -> {"type": "like", "column": left, "pattern": val}
       f. Regular comparison: CMP or SYMBOL(=,<,>) operator, then parse right side.
          Right side can be a dotted name (IDENT) or a value (NUMBER/STRING).
          -> {"type": "comparison", "left": left, "op": op, "right": right_val}
    """
    # TODO: Implement this function
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTOR (skeleton — implement the TODO functions)
# ═══════════════════════════════════════════════════════════════════════════════

def execute(ast):
    """
    Execute a parsed AST and return a list of result row dicts.

    TODO: Implement this function.

    Steps:
      1. Get rows from the "from" table using get_table(ast["from"])
      2. If the table has an alias, prefix all keys: {alias.col: val, col: val}
         Also keep the original unprefixed keys.
      3. For each join in ast["joins"], call execute_join(rows, join)
      4. If ast["where"] is not None, filter rows using evaluate_condition()
      5. If ast["group_by"] is not None, call execute_group_by()
      6. Else, call execute_select(rows, ast["columns"]) for non-grouped selects
      7. If ast["order_by"] is not None, call execute_order_by()
      8. If ast["distinct"], remove duplicate rows (use list of tuples of sorted items)
      9. If ast["limit"] is not None, slice the rows
     10. Return the result rows
    """
    # TODO: Implement this function
    pass


def execute_join(left_rows, join):
    """
    Execute a JOIN operation.

    TODO: Implement this function.

    Args:
        left_rows: list of row dicts (from the left table)
        join: a join AST dict with keys "type", "table", "alias", "on"

    Returns: list of merged row dicts

    Steps:
      1. Get right table rows using get_table(join["table"])
      2. If join has an alias, prefix right-row keys with alias (like in execute)
      3. For each left row, try to match with each right row:
         - Merge the two dicts into a combined row
         - Evaluate the ON condition with evaluate_condition(combined, join["on"])
         - If match, add combined to results
      4. For LEFT JOIN: if a left row matched nothing, add left row merged with
         None values for all right-table keys
      5. Return results
    """
    # TODO: Implement this function
    pass


def execute_select(rows, columns):
    """
    Apply SELECT column projection to rows.

    TODO: Implement this function.

    Args:
        rows: list of row dicts
        columns: list of column AST dicts with keys "expr", "alias", "aggregate"

    Returns: list of projected row dicts

    Steps:
      1. If columns is [{"expr": "*", ...}], return rows as-is
      2. For aggregate columns without GROUP BY (e.g., SELECT COUNT(*) FROM t):
         - If any column has aggregate != None, compute over all rows:
           COUNT(*) = len(rows), COUNT(col) = count non-None, SUM/AVG/MIN/MAX as expected
         - Return a single-row list with the aggregated values
         - Use the alias if provided, else "AGG(expr)" as key name
      3. For non-aggregate columns: project each row to only include the selected
         columns, using alias as the key name if provided, else the expr
         - _resolve(row, col["expr"]) to get the value
    """
    # TODO: Implement this function
    pass


def execute_group_by(rows, group_cols, select_cols, having=None):
    """
    Execute GROUP BY with aggregates.

    TODO: Implement this function.

    Args:
        rows: list of row dicts
        group_cols: list of column name strings to group by
        select_cols: list of column AST dicts from the SELECT clause
        having: condition AST or None

    Returns: list of result row dicts (one per group)

    Steps:
      1. Build groups: a dict mapping group_key tuple -> list of rows
         group_key = tuple(_resolve(row, col) for col in group_cols)
      2. For each group, build a result row:
         - For each select_col:
           a. If aggregate, compute it over the group rows using _aggregate()
              Key = alias or "AGG(expr)"
           b. Else, take the value from the first row in the group
              Key = alias or expr
      3. If having is not None, filter result rows with evaluate_condition()
      4. Return result rows
    """
    # TODO: Implement this function
    pass


def execute_order_by(rows, order_by):
    """
    Sort rows according to ORDER BY clause.

    TODO: Implement this function.

    Args:
        rows: list of row dicts
        order_by: list of {"column": str, "direction": "ASC"/"DESC"}

    Returns: sorted list of row dicts

    Use _sort_key helper to build sort keys, then sort with reverse=False
    since _sort_key handles direction internally. Actually, the simplest
    approach: sort rows using a key function that returns a tuple.
    For each order_by entry, resolve the column value.
    Sort ascending by default; for DESC, you can negate numbers or use
    multiple sorted() passes (sort is stable).

    Simplest: use _sort_key(row, order_by) as the key function.
    """
    # TODO: Implement this function
    pass


def evaluate_condition(row, cond):
    """
    Evaluate a condition AST against a row.

    TODO: Implement this function.

    Args:
        row: a dict representing a data row
        cond: a condition AST dict

    Returns: bool

    Handle each condition type:
      - "comparison": resolve left and right, use _compare(left, op, right)
      - "and": evaluate left AND right (both must be True)
      - "or": evaluate left OR right (either can be True)
      - "not": negate the inner expression
      - "is_null": _resolve(row, cond["column"]) is None
      - "is_not_null": _resolve(row, cond["column"]) is not None
      - "in": _resolve(row, cond["column"]) in cond["values"]
      - "between": low <= _resolve(row, cond["column"]) <= high
      - "like": convert SQL LIKE pattern to regex (% -> .*, _ -> .)
                and match against _resolve(row, cond["column"])
    """
    # TODO: Implement this function
    pass


# ── Provided helpers for execution ──────────────────────────────────────────

def _resolve(row, col_name):
    """Resolve a column name against a row dict. Supports dotted names."""
    if col_name in row:
        return row[col_name]
    # Try without table prefix
    if "." in col_name:
        _, short = col_name.split(".", 1)
        if short in row:
            return row[short]
    # Try matching with any table prefix
    for key in row:
        if "." in key and key.split(".", 1)[1] == col_name:
            return row[key]
    return None


def _compare(left, op, right):
    """Compare two values with the given operator."""
    if left is None or right is None:
        return False
    ops = {
        "=": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<>": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
    }
    return ops[op](left, right)


def _sort_key(row, order_by):
    """Build a sort key tuple for a row given ORDER BY spec."""
    key = []
    for spec in order_by:
        val = _resolve(row, spec["column"])
        if val is None:
            val = ""
        key.append(val)
    return tuple(key)


def _aggregate(func, rows, expr):
    """Compute an aggregate function over rows for a given expression."""
    if func == "COUNT":
        if expr == "*":
            return len(rows)
        return sum(1 for r in rows if _resolve(r, expr) is not None)
    values = [_resolve(r, expr) for r in rows]
    values = [v for v in values if v is not None]
    if not values:
        return None
    if func == "SUM":
        return sum(values)
    if func == "AVG":
        return sum(values) / len(values)
    if func == "MIN":
        return min(values)
    if func == "MAX":
        return max(values)
    raise ValueError(f"Unknown aggregate: {func}")
'''

# ─── Test: Tokenizer ───────────────────────────────────────────────────────

TEST_TOKENIZER_PY = '''\
"""Tests for the SQL tokenizer."""

import pytest
from db import tokenize


class TestTokenizeBasicSelect:
    def test_simple_select(self):
        tokens = tokenize("SELECT name FROM employees")
        assert tokens == [
            ("KEYWORD", "SELECT"),
            ("IDENT", "name"),
            ("KEYWORD", "FROM"),
            ("IDENT", "employees"),
        ]

    def test_select_star(self):
        tokens = tokenize("SELECT * FROM employees")
        assert ("SYMBOL", "*") in tokens

    def test_select_multiple_columns(self):
        tokens = tokenize("SELECT name, salary FROM employees")
        assert ("SYMBOL", ",") in tokens
        assert ("IDENT", "name") in tokens
        assert ("IDENT", "salary") in tokens


class TestTokenizeNumbers:
    def test_integer(self):
        tokens = tokenize("SELECT * FROM t WHERE id = 42")
        assert ("NUMBER", "42") in tokens

    def test_decimal(self):
        tokens = tokenize("SELECT * FROM t WHERE price > 9.99")
        assert ("NUMBER", "9.99") in tokens


class TestTokenizeStrings:
    def test_single_quoted_string(self):
        tokens = tokenize("SELECT * FROM t WHERE name = \\'Alice\\'")
        assert ("STRING", "\\'Alice\\'") in tokens

    def test_string_with_spaces(self):
        tokens = tokenize("SELECT * FROM t WHERE city = \\'New York\\'")
        assert ("STRING", "\\'New York\\'") in tokens


class TestTokenizeOperators:
    def test_equals(self):
        tokens = tokenize("WHERE x = 1")
        assert ("SYMBOL", "=") in tokens

    def test_not_equals(self):
        tokens = tokenize("WHERE x != 1")
        assert ("CMP", "!=") in tokens

    def test_less_than_or_equal(self):
        tokens = tokenize("WHERE x <= 10")
        assert ("CMP", "<=") in tokens

    def test_greater_than_or_equal(self):
        tokens = tokenize("WHERE x >= 5")
        assert ("CMP", ">=") in tokens

    def test_less_than(self):
        tokens = tokenize("WHERE x < 10")
        assert ("SYMBOL", "<") in tokens

    def test_greater_than(self):
        tokens = tokenize("WHERE x > 5")
        assert ("SYMBOL", ">") in tokens


class TestTokenizeKeywords:
    def test_keywords_case_insensitive(self):
        tokens = tokenize("select name from employees where salary > 50000")
        types = [t[0] for t in tokens]
        assert types.count("KEYWORD") >= 3

    def test_all_keywords(self):
        sql = "SELECT DISTINCT name FROM t JOIN t2 ON t.id = t2.id WHERE x > 1 GROUP BY name HAVING COUNT(*) > 1 ORDER BY name ASC LIMIT 10"
        tokens = tokenize(sql)
        kw_values = [t[1] for t in tokens if t[0] == "KEYWORD"]
        for kw in ["SELECT", "DISTINCT", "FROM", "JOIN", "ON", "WHERE", "GROUP", "BY", "HAVING", "COUNT", "ORDER", "ASC", "LIMIT"]:
            assert kw in kw_values


class TestTokenizeDottedNames:
    def test_dotted_identifier(self):
        tokens = tokenize("SELECT e.name FROM employees e")
        # The tokenizer splits "e.name" into IDENT "e", SYMBOL ".", IDENT "name"
        assert ("IDENT", "e") in tokens
        assert ("SYMBOL", ".") in tokens
        assert ("IDENT", "name") in tokens

    def test_dotted_name_in_condition(self):
        tokens = tokenize("WHERE employees.salary > 50000")
        assert ("IDENT", "employees") in tokens
        assert ("SYMBOL", ".") in tokens
        assert ("IDENT", "salary") in tokens


class TestTokenizeComplexQueries:
    def test_complex_query(self):
        sql = "SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id WHERE e.salary > 50000 ORDER BY e.salary DESC LIMIT 5"
        tokens = tokenize(sql)
        assert len(tokens) > 20  # Should have many tokens
        assert tokens[0] == ("KEYWORD", "SELECT")

    def test_aggregate_in_query(self):
        sql = "SELECT department_id, COUNT(*) FROM employees GROUP BY department_id"
        tokens = tokenize(sql)
        assert ("KEYWORD", "COUNT") in tokens
        assert ("SYMBOL", "(") in tokens
        assert ("SYMBOL", ")") in tokens

    def test_between_query(self):
        sql = "SELECT * FROM employees WHERE salary BETWEEN 50000 AND 100000"
        tokens = tokenize(sql)
        assert ("KEYWORD", "BETWEEN") in tokens
        assert ("KEYWORD", "AND") in tokens
'''

# ─── Test: Parser ───────────────────────────────────────────────────────────

TEST_PARSER_PY = '''\
"""Tests for the SQL parser."""

import pytest
from db import parse


class TestParseBasicSelect:
    def test_select_star(self):
        ast = parse("SELECT * FROM employees")
        assert ast["type"] == "select"
        assert ast["columns"][0]["expr"] == "*"
        assert ast["from"] == "employees"

    def test_single_column(self):
        ast = parse("SELECT name FROM employees")
        assert len(ast["columns"]) == 1
        assert ast["columns"][0]["expr"] == "name"
        assert ast["columns"][0]["aggregate"] is None

    def test_multiple_columns(self):
        ast = parse("SELECT name, salary, hire_date FROM employees")
        assert len(ast["columns"]) == 3
        exprs = [c["expr"] for c in ast["columns"]]
        assert exprs == ["name", "salary", "hire_date"]


class TestParseWhere:
    def test_simple_where(self):
        ast = parse("SELECT * FROM employees WHERE salary > 80000")
        assert ast["where"] is not None
        assert ast["where"]["type"] == "comparison"
        assert ast["where"]["left"] == "salary"
        assert ast["where"]["op"] == ">"
        assert ast["where"]["right"] == 80000

    def test_where_with_string(self):
        ast = parse("SELECT * FROM employees WHERE name = \\'Alice Johnson\\'")
        assert ast["where"]["right"] == "Alice Johnson"

    def test_where_and(self):
        ast = parse("SELECT * FROM employees WHERE salary > 70000 AND department_id = 1")
        assert ast["where"]["type"] == "and"

    def test_where_or(self):
        ast = parse("SELECT * FROM employees WHERE department_id = 1 OR department_id = 2")
        assert ast["where"]["type"] == "or"


class TestParseAggregates:
    def test_count_star(self):
        ast = parse("SELECT COUNT(*) FROM employees")
        assert ast["columns"][0]["aggregate"] == "COUNT"
        assert ast["columns"][0]["expr"] == "*"

    def test_aggregate_with_alias(self):
        ast = parse("SELECT AVG(salary) AS avg_salary FROM employees")
        col = ast["columns"][0]
        assert col["aggregate"] == "AVG"
        assert col["expr"] == "salary"
        assert col["alias"] == "avg_salary"

    def test_sum_aggregate(self):
        ast = parse("SELECT SUM(salary) FROM employees")
        assert ast["columns"][0]["aggregate"] == "SUM"


class TestParseGroupBy:
    def test_group_by(self):
        ast = parse("SELECT department_id, COUNT(*) FROM employees GROUP BY department_id")
        assert ast["group_by"] == ["department_id"]

    def test_group_by_having(self):
        ast = parse("SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*) > 2")
        assert ast["group_by"] == ["department_id"]
        assert ast["having"] is not None


class TestParseOrderBy:
    def test_order_by_asc(self):
        ast = parse("SELECT * FROM employees ORDER BY salary ASC")
        assert ast["order_by"][0]["column"] == "salary"
        assert ast["order_by"][0]["direction"] == "ASC"

    def test_order_by_desc(self):
        ast = parse("SELECT * FROM employees ORDER BY salary DESC")
        assert ast["order_by"][0]["direction"] == "DESC"

    def test_order_by_default_asc(self):
        ast = parse("SELECT * FROM employees ORDER BY name")
        assert ast["order_by"][0]["direction"] == "ASC"


class TestParseLimit:
    def test_limit(self):
        ast = parse("SELECT * FROM employees LIMIT 5")
        assert ast["limit"] == 5


class TestParseJoin:
    def test_simple_join(self):
        ast = parse("SELECT * FROM employees JOIN departments ON employees.department_id = departments.id")
        assert len(ast["joins"]) == 1
        assert ast["joins"][0]["type"] == "JOIN"
        assert ast["joins"][0]["table"] == "departments"

    def test_left_join(self):
        ast = parse("SELECT * FROM employees LEFT JOIN departments ON employees.department_id = departments.id")
        assert ast["joins"][0]["type"] == "LEFT JOIN"


class TestParseDistinct:
    def test_distinct(self):
        ast = parse("SELECT DISTINCT department_id FROM employees")
        assert ast["distinct"] is True

    def test_no_distinct(self):
        ast = parse("SELECT department_id FROM employees")
        assert ast["distinct"] is False


class TestParseSpecialConditions:
    def test_in_clause(self):
        ast = parse("SELECT * FROM employees WHERE department_id IN (1, 2, 3)")
        assert ast["where"]["type"] == "in"
        assert ast["where"]["values"] == [1, 2, 3]

    def test_between(self):
        ast = parse("SELECT * FROM employees WHERE salary BETWEEN 60000 AND 90000")
        assert ast["where"]["type"] == "between"
        assert ast["where"]["low"] == 60000
        assert ast["where"]["high"] == 90000

    def test_like(self):
        ast = parse("SELECT * FROM employees WHERE name LIKE \\'Alice%\\'")
        assert ast["where"]["type"] == "like"
        assert ast["where"]["pattern"] == "Alice%"

    def test_is_null(self):
        ast = parse("SELECT * FROM employees WHERE manager_id IS NULL")
        assert ast["where"]["type"] == "is_null"
        assert ast["where"]["column"] == "manager_id"

    def test_is_not_null(self):
        ast = parse("SELECT * FROM employees WHERE manager_id IS NOT NULL")
        assert ast["where"]["type"] == "is_not_null"


class TestParseAlias:
    def test_table_alias(self):
        ast = parse("SELECT e.name FROM employees AS e")
        assert ast["alias"] == "e"
        assert ast["from"] == "employees"

    def test_join_alias(self):
        ast = parse("SELECT * FROM employees AS e JOIN departments AS d ON e.department_id = d.id")
        assert ast["alias"] == "e"
        assert ast["joins"][0]["alias"] == "d"
'''

# ─── Test: Executor ─────────────────────────────────────────────────────────

TEST_EXECUTOR_PY = '''\
"""Tests for the SQL executor."""

import pytest
import os
from database import init_db, reset
from db import parse, execute


@pytest.fixture(autouse=True)
def setup_db():
    reset()
    init_db(os.path.dirname(os.path.abspath(__file__)))
    yield
    reset()


class TestExecuteBasicSelect:
    def test_select_all(self):
        ast = parse("SELECT * FROM employees")
        rows = execute(ast)
        assert len(rows) == 10

    def test_select_single_column(self):
        ast = parse("SELECT name FROM employees")
        rows = execute(ast)
        assert len(rows) == 10
        assert "name" in rows[0]

    def test_select_multiple_columns(self):
        ast = parse("SELECT name, salary FROM employees")
        rows = execute(ast)
        assert set(rows[0].keys()) == {"name", "salary"}


class TestExecuteWhere:
    def test_where_greater_than(self):
        ast = parse("SELECT * FROM employees WHERE salary > 90000")
        rows = execute(ast)
        assert all(r["salary"] > 90000 for r in rows)
        assert len(rows) == 3  # Alice(95k), David(91k), Frank(105k)

    def test_where_equals(self):
        ast = parse("SELECT * FROM employees WHERE department_id = 1")
        rows = execute(ast)
        assert len(rows) == 4  # Alice, Bob, Grace, Jack

    def test_where_string_equals(self):
        ast = parse("SELECT * FROM employees WHERE name = \\'Alice Johnson\\'")
        rows = execute(ast)
        assert len(rows) == 1
        assert rows[0]["name"] == "Alice Johnson"

    def test_where_and(self):
        ast = parse("SELECT * FROM employees WHERE department_id = 1 AND salary > 90000")
        rows = execute(ast)
        assert len(rows) == 2  # Alice(95k), Jack(92k)


class TestExecuteOrderBy:
    def test_order_by_asc(self):
        ast = parse("SELECT name, salary FROM employees ORDER BY salary ASC")
        rows = execute(ast)
        salaries = [r["salary"] for r in rows]
        assert salaries == sorted(salaries)

    def test_order_by_desc(self):
        ast = parse("SELECT name, salary FROM employees ORDER BY salary DESC")
        rows = execute(ast)
        salaries = [r["salary"] for r in rows]
        assert salaries == sorted(salaries, reverse=True)


class TestExecuteLimit:
    def test_limit(self):
        ast = parse("SELECT * FROM employees ORDER BY salary DESC LIMIT 3")
        rows = execute(ast)
        assert len(rows) == 3

    def test_limit_with_where(self):
        ast = parse("SELECT * FROM employees WHERE department_id = 1 LIMIT 2")
        rows = execute(ast)
        assert len(rows) == 2


class TestExecuteGroupBy:
    def test_group_by_count(self):
        ast = parse("SELECT department_id, COUNT(*) AS cnt FROM employees GROUP BY department_id")
        rows = execute(ast)
        assert len(rows) == 3  # departments 1,2,3
        counts = {r["department_id"]: r["cnt"] for r in rows}
        assert counts[1] == 4  # Alice, Bob, Grace, Jack
        assert counts[2] == 3  # Carol, David, Henry
        assert counts[3] == 3  # Eve, Frank, Ivy

    def test_group_by_avg(self):
        ast = parse("SELECT department_id, AVG(salary) AS avg_sal FROM employees GROUP BY department_id")
        rows = execute(ast)
        dept1 = next(r for r in rows if r["department_id"] == 1)
        assert dept1["avg_sal"] == (95000 + 87000 + 78000 + 92000) / 4

    def test_group_by_having(self):
        ast = parse("SELECT department_id, COUNT(*) AS cnt FROM employees GROUP BY department_id HAVING COUNT(*) >= 4")
        rows = execute(ast)
        assert len(rows) == 1
        assert rows[0]["department_id"] == 1


class TestExecuteJoin:
    def test_inner_join(self):
        ast = parse("SELECT employees.name, departments.name FROM employees JOIN departments ON employees.department_id = departments.id")
        rows = execute(ast)
        assert len(rows) == 10  # All employees have valid departments

    def test_left_join(self):
        ast = parse("SELECT departments.name, projects.name FROM departments LEFT JOIN projects ON departments.id = projects.department_id")
        rows = execute(ast)
        assert len(rows) >= 6  # At least all projects, plus HR may have one


class TestExecuteDistinct:
    def test_distinct(self):
        ast = parse("SELECT DISTINCT department_id FROM employees")
        rows = execute(ast)
        assert len(rows) == 3  # Only 3 unique departments

    def test_distinct_vs_non_distinct(self):
        ast1 = parse("SELECT department_id FROM employees")
        ast2 = parse("SELECT DISTINCT department_id FROM employees")
        rows1 = execute(ast1)
        rows2 = execute(ast2)
        assert len(rows1) > len(rows2)


class TestExecuteAggregatesWithoutGroupBy:
    def test_count_all(self):
        ast = parse("SELECT COUNT(*) AS total FROM employees")
        rows = execute(ast)
        assert len(rows) == 1
        assert rows[0]["total"] == 10

    def test_max_salary(self):
        ast = parse("SELECT MAX(salary) AS max_sal FROM employees")
        rows = execute(ast)
        assert rows[0]["max_sal"] == 105000

    def test_min_salary(self):
        ast = parse("SELECT MIN(salary) AS min_sal FROM employees")
        rows = execute(ast)
        assert rows[0]["min_sal"] == 68000
'''


# ─── Setup Function ────────────────────────────────────────────────────────

def setup_test_project():
    """Create the test project directory with all files."""
    os.makedirs(WORKDIR, exist_ok=True)

    files = {
        "employees.csv": EMPLOYEES_CSV,
        "departments.csv": DEPARTMENTS_CSV,
        "projects.csv": PROJECTS_CSV,
        "database.py": DATABASE_PY,
        "db.py": DB_PY,
        "test_tokenizer.py": TEST_TOKENIZER_PY,
        "test_parser.py": TEST_PARSER_PY,
        "test_executor.py": TEST_EXECUTOR_PY,
    }

    for filename, content in files.items():
        filepath = os.path.join(WORKDIR, filename)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"✅ Test project created in {WORKDIR}")
    print(f"   Files: {', '.join(files.keys())}")
    return WORKDIR


if __name__ == "__main__":
    setup_test_project()
