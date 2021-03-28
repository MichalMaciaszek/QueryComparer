import re
import pytest

def get_arguments_for_max_and_groupby(splitted_query):                                          #gets info about max and groupby arguments
    funcs_with_arguments = []
    for index, element in enumerate(splitted_query,start=0):
        if element == 'max':
            max_argument = splitted_query[index + 1].count('+')                                 #how many '+' are there - if 0, then it's just col_1, if more, there are some operations there
            funcs_with_arguments.append([element,max_argument])
        if element == 'group by':
            groupby_argument = splitted_query[index + 1]
            groupby_argument = groupby_argument.replace("(","").replace(" ","").split(",")       #it's getting complicated here - this way it work for both (col_1) and (col_1, col_2)
            groupby_argument = sorted(groupby_argument)                                          #unification (so columns in different order will work aswell)
            funcs_with_arguments.append([element, groupby_argument])
    return funcs_with_arguments

def compare_query_keywords(splitted_first_query, splitted_second_query, keywords_tuple = ('select', 'max', 'group by', '+')):       #main information about querys
    a_actions = [e for e in splitted_first_query if e in ('select', 'max', 'group by', '+')]
    b_actions = [e for e in splitted_second_query if e in ('select', 'max', 'group by', '+')]

    if a_actions == b_actions:                                                                                                      #let's say that order does matter in this case
        return True
    return False

def compare_queries_classes(first_query, second_query):
    first_splitted_queries = list(filter(None, re.split(r"(\)|max|select|group by)", first_query.lower())))
    first_splitted_queries = [e for e in first_splitted_queries if e not in (' ')]              #remove standalone whitespaces

    second_splitted_queries = list(filter(None, re.split(r"(\)|max|select|group by)", second_query.lower())))
    second_splitted_queries = [e for e in second_splitted_queries if e not in (' ')]

    if(compare_query_keywords(first_splitted_queries,second_splitted_queries)):                 #there is no need to go further, if even query keywords (select, max, groupby, +) are different, therefore classes are different

        arguments_list_first_query = get_arguments_for_max_and_groupby(first_splitted_queries)
        arguments_list_second_query = get_arguments_for_max_and_groupby(second_splitted_queries)
        if arguments_list_first_query == arguments_list_second_query:
            return True
    return False


def test_queries(first_query, second_query):
    if compare_queries_classes(first_query,second_query):
        print("%s \n %s \n are of the same classes \n" % (first_query,second_query))
    else:
        print("%s \n %s \n are NOT of the same classes \n" % (first_query,second_query))

if __name__ == '__main__':
    print("Test running for all options")

    a = "SELECT MAX(col_1) FROM table"
    b = "SELECT MAX(col_1+1) FROM table"
    test_queries(a, b)

    a = "SELECT MAX(col_1 + 1) FROM table"
    b = "SELECT MAX(col_1 + 2)"
    test_queries(a, b)

    a = "SELECT MAX(col_1) FROM table"
    b = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    test_queries(a, b)

    a = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1 + 1) FROM table GROUP BY col_3"
    test_queries(a, b)

    a = "SELECT MAX(col_1 + 2) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1 + 1) FROM table GROUP BY col_2"
    test_queries(a, b)

    a = "SELECT MAX(col_1) FROM table GROUP BY col_2"
    b = "SELECT MAX(col_1) FROM table GROUP BY col_3"
    test_queries(a,b)
    print("Add your first query to test: ")
    a = input()
    print("Add your second query to test: ")
    b = input()
    test_queries(a, b)