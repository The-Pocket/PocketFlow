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
        tokens = tokenize("SELECT * FROM t WHERE name = \'Alice\'")
        assert ("STRING", "\'Alice\'") in tokens

    def test_string_with_spaces(self):
        tokens = tokenize("SELECT * FROM t WHERE city = \'New York\'")
        assert ("STRING", "\'New York\'") in tokens


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
