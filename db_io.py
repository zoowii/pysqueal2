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

def get_table_name(filename):
    # get table name from table-file name without extension name
    dot_pos = filename.find('.')
    table_name = filename[:dot_pos]
    return table_name


def read_database():
    import glob

    files = glob.glob('*.csv')
    database = {}
    for filename in files:
        file = open(filename)
        table = read_table(file)
        file.close()
        table_name = get_table_name(filename)
        database[table_name] = table
    return database


def make_table_with_columns_and_rows(columns, rows):
    """
    create a table dict with columns and rows
    """
    table = {}
    for i in range(len(columns)):
        col = columns[i]
        if table.get(col) is None:
            table[col] = []
        l = table[col]
        for row in rows:
            l.append(row[i])
    return table


def read_table(file):
    import csv

    reader = csv.reader(file, delimiter=',', quotechar='|')
    rows = [row for row in reader]
    table = make_table_with_columns_and_rows(rows[0], rows[1:])
    return table


if __name__ == '__main__':
    print(read_table(open('movies.csv')))
    print(read_database())