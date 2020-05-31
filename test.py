import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id int, username text, password text)'
cursor.execute(create_table)

users = [(1, 'shr', 'india'), (2, 'anna', 'australia'),
         (3, 'tanya', 'america')]

insert_query = 'INSERT INTO users VALUES(?, ?, ?)'
cursor.executemany(insert_query, users)

select_query = 'SELECT * FROM users'

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
