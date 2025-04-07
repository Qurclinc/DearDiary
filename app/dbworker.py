from flask import g
import psycopg2
from config import CONNECTION
from app.fileworker import FileWorker

def connect_db():
    conn = psycopg2.connect(
        host=CONNECTION["host"],
        user=CONNECTION["user"],
        password=CONNECTION["password"],
        database=CONNECTION["db_name"]
    )
    return conn

def create_db():
    db = connect_db()
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
id serial PRIMARY KEY,
login text NOT NULL,
passwd text NOT NULL,       
is_admin bool NOT NULL   
);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS cases(
id integer PRIMARY KEY,
title text NOT NULL,
text text NOT NULL
);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS users_test(
id serial PRIMARY KEY,
login text NOT NULL,
passwd text NOT NULL,       
is_admin bool NOT NULL   
);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS cases_test(
id integer PRIMARY KEY,
title text NOT NULL,
text text NOT NULL
);""")
    db.commit()
    db.close()

def get_db():
    if not(hasattr(g, "link_db")):
        g.link_db = connect_db()
    return g.link_db


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = self.__db.cursor()

    def checkUser(self, username):
        try:
            self.__cur.execute(f"""SELECT COUNT(*) FROM users WHERE login='{username}'""")
            res = self.__cur.fetchone()
            if res[0] > 0:
                return False
        except Exception as e:
            print("Error " + str(e))
        return True
    
    def addUser(self, username, passwd):
        try:
            if username == "cxder" or username == "admin":
                is_admin = True
            else:
                is_admin = False
            self.__cur.execute("""INSERT INTO users (login, passwd, is_admin) VALUES (%s, %s, %s)""", (username, passwd, is_admin))
            self.__db.commit()
        except Exception as e:
            print("Error " + str(e))
            return False
        return True
    
    def auth(self, username, passwd):
        try:
            self.__cur.execute(f"""SELECT COUNT(*) FROM users WHERE login='{username}' AND passwd='{passwd}'""")
            res = self.__cur.fetchone()
            if res[0] > 0:
                return True
        except Exception as e:
            print("Error " + str(e))
        return False

    def login(self, username, passwd):
        try:
            self.__cur.execute(f"""SELECT id, login, is_admin FROM users WHERE login='{username}' AND passwd='{passwd}'""")
            res = self.__cur.fetchone()
            if res: return res
        except Exception as e:
            print("Error " + str(e))
        return []
    
    def getUsers(self):
        try:
            self.__cur.execute("""SELECT id, login, passwd, is_admin FROM users""")
            res = self.__cur.fetchall()
            if res: return res
        except Exception as e:
            print("Error " + str(e))
        return []
    
    def addCase(self, title, text):
        if "случай" not in title.lower():
            return (False, "Неверное название: Пропущено слово \"Случай\"")
        # url = "static/cases/case" + title.split()[1].strip(".")
        # fw = FileWorker(url)
        # fw.createFile(text)
        try:
            # id = int(url.split('/')[-1][4:])
            id = title.split()[1].strip(".")
            self.__cur.execute("""INSERT INTO cases (id, title, text) VALUES (%s, %s, %s)""", (id, title, text))
            self.__db.commit()
            return (True, "Запись успешно добавлена!")
        except Exception as e:
            print("Error " + str(e))
            return (False, "Не удалось добавить запись в базу данных.\n" + str(e))
        return (False, "Не удалось добавить запись в базу данных.\n" + str(e))
    
    def caseList(self):
        try:
            self.__cur.execute("""SELECT id, title, text FROM cases""")
            res = self.__cur.fetchall()
            if res: return res
        except Exception as e:
            print("Error " + str(e))
        return []
    
    def getCase(self, id):
        try:
            self.__cur.execute(f"""SELECT title, text FROM cases WHERE id={id}""")
            res = self.__cur.fetchone()
            if res: return res
        except Exception as e:
            print("Error " + str(e))
        return []
    
    def removeCase(self, id):
        try:
            self.__cur.execute(f"""DELETE FROM cases WHERE id={id}""")
            # fw = FileWorker()
            # fw.remove(f"static/cases/case{id}.txt")
            self.__db.commit()
        except Exception as e:
            print("Error " + str(e))