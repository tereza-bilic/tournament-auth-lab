from flask import Flask
from flask import request
import sqlite3

def round_robin_tournament(participants):
    if len(participants) < 4 or len(participants) > 8:
        raise ValueError("Number of participants must be between 4 and 8")

    if len(participants) % 2 != 0:
        raise ValueError("Number of participants must be even")

    schedule = []

    for _ in range(len(participants) - 1):
        mid = len(participants) // 2
        first_half = participants[:mid]
        second_half = participants[mid:]

        matches = []
        for i in range(mid):
            matches.append((first_half[i], second_half[i]))

        schedule.extend(matches)

        # Rotate participants for the next round
        participants = [participants[0]] + [participants[-1]] + participants[1:-1]

    return schedule


# ------------------ Flask app logic ------------------

app = Flask(__name__)
conn = sqlite3.connect('test.db')
print('Opened database successfully')

conn.execute('''CREATE TABLE GAME
        (ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        PARTICIPANTS   TEXT     NOT NULL,
        WINSCORE        INT     NOT NULL,
        TIESCORE        INT     NOT NULL,
        LOSESCORE       INT     NOT NULL
        );''')


conn.execute('''CREATE TABLE MATCH
            (ID INT PRIMARY KEY     NOT NULL,
            player1           TEXT    NOT NULL,
            player2           TEXT    NOT NULL,
            score            INT     NOT NULL,
            FOREIGN KEY (player1) REFERENCES GAME (PARTICIPANTS)
            );''')

print("Table created successfully")


@app.post("/game")
def createGame():
    print(request.json)

    name = request.json['name']
    participants = request.json['participants'].split(',')
    win_score = request.json['win_score']
    tie_score = request.json['tie_score']
    lose_score = request.json['lose_score']


    schedule = round_robin_tournament(participants)
    print(schedule)

    match_ids = []

    conn.execute("INSERT INTO GAME (NAME,PARTICIPANTS,WINSCORE,TIESCORE,LOSESCORE) \
        VALUES (?,?,?,?,?)" "RETURNING id", (name, participants, win_score, tie_score, lose_score));


    for match in schedule:
      conn.execute("INSERT INTO MATCH (player1,player2,score) \
        VALUES (?,?,?)" (match[0], match[1], 0));

    # get the id of the game and return it
    cursor = conn.execute("SELECT MAX(id) FROM GAME")
    game = cursor.fetchone()[0]

    conn.commit()
    print("Records created successfully")


    return game



@app.patch("/match/<id>")
def updateMatchScore():
    print(request.json)

    id = request.json['id']
    score = request.json['score']

    conn.execute("UPDATE MATCH set score = ? where ID = ?", (score, id));

    return "<p>Match updated!</p>"
