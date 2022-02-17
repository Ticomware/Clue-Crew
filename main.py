import arcade
from menu import Menu
from constants import MAIN_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, MAIN_TITLE)
    menuView = Menu()
    window.show_view(menuView)
    arcade.run()

if __name__ == '__main__':
    main()