import random
import typing
import asyncio
import time

def info() -> typing.Dict:
  print("INFO")

  return {
      "apiversion": "1",
      "author": "Taketo Usui",
      "color": "#FFFFFF",
      "head": "tiger-king",
      "tail": "tiger-tail",
  }

def start(game_state: typing.Dict):
  print("GAME START")

def end(game_state: typing.Dict):
  print("GAME OVER\n")

board_width = 0
board_height = 0
time_spent = 0
MAX_TIME = 10000

# メイン関数
def move(game_state: typing.Dict) -> typing.Dict:
  # 以下、各種変数の初期化。
  global board_width, board_height
  board_width = game_state["board"]["width"]
  board_height = game_state["board"]["height"]
  turn = game_state["turn"]
  foods = game_state["board"]["food"]
  move_options = ["up", "down", "left", "right"]

  my_body = game_state["you"]["body"]
  head = my_body[0]
  enemy_body = []
  for snakes in game_state["board"]["snakes"]:
    if snakes["id"] != game_state["you"]["id"]:
      enemy_body = snakes["body"]
  moves_score = {"left": 0, "right": 0, "up": 0, "down": 0}

  hungry = 1 # 空腹度
  if turn < 50:
    hungry = 10
  elif turn < 100:
    hungry = 7
  elif turn < 150:
    hungry = 4
  elif turn < 250:
    hungry = 2
  # 変数の初期化、ここまで

  # 次のターンで死なない。
  safe_moves = find_safe_moves(head, my_body, enemy_body, [])
  for move in safe_moves:
    moves_score[move] += 50000
  if len(enemy_body) > len(my_body):
    extra_safe_moves = find_safe_moves(head, my_body, enemy_body, [move_to_coordinate(enemy_body[0], "up"), move_to_coordinate(enemy_body[0], "down"), move_to_coordinate(enemy_body[0], "left"), move_to_coordinate(enemy_body[0], "right")])
    for move in extra_safe_moves:
      moves_score[move] += 50000
  if len(safe_moves) <= 1 or len(enemy_body) < 1:
    return calc_best_move(moves_score, turn)
  
  # 袋小路を避ける。
  if len(enemy_body) != 0:
    enemy_safe_moves = find_safe_moves(enemy_body[0], enemy_body, my_body, [])
    enemy_next_heads = [move_to_coordinate(enemy_body[0], move) for move in enemy_safe_moves]
    enemy_option_data = {"heads": enemy_next_heads, "body": enemy_body[:-1], "original_bodies": enemy_body[:-1]}

    for move in safe_moves:
      new_head = move_to_coordinate(head, move)
      isOnFood = False
      for food in foods:
        if new_head == food:
          isOnFood = True
          break
      if isOnFood:
        new_my_body = [new_head] + my_body
      else:
        new_my_body = [new_head] + my_body[:-1]
      
      global time_spent
      time_spent = 0
      span = life_span(new_head, new_my_body, enemy_option_data, foods, 10)
      moves_score[move] += span*2000

  # 食べ物を取る。
  board_scale = board_width + board_height
  for food in foods:
    distance = abs(head["x"] - food["x"]) + abs(head["y"] - food["y"])
    distance_from_enemy = abs(enemy_body[0]["x"] - food["x"]) + abs(enemy_body[0]["y"] - food["y"])
    if food["x"] <= 0 or food["x"] >= board_width - 1 or food["y"] <= 0 or food["y"] >= board_height - 1:
      importance = 0
    elif distance_from_enemy + 1 > distance:
      if distance == 1:
        importance = 600*hungry
      else:
        importance = pow(max(1, board_scale//2 - distance), 3)//5*hungry
    else:
      importance = 0
    print(f"FOOD {food} (distance: {distance}, importance: {importance})")
    if head["x"] < food["x"]:
      moves_score["right"] += importance
      moves_score["left"] -= importance//2
    elif head["x"] > food["x"]:
      moves_score["left"] += importance
      moves_score["right"] -= importance//2
    if head["y"] < food["y"]:
      moves_score["up"] += importance
      moves_score["down"] -= importance//2
    elif head["y"] > food["y"]:
      moves_score["down"] += importance
      moves_score["up"] -= importance//2
  
  # プレッシャーを与える。
  if len(enemy_body) < len(my_body):
    assertive = 5
  else:
    assertive = 4
  if head["x"] < enemy_body[0]["x"]:
    moves_score["right"] += 100*assertive
    moves_score["left"] -= 50*assertive
  elif head["x"] > enemy_body[0]["x"]:
    moves_score["left"] += 100*assertive
    moves_score["right"] -= 50*assertive
  if head["y"] < enemy_body[0]["y"]:
    moves_score["up"] += 100*assertive
    moves_score["down"] -= 50*assertive
  elif head["y"] > enemy_body[0]["y"]:
    moves_score["down"] += 100*assertive
    moves_score["up"] -= 50*assertive
  
  # 端を極端に避ける。
  if head["x"] == 1:
    moves_score["left"] -= 1000
    moves_score["right"] += 100
  elif head["x"] == board_width - 2:
    moves_score["right"] -= 1000
    moves_score["left"] += 100
  if head["y"] == 1:
    moves_score["down"] -= 1000
    moves_score["up"] += 100
  elif head["y"] == board_height - 2:
    moves_score["up"] -= 1000
    moves_score["down"] += 100

  # ぼんやりと真ん中へ寄る。
  if head["x"] + 1 < board_width//2:
    moves_score["right"] += 100
    moves_score["left"] -= 50
  elif head["x"] - 1 > board_width//2:
    moves_score["left"] += 100
    moves_score["right"] -= 50
  if head["y"] + 1 < board_height//2:
    moves_score["up"] += 100
    moves_score["down"] -= 50
  elif head["y"] - 1 > board_height//2:
    moves_score["down"] += 100
    moves_score["up"] -= 50

  return calc_best_move(moves_score, turn)

# 寿命を計算
def life_span(my_head, my_body, enemy_option_data, foods, depth) -> int:
  if depth == 0:
    return 0
  
  safe_moves = find_safe_moves(my_head, my_body, enemy_option_data["body"], [])
  if len(safe_moves) == 0:
    return 0
  
  global time_spent
  global MAX_TIME
  
  new_enemy_body = enemy_option_data["body"].copy()
  if len(enemy_option_data["original_bodies"]) > 0:
    new_enemy_original_bodies = enemy_option_data["original_bodies"].copy()
    new_enemy_original_bodies.pop()
  else:
    new_enemy_original_bodies = []
  new_enemy_heads = []
  new_enemy_head_possible = []
  for head in enemy_option_data["heads"]:
    for move in ["up", "down", "left", "right"]:
      new_enemy_head = move_to_coordinate(head, move)
      if new_enemy_head not in new_enemy_head_possible:
        new_enemy_head_possible.append(new_enemy_head)
  for possible_head in new_enemy_head_possible:
    if possible_head["x"] < 0 or possible_head["x"] >= board_width or possible_head["y"] < 0 or possible_head["y"] >= board_height:
      continue
    else:
      if possible_head not in new_enemy_body and possible_head not in my_body:
        new_enemy_heads = [possible_head] + new_enemy_heads
        continue
  max_span = 0
  for move in safe_moves:
    new_my_head = move_to_coordinate(my_head, move)
    isOnFood = False
    for food in foods:
      if new_my_head == food:
        isOnFood = True
        break
    if isOnFood:
      new_my_body = [new_my_head] + my_body
    else:
      new_my_body = [new_my_head] + my_body[:-1]
    time_spent += 1
    if time_spent < MAX_TIME:
      span = life_span(new_my_head, new_my_body, {"heads": new_enemy_heads, "body": new_enemy_body, "original_bodies": new_enemy_original_bodies}, foods, depth-1)
    else:
      return max_span
    if span >= depth - 1:
      return depth
    else:
      if span > max_span:
        max_span = span
  return max_span
  
# 上下左右のうち、死なないマス（空白のマスまたは食べ物だけがあるマス）の方向をすべて返す。
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
  
  if "up" in moves and ((up_head in my_body[:-1]) or (up_head in enemy_body[:-1]) or (up_head in obstacles)):
    moves.remove("up")
  if "down" in moves and ((down_head in my_body[:-1]) or (down_head in enemy_body[:-1]) or (down_head in obstacles)):
    moves.remove("down")
  if "left" in moves and ((left_head in my_body[:-1]) or (left_head in enemy_body[:-1]) or (left_head in obstacles)):
    moves.remove("left")
  if "right" in moves and ((right_head in my_body[:-1]) or (right_head in enemy_body[:-1]) or (right_head in obstacles)):
    moves.remove("right")

  return moves

# 基準マスの上下左右のマスを、座標として返す。
def move_to_coordinate(coordinate: typing.Dict, move: str) -> typing.Dict:
  if move == "up":
    return {"x": coordinate["x"], "y": coordinate["y"] + 1}
  elif move == "down":
    return {"x": coordinate["x"], "y": coordinate["y"] - 1}
  elif move == "left":
    return {"x": coordinate["x"] - 1, "y": coordinate["y"]}
  elif move == "right":
    return {"x": coordinate["x"] + 1, "y": coordinate["y"]}

# スコアの中で最も高いスコアを持つ手を返す。
# また、選択された手をコマンドラインに出力する。
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

  print (f"moves_score: {moves_score}")
  return {"move": bestmove}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8000"})