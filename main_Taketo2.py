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
from collections import deque

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
    
    field_width = game_state["board"]["width"]
    field_height = game_state["board"]["height"]
    # 0: completely safe, -1: food danger, -2: food, -3: body danger, (positive value): body
    field_array = [[0 for i in range(field_width)] for j in range(field_height)]

    for food in game_state["board"]["food"]:
        field_array[food["y"]][food["x"]] = -2
    for snake in game_state["board"]["snakes"]:
        for i, body in enumerate(snake["body"]):
            field_array[body["y"]][body["x"]] = len(snake["body"]) - i + 1

    my_head = game_state["you"]["body"][0]
    
    foot_prints = deque()
    foot_prints.append(my_head)
    returned_from = ""
    next_direction = ""
    while(len(foot_prints)):
        if(returned_from == ""):
            next_direction = "up"
        elif(returned_from == "up"):
            next_direction = "right"
        elif(returned_from == "right"):
            next_direction = "down"
        elif(returned_from == "down"):
            next_direction = "left"
        else:
            next_direction = ""
    

    
    next_move = random.choice(["up", "down", "left", "right"])
    print(f"MOVE {game_state['turn']}: {next_move}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})