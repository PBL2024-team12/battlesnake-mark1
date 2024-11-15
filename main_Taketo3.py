# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import time

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Taketo Usui",  # TODO: Your Battlesnake Username
        "color": "#FFCC4E",  # TODO: Choose color
        "head": "tiger-king",  # TODO: Choose head
        "tail": "tiger-tail",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    start_process_time = time.perf_counter()

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    next_move = "up"
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})


def find_safe_move(field_size, my_snake, foods):
    head = my_snake[0]
    safe_moves = ["up", "down", "left", "right"]
    if(head["x"] == 0):
        safe_moves.pop(safe_moves.index("left"))
    elif(head["x"] == field_size[0] - 1):
        safe_moves.pop(safe_moves.index("right"))
    if(head["y"] == 0):
        safe_moves.pop(safe_moves.index("down"))
    elif(head["y"] == field_size[1] - 1):
        safe_moves.pop(safe_moves.index("up"))
    
    for body in my_snake[1:-1]:
        if ("down" in safe_moves and head["x"] == body["x"] and head["y"] == body["y"] + 1):
            safe_moves.pop(safe_moves.index("down"))
            break
        if ("up" in safe_moves and head["x"] == body["x"] and head["y"] == body["y"] - 1):
            safe_moves.pop(safe_moves.index("up"))
            break
        if ("right" in safe_moves and head["x"] == body["x"] + 1 and head["y"] == body["y"]):
            safe_moves.pop(safe_moves.index("right"))
            break
        if ("left" in safe_moves and head["x"] == body["x"] - 1 and head["y"] == body["y"]):
            safe_moves.pop(safe_moves.index("left"))
            break
    
    avoid_food_moves = safe_moves.copy()
    for food in foods:
        if ("down" in avoid_food_moves and head["x"] == food["x"] and head["y"] == food["y"] + 1):
            avoid_food_moves.pop(avoid_food_moves.index("down"))
        if ("up" in avoid_food_moves and head["x"] == food["x"] and head["y"] == food["y"] - 1):
            avoid_food_moves.pop(avoid_food_moves.index("up"))
        if ("right" in avoid_food_moves and head["x"] == food["x"] + 1 and head["y"] == food["y"]):
            avoid_food_moves.pop(avoid_food_moves.index("right"))
        if ("left" in avoid_food_moves and head["x"] == food["x"] - 1 and head["y"] == food["y"]):
            avoid_food_moves.pop(avoid_food_moves.index("left"))

    return safe_moves, avoid_food_moves

# 目的地への最短ルート探索（目的地以外の食べ物を避ける）
def find_root(field_size, my_snake, snake_length, foods, destination, distance, max_distance):
    head = my_snake[0]
    roots = []
    if head == destination:
        return [head]
    elif max_distance >= 1 and distance >= max_distance:
        return "no way"
    elif abs(head["x"] - destination["x"]) + abs(head["y"] - destination["y"]) == 1:
        return [destination, head]
    
    safe_move_returned = find_safe_move(field_size, my_snake[:snake_length], foods)
    ways = safe_move_returned[1]

    if len(ways) == 0:
        return "no way"
    else:
        for way in ways:
            next_snake = my_snake.copy()
            if way == "up":
                next_snake.insert(0, {"x": head["x"], "y": head["y"] + 1})
            elif way == "down":
                next_snake.insert(0, {"x": head["x"], "y": head["y"] - 1})
            elif way == "right":
                next_snake.insert(0, {"x": head["x"] + 1, "y": head["y"]})
            elif way == "left":
                next_snake.insert(0, {"x": head["x"] - 1, "y": head["y"]})
            
            next_head = next_snake[0]
            return_OK = False
            # 最短ルート探索において、同じ経路は繰り返さない。
            for i, foot_print in enumerate(my_snake[: - snake_length]):
                if i != 0 and head == foot_print and my_snake[i-1] == next_head:
                    return_OK = True
                    break
            if return_OK:
                # roots.append( [head, {"x": -1, "y": -1}] )
                continue

            new_roots = find_root(field_size, next_snake, snake_length, foods, destination, distance + 1, max_distance)
            if new_roots != "no way":
                for new_root in new_roots:
                    roots.append(new_root.insert(0, head))
            # １つでもルートが見つかれば、それ以外は探索しない
            if len(roots) != 0:
                return roots
    if len(roots) == 0:
        return "no way"
    else:
        return roots

# 次のターンで最も近い食べ物への距離を計算できれば、尻尾を追うモードを継続して良いかどうかを判断できる？