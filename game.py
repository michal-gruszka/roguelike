import tiletools
import graphictools
import maptools
import time
import random


def getch():
    """Function get the type of character pressed
        @:return: None
    """
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_hint(answer, random_number):
    if (answer == list(random_number)):
        return True
    elif (not set(answer) & set(random_number)):
        return ['None of the numbers', 'are correct']
    else:
        wrong_placed = 0
        correct_placed = 0
        for i in range(0, 3):
            if (answer[i] == random_number[i]):
                correct_placed += 1
            elif (random_number.__contains__(answer[i])):
                wrong_placed += 1
        if (wrong_placed > 0 and correct_placed == 0):
            return [str("There are " + str(wrong_placed) + " wrong placed.")]
        elif (wrong_placed == 0 and correct_placed > 0):
            return ["There are " + str(correct_placed) + " correct placed"]
        else:
            return [str("There are " + str(wrong_placed) + " wrong placed"), str("and " + str(correct_placed) + " correct placed")]


def generate_random_number():
    numbers = ['0', '1', '2', '3', '4','5', '6', '7', '8', '9']
    random.shuffle(numbers)
    return ''.join(numbers[0:3])

def save_to_scoreboard(player_name, time):
    with open("scoreboard.txt", 'a') as f:
        f.write(";".join([player_name, str(time)]) + '\n')

def prepare_inventory_list(inventory):
    line_list = []
    item_info_length = 0
    name_max_length = 0
    for item in inventory:
        if (len(item) > name_max_length):
            name_max_length = len(item)
        if (len(str(inventory.__getitem__(item))) > item_info_length):
            item_info_length = len(str(inventory.__getitem__(item)))
    line_list.append("Name         amount weight")
    item_info_length += 2;
    name_max_length -= 5
    format1 = str("{:<" + str(item_info_length) + "s}")
    format2 = str("{:<" + str(name_max_length) + "s}")
    for item in inventory:
        format3 = "{}"
        item_info = inventory.__getitem__(item)
        line = str(format1 + format2 + format3).format(item, str(item_info[0]), str(item_info[1]))
        line_list.append(line)
    return line_list

def load_scoreboard():
    with open('scoreboard.txt', 'r') as f:
        scoreboard_dict = {}
        lines = f.readlines()
        for line in lines:
            values = line.split(';')
            name = values[0]
            time = values[1].replace('\n','')
            scoreboard_dict.__setitem__(float(time), name)
        return scoreboard_dict

def print_scoreboard():
    scoreboard_dict = load_scoreboard()
    sorted_keys = sorted(scoreboard_dict.keys(), reverse= False)
    max_range = 10
    if(len(sorted_keys) < 10):
        max_range = len(sorted_keys)-1

    with open("graphics/scoreboard_screen.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            i = 0
            while(i != max_range):
                if (line.__contains__("%" + str(i+1))):
                    line = line.replace("%" + str(i+1) + "name", scoreboard_dict.__getitem__(sorted_keys[i]))
                    line = line.replace("%" + str(i+1) + "time", str(int(sorted_keys[i])))
                    line = line.replace("%" + str(i+1), str(i+1) + ". ")
                elif (line.__contains__("%")):
                    index = line.index('%')
                    next_char = line[index+1]
                    if(int(next_char) > max_range):
                        line = "\n"
                i += 1
            if(not line.__contains__("0time")):
                print(line, end='')
    getch()



def add_to_inventory(item,amount,weight):
    if tiletools.Hero.inventory.__contains__("item"):
        item_info = tiletools.Hero.inventory[item]
        item_amount = item_info[1] + float(amount)
        item_weight = item_info[2] + float(weight)
        tiletools.Hero.inventory[item] = [item_amount , item_weight]
    else:
        tiletools.Hero.inventory.__setitem__(item, [float(amount), float(weight)])
    

def map_3_handler():
    interface = graphictools.import_graphic_from_file('graphics/interface.gfx', 80, 23)
    current_map = maptools.Map('map3', 'graphics/map3.gfx')
    display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)
    game_loop_3(interface, current_map, display)

def map_2_handler():
    interface = graphictools.import_graphic_from_file('graphics/interface.gfx', 80, 23)
    current_map = maptools.Map('map2', 'graphics/map1.gfx')
    hero = tiletools.Hero(100, 10, 10, 'up')
    display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)
    game_loop_2(interface, current_map, display, hero)

def map_1_handler():
    interface = graphictools.import_graphic_from_file('graphics/interface.gfx', 80, 23)
    hero = tiletools.Hero(100, 10, 10, 'up')
    """  map initialization """
    map1 = maptools.Map('map1', 'graphics/map2.gfx', hero)
    gold1 = tiletools.Gold(4, 4, 10, hero)
    gold2 = tiletools.Gold(3, 3, 10, hero)
    gold3 = tiletools.Gold(5, 3, 10, hero)
    gold4 = tiletools.Gold(6, 3, 10, hero)
    gold5 = tiletools.Gold(7, 3, 10, hero)
    gold6 = tiletools.Gold(8, 3, 20, hero)
    gold7 = tiletools.Gold(9, 3, 10, hero)
    gold8 = tiletools.Gold(11, 3, 20, hero)
    gold_coins = [gold1, gold2, gold3, gold4, gold5, gold6, gold7, gold8]
    current_map = map1
    """ ------------------- """
    display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)


    game_loop_1(interface, current_map, display, hero, gold_coins)


def game_loop_1(interface, current_map, display, hero, gold_coins):

    while True:
        display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)
        display = graphictools.add_single_tile_to_graphic(display, hero, hero.x, hero.y)

        if hero.gold <= 100:
            message = ['Collect 100 gold to proceed.', 'Your gold: ' + str(hero.gold)]
            graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(message))

        for coin in gold_coins:
            if current_map.name == "map1" and coin.exist:
                display[coin.x][coin.y] = coin
        
        rabbit1 = tiletools.Rabbit()

        if rabbit1.alive:
            display[30][17] = rabbit1
            print(rabbit1.alive)

        graphictools.print_graphic(display)

        key_pressed = getch()

        handle_user_input(display, current_map, key_pressed, hero)
        
        for coin in gold_coins:
            coin.collision_check()



        if hero.y == 1 and current_map.name == "map1":
            current_map = maptools.Maps.map2
            hero.y = 21


def game_loop_2(interface, current_map, display, hero):
    info_box_message = ['Prepare yourself for','the final fight.', 'Gather all items marked', 'as "?" on the map.']
    while True:
        hero_string_pos = str(hero.x) + ',' + str(hero.y)
        if (maptools.Maps.items.__contains__(hero_string_pos)):
            item = maptools.Maps.items[hero_string_pos].split(',')
            add_to_inventory(item[0], item[1], item[2])
            graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(
                [[tiletools.Tiles.black.string] * 28] * 9))
            info_box_message = ['You gained:', str('name: ' + item[0]), str('amount: ' + item[1])]
            current_map.map_graphic[hero.x - 1][hero.y -1 ] = tiletools.Tiles.grass
            maptools.Maps.items.__delitem__(hero_string_pos)
            if(not maptools.Maps.items):
                graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(
                    [[tiletools.Tiles.black.string] * 28] * 9))
                info_box_message = ['You are ready for the battle',
                                    'get to the boss cave',
                                    'using black entrance',
                                    'at the bottom of the map']
            print(tiletools.Hero.inventory)

        display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)
        graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(info_box_message))
        display = graphictools.add_single_tile_to_graphic(display, hero, hero.x, hero.y)
        graphictools.print_graphic(display)

        key_pressed = getch()
        if (key_pressed == 'i' or key_pressed == 'i'):
            info_box_message = prepare_inventory_list(hero.inventory)

        handle_user_input(display, current_map, key_pressed, hero)
        if(not maptools.Maps.items and hero_string_pos in ['13,18', '14,18', '15,18']):
            map_3_handler()
            break

def game_loop_3(interface, current_map, display):
    info_box_message = ['You have to kill the boss by', 'winning hot worm cold fight.',
                        'Type 3-number digit', 'without duplications.', ' ']
    answer_dict = {'Numbers' : []}
    random_number = generate_random_number()
    while True:
        print(random_number.__str__())
        display = graphictools.add_to_graphic(interface, current_map.map_graphic, 1, 1)
        graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(
            [[tiletools.Tiles.black.string] * 28] * 9))
        graphictools.add_dialogue_to_display(interface, graphictools.get_dialogue_graphic(info_box_message))
        graphictools.print_graphic(display)
        key_pressed = getch()
        if(key_pressed in ['0','1','2','3','4','5','6','7', '8','9']):
            answers = answer_dict.__getitem__("Numbers")
            if (len(answers) == 3):
                hint = get_hint(answers, random_number)
                if(hint == True):
                    time2 = time.time()
                    timeDifference = time2 - maptools.Maps.start_time
                    print("You win it took: ", timeDifference)
                    save_to_scoreboard(tiletools.Hero.player_name, timeDifference)
                    print_scoreboard()
                    exit()
                else:
                    info_box_message = hint
                    answer_dict.__setitem__("Numbers", [])
            elif(not answers.__contains__(key_pressed)):
                answers.append(key_pressed)
                answer_dict.__setitem__("Numbers", answers)
                info_box_message = [str('Your number: ' + str("".join(answers)))]
            else:
                info_box_message = ["Your number cannot",'have any duplications',str('Your number: ' + str("".join(answers)))]
        elif key_pressed == 'q':
            exit()



def handle_user_input(display, current_map, key_pressed, hero):
    """ Make the move if there is no collision. """
    if key_pressed == "w" and display[hero.x][hero.y - 1].walkable:
            display[hero.x][hero.y] = current_map.map_graphic[hero.x - 1][hero.y - 1]
            hero.background = display[hero.x][hero.y - 1].background
            hero.update_string()
            hero.y -= 1
            hero.direction = 'up'
    elif key_pressed == "a" and display[hero.x - 1][hero.y].walkable:
            display[hero.x][hero.y] = current_map.map_graphic[hero.x - 1][hero.y - 1]
            hero.background = display[hero.x - 1][hero.y].background
            hero.update_string()
            hero.x -= 1
            hero.direction = 'left'

    elif key_pressed == "s" and display[hero.x][hero.y + 1].walkable:
            display[hero.x][hero.y] = current_map.map_graphic[hero.x - 1][hero.y - 1]
            hero.background = display[hero.x][hero.y + 1].background
            hero.update_string()
            hero.y += 1
            hero.direction = 'down'

    elif key_pressed == "d" and display[hero.x + 1][hero.y].walkable:
            display[hero.x][hero.y] = current_map.map_graphic[hero.x - 1][hero.y - 1]
            hero.background = display[hero.x + 1][hero.y].background
            hero.update_string()
            hero.x += 1
            hero.direction = 'right'

    elif key_pressed == 'k':
        animate_attack(display, hero)

    elif key_pressed == "q":
        exit()


def animate_attack(display, hero):
    if hero.direction == 'up':
        tile_copy = display[hero.x - 1][hero.y - 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '\\' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x-1, hero.y-1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x-1, hero.y-1)
        time.sleep(0.1)
        if tile_copy.name == 'rabbit':
            graphictools.add_single_tile_to_graphic(display, tiletools.Tiles.blood, hero.x-1, hero.y-1)
            tile_copy.alive = False

        tile_copy = display[hero.x][hero.y - 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '|' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x, hero.y-1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x, hero.y-1)
        time.sleep(0.1)

        tile_copy = display[hero.x + 1][hero.y - 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '/' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x+1, hero.y-1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x+1, hero.y-1)
        time.sleep(0.1)

    if hero.direction == 'left':
        tile_copy = display[hero.x - 1][hero.y + 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '/' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x-1, hero.y+1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x-1, hero.y+1)
        time.sleep(0.1)

        tile_copy = display[hero.x - 1][hero.y]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '-' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x-1, hero.y)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x-1, hero.y)
        time.sleep(0.1)

        tile_copy = display[hero.x - 1][hero.y - 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '\\' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x-1, hero.y-1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x-1, hero.y-1)
        time.sleep(0.1)

    if hero.direction == 'down':
        tile_copy = display[hero.x + 1][hero.y + 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '\\' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x+1, hero.y+1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x+1, hero.y+1)
        time.sleep(0.1)

        tile_copy = display[hero.x][hero.y + 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '|' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x, hero.y+1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x, hero.y+1)
        time.sleep(0.1)

        tile_copy = display[hero.x - 1][hero.y + 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '/' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x-1, hero.y+1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x-1, hero.y+1)
        time.sleep(0.1)

    if hero.direction == 'right':
        tile_copy = display[hero.x + 1][hero.y - 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '/' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x+1, hero.y-1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x+1, hero.y-1)
        time.sleep(0.1)

        tile_copy = display[hero.x + 1][hero.y]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '-' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x+1, hero.y)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x+1, hero.y)
        time.sleep(0.1)

        tile_copy = display[hero.x + 1][hero.y + 1]
        string = '\x1b[' + '38;2;255;255;255;' + tile_copy.background + '\\' + '\x1b[0m'
        graphictools.add_single_tile_to_graphic(display, string, hero.x+1, hero.y+1)
        graphictools.print_graphic(display)
        graphictools.add_single_tile_to_graphic(display, tile_copy, hero.x+1, hero.y+1)
        time.sleep(0.1)


def trigger_menu():
    option = 1
    lines_list = []
    with open('graphics/menu.txt', 'r') as f:
        lines_list = f.readlines()
    while True:
        for line in list(lines_list):
            if line.__contains__('%'):
                index = line.index('%')
                if(int(line[index+1]) == option):
                    line = line.replace('%' + str(option), " [6;30;42m")
                else:
                    line = line.replace('%' + line[index+1], ' ')
            print(line, end='')
        input = getch()
        output = handle_main_menu_user_input(input, option)
        if output in [1,2,3,4,5]:
            option = output


def handle_main_menu_user_input(input, option):
    if (input == "A"):
        if (option == 1):
            return 5
        else:
            option -= 1
            return option
    elif (input == "B"):
        if (option == 5):
            return 1
        else:
            option += 1
            return  option
    elif (input == "q"):
        exit()
    elif (input == "C" and option in [1, 5]):
        selected_item_handler(option)
    return None


def selected_item_handler(option):
    """
    Function triggers stage which depends on option variable.
    :param option: 
    :return: None
    """
    if (option == 1):
        maptools.Maps.start_time = time.time()
        map_3_handler()
    if (option == 5):
        exit()
        

if __name__ == '__main__':
        trigger_menu()

