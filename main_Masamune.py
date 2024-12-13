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


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Masamune",  # TODO: Your Battlesnake Username
        "color": "#1f1e33",  # TODO: Choose color
        "head": "all-seeing",  # TODO: Choose head
        "tail": "weight",  # TODO: Choose tail
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

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:  # 左端
        is_move_safe["left"] = False

    elif my_head["x"] == board_width - 1:  # 右端
        is_move_safe["right"] = False

    if my_head["y"] == 0:  # 下
        is_move_safe["down"] = False

    elif my_head["y"] == board_height - 1:  # 上
        is_move_safe["up"] = False
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    left_of_head = {"x": my_head["x"] - 1, "y": my_head["y"]}
    result = left_of_head in my_body
    if result == True:
        is_move_safe["left"] = False
    
    right_of_head = {"x": my_head["x"] + 1, "y": my_head["y"]}
    result = right_of_head in my_body
    if result == True:
        is_move_safe["right"] = False

    down_of_head = {"x": my_head["x"] , "y": my_head["y"] - 1}
    result = down_of_head in my_body
    if result == True:
        is_move_safe["down"] = False

    up_of_head = {"x": my_head["x"] , "y": my_head["y"] + 1}
    result = up_of_head in my_body
    if result == True:
        is_move_safe["up"] = False


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    snakes = game_state['board']['snakes']

    for snake in snakes:
        if snake["name"] != "Masamune":
            result = left_of_head in snake["body"]
            if result == True:
                is_move_safe["left"] = False
            result = right_of_head in snake["body"]
            if result == True:
                is_move_safe["right"] = False
            result = down_of_head in snake["body"]
            if result == True:
                is_move_safe["down"] = False
            result = up_of_head in snake["body"]
            if result == True:
                is_move_safe["up"] = False
    
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    all_food = game_state['board']['food']
    my_health = game_state['you']['health']

    # Choose a random move from the safe ones
    # 体力が10以下なら食べ物に向かう

    food = game_state['board']['food']
    if food:
        # 最も近い食べ物を探す
        closest_food = min(food, key=lambda f: abs(f["x"] - my_head["x"]) + abs(f["y"] - my_head["y"]))
        for snake in snakes:
            if snake["name"] != "Masamune":
                if len(my_body) > len(snake["body"]) + 1:
            # 他のヘビの頭に向かう
                # 最も近い敵のヘビの頭を探す
                    opponent_heads = [snake["body"][0] for snake in snakes]
                    closest_head = min(opponent_heads, key=lambda head: abs(head["x"] - my_head["x"]) + abs(head["y"] - my_head["y"]))

                    # 相手の頭に向かう方向を決定
                    if closest_head["x"] < my_head["x"] and is_move_safe["left"]:
                        next_move = "left"
                    elif closest_head["x"] > my_head["x"] and is_move_safe["right"]:
                        next_move = "right"
                    elif closest_head["y"] < my_head["y"] and is_move_safe["down"]:
                        next_move = "down"
                    elif closest_head["y"] > my_head["y"] and is_move_safe["up"]:
                        next_move = "up"
                    else:
                        # 近づける方向がない場合、ランダムな安全な動きを選択
                        safe_moves = [move for move, is_safe in is_move_safe.items() if is_safe]
                        next_move = random.choice(safe_moves) if safe_moves else "down"
        else:
            # 食べ物への移動方向を決定
            if closest_food["x"] < my_head["x"] and is_move_safe["left"]:
                next_move = "left"
            elif closest_food["x"] > my_head["x"] and is_move_safe["right"]:
                next_move = "right"
            elif closest_food["y"] < my_head["y"] and is_move_safe["down"]:
                next_move = "down"
            elif closest_food["y"] > my_head["y"] and is_move_safe["up"]:
                next_move = "up"
            else:
                next_move = random.choice(safe_moves)  # 安全な動きがない場合、ランダム
            
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8003"})