import os
import sqlite3
from sqlite3 import Error

DBFILE = os.path.join(os.path.dirname(__file__), 'data', 'transforms.db')


def create_db(cursor):
    cursor.execute("""
    CREATE TABLE translations (
    translation_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    translation BLOB(256),
    algsstr TEXT);""")


def insert_translations(conn, cursor, trans_list):
    for trans in trans_list:
        cursor.execute("""
        INSERT INTO translations (translation, algsstr) VALUES(?, ?)""",
                       [sqlite3.Binary(trans), '_-_'.join(trans_list[trans])])


def get_translations(trans_list):
    alphabets = {}
    for trans in trans_list:
        print('Getting alphabets for', trans.__name__)
        for key in trans.all_iteration():
            obj = trans(key)
            alpha = obj.generate_trans_table()
            if alpha in alphabets.keys():
                alphabets[alpha].append(obj.shortname())
            else:
                alphabets[alpha] = [obj.shortname()]

    print('Found {} unique alphabets'.format(len(alphabets)))
    return alphabets


def select_translations(conn, cursor):
    cursor.execute("""
            SELECT translation,algsstr FROM translations""")
    while True:
        results = cursor.fetchmany(1000)
        if not results:
            break
        for result in results:
            yield result
    conn.close()  # yield allows this to work


def generate_database(trans_list,
                      db_file=DBFILE):
    try:
        os.remove(db_file)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        create_db(cursor)
        insert_translations(conn, cursor, get_translations(trans_list))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()


def get_alphabets(db_file=DBFILE):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        return select_translations(conn, cursor)
    except Error as e:
        print(e)
        conn.close()


def prettyhex(string):
    return repr(string)[1:]


def print_table(headers, values):
    # Makes sure everything is a string
    values = [[str(val) for val in row] for row in values]
    maxes = [len(val) for val in headers]
    for row in values:
        for i in range(len(row)):
            maxes[i] = max(maxes[i], len(str(row[i])))
    tmp_str = '{:<%ds}'*len(values[0])
    maxes = [max+2 for max in maxes]
    frmt_str = tmp_str % tuple(maxes)
    print(frmt_str.format(*headers))
    [print(frmt_str.format(*row))for row in values]


