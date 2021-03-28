import pytest
import query_comparisions as qcomp

def test_number_one():
    a = "SELECT MAX(col_1) FROM table"
    b = "SELECT MAX(col_1+1) FROM table"
    assert qcomp.compare_queries_classes(a,b) == False

def test_number_two():
    a = "SELECT MAX(col_1 + 1) FROM table"
    b = "SELECT MAX(col_1 + 2)"
    assert qcomp.compare_queries_classes(a,b) == True

def test_number_three():
    a = "SELECT MAX(col_1) FROM table"
    b = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    assert qcomp.compare_queries_classes(a, b) == False

def test_number_four():
    a = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1 + 1) FROM table GROUP BY col_3"
    assert qcomp.compare_queries_classes(a, b) == False

def test_number_five():
    a = "SELECT MAX(col_1 + 2) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1 + 1) FROM table GROUP BY col_2"
    assert qcomp.compare_queries_classes(a, b) == True

def test_number_six():
    a = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1) FROM table GROUP BY col_3"
    assert qcomp.compare_queries_classes(a, b) == False

