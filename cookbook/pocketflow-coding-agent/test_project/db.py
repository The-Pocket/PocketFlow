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
    ("WHITESPACE", r"\s+"),
    ("NUMBER",     r"\d+(?:\.\d+)?"),
    ("STRING",     r"'[^']*'"),
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
        return t[1].strip("'")
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
