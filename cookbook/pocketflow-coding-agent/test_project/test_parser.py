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
        ast = parse("SELECT * FROM employees WHERE name = \'Alice Johnson\'")
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
        ast = parse("SELECT * FROM employees WHERE name LIKE \'Alice%\'")
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
