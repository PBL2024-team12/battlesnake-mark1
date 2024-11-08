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
# 

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#26CF04",  # TODO: Choose color   a
        "head": "shark",  # TODO: Choose head
        "tail": "swirl",  # TODO: Choose tail
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

    #安全に進む選択肢が複数ある場合に最善の選択肢を選ぶための関数
    recom={"up":False, "down":False, "left":False,"right":False}
    #標準搭載の関数。食べ物を食べるなど、比較的危険を多くする選択肢は一度除いてある
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    #比較的危険を多くする選択肢だが即死はしない行き方を格納したもの。
    #emerは角に行くことを最終手段として許す関数
    emer={"up":False, "down":False, "left":False,"right":False}
    #emer2は
    emer2={"up":False, "down":False, "left":False,"right":False}
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    bigth=game_state["you"]["length"]

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
    
    if my_head["x"]==board_width-1:
        is_move_safe["right"]=False
    elif my_head["x"]==0:
        is_move_safe["left"]=False
    if my_head["y"]==board_width-1:
        is_move_safe["up"]=False
    elif my_head["y"]==0:
        is_move_safe["down"]=False
    
    #角を避ける(行き止まりに行くことを減らしたい)
    if my_head["x"]==board_width-1 or my_head["x"]==0:
        #蛇の長さによって場合分け(最初は食べる事より端でよけることを優先する)
        if bigth<=4:
            if my_head["y"]==1:
                is_move_safe["down"]=False
                emer2["down"]=True
                recom["up"]=True
            elif my_head["y"]==board_width-2:
                is_move_safe["up"]=False
                emer2["up"]=True
                recom["down"]=True
        else:
            if my_head["y"]<=2:
                is_move_safe["down"]=False
                emer2["down"]=True
                recom["up"]=True
            elif my_head["y"]>=board_width-3:
                is_move_safe["up"]=False
                emer2["up"]=True
                recom["down"]=True
    elif my_head["y"]==board_width-1 or my_head["y"]==0:
        #蛇の長さによって場合分け(最初は食べる事より端でよけることを優先する)
        if bigth<=4:
            if my_head["x"]==1:
                is_move_safe["left"]=False
                emer2["left"]=True
                recom["right"]=True
            elif my_head["x"]>=board_width-2:
                is_move_safe["right"]=False
                emer2["right"]=True
                recom["left"]=True
        else:
            if my_head["x"]<=2:
                is_move_safe["left"]=False
                emer2["left"]=True
                recom["right"]=True
            elif my_head["x"]>=board_width-3:
                is_move_safe["right"]=False
                emer2["right"]=True
                recom["left"]=True
    
    # 自身の体とぶつからないようにする
    body = game_state['you']['body']
    for segment in body[1:-1]:  # 頭と尾を除く
        if segment["x"] == my_head["x"] and segment["y"] == my_head["y"] + 1:
            is_move_safe["up"] = False
        elif segment["x"] == my_head["x"] and segment["y"] == my_head["y"] - 1:
            is_move_safe["down"] = False
        elif segment["x"] == my_head["x"] - 1 and segment["y"] == my_head["y"]:
            is_move_safe["left"] = False
        elif segment["x"] == my_head["x"] + 1 and segment["y"] == my_head["y"]:
            is_move_safe["right"] = False

    # 食べ物をhpが少なくなるまで避ける
    food = game_state['board']['food']
    my_health = game_state["you"]["health"]
    next_move="0"
    if food:
        if my_health>15:
            for f in food:
                if f["x"] == my_head["x"] and f["y"] == my_head["y"] + 1:
                    is_move_safe["up"] = False
                    emer["up"]=True
                elif f["x"] == my_head["x"] and f["y"] == my_head["y"] - 1:
                    is_move_safe["down"] = False
                    emer["down"]=True
                elif f["x"] == my_head["x"] - 1 and f["y"] == my_head["y"]:
                    is_move_safe["left"] = False
                    emer["left"]=True
                elif f["x"] == my_head["x"] + 1 and f["y"] == my_head["y"]:
                    is_move_safe["right"] = False
                    emer["right"]=True
        else:
            min=12*(2**0.5)
            for f in food:
                if f["x"] == my_head["x"] and f["y"] == my_head["y"] + 1:
                    next_move="up"
                    break
                elif f["x"] == my_head["x"] and f["y"] == my_head["y"] - 1:
                    next_move="down"
                    break
                elif f["x"] == my_head["x"] - 1 and f["y"] == my_head["y"]:
                    next_move="left"
                    break
                elif f["x"] == my_head["x"] + 1 and f["y"] == my_head["y"]:
                    next_move="right"
                # 食べ物が一番近くにあるか探す
                # 三平方の定理を利用して、直線距離で近い食べ物を探す
                dist=((f["x"]-my_head["x"])**2+(f["x"]-my_head["y"])**2)**0.5
                if(dist<min):
                    min=dist
                    xmin=f["x"]
                    ymin=f["y"]
            if(next_move=="0"):
                #食べ物に近づくことを最善策とする
                if my_head["x"]<xmin:
                    recom["right"]=True
                elif my_head["x"]>xmin:
                    recom["left"]=True
                if my_head["y"]>ymin:
                    recom["down"]=True
                elif my_head["y"]<ymin:
                    recom["up"]=True            
                
                    
                
                    
         

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    # This is only duel

    # Are there any safe moves left?
    safe_moves = []
    rec_moves=[]
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    
    #安全な行き先が複数ある時、最善の行き先を選択する
    if len(safe_moves)>=2:
        for move, isSafe in recom.items():
            if isSafe:
                rec_moves.append(move)
                for i in range(len(safe_moves)):
                    if rec_moves[len(rec_moves)-1]==safe_moves[i]:
                        next_move=rec_moves[len(rec_moves)-1]
        

    #消去法
    if len(safe_moves) == 0:
        for move,isSafe in emer.items():
            if isSafe:
                safe_moves.append(move)
                print("emerge")
    if len(safe_moves) == 0:
        for move,isSafe in emer2.items():
             if isSafe:
                safe_moves.append(move)
                print("emerge2")
    if len(safe_moves)==0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    # hpが少ない時、食べ物がある方向に行く
    print(safe_moves)
        
        
        
    
        
    if next_move=="0":    
        next_move = random.choice(safe_moves)
    

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8004"})
