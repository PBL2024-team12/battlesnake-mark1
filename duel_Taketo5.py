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
  move_options = ["up", "down", "left", "right"]

  my_body = game_state["you"]["body"]
  head = my_body[0]
  enemy_body = []
  for snakes in game_state["board"]["snakes"]:
    if snakes["id"] != game_state["you"]["id"]:
      enemy_body = snakes["body"]
  moves_score = {"left": 0, "right": 0, "up": 0, "down": 0}

  safe_moves = find_safe_moves(head, my_body, enemy_body, [])
  if len(safe_moves) == 0:
    return calc_best_move(moves_score, turn)
  for move in safe_moves:
    moves_score[move] = 500000
  around_enemy_head = []
  if len(enemy_body) > len(my_body):
    for move in move_options:
      around_enemy_head.append(move_to_coordinate(enemy_body[0], move))
  extra_safe_moves = find_safe_moves(head, my_body, enemy_body, around_enemy_head)
  for move in extra_safe_moves:
    moves_score[move] = 1000000

  if head["x"]*2 < (board_width - 1):
    moves_score["right"] += 100*(board_width - 1 - head["x"]*2)**2
  elif head["x"]*2 > (board_width - 1):
    moves_score["left"] += 100*(head["x"]*2 - board_width + 1)**2
  if head["y"]*2 < (board_height - 1):
    moves_score["up"] += 100*(board_height - 1 - head["y"]*2)**2
  elif head["y"]*2 > (board_height - 1):
    moves_score["down"] += 100*(head["y"]*2 - board_height + 1)**2

  return calc_best_move(moves_score, turn)

def find_safe_moves(head: typing.Dict, my_body, enemy_body, obstacles) -> typing.List:
  moves = ["up", "down", "left", "right"]
  if head["x"] == 0:
    moves.remove("left")
  if head["x"] == board_width - 1:
    moves.remove("right")
  if head["y"] == 0:
    moves.remove("down")
  if head["y"] == board_height - 1:
    moves.remove("up")

  up_head = move_to_coordinate(head, "up")
  down_head = move_to_coordinate(head, "down")
  left_head = move_to_coordinate(head, "left")
  right_head = move_to_coordinate(head, "right")
  
  if "up" in moves:
    for body in my_body[1:-1]:
      if up_head == body:
        moves.remove("up")
        break
  if "down" in moves:
    for body in my_body[1:-1]:
      if down_head == body:
        moves.remove("down")
        break
  if "left" in moves:
    for body in my_body[1:-1]:
      if left_head == body:
        moves.remove("left")
        break
  if "right" in moves:
    for body in my_body[1:-1]:
      if right_head == body:
        moves.remove("right")
  
  if "up" in moves:
    for body in enemy_body[:-1]:
      if up_head == body:
        moves.remove("up")
  if "down" in moves:
    for body in enemy_body[:-1]:
      if down_head == body:
        moves.remove("down")
  if "left" in moves:
    for body in enemy_body[:-1]:
      if left_head == body:
        moves.remove("left")
  if "right" in moves:
    for body in enemy_body[:-1]:
      if right_head == body:
        moves.remove("right")
  
  if "up" in moves:
    for body in obstacles:
      if up_head == body:
        moves.remove("up")
  if "down" in moves:
    for body in obstacles:
      if down_head == body:
        moves.remove("down")
  if "left" in moves:
    for body in obstacles:
      if left_head == body:
        moves.remove("left")
  if "right" in moves:
    for body in obstacles:
      if right_head == body:
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
  max_score = 1
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