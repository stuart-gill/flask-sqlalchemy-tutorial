import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"

cursor.execute(create_user_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, price REAL)"

cursor.execute(create_item_table)

cursor.execute("INSERT INTO items (name, price) VALUES ('test item', 10.99)")
connection.commit()

connection.close()
