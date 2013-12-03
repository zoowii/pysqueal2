"""
Process SQuEaL queries from the keyboard and print the results.
"""

import squeal
import pprint


def main():
    """ () -> NoneType

    Ask for queries from the keyboard; stop when empty line is received. For
    each query, process it and use db_io.print_csv to print the results.
    """
    line = input()
    while line.strip() != '':
        result = squeal.squeal(line)
        pprint.pprint(result)
        line = input()


if __name__ == '__main__':
    main()
