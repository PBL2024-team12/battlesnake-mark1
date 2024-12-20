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

# 「しない動き」をたくさん設定する。
def move(game_state: typing.Dict) -> typing.Dict:
  global board_width, board_height
  board_width = game_state["board"]["width"]
  board_height = game_state["board"]["height"]

  bestmove = "___"
  moves_score = {"left": 1000000, "right": 1000000, "up": 1000000, "down": 1000000}

  my_body = game_state["you"]["body"]
  head = my_body[0]
  enemy_body = []
  for snakes in game_state["board"]["snakes"]:
    if snakes["id"] != game_state["you"]["id"]:
      enemy_body = snakes["body"]

  # == 次に死なない == #
  # 次、死ぬ動きは0点
  safe_moves = find_safe_moves(head, my_body, enemy_body[:-1])
  for move in ["left", "right", "up", "down"]:
    if not move in safe_moves:
      moves_score[move] = 0
  # 0点以外の動きが1つしかない場合、その動きを選ぶ。一つもなければランダム。
  if len(safe_moves) == 1:
    bestmove = safe_moves[0]
    print(f"MOVE {game_state['turn']}: {bestmove}(only one safe move)")
    return {"move": bestmove}
  elif len(safe_moves) == 0:
    bestmove = random.choice(["left", "right", "up", "down"])
    print(f"MOVE {game_state['turn']}: {bestmove}(no safe move)")
    return {"move": bestmove}
  # 自分以上の長さの敵は、なるべく避ける
  dangerous_enemy_body = []
  if len(enemy_body) >= len(my_body) and enemy_body != []:
    enemy_head = enemy_body[0]
    dangerous_enemy_body.append(up(enemy_head))
    dangerous_enemy_body.append(down(enemy_head))
    dangerous_enemy_body.append(left(enemy_head))
    dangerous_enemy_body.append(right(enemy_head))
  very_safe_moves = find_safe_moves(head, [], dangerous_enemy_body)
  for move in safe_moves:
    if not move in very_safe_moves:
      moves_score[move] = 500000
      safe_moves.remove(move)
  
  if enemy_body == []:
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
      print(f"MOVE {game_state['turn']}: {bestmove}(best move: {bestmoves}, score: {max_score})")
    else:
      bestmove = random.choice(["left", "right", "up", "down"])
      print(f"MOVE {game_state['turn']}: {bestmove}(no best move)")

    return {"move": bestmove}


  # == 袋小路にならない == #
  # 死なない動きについて、それぞれあと何手生きられるかを計算する。※敵の動きも想定する。
  # もし自身の長さ以上に生きられるなら、その動きは1000000点。生きられる長さに限界がある場合、そのターン数を点数とする。
  for move in safe_moves:
    if move == "up":
      new_head = up(head)
    elif move == "down":
      new_head = down(head)
    elif move == "left":
      new_head = left(head)
    elif move == "right":
      new_head = right(head)
    if enemy_body == []:
      span = life_span(new_head, my_body, {"heads": [], "bodies": [], "original_bodies": []}, len(my_body))
    else:
      isOnFood = False
      for food in game_state["board"]["food"]:
        if new_head == food:
          isOnFood = True
          break
      if(not isOnFood):
        new_my_body = [new_head] + my_body[:-1]
      else:
        new_my_body = [new_head] + my_body
      new_enemy_moves = find_safe_moves(enemy_body[0], enemy_body, new_my_body)
      new_enemy_heads = []
      for enemy_move in new_enemy_moves:
        if enemy_move == "up":
          new_enemy_heads.append(up(enemy_body[0]))
        elif enemy_move == "down":
          new_enemy_heads.append(down(enemy_body[0]))
        elif enemy_move == "left":
          new_enemy_heads.append(left(enemy_body[0]))
        elif enemy_move == "right":
          new_enemy_heads.append(right(enemy_body[0]))
      span = life_span(new_head, new_my_body, {"heads": new_enemy_heads, "bodies": enemy_body[:-1], "original_bodies": enemy_body[:-1]}, max([len(my_body), len(enemy_body)]))
    moves_score[move] = span*1000

  print(f"moves_score: {moves_score}")
  # == 敵を逃がさない == #
  # 

  ## 敵の次の次の動きを計算
  enemy_head = enemy_body[0]
  enemy_potencial = find_safe_moves(enemy_head, enemy_body, my_body)
  enemy_possible_coordinates_next = []
  enemy_possible_coordinates_after_next = []
  for potential in enemy_potencial:
    if potential == "up":
      enemy_possible_coordinate_next = up(head)
    elif potential == "down":
      enemy_possible_coordinate_next = down(head)
    elif potential == "left":
      enemy_possible_coordinate_next = left(head)
    elif potential == "right":
      enemy_possible_coordinate_next = right(head)
    enemy_optencial_after_next = find_safe_moves(enemy_possible_coordinate_next, enemy_body, my_body)
    for potential_after_next in enemy_optencial_after_next:
      if potential_after_next == "up":
        enemy_possible_coordinates_after_next.append(up(enemy_possible_coordinate_next))
        enemy_possible_coordinates_next.append(up(enemy_possible_coordinate_next))
      elif potential_after_next == "down":
        enemy_possible_coordinates_after_next.append(down(enemy_possible_coordinate_next))
        enemy_possible_coordinates_next.append(down(enemy_possible_coordinate_next))
      elif potential_after_next == "left":
        enemy_possible_coordinates_after_next.append(left(enemy_possible_coordinate_next))
        enemy_possible_coordinates_next.append(left(enemy_possible_coordinate_next))
      elif potential_after_next == "right":
        enemy_possible_coordinates_after_next.append(right(enemy_possible_coordinate_next))
        enemy_possible_coordinates_next.append(right(enemy_possible_coordinate_next))
  coordinates_tmp = enemy_possible_coordinates_next.copy()
  enemy_possible_coordinate_next = []
  for i, co in enumerate(coordinates_tmp):
    if not co in coordinates_tmp[i+1:]:
      enemy_possible_coordinates_next.append(co)
  coordinates_tmp = enemy_possible_coordinates_after_next.copy()
  enemy_possible_coordinates_after_next = []
  for i, co in enumerate(coordinates_tmp):
    if not co in coordinates_tmp[i+1:]:
      enemy_possible_coordinates_after_next.append(co)
  
  # == より好ましい動きを計算 == #
  for move in safe_moves:
    if move == "up":
      new_head = up(head)
    elif move == "down":
      new_head = down(head)
    elif move == "left":
      new_head = left(head)
    elif move == "right":
      new_head = right(head)
    # = プレッシャーを与える = #
    if new_head in enemy_possible_coordinates_next and len(my_body) > len(enemy_body):
      moves_score[move] += 200000
    if new_head in enemy_possible_coordinates_after_next:
      moves_score[move] += 100000

    # = 可能なら食べ物に近づく = #
    foods = game_state["board"]["food"]
    nearest_food = None
    nearest_food_distance = board_height + board_width
    for i in range(len(foods)):
      food_distance = abs(new_head["x"] - foods[i]["x"]) + abs(new_head["y"] - foods[i]["y"])
      print(f"food: {foods[i]}, distance: {food_distance}")
      if nearest_food is None:
        nearest_food = foods[i]
        nearest_food_distance = food_distance
      elif food_distance < nearest_food_distance:
        nearest_food = foods[i]
        nearest_food_distance = food_distance
    print(f"move: {move}, distance: {nearest_food_distance}, point: {board_height + board_width - nearest_food_distance - max([len(my_body)- len(enemy_body), 0])}")
    moves_score[move] += pow(max([board_height + board_width - nearest_food_distance - max([len(my_body) - len(enemy_body), 0]), 0]), 2)

  print(f"foods: {foods}")
  print(f"moves_score: {moves_score}")
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
    print(f"MOVE {game_state['turn']}: {bestmove}(best move: {bestmoves}, score: {max_score})")
  else:
    bestmove = random.choice(["left", "right", "up", "down"])
    print(f"MOVE {game_state['turn']}: {bestmove}(no best move)")

  return {"move": bestmove}

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
    if up(head) == body and "up" in moves:
      moves.remove("up")
    if down(head) == body and "down" in moves:
      moves.remove("down")
    if left(head) == body and "left" in moves:
      moves.remove("left")
    if right(head) == body and "right" in moves:
      moves.remove("right")
  
  for body in enemy_body:
    if up(head) == body and "up" in moves:
      moves.remove("up")
    if down(head) == body and "down" in moves:
      moves.remove("down")
    if left(head) == body and "left" in moves:
      moves.remove("left")
    if right(head) == body and "right" in moves:
      moves.remove("right")

  return moves

def life_span(head: typing.Dict, my_body, enemy_body: typing.Dict, max_span) -> typing.Dict:
  span = 0
  span_tmp = 0
  if max_span < 1:
    return 1000000
  safe_moves = find_safe_moves(head, my_body, enemy_body["bodies"])
  new_enemy_body = enemy_body_possible(enemy_body, my_body)
  for move in safe_moves:
    if move == "up":
      new_head = up(head)
    elif move == "down":
      new_head = down(head)
    elif move == "left":
      new_head = left(head)
    elif move == "right":
      new_head = right(head)
    
    new_my_body = [new_head] + my_body[:-1]
    span_tmp = life_span(new_head, new_my_body, new_enemy_body, max_span - 1)
    if span_tmp == 1000000:
      return 1000000
    elif span_tmp > span:
      span = span_tmp
  return span + 1

def enemy_body_possible(enemy_body: typing.Dict, my_body: typing.List) -> typing.Dict:
  heads = enemy_body["heads"]
  bodies = enemy_body["bodies"]
  original_bodies = enemy_body["original_bodies"]
  if len(original_bodies) != 0:
    original_tail = original_bodies[-1]
    number_of_bodies_around_tail = 0
    for move in ["up", "down", "left", "right"]:
      if move == "up":
        around = up(original_tail)
      elif move == "down":
        around = down(original_tail)
      elif move == "left":
        around = left(original_tail)
      elif move == "right":
        around = right(original_tail)
      if around in bodies:
        number_of_bodies_around_tail += 1
    if number_of_bodies_around_tail <= 1 and original_tail in bodies:
      bodies.remove(original_tail)
    original_bodies.pop()
  
  next_heads = []
  for head in heads:
    safe_moves = find_safe_moves(head, bodies, my_body)
    for move in safe_moves:
      if move == "up":
        next_head_possible = up(head)
      elif move == "down":
        next_head_possible = down(head)
      elif move == "left":
        next_head_possible = left(head)
      elif move == "right":
        next_head_possible = right(head)
      
      if not next_head_possible in next_heads and not next_head_possible in heads:
        next_heads.append(next_head_possible)
    bodies.append(head)
  return {"heads": next_heads, "bodies": bodies, "original_bodies": original_bodies}
      

def up(coordinate: typing.Dict) -> typing.Dict:
  return {"x": coordinate["x"], "y": coordinate["y"] + 1}

def down(coordinate: typing.Dict) -> typing.Dict:
  return {"x": coordinate["x"], "y": coordinate["y"] - 1}

def left(coordinate: typing.Dict) -> typing.Dict:
  return {"x": coordinate["x"] - 1, "y": coordinate["y"]}

def right(coordinate: typing.Dict) -> typing.Dict:
  return {"x": coordinate["x"] + 1, "y": coordinate["y"]}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8000"})
