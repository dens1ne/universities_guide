import sqlite3

conn = sqlite3.connect("database/universities.sqlite", check_same_thread=False)
cur = conn.cursor()


def short_name(university: str, olympiad: str):
    result = cur.execute(
        f"""SELECT short_name FROM '{university}'
                             WHERE type_of_comp LIKE '%{olympiad}%' OR type_of_comp LIKE '%{olympiad.lower()}%'
                             OR copm LIKE '%{olympiad}%' OR copm LIKE '%{olympiad.lower()}%'"""
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
# import sqlite3
# import re
#
# conn = sqlite3.connect("database/universities.sqlite", check_same_thread=False)
# cur = conn.cursor()
#
#
# def sqlite_like(template_, value_):
#     return sqlite_like_escape(template_, value_, None)
#
#
# def sqlite_like_escape(template_, value_, escape_):
#     re_ = re.compile(template_.lower().
#                         replace(".", "\\.").replace("^", "\\^").replace("$", "\\$").
#                         replace("*", "\\*").replace("+", "\\+").replace("?", "\\?").
#                         replace("{", "\\{").replace("}", "\\}").replace("(", "\\(").
#                         replace(")", "\\)").replace("[", "\\[").replace("]", "\\]").
#                         replace("_", ".").replace("%", ".*?"))
#     return re_.match(value_.lower()) != None
#
#
#  # Переопределение функции преобразования к нижнему регистру
# def sqlite_lower(value_):
#     return value_.lower()
#
#
# # Переопределение правила сравнения строк
# def sqlite_nocase_collation(value1_, value2_):
#     return value1_.lower() == value2_.lower()
#
#
# # Переопределение функции преобразования к верхнему геристру
# def sqlite_upper(value_):
#     return value_.upper()
#
#
# conn.create_collation("BINARY", sqlite_nocase_collation)
# conn.create_collation("NOCASE", sqlite_nocase_collation)
# conn.create_function("LIKE", 2, sqlite_like)
# conn.create_function("LOWER", 1, sqlite_lower)
# conn.create_function("UPPER", 1, sqlite_upper)
#
#
# def short_name(university: str, olympiad: str):
#     olympiad = '%' + olympiad + '%'
#     result = cur.execute(
#         f"""SELECT short_name FROM '{university}'
#                              WHERE type_of_comp COLLATE NOCASE LIKE '%' || ? || '%' OR
#                              copm COLLATE NOCASE LIKE '%' || ? || '%'""",
#                              (olympiad, olympiad)
#     ).fetchall()
#     print(university, olympiad, result)
#     return result
#
#
# def type_of_comp(university: str, short_name: str):
#     result = cur.execute(
#         f"""SELECT type_of_comp FROM '{university}'
#                              WHERE short_name COLLATE NOCASE = '{short_name}'"""
#     ).fetchone()
#     print(short_name, result)
#     return result
#
#
# def conditions(university: str, short_name: str):
#     result = cur.execute(
#         f"""SELECT conditions FROM '{university}'
#                              WHERE short_name COLLATE NOCASE = '{short_name}'"""
#     ).fetchone()
#     return result
#
#
# def bonuses(university: str, short_name: str):
#     result = cur.execute(
#         f"""SELECT participant, prewinner, winner from '{university}'
#                              WHERE short_name COLLATE NOCASE = '{short_name}'"""
#     ).fetchone()
#     return result
