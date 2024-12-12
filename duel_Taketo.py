import random
import typing
import asyncio
import time

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Taketo Usui",
        "color": "#0FCC4E",
        "head": "tiger-king",
        "tail": "tiger-tail",
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
  global this_turn
  this_turn = -1
  print("GAME OVER\n")

bestmove = ""
this_turn = 0
board_width = 0
board_height = 0

moves_examined = 0
# left_queue2 = [], right_queue2 = [], up_queue2 = [], down_queue2 = []

def move(game_state: typing.Dict) -> typing.Dict:
  global bestmove, this_turn, board_width, board_height
  this_turn = game_state["turn"]
  board_width = game_state["board"]["width"]
  board_height = game_state["board"]["height"]
  # loop = asyncio.new_event_loop()
  # asyncio.set_event_loop(loop)
  # loop.run_in_executor(None, calculate_best_move, game_state)
  # # time.sleep(0.4)
  calculate_best_move(game_state)
  print(f"MOVE {game_state['turn']}: {bestmove} ({moves_examined}moves examined)")
  this_turn = -1
  return {"move": bestmove}

def calculate_best_move(game_state: typing.Dict):
  global bestmove, moves_examined
  moves_examined = 0
  root_arrays = {"up": [], "down": [], "left": [], "right": []}
  my_head = game_state["you"]["body"][0]
  enemy_body = []
  bodies_of_snakes = []
  for snake in game_state["board"]["snakes"]:
    bodies_of_snakes.append(snake["body"])
    if snake["id"] != game_state["you"]["id"]:
      enemy_body = snake["body"]
  if len(enemy_body) == 0:
    print("No enemy body")
    return
  safe_pos, safemoves = move_safe(bodies_of_snakes, my_head, len(game_state["you"]["body"]))
  print("safe_moves: ", safemoves)
  bestmove = random.choice(safemoves)
  if len(safemoves) == 0:
    print("No safe moves")
    return
  # while True:
  #   # TODO: enemy_roots_possibleを更新
  #   enemy_head = enemy_body[0]
  #   enemy_roots_possible = []
  #   for i in range(1, moves_examined + 2):
  #     for j in range(0, moves_examined + 2 - i):
  #       if enemy_head["x"] + i < board_width and enemy_head["y"] + j < board_height:
  #         enemy_roots_possible.append({"x": enemy_head["x"] + i, "y": enemy_head["y"] + j})
  #       if enemy_head["x"] - j >= 0 and enemy_head["y"] + i < board_height:
  #         enemy_roots_possible.append({"x": enemy_head["x"] - j, "y": enemy_head["y"] + i})
  #       if enemy_head["x"] - i >= 0 and enemy_head["y"] - j >= 0:
  #         enemy_roots_possible.append({"x": enemy_head["x"] - i, "y": enemy_head["y"] - j})
  #       if enemy_head["x"] + j < board_width and enemy_head["y"] - i >= 0:
  #         enemy_roots_possible.append({"x": enemy_head["x"] + j, "y": enemy_head["y"] - i})
  #   # print("moves_examined: ", moves_examined)
  #   # print("enemy_head: ", enemy_head)
  #   # print("enemy_roots_possible: ", enemy_roots_possible)
  #   # print("---")
  #   # TODO: 動ける各方向に対して、n手先の選択肢の数を求める。
  #   for move in safemoves:
  #     root_array = root_arrays[move]
  #     new_root_array = []
  #     for root in root_array:
  #       bodies_of_snakes = []
  #       bodies_of_snakes.append(enemy_roots_possible)

  #   if(this_turn != game_state["turn"]):
  #     return
  #   # TODO: 最適解を確定
  #   moves_examined += 1
  #   # bestmove = ""


def move_safe(bodies_of_snakes, head, my_length):
  # TODO: 壁や蛇と衝突しない方向。ただし自分より大きい蛇は三方向に弱い当たり判定を持つ
  safe_moves = ["up", "down", "left", "right"]
  safe_posistions = []
  print("head: ", head)
  print("safe_moves: ", safe_moves)
  for move in ["up", "down", "left", "right"]:
    print("move: ", move)
    next_head = head.copy()
    match move:
      case "up":
        next_head["y"] += 1
      case "down":
        next_head["y"] -= 1
      case "left":
        next_head["x"] -= 1
      case "right":
        next_head["x"] += 1
    # 盤面の外に出る場合
    if next_head["x"] < 0 or next_head["x"] >= board_width or next_head["y"] < 0 or next_head["y"] >= board_height:
      safe_moves.remove(move)
      continue

    for body in bodies_of_snakes:
      # 蛇が自分より大きい
      if len(body) >= my_length and body[0] != head:
        # その大きい蛇の頭と次のターンでぶつかり得る場合
        if abs(body[0]["x"] - next_head["x"]) + abs(body[0]["y"] - next_head["y"]) == 1:
          safe_moves.remove(move)
          break
      # 盤上のあらゆる蛇の胴体を避ける
      print("body[:-1]: ", body[:-1])
      for single_body in body[:-1]:
        if single_body == next_head:
          safe_moves.remove(move)
          break
      if move not in safe_moves:
        break
    if move in safe_moves:
      safe_posistions.append(next_head)
  print("safe_moves: ", safe_moves)
  return safe_posistions, safe_moves

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})
