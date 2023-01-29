from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import random

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

GAME_BOARD = []
ALGORITME = []
all_clicked = []
CONSTANT_VALG = [1]
BOARD_LENGTH = []
ANSWER = 7
SIZE = 0
TOTAL_SCORE = [0]
ENEMIES_PLAYED = []


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  points = db.Column(db.Integer, nullable=False)



@app.route('/startGame', methods=['POST'])
def start_game():
  all_clicked.clear()
  ENEMIES_PLAYED.clear()
  TOTAL_SCORE[0] = 0
  return "success"

@app.route("/arena")
def arena():
  # returning JSON as: {"antall": int, "algo_robot": String, "correct_index": int}
  return {"gameboard": GAME_BOARD, "algorithm": str(ALGORITME[0]), "answer": ANSWER} # sending all the data (/information) 

@app.route('/algoritmeData', methods=['POST'])
def my_route():
  data = request.get_json()
  # do something with the data
  print(data["antall"], data["algoritme"])
  all_clicked.clear()
  lag_liste(data["antall"])
  ALGORITME.clear()
  ALGORITME.append(data["algoritme"])
  ENEMIES_PLAYED.append(str(ALGORITME[0]))
  CONSTANT_VALG[0] = 0
  return arena()

def lag_liste(antall):
  GAME_BOARD.clear()
  liste_str = int(antall)
  index = 1
  for i in range(liste_str):
    GAME_BOARD.append(index)
    index += 1


def hent_liste_storrelse():
  storrelse = 0
  for i in GAME_BOARD:
    storrelse += 1
  return storrelse

def next_round_reset():
  all_clicked.clear()
  ALGORITME.clear()
  BOARD_LENGTH.clear()
  GAME_BOARD.clear()

@app.route("/robot_valg", methods=['POST'])
def robot_valg():
  data = request.get_json()
  print("data from API: ", data["valgte_bokser"])
  for valgte_elementer in data["valgte_bokser"]:
    all_clicked.append(int(valgte_elementer))
  
  valgte_tall = 1  
  if ALGORITME[0] == "Tesla":
    CONSTANT_VALG[0] = 1 #midl for testing underveis av programmet for restart av verdien, sånn robot ikke husker noe
    valgte_tall = Tesla()
  elif ALGORITME[0] == "Kidy":
    valgte_tall = Kidy()
  elif ALGORITME[0] == "Alan":
    valgte_tall = Alan(0, len(GAME_BOARD))
  all_clicked.append(valgte_tall)
  print("alle klikket: ", all_clicked)
  if valgte_tall == ANSWER: # fjerner alle elementer når tallet er funnet, så vi forbreder til neste kamp
    next_round_reset()

  return {"valg": valgte_tall}

def sjekkValgteElementer():
  if ANSWER in all_clicked:
    return True
  return False

def get_length_alle_clicked(all_clicked):
  size = 0
  for i in all_clicked:
    size += 1
  return size

def Tesla():
  for i in all_clicked:
    if CONSTANT_VALG[0] == i:
      CONSTANT_VALG[0] += 1
      return Tesla()
  print("Valgte tall fra Tesla er: ", CONSTANT_VALG[0])
  return CONSTANT_VALG[0]

#binary search
def Alan(start, end):
  i = (start + end) // 2
  print("i er", i)
  valgte_element = int(GAME_BOARD[i-1])
  if start < end:
    if valgte_element in all_clicked:
      if valgte_element < ANSWER:
        return Alan(i+1, end)
      else:
        return Alan(start, i-1)
    
  print("valgte element fra Alan er: ", valgte_element)
  return valgte_element

def Kidy():
  size = hent_liste_storrelse()
  tilfeldig_tall = random.randint(1, size)
  for i in all_clicked:
    if tilfeldig_tall == i:
      return Kidy() 
  print("Valgte tall fra Kidy er: ", tilfeldig_tall)
  return tilfeldig_tall


@app.route("/last_standing")
def neste_runde():
  print("Total poeng:", TOTAL_SCORE[0])
  return {"played_enemies": ENEMIES_PLAYED, "total_points": TOTAL_SCORE[0]}

@app.route("/round_results", methods=['POST'])
def round_over():
  data = request.get_json()
  print("Round Over API: ", data["poeng"], data["bruker_fant"])
  TOTAL_SCORE[0] += int(data["poeng"])
  print("Fant bruker svar: ", data["bruker_fant"])
  print("API poeng mottat: ",data["poeng"])
  print("Total poeng:", TOTAL_SCORE[0])
  next_round_reset()
  print(all_clicked)
  print("enemie played: ", ENEMIES_PLAYED[0])
  return neste_runde()


@app.route("/register_user_points", methods=['POST'])
def register_user():
  data = request.get_json()
  print(data["username"])

  return "success"
  

if __name__ == "__main__":
    app.run(debug=True)