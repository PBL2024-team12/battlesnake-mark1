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
        "author": "Mitsuku",  # TODO: Your Battlesnake Username
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

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    my_body = game_state['you']['body']

    all_food = game_state['board']['food']

    my_health = game_state['you']['health']

    def avoid_bound():
        
            if my_head["x"] == 0:
                    is_move_safe["left"] = False

            if my_head["x"] == board_width - 1:
                    is_move_safe["right"] = False

            if my_head["y"] ==  0:
                    is_move_safe["down"] = False

            if my_head["y"] == board_height - 1:
                    is_move_safe["up"] = False

    
    avoid_bound()

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']
    def avoid_itself():

        #蛇のしっぽの先だけポップさせている（バグるので今は停止）
        cutted_my_tail = my_body.pop()  
    
        for body in my_body:
    
            if my_head["x"] - 1 == body["x"] and my_head["y"] == body["y"]:
                    is_move_safe["left"] = False

            if my_head["x"] + 1 == body["x"] and my_head["y"] == body["y"]:
                    is_move_safe["right"] = False

            if my_head["y"] - 1 == body["y"] and my_head["x"] == body["x"]:
                    is_move_safe["down"] = False

            if my_head["y"] + 1 == body["y"] and my_head["x"] == body["x"]:
                    is_move_safe["up"] = False
                                           #ここで蛇のしっぽを復活？(関数化しているので今は不要)
    
    avoid_itself()

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    opponents = game_state['board']['snakes']
    opponent_body = opponents[1]['body']

    def avoid_opponent_body():
        
        
            opponent_count = 0
    
            for body in opponent_body:
        
                if my_head["x"] - 1 == body["x"] and my_head["y"] == body["y"]:

                        is_move_safe["left"] = False

                if my_head["x"] + 1 == body["x"] and my_head["y"]== body["y"]:

                        is_move_safe["right"] = False

                if my_head["y"] - 1 == body["y"] and my_head["x"] == body["x"]:
                        is_move_safe["down"] = False

                if my_head["y"] + 1 == body["y"] and my_head["x"] == body["x"]:
                        is_move_safe["up"] = False

                                        
    avoid_opponent_body()


    if len(game_state["board"]["food"]) >= 1:
        food0 = game_state["board"]["food"][0]
    if len(game_state["board"]["food"]) >= 2:
        food1 = game_state["board"]["food"][1]
    if len(game_state["board"]["food"]) >= 3:
        food2 = game_state["board"]["food"][2]

    


    recom={"up":False, "down":False, "left":False,"right":False}
    
    def go_to_food():
        #初期化
        recom["down"] = False 
        recom["up"] = False
        recom["left"] = False
        recom["right"] = False
        next_to_food = 0 #餌が隣にあったら1
        distance_to_food = [0,0,0]
        i = 0

        for food in all_food:
            distance_to_food[i] = abs(my_head["x"] - food["x"]) + abs(my_head["y"] - food["y"])
            i = i + 1
            if i == len(game_state["board"]["food"]):
                  break

        min_food_distance = min(distance_to_food[0], distance_to_food[1], distance_to_food[2])
        fd_count = 0

        if min_food_distance == distance_to_food[0]:

            if my_head["x"] - food0["x"] < 0:
                recom["right"] = True

            elif my_head["x"] - food0["x"] > 0:
                recom["left"] = True

            if my_head["y"] - food0["y"] < 0:
                recom["up"] = True

            elif my_head["y"] - food0["y"] > 0:
                recom["down"] = True

            if my_head["x"] - food0["x"] == 0 and my_head["y"] - food0["y"] == 1:
                recom["down"] = True
                recom["up"] = False
                recom["left"] = False
                recom["right"] = False
                next_to_food = 1

            elif my_head["x"] - food0["x"] == 0 and my_head["y"] - food0["y"] == -1:
                recom["down"] = False
                recom["up"] = True
                recom["left"] = False
                recom["right"] = False
                next_to_food = 1

            if my_head["x"] - food0["x"] == 1 and my_head["y"] - food0["y"] == 0:
                recom["down"] = False
                recom["up"] = False
                recom["left"] = True
                recom["right"] = False
                next_to_food = 1

            elif my_head["x"] - food0["x"] == -1 and my_head["y"] - food0["y"] == 0:
                recom["down"] = False
                recom["up"] = False
                recom["left"] = False
                recom["right"] = True
                next_to_food = 1

                fd_count = fd_count + 1

        if min_food_distance == distance_to_food[1] and fd_count == 0 and len(game_state["board"]["food"]) >= 2:

            if my_head["x"] - food1["x"] < 0:
                    recom["right"] = True

            elif my_head["x"] - food1["x"] > 0:
                    recom["left"] = True

            if my_head["y"] - food1["y"] < 0:
                    recom["up"] = True

            elif my_head["y"] - food1["y"] > 0:
                    recom["down"] = True

            if my_head["x"] - food1["x"] == 0 and my_head["y"] - food1["y"] == 1:
                    recom["down"] = True
                    recom["up"] = False
                    recom["left"] = False
                    recom["right"] = False
                    next_to_food = 1

            elif my_head["x"] - food1["x"] == 0 and my_head["y"] - food1["y"] == -1:
                    recom["down"] = False
                    recom["up"] = True
                    recom["left"] = False
                    recom["right"] = False
                    next_to_food = 1

            if my_head["x"] - food1["x"] == 1 and my_head["y"] - food1["y"] == 0:
                    recom["down"] = False
                    recom["up"] = False
                    recom["left"] = True
                    recom["right"] = False
                    next_to_food = 1

            elif my_head["x"] - food1["x"] == -1 and my_head["y"] - food1["y"] == 0:
                    recom["down"] = False
                    recom["up"] = False
                    recom["left"] = False
                    recom["right"] = True
                    next_to_food = 1

            fd_count = fd_count + 1

                
        if min_food_distance == distance_to_food[2] and fd_count == 0 and len(game_state["board"]["food"]) >= 3:

            if my_head["x"] - food2["x"] < 0:
                    recom["right"] = True

            elif my_head["x"] - food2["x"] > 0:
                    recom["left"] = True

            if my_head["y"] - food2["y"] < 0:
                    recom["up"] = True

            elif my_head["y"] - food2["y"] > 0:
                    recom["down"] = True

            if my_head["x"] - food2["x"] == 0 and my_head["y"] - food2["y"] == 1:
                    recom["down"] = True
                    recom["up"] = False
                    recom["left"] = False
                    recom["right"] = False
                    next_to_food = 1

            elif my_head["x"] - food2["x"] == 0 and my_head["y"] - food2["y"] == -1:
                    recom["down"] = False
                    recom["up"] = True
                    recom["left"] = False
                    recom["right"] = False
                    next_to_food = 1

            if my_head["x"] - food2["x"] == 1 and my_head["y"] - food2["y"] == 0:
                    recom["down"] = False
                    recom["up"] = False
                    recom["left"] = True
                    recom["right"] = False
                    next_to_food = 1

            elif my_head["x"] - food2["x"] == -1 and my_head["y"] - food2["y"] == 0:
                    recom["down"] = False
                    recom["up"] = False
                    recom["left"] = False
                    recom["right"] = True
                    next_to_food = 1

            fd_count = fd_count + 1

        if recom["down"] == True and is_move_safe["down"] == True:
            is_move_safe["right"] = False
            is_move_safe["up"] = False
            is_move_safe["left"] = False
        
        if recom["up"] == True and is_move_safe["up"] == True:
            is_move_safe["right"] = False
            is_move_safe["down"] = False
            is_move_safe["left"] = False

        if recom["left"] == True and is_move_safe["left"] == True:
            is_move_safe["right"] = False
            is_move_safe["up"] = False
            is_move_safe["down"] = False

        if recom["right"] == True and is_move_safe["right"] == True:
            is_move_safe["down"] = False
            is_move_safe["up"] = False
            is_move_safe["left"] = False

        if next_to_food == 1:
            return 1

    go_to_food()



    

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

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8000"})