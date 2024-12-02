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
    foods = game_state["board"]["food"]
    field_scale = [game_state["board"]["width"], game_state["board"]["height"]]
    next_move = "up"

    print(f"body: {body}")
    if len(body) <= 3 and body[-2] == body[-1]:
        next_move = random.choice(directions_which_has_biggest_room(field_scale, body, foods))
        print(f"MOVE {game_state['turn']}: {next_move}")
        end_process_time = time.perf_counter()
        print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
        return {"move": next_move}


    # 食べ物を避ける経路
    path = find_avoid_food_path(field_scale, body, foods)
    print(f"path: {path}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    
    if len(path) > 0:
        next_move = path[0]
    else:
        # 食べ物を避ける経路が見つからなかった場合、一旦は食べ物を食べるとして、そのあとに食べ物を避ける空間が広い方向に進む
        next_move = ""
    
    next_position = body[0].copy()
    if next_move == "up":
        next_position["y"] += 1
    elif next_move == "down":
        next_position["y"] -= 1
    elif next_move == "left":
        next_position["x"] -= 1
    elif next_move == "right":
        next_position["x"] += 1
    
    # 食べた後に死ににくいような食べ物を選ぶ
    foods_sorted_with_chance_of_live = []
    for food in foods:
        number_of_ways_from_food = 0
        number_of_ways_from_food_without_food = 0
        ways_count_temp = []
        ways_count_temp_without_food = []
        place_used = []
        for direction_from_food in ["up", "down", "left", "right"]:
            number_of_ways_from_food_temp = 0
            number_of_ways_from_food_without_food_temp = 0
            next = food.copy()
            if direction_from_food == "up":
                next["y"] += 1
            elif direction_from_food == "down":
                next["y"] -= 1
            elif direction_from_food == "left":
                next["x"] -= 1
            elif direction_from_food == "right":
                next["x"] += 1
            if next["x"] < 0 or next["x"] >= field_scale[0] or next["y"] < 0 or next["y"] >= field_scale[1]:
                continue
            if next in body[1:]:
                continue
            for direction_from_next in ["up", "down", "left", "right"]:
                next_next = next.copy()
                if direction_from_next == "up":
                    next_next["y"] += 1
                elif direction_from_next == "down":
                    next_next["y"] -= 1
                elif direction_from_next == "left":
                    next_next["x"] -= 1
                elif direction_from_next == "right":
                    next_next["x"] += 1
                if next_next["x"] < 0 or next_next["x"] >= field_scale[0] or next_next["y"] < 0 or next_next["y"] >= field_scale[1]:
                    continue
                if next_next not in body[1:] and next_next not in place_used:
                    number_of_ways_from_food_temp += 1
                    place_used.append(next_next)
                    if next not in foods and next_next not in foods:
                        number_of_ways_from_food_without_food_temp += 1
                    continue
            ways_count_temp.append(number_of_ways_from_food_temp)
            ways_count_temp_without_food.append(number_of_ways_from_food_without_food_temp)
        for index in range(0, len(ways_count_temp)):
            if index != 0:
                number_of_ways_from_food += ways_count_temp[index]
        for index in range(0, len(ways_count_temp_without_food)):
            if index != 0:
                number_of_ways_from_food_without_food += ways_count_temp_without_food[index]
        
        food_data = {"food": food, "chance_of_live": number_of_ways_from_food or 0, "chance_without_food": number_of_ways_from_food_without_food or 0}
        
        if len(foods_sorted_with_chance_of_live) < 1:
            foods_sorted_with_chance_of_live.append(food_data)
        else:
            inserted = False
            for index in range(0, len(foods_sorted_with_chance_of_live)):
                if number_of_ways_from_food_without_food > foods_sorted_with_chance_of_live[index]["chance_without_food"]:
                    foods_sorted_with_chance_of_live.insert(index, food_data)
                    inserted = True
                    break
            if not inserted:
                foods_sorted_with_chance_of_live.append(food_data)
    edible_foods_avoid_food = []
    for food in foods_sorted_with_chance_of_live:
        if food["chance_without_food"] != 0:
            edible_foods_avoid_food.append(food["food"])

    edible_foods_avoid_death = []
    for food in foods_sorted_with_chance_of_live:
        if food["chance_of_live"] != 0:
            edible_foods_avoid_death.append(food["food"])

    print(f"edible_foods_avoid_food: {edible_foods_avoid_food}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))

    food_reachable = False
    if next_move != "":
        # 次の場所から食べ物を目指すことができるか
        if len(edible_foods_avoid_food) > 0:
            food_to_eat = edible_foods_avoid_food[0]
        elif len(edible_foods_avoid_death) > 0:
            food_to_eat = edible_foods_avoid_death[0]
        else: 
            food_to_eat = foods[0]

        next_body = body[:-1].copy()
        next_body.insert(0, next_position)
        shortest_path_for_food = find_shortest_path(field_scale, next_body, [], food_to_eat)
        if shortest_path_for_food is not None and len(shortest_path_for_food) < game_state["you"]["health"] - 1:
            food_reachable = True
        print(f"food_reachable: {food_reachable}")
        end_process_time = time.perf_counter()
        print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    # もし次の場所から遠い食べ物を目指せないのであれば、たどり着ける中で最も遠い食べ物を目指す。
    if next_move == "" or not food_reachable:
        next_move = ""
        longest_path_for_food = []
        longest_distance_for_food = 0
        for food in edible_foods_avoid_food:
            path_for_food = find_shortest_path(field_scale, body, foods, food)
            if path_for_food is not None and len(path_for_food) < game_state["you"]["health"]:
                if len(path_for_food) > longest_distance_for_food:
                    longest_distance_for_food = len(path_for_food)
                    longest_path_for_food = path_for_food
                continue
        if longest_distance_for_food > 0:
            next_move = longest_path_for_food[0]
        else:
            for food in edible_foods_avoid_death:
                path_for_food = find_shortest_path(field_scale, body, foods, food)
                if path_for_food is not None and len(path_for_food) < game_state["you"]["health"]:
                    if len(path_for_food) > longest_distance_for_food:
                        longest_distance_for_food = len(path_for_food)
                        longest_path_for_food = path_for_food
                    continue
            if longest_distance_for_food > 0:
                next_move = longest_path_for_food[0]
            else:
                biggest_room = directions_which_has_biggest_room(field_scale, body, foods)
                if biggest_room is not None and len(biggest_room) > 0:
                    next_move = random.choice(biggest_room)
                else:
                    next_move = choose_direction_try_to_avoid_obstacles(field_scale, body, foods)

    print(f"MOVE {game_state['turn']}: {next_move}")
    end_process_time = time.perf_counter()
    print('process time: {:.2f}ms'.format((end_process_time - start_process_time)*1000))
    return {"move": next_move}

# 目的地への最短経路を返す
def find_shortest_path(field_scale, body, obstacles, target):
    # 未探索の座標を格納するキュー
    queue = []
    # すでに探索済みの座標を格納するリスト
    searched = []
    # 未探索の座標をキューに追加
    queue.append(body[0])
    # スタート地点からの最短距離を格納する辞書
    distance = {str(body[0]): 0}
    # スタート地点からの最短経路を格納する辞書
    path = {str(body[0]): []}

    while len(queue) > 0:
        # キューの先頭の座標を取得
        current = queue.pop(0)
        # 探索済みの座標に追加
        searched.append(current)
        
        # 4方向に移動
        for direction in ["up", "down", "left", "right"]:
            next = current.copy()
            if direction == "up":
                next["y"] += 1
            elif direction == "down":
                next["y"] -= 1
            elif direction == "left":
                next["x"] -= 1
            elif direction == "right":
                next["x"] += 1
            
            # 体が残っているなら、自分の体の座標はスキップ
            need_care_for_tail = False
            if body[-1] == body[-2]:
                need_care_for_tail = True
            body_len = len(body)
            if body_len > distance[str(current)] + 1:
                if need_care_for_tail:
                    if distance[str(current)] < 1:
                        body_to_care = body
                    else:
                        body_to_care = body[0:-distance[str(current)]]
                else:
                    body_to_care = body[0:-distance[str(current)] - 1]
                if next in body_to_care:
                    continue

            # ゴールに到達したら経路を返す
            if next == target:
                current_path = path[str(current)].copy()
                current_path.append(direction)
                return current_path
            
            # フィールド外、障害物、探索済みの座標はスキップ
            if next["x"] < 0 or next["x"] >= field_scale[0] or next["y"] < 0 or next["y"] >= field_scale[1]:
                continue
            if next in obstacles or next in searched:
                continue
            # 未探索の座標をキューに追加
            queue.append(next)
            # スタート地点からの最短距離を更新
            distance[str(next)] = distance[str(current)] + 1
            # スタート地点からの最短経路を更新
            path[str(next)] = path[str(current)].copy()
            path[str(next)].append(direction)
    return []

# 食べ物を避ける経路を返す。
def find_avoid_food_path(field_scale, body, obstacles):
#    for body_part in [body[-1], body[0]]:
    for body_part in [body[-1]]:
        path = find_shortest_path(field_scale, body, obstacles, body_part)
        if path is not None and len(path) > 0:
            return path
    biggest_room = directions_which_has_biggest_room(field_scale, body, obstacles)
    if biggest_room is not None and len(biggest_room) > 0:
        return [random.choice(biggest_room)]
    else:
        for direction in ["up", "down", "left", "right"]:
            next = body[0].copy()
            if direction == "up":
                next["y"] += 1
            elif direction == "down":
                next["y"] -= 1
            elif direction == "left":
                next["x"] -= 1
            elif direction == "right":
                next["x"] += 1
            if next["x"] < 0 or next["x"] >= field_scale[0] or next["y"] < 0 or next["y"] >= field_scale[1]:
                continue
            return [direction]
    return []

def directions_which_has_biggest_room(field_scale, body, obstacles):
    head = body[0]
    directions = []
    biggest_room = 0
    for direction in ["up", "down", "left", "right"]:
        next = head.copy()
        if direction == "up":
            next["y"] += 1
        elif direction == "down":
            next["y"] -= 1
        elif direction == "left":
            next["x"] -= 1
        elif direction == "right":
            next["x"] += 1
        if next["x"] < 0 or next["x"] >= field_scale[0] or next["y"] < 0 or next["y"] >= field_scale[1]:
            continue
        if next in obstacles:
            continue
        if next in body:
            continue

        room = 0
        queue = []
        searched = []
        queue.append(next)
        while len(queue) > 0:
            current = queue.pop(0)
            searched.append(current)
            room += 1
            for this_direction in ["up", "down", "left", "right"]:
                next = current.copy()
                if this_direction == "up":
                    next["y"] += 1
                elif this_direction == "down":
                    next["y"] -= 1
                elif this_direction == "left":
                    next["x"] -= 1
                elif this_direction == "right":
                    next["x"] += 1
                if next["x"] < 0 or next["x"] >= field_scale[0] or next["y"] < 0 or next["y"] >= field_scale[1]:
                    continue
                if next in obstacles:
                    continue
                if next in body:
                    continue
                if next in searched:
                    continue
                queue.append(next)
        if room > biggest_room:
            biggest_room = room
            directions = [direction]
        elif room == biggest_room:
            directions.append(direction)
    return directions

def choose_direction_try_to_avoid_obstacles(field_scale, body, obstacles):
    directions = ["up", "down", "left", "right"]
    valid_directions = []

    for direction in directions:
        next_position = body[0].copy()
        if direction == "up":
            next_position["y"] += 1
        elif direction == "down":
            next_position["y"] -= 1
        elif direction == "left":
            next_position["x"] -= 1
        elif direction == "right":
            next_position["x"] += 1

        if next_position["x"] < 0 or next_position["x"] >= field_scale[0] or next_position["y"] < 0 or next_position["y"] >= field_scale[1]:
            continue
        if next_position not in obstacles and next_position not in body:
            valid_directions.append(direction)

    if valid_directions:
        return random.choice(valid_directions)

    for direction in directions:
        next_position = body[0].copy()
        if direction == "up":
            next_position["y"] += 1
        elif direction == "down":
            next_position["y"] -= 1
        elif direction == "left":
            next_position["x"] -= 1
        elif direction == "right":
            next_position["x"] += 1

        if next_position["x"] < 0 or next_position["x"] >= field_scale[0] or next_position["y"] < 0 or next_position["y"] >= field_scale[1]:
            continue
        if next_position not in body:
            valid_directions.append(direction)

    if valid_directions:
        return random.choice(valid_directions)

    return random.choice(directions)
    

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end, "port": "8001"})