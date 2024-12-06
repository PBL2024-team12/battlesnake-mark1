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

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    my_body = game_state['you']['body']

    all_food = game_state['board']['food']

    my_health = game_state['you']['health']

    food0 = game_state["board"]["food"][0]
    if len(game_state["board"]["food"]) > 2:
        food1 = game_state["board"]["food"][1]
        food2 = game_state["board"]["food"][2]

    dead_end_counter = 0 #このカウンターで再帰が何回目なのか判断する．




    def avoid_neck(x1,y1,z1):#どのような動きをしても首は固定で一方向制限されるのでカウントする必要がない．
        if z1 == 0:
            if my_neck["x"] < my_head["x"] + x1:  # Neck is left of head, don't move left
                    is_move_safe["left"] = False
            elif my_neck["x"] > my_head["x"] + x1:  # Neck is right of head, don't move right
                    is_move_safe["right"] = False
            elif my_neck["y"] < my_head["y"] + y1:  # Neck is below head, don't move down
                    is_move_safe["down"] = False
            elif my_neck["y"] > my_head["y"] + y1:  # Neck is above head, don't move up
                    is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    def prevent_bound(x1,y1,z1):
        bound_count = 0
    
        if my_head["x"] + x1 == 0:
            if z1 == 0:
                is_move_safe["left"] = False
            else:
                bound_count = bound_count + 1

        if my_head["x"] + x1 == board_width - 1:
            if z1 == 0:
                is_move_safe["right"] = False
            else:
                bound_count = bound_count + 1

        if my_head["y"] + y1 ==  0:
            if z1 == 0:
                is_move_safe["down"] = False
            else:
                bound_count = bound_count + 1

        if my_head["y"] + y1 == board_height - 1:
            if z1 == 0:
                is_move_safe["up"] = False
            else:
                bound_count = bound_count + 1

        return bound_count

    

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']
    
    
    

    def prevent_itself(x1,y1,z1):

        #蛇のしっぽの先だけポップさせている（バグるので今は停止）
        if z1 == 0:
            cutted_my_tail = my_body.pop()  
                                     
        itself_count = 0
    
        for body in my_body:
    
            if my_head["x"] + x1 - 1 == body["x"] and my_head["y"] + y1 == body["y"]:
                if z1 == 0:
                    is_move_safe["left"] = False
                else:
                    itself_count = itself_count + 1

            if my_head["x"] + x1 + 1 == body["x"] and my_head["y"] + y1 == body["y"]:
                if z1 == 0:
                    is_move_safe["right"] = False
                else:
                    itself_count = itself_count + 1

            if my_head["y"] + y1 - 1 == body["y"] and my_head["x"] + x1 == body["x"]:
                if z1 == 0:
                    is_move_safe["down"] = False
                else:
                    itself_count = itself_count + 1

            if my_head["y"] + y1 + 1 == body["y"] and my_head["x"] + x1 == body["x"]:
                if z1 == 0:
                    is_move_safe["up"] = False
                else:
                    itself_count = itself_count + 1

                                           #ここで蛇のしっぽを復活？(関数化しているので今は不要)

        return itself_count

    

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    

    def prevent_food(x1,y1,z1):

        
        food_count = 0
           
        for food in all_food:

            if my_head["x"] + x1 - 1 == food["x"] and my_head["y"] + y1 == food["y"]:
                if z1 == 0:
                    is_move_safe["left"] = False
                else:
                    food_count = food_count + 1

            if my_head["x"] + x1 + 1 == food["x"] and my_head["y"] + y1 == food["y"]:
                if z1 == 0:
                    is_move_safe["right"] = False
                else:
                    food_count = food_count + 1

            if my_head["y"] + y1 - 1 == food["y"] and my_head["x"] + x1 == food["x"]:
                if z1 == 0:
                    is_move_safe["down"] = False
                else:
                    food_count = food_count + 1

            if my_head["y"] + y1 + 1 == food["y"] and my_head["x"] + x1 == food["x"]:
                if z1 == 0:
                    is_move_safe["up"] = False
                else:
                    food_count = food_count + 1

        return food_count

    


    

    #餌と壁なら餌を選ぶ
    def rather_food_than_border():
        for food in all_food:

            if is_move_safe["left"] == False and is_move_safe["right"] == False and is_move_safe["up"] == False and is_move_safe["down"] == False:
                
                if my_head["x"] - 1 == food["x"] and my_head["y"] == food["y"]:
                    is_move_safe["left"] = True

                if my_head["x"] + 1 == food["x"] and my_head["y"] == food["y"]:
                    is_move_safe["right"] = True

                if my_head["y"] - 1 == food["y"] and my_head["x"] == food["x"]:
                    is_move_safe["down"] = True

                if my_head["y"] + 1 == food["y"] and my_head["x"] == food["x"]:
                    is_move_safe["up"] = True


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    opponents = game_state['board']['snakes']

#短絡的袋小路の回避

    

    def avoid_dead_end(x1,y1,z1,u,d,r,l):
        if z1 ==0:
            next_left_obstacle_count = next_right_obstacle_count = next_down_obstacle_count = next_up_obstacle_count = 10000
        else:
            next_left_obstacle_count = next_right_obstacle_count = next_down_obstacle_count = next_up_obstacle_count = 4
        
        if is_move_safe["left"] == True:

            next_left_obstacle_count = 0

            next_left_obstacle_count = next_left_obstacle_count + prevent_bound(x1-1,y1,1) + prevent_itself(x1-1,y1,1)
            
            #if z1 == 0:
                #next_left_obstacle_count = next_left_obstacle_count + avoid_dead_end(-1,0,1,1,0,0,0) + avoid_dead_end(-1,0,1,0,1,0,0) + avoid_dead_end(-1,0,1,0,0,1,0) + avoid_dead_end(-1,0,1,0,0,0,1)

        if my_health > 10:
            next_left_obstacle_count = next_left_obstacle_count + prevent_food(x1-1,y1,1)

        if is_move_safe["right"] == True:
                
            next_right_obstacle_count = 0

            next_right_obstacle_count = next_right_obstacle_count + prevent_bound(x1+1,y1,1) + prevent_itself(x1+1,y1,1) 

            #if z1 == 0:
                #next_right_obstacle_count = next_right_obstacle_count + avoid_dead_end(1,0,1,1,0,0,0) + avoid_dead_end(1,0,1,0,1,0,0) + avoid_dead_end(1,0,1,0,0,1,0) + avoid_dead_end(1,0,1,0,0,0,1)

        if my_health > 10:
            next_right_obstacle_count = next_right_obstacle_count + prevent_food(x1+1,y1,1)

        if is_move_safe["down"] == True:
                
            next_down_obstacle_count = 0

            next_down_obstacle_count = next_down_obstacle_count + prevent_bound(x1,y1+-1,1) + prevent_itself(x1,y1-1,1) 

            #if z1 == 0:
                #next_down_obstacle_count = next_down_obstacle_count + avoid_dead_end(0,-1,1,1,0,0,0) + avoid_dead_end(0,-1,1,0,1,0,0) + avoid_dead_end(0,-1,1,0,0,1,0) + avoid_dead_end(0,-1,1,0,0,0,1)
                
        if my_health > 10:
            next_down_obstacle_count = next_down_obstacle_count + prevent_food(x1,y1-1,1)

        if is_move_safe["up"] == True:
                
            next_up_obstacle_count = 0

            next_up_obstacle_count = next_up_obstacle_count + prevent_bound(x1,y1+1,1) + prevent_itself(x1,y1+1,1) 

            #if z1 == 0:
                #next_up_obstacle_count = next_up_obstacle_count + avoid_dead_end(0,1,1,1,0,0,0) + avoid_dead_end(0,1,1,0,1,0,0) + avoid_dead_end(0,1,1,0,0,1,0) + avoid_dead_end(0,1,1,0,0,0,1)

        if my_health > 10:
                next_up_obstacle_count = next_up_obstacle_count + prevent_food(x1,y1+1,1)

        next_min_count = min(next_left_obstacle_count, next_right_obstacle_count, next_down_obstacle_count, next_up_obstacle_count)

        done_count = 0

        if z1 == 0:
            if next_min_count < 10000:
        
                if next_min_count == next_left_obstacle_count:
                        is_move_safe["right"] = False
                        is_move_safe["down"] = False
                        is_move_safe["up"] = False
                        done_count = 1

                if next_min_count == next_right_obstacle_count and done_count == 0:
                        is_move_safe["left"] = False
                        is_move_safe["down"] = False
                        is_move_safe["up"] = False
                        done_count = 1

                if next_min_count == next_down_obstacle_count and done_count == 0:
                        is_move_safe["right"] = False
                        is_move_safe["left"] = False
                        is_move_safe["up"] = False
                        done_count = 1

                if next_min_count == next_up_obstacle_count and done_count == 0:
                        is_move_safe["right"] = False
                        is_move_safe["down"] = False
                        is_move_safe["left"] = False
                        done_count = 1
        if d == 1:
            return next_down_obstacle_count
        elif u == 1:
            return next_up_obstacle_count
        elif r == 1:
            return next_right_obstacle_count
        elif l == 1:
            return next_left_obstacle_count
 
                    
    #餌に向かって動く
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
        if my_health < 10:

            for food in all_food:
                distance_to_food[i] = abs(my_head["x"] - food["x"]) + abs(my_head["y"] - food["y"])
                i = i + 1

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

            if min_food_distance == distance_to_food[1] and fd_count == 0:

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

                
            if min_food_distance == distance_to_food[2] and fd_count == 0:

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

    #オススメ関数（行くべき場所を判定して，戻り値として基本は一方向を返す）と，安全関数(行って安全な場所を判定して，戻り値として複数方向を返す)をつくって，
    #二つの関数が出した方向が一致すると
    #全ての判定にprintを付けて，どこの判定を使用したのか確認できるようにするとデバックしやすくなる．
    #100ターン先（餌をぎりぎりで取る時）までの行動を再帰的に関数を使っている人が要るっぽい

    #袋小路がどっちに行ってもいい場合により良い方を選択できるように，餌によって行き止まりだと思っている方を解除したらどうなるのかも書いておくとよいのでは？
        
    #実行ゾーン
    avoid_neck(0,0,0)
    prevent_bound(0,0,0)
    prevent_itself(0,0,0)

    if (my_health > 10 and game_state['you']["length"] < 12) or my_health >15:
        if game_state["turn"] <700:
            prevent_food(0,0,0)
        avoid_dead_end(0,0,0,0,0,0,0)
    else:
        if go_to_food() != 1:
            avoid_dead_end(0,0,0,0,0,0,0)

    rather_food_than_border()
    
    








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
