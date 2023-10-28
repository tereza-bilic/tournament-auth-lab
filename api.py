from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import logging
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

# Initialize CORS with your app and specify custom options
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}, "/*": {"origins": "*"}},
          allow_headers=["Content-Type", "Authorization"],
          supports_credentials=True)


@app.post("/games")
@cross_origin(supports_credentials=True)
def createGame():
    name = request.json['name']
    participants = request.json['participants']
    win_score = request.json['winScore']
    tie_score = request.json['tieScore']
    lose_score = request.json['loseScore']
    schedule = round_robin_tournament(participants.split(','))


    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO GAME (NAME,PARTICIPANTS,WINSCORE,TIESCORE,LOSESCORE) \
        VALUES (?,?,?,?,?)" "RETURNING id", (name, participants, win_score, tie_score, lose_score));

    row = cursor.fetchone()
    (game_id, ) = row if row else None
    print(row)

    for match in schedule:
      cursor.execute("INSERT INTO MATCH (player1,player2,score,game) \
        VALUES (?,?,?,?)", (match[0], match[1], 0, game_id));


    conn.commit()
    print("Records created successfully")

    return ({"id": game_id}, 200)



@app.patch("/matches/<id>")
def updateMatchScore():
    print(request.json)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    id = request.json['id']
    score = request.json['score']

    cursor.execute("UPDATE MATCH set score = ? where ID = ?", (score, id));
    conn.commit()

    return "<p>Match updated!</p>"


if __name__ == '__main__':
    app.run(debug=True)
    logging.getLogger('flask_cors').level = logging.DEBUG
