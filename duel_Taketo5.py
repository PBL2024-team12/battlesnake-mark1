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

  # 真ん中による
  if head["x"]*2 < (board_width - 1):
    moves_score["right"] += 100*(board_width - 1 - head["x"]*2)**2
  elif head["x"]*2 > (board_width - 1):
    moves_score["left"] += 100*(head["x"]*2 - board_width + 1)**2
  if head["y"]*2 < (board_height - 1):
    moves_score["up"] += 100*(board_height - 1 - head["y"]*2)**2
  elif head["y"]*2 > (board_height - 1):
    moves_score["down"] += 100*(head["y"]*2 - board_height + 1)**2

  # 食べ物による

  # 盤上の各マスについて、自分が相手より先に到達できるマスを数え、より到達可能マスが多い方向のスコアを上げる。
  # ただし、到達可能マスが少ないほどスコアの上昇率が大きくなるようにする。
  # あるいは、到達可能マスが小さい場合は、到達可能マスによるスコア変動を大きく、到達可能マスが大きい場合は、食べ物や真ん中偏重によるスコア変動を大きくする。

  return calc_best_move(moves_score, turn)

def count_reachable_cells(safe_moves, m_body, e_body, foods):
  cells = [[0 for _ in range(board_height)] for _ in range(board_width)]
  my_reachable_cells = 0
  enemy_reachable_cells = 0
  my_body = m_body.copy()
  enemy_body = e_body.copy()
  enemy_safe_moves = find_safe_moves(enemy_body[0], enemy_body, my_body, [])

  # cellsの初期化。無：0、食べ物：-1、体：1、自分到達：1000+長さ、敵到達：2000+長さ。
  my_length = len(my_body)
  for body in my_body:
    cells[body["x"]][body["y"]] = 1
  for body in enemy_body:
    cells[body["x"]][body["y"]] = 1
  for food in foods:
    cells[food["x"]][food["y"]] = -1
  for move in safe_moves:
    cells_temp = cells.copy()
    listner_cells = [move_to_coordinate(my_body[0], move)]
    for en_move in enemy_safe_moves:
      listner_cells.append(move_to_coordinate(enemy_body[0], en_move))
    while len(listner_cells) > 0:
      new_listner_cells = []
      for listner_cell in listner_cells:
        x = listner_cell["x"]
        y = listner_cell["y"]
        
      listner_cells = new_listner_cells

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