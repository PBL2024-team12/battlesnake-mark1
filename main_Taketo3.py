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
    body = game_state["you"]["body"]

    print(f'body: {body}')
    safe_move = find_safe_move([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["board"]["food"])
    print(f"safe_move: {safe_move}")

    if(len(body) <= 3):
        for i in range(len(body)):
            for j in range(i+1, len(body)):
                if(body[i] != body[j]):
                    safe_move = find_safe_move([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["board"]["food"])
                    if len(safe_move[1]) != 0:
                        next_move = random.choice(safe_move[1])
                    elif len(safe_move[0]) != 0:
                        next_move = random.choice(safe_move[0])
                    else:
                        next_move = "up"
                    print(f"MOVE {game_state['turn']}: {next_move}")
                    end_process_time = time.perf_counter()
                    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
                    return {"move": next_move}

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    roots_for_tail = find_roots([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["you"]["length"], game_state["board"]["food"], body[-1], 0, game_state["you"]["health"] - 1)
    print(f"roots_for_tail: {roots_for_tail}")
    if roots_for_tail == "no way":
        # 尻尾を追うことができない場合、（たどり着ける中で）最も遠い食べ物を探す
        next_move = move_to_eat(game_state)
    else:
        # 尻尾を追うことができる場合。
        if body[0] == body[-1]:
            safe_move = find_safe_move([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["board"]["food"])
            if len(safe_move[1]) != 0:
                next_move = random.choice(safe_move[1])
            elif len(safe_move[0]) != 0:
                next_move = random.choice(safe_move[0])
            else:
                next_move = "up"
        else:
            print(f"roots_for_tail: {roots_for_tail}")

            if roots_for_tail[0] is None:
                print("ERROR: roots_for_tail is None")
                return {"move": "up"}

            next_position = roots_for_tail[0][1]
            if next_position["x"] == body[0]["x"] and next_position["y"] == body[0]["y"] + 1:
                next_move = "up"
            elif next_position["x"] == body[0]["x"] and next_position["y"] == body[0]["y"] - 1:
                next_move = "down"
            elif next_position["x"] == body[0]["x"] + 1 and next_position["y"] == body[0]["y"]:
                next_move = "right"
            elif next_position["x"] == body[0]["x"] - 1 and next_position["y"] == body[0]["y"]:
                next_move = "left"
            else:
                print("ERROR: next_position is not adjacent to the head")
                return {"move": "up"}
            
            next_body = body.copy()
            next_body.insert(0, next_position)
            for food in game_state["board"]["food"]:
                roots_for_food = find_roots([game_state["board"]["width"], game_state["board"]["height"]], next_body, game_state["you"]["length"], game_state["board"]["food"], food, 0, game_state["you"]["health"] - 1)
                if roots_for_food == "no way" or len(roots_for_food) == 0:
                    continue
                else:
                    next_body = []
            if len(next_body) != 0:
                # 移動した後から動き始めても食べ物にたどり着ける場合、その移動は安全といえる。
                next_move = next_move
            else:
                # 移動した後で食べ物にたどり着けない場合、最も遠い食べ物を探す
                next_move = move_to_eat(game_state)

    print(f"MOVE {game_state['turn']}: {next_move}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    return {"move": next_move}


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
    
    for body in my_snake[1:]:
        if ("down" in safe_moves and head["x"] == body["x"] and head["y"] == body["y"] + 1):
            safe_moves.pop(safe_moves.index("down"))
            break
        if ("up" in safe_moves and head["x"] == body["x"] and head["y"] == body["y"] - 1):
            safe_moves.pop(safe_moves.index("up"))
            break
        if ("right" in safe_moves and head["x"] == body["x"] - 1 and head["y"] == body["y"]):
            safe_moves.pop(safe_moves.index("right"))
            break
        if ("left" in safe_moves and head["x"] == body["x"] + 1 and head["y"] == body["y"]):
            safe_moves.pop(safe_moves.index("left"))
            break
    
    avoid_food_moves = safe_moves.copy()
    for food in foods:
        if ("down" in avoid_food_moves and head["x"] == food["x"] and head["y"] == food["y"] + 1):
            avoid_food_moves.pop(avoid_food_moves.index("down"))
        if ("up" in avoid_food_moves and head["x"] == food["x"] and head["y"] == food["y"] - 1):
            avoid_food_moves.pop(avoid_food_moves.index("up"))
        if ("right" in avoid_food_moves and head["x"] == food["x"] - 1 and head["y"] == food["y"]):
            avoid_food_moves.pop(avoid_food_moves.index("right"))
        if ("left" in avoid_food_moves and head["x"] == food["x"] + 1 and head["y"] == food["y"]):
            avoid_food_moves.pop(avoid_food_moves.index("left"))

    return safe_moves, avoid_food_moves

# 目的地への最短ルート探索（目的地以外の食べ物を避ける）
def find_roots(field_size, my_snake, snake_length, foods, destination, distance, max_distance):
    head = my_snake[0]
    roots = [None]
    if head == destination:
        return [[head]]
    elif max_distance >= 1 and distance >= max_distance:
        return "no way"
    elif abs(head["x"] - destination["x"]) + abs(head["y"] - destination["y"]) == 1:
        return [[head, destination]]
    
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

            new_roots = find_roots(field_size, next_snake, snake_length, foods, destination, distance + 1, max_distance)
            if new_roots != "no way":
                for new_root in new_roots:
                    if new_root is not None and len(new_root) != 0:
                        roots.append(new_root.insert(0, head))
                    else:
                        roots.append([head])
            # １つでもルートが見つかれば、それ以外は探索しない
            if (roots is not None) and (roots[0] is not None) and (len(roots) > 0):
                return roots
    if (roots is None) or (len(roots) == 0) or (roots[0] is None):
        return "no way"
    else:
        return roots

# 目的地への最も遠いルート探索（目的地以外の食べ物を避ける）
def find_farthest_roots(field_size, my_snake, snake_length, foods, destination, distance, max_distance):
    head = my_snake[0]
    roots = []
    if head == destination:
        return [[head]]
    elif max_distance >= 1 and distance >= max_distance:
        return "no way"
    
    safe_move_returned = find_safe_move(field_size, my_snake[:snake_length], foods)
    ways = safe_move_returned[1]

    if len(ways) == 0:
        return "no way"
    else:
        for way in ["up", "down", "right", "left"]:
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
            if next_head == destination:
                roots.append([head, destination])
                continue
            
            if not (way in ways):
                continue

            new_roots = find_roots(field_size, next_snake, snake_length, foods, destination, distance + 1, max_distance)
            if new_roots != "no way":
                for new_root in new_roots:
                    if new_root is not None and len(new_root) != 0:
                        roots.append(new_root.insert(0, head))
                    else:
                        roots.append([head])
    if (roots is None) or (len(roots) == 0) or (roots[0] is None):
        return "no way"
    else:
        return_value = []
        max_distance_found = 0
        for root in roots:
            if len(root) > max_distance_found:
                return_value = root
                max_distance_found = len(root)
            if max_distance_found == max_distance:
                break
        return [return_value]
    
def move_to_eat(game_state: typing.Dict) -> typing.Dict:
    body = game_state["you"]["body"]
    farthest_roots_in_all_foods = []
    farthest_distance_in_all_foods = 0
    for food in game_state["board"]["food"]:
        farthest_roots_for_a_food = find_farthest_roots([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["you"]["length"], game_state["board"]["food"], food, 0, game_state["you"]["health"])
        if farthest_roots_for_a_food == "no way" or len(farthest_roots_for_a_food) == 0:
            continue
        else:
            if len(farthest_roots_for_a_food) > farthest_distance_in_all_foods:
                farthest_roots_in_all_foods = farthest_roots_for_a_food
                farthest_distance_in_all_foods = len(farthest_roots_for_a_food)
    if len(farthest_roots_in_all_foods) == 0:
        # どの食べ物にもたどり着けない場合、安全な移動を探す
        safe_moves = find_safe_move([game_state["board"]["width"], game_state["board"]["height"]], body, game_state["board"]["food"])
        if len(safe_moves[1]) != 0:
            next_move = random.choice(safe_moves[1])
        elif len(safe_moves[0]) != 0:
            next_move = random.choice(safe_moves[0])
        else:
            next_move = "up"
    else:
        next_position = farthest_roots_in_all_foods[1]
        if next_position["x"] == body[0]["x"] and next_position["y"] == body[0]["y"] + 1:
            next_move = "up"
        elif next_position["x"] == body[0]["x"] and next_position["y"] == body[0]["y"] - 1:
            next_move = "down"
        elif next_position["x"] == body[0]["x"] + 1 and next_position["y"] == body[0]["y"]:
            next_move = "right"
        elif next_position["x"] == body[0]["x"] - 1 and next_position["y"] == body[0]["y"]:
            next_move = "left"
        else:
            next_move = "up"
    return next_move


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})