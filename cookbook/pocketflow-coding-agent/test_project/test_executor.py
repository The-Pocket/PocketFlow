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
        ast = parse("SELECT * FROM employees WHERE name = \'Alice Johnson\'")
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
