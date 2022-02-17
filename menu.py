import arcade
from pip import main
from board import BOX_HEIGHT, Board
from buttons import Button
from constants import BOX_PADDING, MAIN_TITLE, MAIN_TITLE_COLOR, BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 75
BUTTON_COLOR = arcade.color.GREEN
BUTTON_TEXT_COLOR = arcade.color.PURPLE
BUTTON_FONT_SIZE = 10

class PlayGameButton(Button):
    def __init__(self, x, y, main_menu_view, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, font_size=BUTTON_FONT_SIZE):
        super().__init__("Play Game", x, y, width=width, height=height, color=color, text_color=text_color, font_size=font_size)
        self.main_menu_view = main_menu_view

    def on_click(self):
        board_view = Board(self.main_menu_view)
        arcade.get_window().show_view(board_view)

class ExitButton(Button):
    def __init__(self, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, font_size=BUTTON_FONT_SIZE):
        super().__init__("Exit", x, y, width=width, height=height, color=color, text_color=text_color, font_size=font_size)
    
    def on_click(self):
        arcade.close_window()

class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)

        self.buttons = [PlayGameButton(WINDOW_WIDTH / 2, (WINDOW_HEIGHT + BOX_PADDING + BUTTON_HEIGHT)/2, self), ExitButton(WINDOW_WIDTH / 2, (WINDOW_HEIGHT - BOX_PADDING - BUTTON_HEIGHT) / 2)]
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(MAIN_TITLE, self.window.width // 2, self.window.height - 75, color=MAIN_TITLE_COLOR, font_size=50, anchor_x="center")

        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.buttons:
            button.check_hovered(x, y)
    
    def on_mouse_release(self, x, y, dx, dy):
        for button in self.buttons:
            if button.hovered:
                button.on_click()