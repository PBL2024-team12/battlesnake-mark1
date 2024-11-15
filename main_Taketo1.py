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
    if(my_head["x"] == 0):
        is_move_safe["left"] = False
    elif(my_head["x"] == board_width - 1):
        is_move_safe["right"] = False
    if(my_head["y"] == 0):
        is_move_safe["down"] = False
    elif(my_head["y"] == board_height - 1):
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    snakes = game_state['board']['snakes']
    for snake in snakes:
        for body in snake['body']:
            if my_head["x"] == body["x"] and my_head["y"]+1 == body["y"]:
                is_move_safe["up"] = False
            if my_head["x"] == body["x"] and my_head["y"]-1 == body["y"]:
                is_move_safe["down"] = False
            if my_head["x"]+1 == body["x"] and my_head["y"] == body["y"]:
                is_move_safe["right"] = False
            if my_head["x"]-1 == body["x"] and my_head["y"] == body["y"]:
                is_move_safe["left"] = False

    # Is the move really safe?
    for direction in ["up", "down", "left", "right"]:
        if not is_move_safe[direction]:
            continue
        direction_safe = ["up", "down", "left", "right"]
        next_head = my_head.copy()
        if direction == "up":
            next_head["y"] += 1
        elif direction == "down":
            next_head["y"] -= 1
        elif direction == "right":
            next_head["x"] += 1
        elif direction == "left":
            next_head["x"] -= 1

        if next_head["x"] == 0:
            direction_safe.pop(direction_safe.index("left"))
        elif next_head["x"] == board_width - 1:
            direction_safe.pop(direction_safe.index("right"))
        if next_head["y"] == 0:
            direction_safe.pop(direction_safe.index("down"))
        elif next_head["y"] == board_height - 1:
            direction_safe.pop(direction_safe.index("up"))
        
        for snake in snakes:
            for body in snake['body']:
                if (next_head["x"] == body["x"] and next_head["y"] == body["y"] + 1):
                    direction_safe.pop(direction_safe.index("down"))
                    break
                if (next_head["x"] == body["x"] and next_head["y"] == body["y"] - 1):
                    direction_safe.pop(direction_safe.index("up"))
                    break
                if (next_head["x"] == body["x"] + 1 and next_head["y"] == body["y"]):
                    direction_safe.pop(direction_safe.index("right"))
                    break
                if (next_head["x"] == body["x"] - 1 and next_head["y"] == body["y"]):
                    direction_safe.pop(direction_safe.index("left"))
                    break
        is_move_safe[direction] = len(direction_safe) > 0

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        end_process_time = time.perf_counter()
        print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
        return {"move": "down", "shout": "I'm stuck!(´;ω;｀)"}

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    
    # calculate the distance to the nearest food
    board_height = game_state['board']['height']
    board_width = game_state['board']['width']
    foods = game_state['board']['food']
    nearest_food = None
    nearest_food_distance = board_height + board_width
    for i in range(len(foods)):
        food_distance = abs(my_head["x"] - foods[i]["x"]) + abs(my_head["y"] - foods[i]["y"])
        if nearest_food is None:
            nearest_food = foods[i]
        elif food_distance < nearest_food_distance:
            nearest_food = foods[i]
            nearest_food_distance = food_distance

    health = game_state['you']['health']
    if health <= nearest_food_distance + 1:
        # if health is low, move towards the nearest food
        if nearest_food["x"] > my_head["x"] and is_move_safe["right"]:
            next_move = "right"
        elif nearest_food["x"] < my_head["x"] and is_move_safe["left"]:
            next_move = "left"
        elif nearest_food["y"] > my_head["y"] and is_move_safe["up"]:
            next_move = "up"
        elif nearest_food["y"] < my_head["y"] and is_move_safe["down"]:
            next_move = "down"
        else:
            next_move = random.choice(safe_moves)
    else:
        # if health is high, aboid both of foods and dangerous moves
        is_move_aboid_food = is_move_safe.copy()
        for food in foods:
            if my_head["x"] == food["x"] and my_head["y"]+1 == food["y"]:
                is_move_aboid_food["up"] = False
            if my_head["x"] == food["x"] and my_head["y"]-1 == food["y"]:
                is_move_aboid_food["down"] = False
            if my_head["x"]+1 == food["x"] and my_head["y"] == food["y"]:
                is_move_aboid_food["right"] = False
            if my_head["x"]-1 == food["x"] and my_head["y"] == food["y"]:
                is_move_aboid_food["left"] = False
        aboid_food_moves = []
        for move, aboidFood in is_move_aboid_food.items():
            if aboidFood:
                aboid_food_moves.append(move)
        print (aboid_food_moves)
        if len(aboid_food_moves) == 0:
            next_move = ""
            if(len(safe_moves) > 1):
                for move in safe_moves:
                    if move == "up" and my_head["y"] <= 1:
                        next_move = "up"
                        break
                    elif move == "down" and my_head["y"] >= board_height - 2:
                        next_move = "down"
                        break
                    elif move == "left" and my_head["x"] <= 1:
                        next_move = "left"
                        break
                    elif move == "right" and my_head["x"] >= board_width - 2:
                        next_move = "right"
                        break
            if next_move == "":
                next_move = random.choice(safe_moves)
        else:
            next_move = ""
            if(len(aboid_food_moves) > 1):
                for move in aboid_food_moves:
                    if move == "up" and my_head["y"] <= 1:
                        next_move = "up"
                        break
                    elif move == "down" and my_head["y"] >= board_height - 2:
                        next_move = "down"
                        break
                    elif move == "left" and my_head["x"] <= 1:
                        next_move = "left"
                        break
                    elif move == "right" and my_head["x"] >= board_width - 2:
                        next_move = "right"
                        break
            if next_move == "":
                next_move = random.choice(aboid_food_moves)
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})