import arcade
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import Tk

from board import Board
from buttons import Box, ExitButton, FunctionButton, ViewButton
from constants import BOX_PADDING, DEFAULT_BUTTON_HEIGHT, DEFAULT_BUTTON_WIDTH, MAIN_TITLE, MAIN_TITLE_COLOR, DEFAULT_BACKGROUND_COLOR, DEFAULT_FOREGROUND_COLOR, DEFAULT_TEXT_COLOR, MAX_NUM_TEAMS, MIN_NUM_TEAMS, WINDOW_HEIGHT, WINDOW_WIDTH, MESSAGE_BOX_HEIGHT
from board import InvalidQuestionFile
from question import BUTTON_HEIGHT

#board editor
import questionMaker as questMaker

BUTTON_WIDTH = DEFAULT_BUTTON_WIDTH
BUTTON_HEIGHT = DEFAULT_BUTTON_HEIGHT
BUTTON_COLOR = arcade.color.GREEN
BUTTON_TEXT_COLOR = arcade.color.PURPLE
BUTTON_FONT_SIZE = 10

TEAM_CHOICE_HEIGHT = 75
TEAM_CHOICE_WIDTH = 225


class SelectTeamsView(arcade.View):
    def __init__(self, question_file_path, main_menu_view):
        super().__init__()
        self.question_file_path = question_file_path
        self.main_menu_view = main_menu_view
        self.teams_boxes = self.setup_boxes()
        cancel_button = ViewButton(main_menu_view, 'Cancel', WINDOW_WIDTH/2, (WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - TEAM_CHOICE_HEIGHT /
                                   2 - BOX_PADDING) - (TEAM_CHOICE_HEIGHT + BOX_PADDING)*(MAX_NUM_TEAMS - MIN_NUM_TEAMS + 1), TEAM_CHOICE_WIDTH, TEAM_CHOICE_HEIGHT)
        self.buttons = [cancel_button]

    def setup_boxes(self):
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - TEAM_CHOICE_HEIGHT / 2 - BOX_PADDING
        teams_boxes = []
        for i in range(MIN_NUM_TEAMS, MAX_NUM_TEAMS + 1):
            teams_box = Box(i, f'{i} Teams', x, y, width=TEAM_CHOICE_WIDTH,
                            height=TEAM_CHOICE_HEIGHT, font_size=10)
            teams_boxes.append(teams_box)
            y -= TEAM_CHOICE_HEIGHT + BOX_PADDING
        return teams_boxes

    def on_draw(self):
        arcade.start_render()
        for box in self.teams_boxes:
            box.draw()

        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for box in self.teams_boxes:
            if box.hovered:
                num_teams = box.on_click()
                board_view = Board(self.question_file_path,
                                   num_teams, self.main_menu_view)
                board_view.window.show_view(board_view)

        for button in self.buttons:
            if button.hovered:
                button.on_click()

    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.teams_boxes:
            box.check_hovered(x, y)

        for button in self.buttons:
            button.check_hovered(x, y)


class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        play_game_button = FunctionButton(self.begin_game, "New Game", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + BUTTON_HEIGHT + BOX_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT)
        load_game_button = FunctionButton(self.load_game, "Load Game", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        board_editor_button = FunctionButton(self.board_editor,"Open Board Editor", WINDOW_WIDTH/2, 50, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        exit_button = ExitButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - BOX_PADDING - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.buttons = [play_game_button,load_game_button, board_editor_button, exit_button]

    def on_show_view(self):
        arcade.set_background_color(DEFAULT_BACKGROUND_COLOR)


    #creation of textEditor object and make it run with mainloop()
    def board_editor(self):
        boardMaker = questMaker.TextEditor()
        boardMaker.mainloop()

    def load_game(self):
        filetypes = [('Jeopardy Board', '*.jpd')]
        file_name = askopenfilename(filetypes=filetypes, defaultextension=filetypes, initialdir='./Saved Boards')
        if file_name:
            file = open(file_name, 'rb')
            board_view = Board.load_from_saved_board_file(file, self)
            self.window.show_view(board_view)

    def begin_game(self):
        try:
            Tk().withdraw()
            question_file_path = askopenfilename(title="Select Question File", filetypes=[
                                                 ("Board Files", "*.xml")], initialdir='./Created Boards')
            if (question_file_path != ""):
                select_teams_view = SelectTeamsView(question_file_path, self)
                arcade.get_window().show_view(select_teams_view)

        except InvalidQuestionFile as e:
            messagebox.showerror(
                title="Invalid Question File", message=e.message)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(MAIN_TITLE, self.window.width // 2, self.window.height -
                         75, color=MAIN_TITLE_COLOR, font_size=50, anchor_x="center")

        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, dx, dy):
        button_clicked = False
        for button in self.buttons:
            if button.hovered and not button_clicked:
                button.on_click()
                button_clicked = True

    def on_hide_view(self):
        for button in self.buttons:
            button.hovered = False