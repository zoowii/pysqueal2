"""
Process SQuEaL queries from the keyboard and print the results.
"""

import db_io
import squeal
import pprint


def test_compile(text):
    print(squeal.compile_query(text))


def main():
    """ () -> NoneType

    Ask for queries from the keyboard; stop when empty line is received. For
    each query, process it and use db_io.print_csv to print the results.
    """

    # Write your main function body here.
    #text = 'select m.title,m.studio,m.gross,o.category  from movies,oscars  where m.title=o.title'
    #test_compile(text)
    #query = squeal.compile_query(text)
    #result = query.execute()
    #pprint.pprint(result)
    line = input()
    while len(line.strip()) > 0:
        query = squeal.compile_query(line)
        result = query.execute()
        pprint.pprint(result)
        line = input()


if __name__ == '__main__':
    main()
