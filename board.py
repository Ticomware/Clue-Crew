import arcade
from buttons import Box, FunctionButton, ViewButton
from file_parser import FileParser
from question import Question, QuestionView
from team import Team
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, DEFAULT_BUTTON_HEIGHT, DEFAULT_BUTTON_WIDTH, MESSAGE_BOX_HEIGHT, TEAM_DISPLAY_HEIGHT
from tkinter.messagebox import askyesnocancel
from tkinter.filedialog import asksaveasfile
from database import database
import pickle

DEFAULT_BACKGROUND_COLOR = arcade.color.BLACK
DEFAULT_FOREGROUND_COLOR = arcade.color.GREEN
DEFAULT_TEXT_COLOR = arcade.color.PURPLE

QUIT_BUTTON_WIDTH = 50
QUIT_BUTTON_HEIGHT = 35

TEAM_DISPLAY_FONT_COLOR = arcade.color.ANTIQUE_WHITE
TEAM_DISPLAY_FONT_SIZE = 15
CATEGORY_FONT_SIZE_SCALE = 12

class InvalidQuestionFile(Exception):
    def __init__(self, message) -> None:
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return f"INVALID QUESTION FILE: {self.message}"

class Board(arcade.View):
    @classmethod
    def load_from_saved_board_file(self, saved_board_file, main_menu_view):
        saved_board_dictionary = pickle.load(saved_board_file)
        saved_board = Board(main_menu_view=main_menu_view)
        saved_board.question_boxes = saved_board_dictionary['question_boxes']
        saved_board.colors = saved_board_dictionary['colors']
        
        BOX_WIDTH = saved_board.question_boxes[0].width
        saved_board.category_labels = [arcade.Text(**category, color=saved_board.colors['text'], anchor_x='center', anchor_y='center', align='center', width=BOX_WIDTH, multiline= True) for category in saved_board_dictionary['categories']]
        saved_board.teams = saved_board_dictionary['teams']
        saved_board.team_display.color = saved_board.colors['text']
        for button in saved_board.buttons:
            button.color = saved_board.colors['foreground']
            button.text_color = saved_board.colors['text']
        arcade.set_background_color(saved_board.colors['background'])
        return saved_board

    def __init__(self, question_file_path=None, num_teams=None, main_menu_view=None):
        super().__init__()
        self.teams = []
        self.main_menu_view = None
        self.category_labels = []
        self.question_boxes = []
        self.colors = {'background': DEFAULT_BACKGROUND_COLOR, 'foreground': DEFAULT_FOREGROUND_COLOR, 'text': DEFAULT_TEXT_COLOR}
        
        if num_teams:
            self.teams = [Team(f"Team {i+1}") for i in range(num_teams)]        
        if main_menu_view:
            self.main_menu_view = main_menu_view
        if question_file_path:
            board_data = database(question_file_path)
            self.setup_colors(board_data)
            self.setup_boxes(board_data)

        self.team_display = arcade.Text('', WINDOW_WIDTH / 2, TEAM_DISPLAY_HEIGHT / 2, color=self.colors['text'], font_size=TEAM_DISPLAY_FONT_SIZE, anchor_x="center", anchor_y="center")
        self.message_display = arcade.Text(f"Please select a question...", WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", font_size=20)
        arcade.set_background_color(self.colors['background'])

        quit_button = FunctionButton(self.quit, 'Quit', WINDOW_WIDTH - QUIT_BUTTON_WIDTH / 2 - BOX_PADDING, WINDOW_HEIGHT - QUIT_BUTTON_HEIGHT / 2 - BOX_PADDING, QUIT_BUTTON_WIDTH, QUIT_BUTTON_HEIGHT, color=self.colors['foreground'], text_color=self.colors['text'])
        self.buttons = [quit_button]

    def setup_colors(self, board_data):
        self.colors['background'] = self.hex_to_rgb(board_data.getBackgroundColor())
        self.colors['foreground'] = self.hex_to_rgb(board_data.getForegroundColor())
        self.colors['text'] = self.hex_to_rgb(board_data.getPointColor())
    
    def hex_to_rgb(self, hex_string):
        nums = hex_string.strip('#')
        return [int(nums[i:i+2], 16) for i in range(0, len(nums), 2)]

    def setup_boxes(self, board_data):
        categories = board_data.getBoard()
        num_categories = len(categories)
        num_questions = len(max(categories, key=lambda category: len(category.questions)).questions)


        BOX_WIDTH = (WINDOW_WIDTH - BOX_PADDING *
                     (num_categories + 1)) / num_categories
        BOX_HEIGHT = (WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - TEAM_DISPLAY_HEIGHT -
                      (BOX_PADDING * num_questions + 2)) / (num_questions + 0.5)
        CATEGORY_HEIGHT = BOX_HEIGHT / 2
        x = BOX_WIDTH / 2 + BOX_PADDING
        y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT - CATEGORY_HEIGHT - BOX_PADDING
        category_y = WINDOW_HEIGHT - BOX_PADDING - MESSAGE_BOX_HEIGHT
        CATEGORY_FONT_SIZE = BOX_WIDTH // CATEGORY_FONT_SIZE_SCALE

        for category in categories:
            self.category_labels.append(arcade.Text(category.title, x, category_y, color=self.colors['text'], font_size=CATEGORY_FONT_SIZE, anchor_x='center', anchor_y='center', align='center', width=BOX_WIDTH, multiline= True))

            for question in category.questions:
                question.pointValue = int(question.pointValue)
                box = Box(question, str(question.pointValue), x, y,
                          width=BOX_WIDTH, height=BOX_HEIGHT, color=self.colors['foreground'], text_color=self.colors['text'])
                self.question_boxes.append(box)
                y -= box.height + BOX_PADDING
            x += box.width + BOX_PADDING
            y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT - CATEGORY_HEIGHT - BOX_PADDING

    def update_team_display(self):
        self.team_display.value = '     '.join([f"{team.name}: {team.score:<5g}" for team in self.teams])

    def check_game_over(self):
        if (len(self.question_boxes) == 0):
            gameOverView = GameOver(self.teams, self.main_menu_view)
            self.window.show_view(gameOverView)

    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.question_boxes:
            box.check_hovered(x, y)

        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        button_clicked = False
        for button in self.buttons:
            if button.hovered and not button_clicked:
                button.on_click()
                button_clicked = True

        for box in self.question_boxes:
            if box.hovered and not button_clicked:
                button_clicked = True
                self.ask_question(box)

    def ask_question(self, box):
        question_view = QuestionView(box, self)
        self.window.show_view(question_view)
    
    def question_answered(self, question_box):
        self.update_team_display()
        self.question_boxes.remove(question_box)
        self.check_game_over()

    def on_draw(self):
        arcade.start_render()
        
        self.message_display.draw()

        for category in self.category_labels:
            category.draw()

        all_buttons = self.buttons + self.question_boxes
        for button in all_buttons:
            button.draw()

        self.team_display.draw()
    
    def on_show_view(self):
        self.update_team_display()

    def quit(self):
        should_save_before_quit = askyesnocancel(title='Save Before Quit?', message='Would you like to save the board before quitting?')
        if should_save_before_quit is not None:
            if should_save_before_quit:
                filetypes = [('Jeopardy Board', '*.jpd')]
                file = asksaveasfile(mode='wb', filetypes=filetypes, defaultextension=filetypes, initialdir='./Saved Boards/')
                if file is not None:
                    board_dictionary = {
                        'teams': self.teams,
                        'categories': [{'text':category_label.value, 'start_x': category_label.x, 'start_y': category_label.y, 'font_size':category_label.font_size} for category_label in self.category_labels],
                        'question_boxes': self.question_boxes,
                        'colors': self.colors
                    }
                    pickle.dump(board_dictionary, file)
                    self.window.show_view(self.main_menu_view)
            else:
                self.window.show_view(self.main_menu_view)
                


class GameOver(arcade.View):
    def __init__(self, teams, main_menu_view):
        super().__init__()
        self.title = arcade.Text('Results', self.window.width / 2, self.window.height - 75, color=DEFAULT_TEXT_COLOR, font_size=50, anchor_x="center", anchor_y="center")
        self.team_texts = self.create_team_texts(teams)

        main_menu_button = ViewButton(main_menu_view, 'Main Menu', self.window.width / 2, DEFAULT_BUTTON_HEIGHT + BOX_PADDING, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT)
        self.buttons = [main_menu_button]

    def create_team_texts(self, teams):
        teams.sort(key=lambda team: team.score, reverse=True)

        team_texts = []
        y = WINDOW_HEIGHT - 150
        for string in [f'{team.name} : {team.score}' for team in teams]:
            team_text = arcade.Text(string, self.window.width / 2, y, font_size=20, anchor_x="center", anchor_y="center", color=DEFAULT_TEXT_COLOR)
            team_texts.append(team_text)
            y -= 50
        return team_texts

    def on_draw(self):
        arcade.start_render()

        self.title.draw()

        for text in self.team_texts:
            text.draw()

        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, dx, dy):
        for button in self.buttons:
            if button.hovered:
                button.on_click()
