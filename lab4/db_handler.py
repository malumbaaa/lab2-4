import mysql.connector
from models import *
from config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USERNAME

def create_connection(hostname:str, user:str, password:str, database:str):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname, user=user,
            password=password, database=database 
        )
    except Exception as e:
        print(e.with_traceback)
                
    return connection


# words table

def insert_word(word:Word):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO words(word_en, word_type) VALUES ('{}', '{}');".format(word.word_en, word.word_type))
    connection.commit()
    connection.close()

def delete_word(word:Word):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    word_id = find_word_id(word)
    cursor.execute("DELETE FROM words WHERE id={}".format(word_id))
    cursor.execute("DELETE FROM meanings WHERE word_id={}".format(word_id))
    connection.commit()
    connection.close()

def find_word_id(word:Word):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM words WHERE word_en='{}' AND word_type='{}';".format(word.word_en, word.word_type))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]

def get_random_words(amount):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words ORDER BY rand() LIMIT {};".format(amount))
    res = cursor.fetchall()
    connection.close()
    return res


# meanings table

def insert_meaning(meaning:Meaning):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meanings(word_id, meaning) VALUES ({}, '{}');".format(meaning.word_id, meaning.meaning))
    connection.commit()
    connection.close()


# users table

def insert_user(user:User):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(user_id, role, chat_id, status, login_status, username, password) VALUES ({}, '{}', {}, {}, {}, '{}', '{}');".\
        format(user.user_id, user.role, user.chat_id, user.status, user.login_status, user.username, user.password))
    connection.commit()
    connection.close()

def find_user(user_id):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res

def find_user(username, password):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE USERNAME='{}' AND PASSWORD='{}'".format(username, password))
    res = cursor.fetchall()
    connection.close()
    return res

def set_status(user_id, status:int):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET status={} WHERE user_id={};".format(status, user_id))
    connection.commit()
    connection.close()

def get_status(user_id):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT status FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]

def set_login_status(user_id, login_status:int):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET login_status={} WHERE user_id={}".format(login_status, user_id))
    connection.commit()
    connection.close()

def get_login_status(user_id):
    connection = create_connection(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT login_status FROM users WHERE user_id={}".format(user_id))
    res = cursor.fetchall()
    connection.close()
    return res[0][0]
