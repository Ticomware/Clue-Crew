import arcade
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger
from tkinter import messagebox

from board import Board
from buttons import Button
from constants import BOX_PADDING, MAIN_TITLE, MAIN_TITLE_COLOR, BACKGROUND_COLOR, MAX_NUM_TEAMS, MIN_NUM_TEAMS, WINDOW_HEIGHT, WINDOW_WIDTH
from board import InvalidQuestionFile


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
        try:
            question_file_path = askopenfilename(title="Select Question File", filetypes=[("Question Files","*.txt")])
            if (question_file_path != ""):
                num_teams = askinteger(title='Number of Teams', prompt=f'Please enter the number of teams ({MIN_NUM_TEAMS}-{MAX_NUM_TEAMS})', initialvalue=2, minvalue=MIN_NUM_TEAMS, maxvalue=MAX_NUM_TEAMS)
                if(num_teams != None):
                    board_view = Board(question_file_path, num_teams, self.main_menu_view)
                    board_view.window.show_view(board_view)
        except InvalidQuestionFile as e:
            messagebox.showerror(title="Invalid Question File", message=e.message)

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
