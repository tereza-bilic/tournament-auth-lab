from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import logging
import sqlite3

from authlib.integrations.flask_client import OAuth
from os import environ as env
from dotenv import find_dotenv, load_dotenv

from flask import request


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


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
CORS(app, resources={r"/api/*": {"origins": "*"}, "/*": {"origins": "*"}},
          allow_headers=["Content-Type", "Authorization"],
          supports_credentials=True)


app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        "audience": "https://dev-nt27a611kij250c4.us.auth0.com/api/v2/"
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)



@app.post("/games")
# @require_auth()
@cross_origin(supports_credentials=True)
def createGame():


    print(request.headers.get('Authorization'))

    token = oauth.auth0.authorize_access_token()
    print(token)


    name = request.json['name']
    participants = request.json['participants']
    win_score = request.json['winScore']
    tie_score = request.json['tieScore']
    lose_score = request.json['loseScore']
    creator = request.json['creator']
    schedule = round_robin_tournament(participants.split(','))

    splittedParticipants = participants.split(',')

    if len(splittedParticipants) < 4 or len(splittedParticipants) > 8:
        return ("Number of participants must be between 4 and 8", 422)

    if len(splittedParticipants) % 2 != 0:
        return ("Number of participants must be even", 422)


    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO GAME (NAME,PARTICIPANTS,WINSCORE,TIESCORE,LOSESCORE,CREATOR) \
        VALUES (?,?,?,?,?,?)" "RETURNING id, name, participants, winscore, tiescore, losescore", (name, participants, win_score, tie_score, lose_score, creator));

    row = cursor.fetchone()
    print(row)
    (game_id, name, participants, win_score, tie_score, lose_score) = row if row else None
    print(row)

    matches = []

    for match in schedule:
      cursor.execute("INSERT INTO MATCH (player1,player2, score, game) \
        VALUES (?,?,?,?)" "RETURNING id, player1, player2, score", (match[0], match[1], 0, game_id));
      row = cursor.fetchone()
      (match_id, player1, player2, score) = row if row else None
      matches.append({
        "id": match_id,
        "player1": player1,
        "player2": player2,
        "score": score
      })



    conn.commit()
    print("Records created successfully")

    return ({
      "id": game_id,
      "name": name,
      "winScore": win_score,
      "tieScore": tie_score,
      "loseScore": lose_score,
      "matches": matches
      }, 200)


@app.get("/games/<id>")
def getGame(id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM GAME where ID = ?", (id,));
    row = cursor.fetchone()
    (game_id, name, participants, win_score, tie_score, lose_score, creator) = row if row else None

    cursor.execute("SELECT * FROM MATCH where GAME = ?", (id,));
    rows = cursor.fetchall()
    matches = []
    for row in rows:
      (match_id, player1, player2, score, game) = row if row else None
      matches.append({
        "id": match_id,
        "player1": player1,
        "player2": player2,
        "score": score
      })

    return ({
      "id": game_id,
      "participants": participants,
      "name": name,
      "winScore": win_score,
      "tieScore": tie_score,
      "loseScore": lose_score,
      "matches": matches,
      "creator": creator
      }, 200)


@app.patch("/matches/<id>")
def updateMatchScore(id):
    print(request.json)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    score = request.json['score']

    cursor.execute("UPDATE MATCH set score = ? where ID = ?", (score, id));
    conn.commit()

    return "<p>Match updated!</p>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    logging.getLogger('flask_cors').level = logging.DEBUG
