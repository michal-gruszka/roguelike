import tiletools
import graphictools


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


def main():
    interface = graphictools.import_graphic_from_file('graphics/interface.gfx', 80, 23)
    map1 = graphictools.import_graphic_from_file('graphics/map1.gfx', 47, 21)
    display = graphictools.add_to_graphic(interface, map1, 1, 1)
    hero_x = 10
    hero_y = 10

    while True:
        hero = tiletools.Tile('player', '@', '38;2;255;255;255;', display[hero_x][hero_y].background, True)
        display = graphictools.add_single_tile_to_graphic(display, hero, hero_x, hero_y)
        graphictools.print_graphic(display)
        key_pressed = getch()

        direction = 'up'

        # make the move if there is no collision
        if key_pressed == "w" and display[hero_x][hero_y-1].walkable:
                display[hero_x][hero_y] = map1[hero_x - 1][hero_y - 1]
                hero_y -= 1
                direction = 'up'
        elif key_pressed == "a" and display[hero_x-1][hero_y].walkable:
                display[hero_x][hero_y] = map1[hero_x - 1][hero_y - 1]
                hero_x -= 1
                direction = 'left'

        elif key_pressed == "s" and display[hero_x][hero_y+1].walkable:
                display[hero_x][hero_y] = map1[hero_x - 1][hero_y - 1]
                hero_y += 1
                direction = 'down'

        elif key_pressed == "d" and display[hero_x+1][hero_y].walkable:
                display[hero_x][hero_y] = map1[hero_x - 1][hero_y - 1]
                hero_x += 1
                direction = 'right'

        elif key_pressed == "q":
            exit()

            
if __name__ == '__main__':
        main()