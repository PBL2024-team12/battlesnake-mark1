import random
import typing
import asyncio
import time

def info() -> typing.Dict:
  print("INFO")

  return {
      "apiversion": "1",
      "author": "Taketo Usui",
      "color": "#000000",
      "head": "tiger-king",
      "tail": "tiger-tail",
  }

def start(game_state: typing.Dict):
  print("GAME START")

def end(game_state: typing.Dict):
  print("GAME OVER\n")

board_width = 0
board_height = 0

def move(game_state: typing.Dict) -> typing.Dict:
  global board_width, board_height
  board_width = game_state["board"]["width"]
  board_height = game_state["board"]["height"]
  turn = game_state["turn"]

  my_body = game_state["you"]["body"]
  head = my_body[0]
  enemy_body = []
  for snakes in game_state["board"]["snakes"]:
    if snakes["id"] != game_state["you"]["id"]:
      enemy_body = snakes["body"]
  
  moves_score = {"left": 1000000, "right": 1000000, "up": 1000000, "down": 1000000}

  return calc_best_move(moves_score, turn)

def find_safe_moves(head: typing.Dict, my_body, enemy_body) -> typing.List:
  moves = ["up", "down", "left", "right"]
  if head["x"] == 0:
    moves.remove("left")
  if head["x"] == board_width - 1:
    moves.remove("right")
  if head["y"] == 0:
    moves.remove("down")
  if head["y"] == board_height - 1:
    moves.remove("up")
  
  for body in my_body[1:-1]:
    if move_to_coordinate(head, "up") == body and "up" in moves:
      moves.remove("up")
    if move_to_coordinate(head, "down") == body and "down" in moves:
      moves.remove("down")
    if move_to_coordinate(head, "left") == body and "left" in moves:
      moves.remove("left")
    if move_to_coordinate(head, "right") == body and "right" in moves:
      moves.remove("right")
  
  for body in enemy_body:
    if move_to_coordinate(head, "up") == body and "up" in moves:
      moves.remove("up")
    if move_to_coordinate(head, "down") == body and "down" in moves:
      moves.remove("down")
    if move_to_coordinate(head, "left") == body and "left" in moves:
      moves.remove("left")
    if move_to_coordinate(head, "right") == body and "right" in moves:
      moves.remove("right")

  return moves

def move_to_coordinate(coordinate: typing.Dict, move: str) -> typing.Dict:
  if move == "up":
    return {"x": coordinate["x"], "y": coordinate["y"] + 1}
  elif move == "down":
    return {"x": coordinate["x"], "y": coordinate["y"] - 1}
  elif move == "left":
    return {"x": coordinate["x"] - 1, "y": coordinate["y"]}
  elif move == "right":
    return {"x": coordinate["x"] + 1, "y": coordinate["y"]}

def calc_best_move(moves_score: typing.Dict, turn: int) -> str:
  bestmove = "___"
  bestmoves = []
  max_score = 0
  for move in ["left", "right", "up", "down"]:
    if moves_score[move] > max_score:
      max_score = moves_score[move]
      bestmoves = [move]
    elif moves_score[move] == max_score:
      bestmoves.append(move)
  if len(bestmoves) > 0:
    bestmove = random.choice(bestmoves)
    print(f"MOVE {turn}: {bestmove}(best move: {bestmoves}, score: {max_score})")
  else:
    bestmove = random.choice(["left", "right", "up", "down"])
    print(f"MOVE {turn}: {bestmove}(no best move)")

  return {"move": bestmove}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8000"})