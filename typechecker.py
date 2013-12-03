'''This module should be used to test the parameter and return types of your
functions. Before submitting your assignment, run this type-checker. This
typechecker expects to find files db_io.py, squeal.py, and
the .csv files provided in the starter code.

If errors occur when you run this typechecker, fix them before you submit
your assignment.

If no errors occur when you run this typechecker, then the type checks passed.
This means that the function parameters and return types match the assignment
specification, but it does not mean that your code works correctly in all
situations. Be sure to test your code before submitting.
'''

import db_io

def is_table(d):
    if not isinstance(d, dict):
        return False
    for k in d:
        if not isinstance(k, str):
            return False
        value = d[k]
        if not isinstance(value, list):
            return False
        for s in value:
            if not isinstance(s, str):
                return False    
    return True

def is_database(d):
    if not isinstance(d, dict):
        return False
    for k in d:
        if not isinstance(k, str):
            return False
        value = d[k]
        if not is_table(value):
            return False
    return True
    

# typecheck the db_io.py functions

# typecheck db_io.read_table

result = db_io.read_table(open('movies.csv'))
assert is_table(result), \
    'read_table should return a table; please check the handout \
    for the definition of a table.'
    
    
    # typecheck db_io.read_database

result = db_io.read_database()
assert is_database(result), \
    'read_database should return a database; please check the handout \
    for the definition of a database.'
    
    
    # typecheck the required squeal.py function

import squeal

t1 = {'a':['b', 'c']}
t2 = {'d':['e', 'f']}

result = squeal.cartesian_product(t1, t2)
assert is_table(result), \
    'cartesian_product should return a table; please check the handout \
    for the definition of a table.'
