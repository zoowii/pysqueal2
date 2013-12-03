"""Module db_io: functions for I/O on tables and databases.

A table file has a .csv extension.

We define "table" to mean this:

    dict of {str: list of str}

Each key is a column name from the table and each value is the list of strings
in that column from top row to bottom row.

We define "database" to mean this:

    dict of {str: table}

Each key is the name of the .csv file without the extension.  Each value is
the corresponding table as defined above.
"""
import os
import glob


def print_csv(table):
    """ (table) -> NoneType

    Print a representation of table in the same format as a table file.
    """

    columns = list(table.keys())
    print(','.join(columns))

    # All columns are the same length; figure out the number of rows.
    num_rows = len(table[columns[0]])

    # Print each row in the table.
    for i in range(num_rows):

        # Build a list of the values in row i.
        curr_row = []
        for column_name in columns:
            curr_row.append(table[column_name][i])

        print(','.join(curr_row))


# Write your read_table and read_database functions below.
# Use glob.glob('*.csv') to return a list of csv filenames from
#   the current directory.
def read_database():
    files = glob.glob('*.csv')
    database = dict()
    for file in files:
        table = read_table(open(file))
        table_name = os.path.splitext(file)[0]
        database[table_name] = table
    return database


def read_table(table_file):
    lines = table_file.readlines()
    cols = lines[0].split(',')
    table = dict()
    for i in range(len(cols)):
        cols[i] = cols[i].strip()
        table[cols[i]] = []
    for i in range(1, len(lines)):
        row = lines[i].split(',')
        for j in range(len(cols)):
            table[cols[j]].append(row[j].strip())
    table_file.close()
    return table


if __name__ == '__main__':
    print(read_table(open('movies.csv')))
    print(read_database())