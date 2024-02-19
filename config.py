from database.db_requests import cur

BOT_TOKEN = "6648598438:AAFknapznx-jRJcsHqNqzSwlF9EpplQ3PCs"
DEFAULT_COMMANDS = (
    ("start", "Начать подбор университета"),
)

res = cur.execute("""SELECT name FROM universities_list""").fetchall()
universities = [i[0] for i in res]
current_university = -1
