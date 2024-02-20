import sqlite3

conn = sqlite3.connect("database/universities.sqlite", check_same_thread=False)
cur = conn.cursor()


def short_name(university: str, olympiad: str):
    result = cur.execute(
        f"""SELECT short_name FROM '{university}' 
                             WHERE type_of_comp like '%{olympiad}%' OR copm like '%{olympiad}%'"""
    ).fetchall()
    return result


def type_of_comp(university: str, short_name: str):
    result = cur.execute(
        f"""SELECT type_of_comp FROM '{university}'
                             WHERE short_name = '{short_name}'"""
    ).fetchone()
    return result


def conditions(university: str, short_name: str):
    result = cur.execute(
        f"""SELECT conditions FROM '{university}'
                             WHERE short_name = '{short_name}'"""
    ).fetchone()
    return result


def bonuses(university: str, short_name: str):
    result = cur.execute(
        f"""SELECT participant, prewinner, winner from '{university}' 
                             WHERE short_name = '{short_name}'"""
    ).fetchone()
    return result
