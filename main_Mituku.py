# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>s
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
        "author": "SnAkE",  # TODO: Your Battlesnake Username
        "color": "#006400",  # TODO: Choose color
        "head": "replit-mark",  # TODO: Choose head
        "tail": "mouse",  # TODO: Choose tail
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
    length_for_tail = game_state["you"]["length"] - 1 #蛇のしっぽの再現のための変数
    my_tail = game_state["you"]["body"][length_for_tail] #蛇のしっぽの先

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    def prevent_bound(x1,y1):

        board_width = game_state['board']['width']
        board_height = game_state['board']['height']
    
        if my_head["x"] + x1 == 0:
            is_move_safe["left"] = False

        if my_head["x"] + x1 == board_width - 1:
            is_move_safe["right"] = False

        if my_head["y"] + y1 ==  0:
            is_move_safe["down"] = False

        if my_head["y"] + y1 == board_height - 1:
            is_move_safe["up"] = False

    prevent_bound(0,0)


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    my_body = game_state['you']['body']
    cutted_my_tail = my_body.pop()                            #蛇のしっぽの先だけポップさせている
    
    for body in my_body:
    
        if my_head["x"] - 1 == body["x"] and my_head["y"] == body["y"]:
            is_move_safe["left"] = False

        if my_head["x"] + 1 == body["x"] and my_head["y"] == body["y"]:
            is_move_safe["right"] = False

        if my_head["y"] - 1 == body["y"] and my_head["x"] == body["x"]:
            is_move_safe["down"] = False

        if my_head["y"] + 1 == body["y"] and my_head["x"] == body["x"]:
            is_move_safe["up"] = False

    my_body = game_state['you']['body']                                   #蛇のしっぽを復活


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    all_food = game_state['board']['food']
    my_health = game_state['you']['health']

    if my_health > 20:
           
        for food in all_food:

            if my_head["x"] - 1 == food["x"] and my_head["y"] == food["y"]:
                is_move_safe["left"] = False

            if my_head["x"] + 1 == food["x"] and my_head["y"] == food["y"]:
                is_move_safe["right"] = False

            if my_head["y"] - 1 == food["y"] and my_head["x"] == food["x"]:
                is_move_safe["down"] = False

            if my_head["y"] + 1 == food["y"] and my_head["x"] == food["x"]:
                is_move_safe["up"] = False

    #餌と壁なら餌を選ぶ

    if is_move_safe["left"] == False and is_move_safe["right"] == False and is_move_safe["up"] == False and is_move_safe["down"] == False and ( my_head["x"] - 1 == food["x"] and my_head["y"] == food["y"] ):
        is_move_safe["left"] = True

    if is_move_safe["left"] == False and is_move_safe["right"] == False and is_move_safe["up"] == False and is_move_safe["down"] == False and ( my_head["x"] + 1 == food["x"] and my_head["y"] == food["y"] ):
        is_move_safe["right"] = True

    if is_move_safe["left"] == False and is_move_safe["right"] == False and is_move_safe["up"] == False and is_move_safe["down"] == False and ( my_head["y"] - 1 == food["y"] and my_head["x"] == food["x"] ):
        is_move_safe["down"] = True

    if is_move_safe["left"] == False and is_move_safe["right"] == False and is_move_safe["up"] == False and is_move_safe["down"] == False and ( my_head["y"] + 1 == food["y"] and my_head["x"] == food["x"] ):
        is_move_safe["up"] = True


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    opponents = game_state['board']['snakes']

    #短絡的袋小路の回避


    

    








    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    

    
    


    

    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8002"})
