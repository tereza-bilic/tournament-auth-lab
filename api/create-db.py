import sqlite3

conn = sqlite3.connect('test.db')
print('Opened database successfully')

# drop table if it exists
conn.execute("DROP TABLE IF EXISTS GAME")
conn.execute("DROP TABLE IF EXISTS MATCH")

conn.execute('''CREATE TABLE GAME
        (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
        NAME           TEXT    NOT NULL,
        PARTICIPANTS   TEXT     NOT NULL,
        WINSCORE        INT     NOT NULL,
        TIESCORE        INT     NOT NULL,
        LOSESCORE       INT     NOT NULL,
        CREATOR        TEXT    NOT NULL
        );''')


conn.execute('''CREATE TABLE MATCH
            (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
            player1           TEXT    NOT NULL,
            player2           TEXT    NOT NULL,
            score            INT     NOT NULL,
            game           INT     NOT NULL,
            FOREIGN KEY (game) REFERENCES GAME (ID)
            );''')

print("Table created successfully")
