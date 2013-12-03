""" Module squeal: table and database manipulation functions.

The meanings of "table" and "database" are as described in db_io.py.
"""

# Write your Cartesian product function and all your other helper functions
# here.
import re
import db_io


class Query(object):
    """
    query of the squeal language compiled from input text
    """
    type = 'multi'
    items = []
    where_type = None  # column, string
    table = None  # table of last query result or None, and the result table store here

    def __init__(self, type='multi'):
        self.type = type
        self.items = []

    def __repr__(self):
        s = 'Query<%s>\n' % self.type
        if self.type == 'where':
            s += "where type: %s" % self.where_type + '\n'
        for item in self.items:
            s += repr(item) + '\n'
        return s

    def sort_clauses(self):
        """
        sort the sub queries if the query's type is multi
        the order is from, where, select if exists
        """
        if self.type != 'multi':
            return
        if len(self.items) <= 1:
            return
        sort_range = {
            'from': 1,
            'where': 2,
            'select': 3
        }

        self.items.sort(key=lambda x: sort_range[x.type])

    def execute(self):
        """
        return table of the query result
        params query the Query object compiled
        """
        if self.type != 'multi':
            print("error query type, not multi")
            return
        table = None
        for query in self.items:
            query.table = table
            table = query.execute()
        return table


class FromQuery(Query):
    type = 'from'

    def read_tables(self):
        """
        read table in from clause
        if self.items are not string, but Query object or Table(dict), then just return them
        """
        db = db_io.read_database()
        tables = list()
        for i in range(len(self.items)):
            item = self.items[i]
            if isinstance(item, Query):
                item.table = self.table
                tables.append(item.execute())
            elif isinstance(item, dict):
                tables.append(item)
            elif isinstance(item, str):
                tables.append(db[item])
            else:
                print('error in from clause')
        return tables

    def execute(self):
        """
        read and/or product tables and return the result
        """
        tables = self.read_tables()
        if len(tables) == 1:
            return tables[0]
        elif len(tables) == 2:
            return cartesian_product(tables[0], tables[1])
        else:
            print("error in from clause, too more from tables")
            return None


class SelectQuery(Query):
    type = 'select'

    def execute(self):
        if self.items[0] == '*':
            return self.table
        result_table = dict()
        for key in self.items:
            result_table[key] = self.table[key]
        return result_table


class WhereQuery(Query):
    def execute(self):
        """
        fetch rows from table which match the where condition
        """
        result_table = dict()
        for key in self.table.keys():
            result_table[key] = []
        for i in range(count_table_size(self.table)):
            row = self.get_row(i)
            if self.match_condition(row):
                insert_row_to_table(result_table, row)
        return result_table

    def get_row(self, row_index):
        """
        get row of row_index in self.table
        """
        row = dict()
        for k in self.table.keys():
            row[k] = self.table[k][row_index]
        return row

    def match_condition(self, row):
        """
        row is one row in self.table, check where the row matches the where condition
        """
        value1 = row[self.items[0]]
        if self.where_type == 'column':
            value2 = row[self.items[2]]
        elif self.where_type == 'string':
            value2 = self.items[2]
        else:
            print("unsupported where type")
            return None
        op = self.items[1]
        return (op == '=' and value1 == value2) or (op == '>' and value1 > value2)


def cartesian_product(table1, table2):
    result_table = dict()
    result_keys = []
    result_keys.extend(table1.keys())
    result_keys.extend(table2.keys())
    for k in result_keys:
        result_table[k] = []
    len1 = count_table_size(table1)
    len2 = count_table_size(table2)
    for i in range(len1):
        for j in range(len2):
            row = dict()
            for k in table1.keys():
                row[k] = table1[k][i]
            for k in table2.keys():
                row[k] = table2[k][j]
            insert_row_to_table(result_table, row)
    return result_table


def count_table_size(table):
    """
    return size of the table, count of rows in table
    """
    return len(table[list(table.keys())[0]])


def insert_row_to_table(table, row):
    for key in table.keys():
        table[key].append(row[key])
    return table


def compile_query(query_text):
    """
    when the where clause has comma or empty_space in string value
    need split the where clause first of all
    """
    has_where_clause = False
    where_clause_text = None
    splited_by_where = query_text.split('where')
    if len(splited_by_where) > 1:
        has_where_clause = True
        where_clause_text = splited_by_where[1]
        query_text = splited_by_where[0]
        # split token from input by space and comma
    tokens = list(filter(lambda x: len(x.strip()) > 0, re.split(r'[\s,]', query_text)))
    query = Query('multi')
    tmp_tokens = []

    def create_sub_query():
        """
        create sub query like select, from, where
        """
        sub_query_type = tmp_tokens[0]
        cls_map = {
            'select': SelectQuery,
            'from': FromQuery,
            'where': WhereQuery
        }
        sub_query = cls_map[sub_query_type](sub_query_type)

        if sub_query_type != 'where':
            sub_query.items = tmp_tokens[1:]
        else:
            where_text = tmp_tokens[1]
            has_string_re = r'\s*([a-zA-Z0-9\.]+?)\s*([=>])\s*\'([\w\W]*?)\'\s*'
            no_string_re = r"\s*([a-zA-Z0-9\.]+?)\s*([=>])\s*([^']+)\s*"
            m1 = re.match(has_string_re, where_text)
            # judge where the where condition is like column_name1>/=columnname2 or column_name1>/='value1'
            if m1:
                sub_query.where_type = 'string'
                sub_query.items = m1.groups()
            else:
                m2 = re.match(no_string_re, where_text)
                sub_query.where_type = 'column'
                sub_query.items = m2.groups()
        tmp_tokens.clear()
        query.items.append(sub_query)

    token_keys = ['select', 'where', 'from']

    for i in range(len(tokens)):
        token = tokens[i]
        tmp_tokens.append(token)
        if i == len(tokens) - 1 or (tokens[i + 1] in token_keys):
            create_sub_query()
    if has_where_clause:
        tmp_tokens = ['where', where_clause_text]
        create_sub_query()
    query.sort_clauses()
    return query