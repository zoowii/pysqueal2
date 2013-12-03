import db_io


def split_text_before(text, word):
    """
    get the text before word(or None) with the remaining
    eg. get text before ' from '/' where ' keyword with the remaining
    """
    if word is None:
        return [text, '']
    pos = text.find(word)
    if pos < 0:
        return [text, '']
    return [text[:pos], text[pos + len(word):]]


def get_columns_of_table(table):
    return list(table.keys())


def get_size_of_table(table):
    return len(table[get_columns_of_table(table)[0]])


def get_rows_of_table(table):
    """
    return rows of table like ['value1', 'value2', 'value3']
    """
    columns = get_columns_of_table(table)
    rows = []
    for i in range(get_size_of_table(table)):
        row = []
        for col in columns:
            row.append(table[col][i])
        rows.append(row)
    return rows


def get_key_rows_of_table(table):
    """
    return rows of table like {'column1':'value1','column2':'value2'}
    """
    columns = get_columns_of_table(table)
    rows = []
    for i in range(get_size_of_table(table)):
        row = {}
        for col in columns:
            row[col] = table[col][i]
        rows.append(row)
    return rows


def where_execute(sql_str):
    """
    return a funtion witch accept a table and return filtered table back
    execute the where sub query.
    just return a function as judgement
    """
    import re

    sql_str = sql_str.strip()
    where_type = 'no_string'
    if sql_str[-1] == "'":
        where_type = 'string'
    identity_re = r'[a-zA-Z0-9\.]+'
    c1 = re.match(identity_re, sql_str).group()
    remaining_str = sql_str[sql_str.find(c1) + len(c1):].strip()
    op = remaining_str[0]
    remaining_str = remaining_str[1:].strip()
    c2 = remaining_str
    if where_type == 'string':
        c2 = remaining_str[1:-1]

    def is_row_match(cols, row, key_row):
        value1 = key_row[c1]
        if where_type == 'string':
            value2 = c2
        else:
            value2 = key_row[c2]
        if op == '=':
            return value1 == value2
        elif op == '>':
            return value1 > value2
        else:
            print('error happen in where sub-query')
            return 'error'

    def where_filter(table):
        cols = get_columns_of_table(table)
        rows = get_rows_of_table(table)
        key_rows = get_key_rows_of_table(table)
        result_rows = []
        for i in range(len(rows)):
            row = rows[i]
            key_row = key_rows[i]
            if is_row_match(cols, row, key_row):
                result_rows.append(row)
        return db_io.make_table_with_columns_and_rows(cols, result_rows)

    return where_filter


def cartesian_product(table1, table2):
    columns1 = get_columns_of_table(table1)
    columns2 = get_columns_of_table(table2)
    columns = []
    columns.extend(columns1)
    columns.extend(columns2)
    rows = []
    rows1 = get_rows_of_table(table1)
    rows2 = get_rows_of_table(table2)
    for row1 in rows1:
        for row2 in rows2:
            row = []
            row.extend(row1)
            row.extend(row2)
            rows.append(row)
    return db_io.make_table_with_columns_and_rows(columns, rows)


def from_execute(sql_str):
    """
    return a table filtered by where sub-query if exists
    """
    splited_sql = split_text_before(sql_str, ' where ')
    where = None
    table_names = splited_sql[0].strip().split(',')
    table_names = [item.strip() for item in table_names]
    if len(splited_sql[1].strip()) > 0:
        where_sql = splited_sql[1].strip()
        where = where_execute(where_sql)
    database = db_io.read_database()

    if len(table_names) == 1:
        tbl = database[table_names[0]]
    elif len(table_names) == 2:
        table1 = database[table_names[0]]
        table2 = database[table_names[1]]
        tbl = cartesian_product(table1, table2)
    else:
        print('from sub-query only accept one or two table-name')
        return 'error'
    if where is not None:
        tbl = where(tbl)
    return tbl


def select_execute(sql_str):
    splited_sql = split_text_before(sql_str, ' from ')
    columns = splited_sql[0].split(',')
    columns = [item.strip() for item in columns]
    from_sql = splited_sql[1].strip()
    table = from_execute(from_sql)

    def select_func(table):
        if len(columns) == 1 and columns[0] == '*':
            return table
        result_table = {}
        for col in columns:
            if table.get(col) is not None:
                result_table[col] = table[col]
        return result_table

    table = select_func(table)
    return table


def squeal(sql_str):
    """
    execute sql_str as squeal language
    as the squeal str always starts with select, so do select_execute
    """
    select_pos = sql_str.find('select ')
    select_sql = sql_str[(select_pos + len('select ')):]
    return select_execute(select_sql)