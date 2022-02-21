import arcade
from buttons import Box, ViewButton
from file_parser import FileParser
from question import Question, QuestionView
from team import Team
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, DEFAULT_BUTTON_HEIGHT, DEFAULT_BUTTON_WIDTH, MESSAGE_BOX_HEIGHT, TEAM_DISPLAY_HEIGHT

BOX_COLOR = arcade.color.GREEN
BOX_TEXT_COLOR = arcade.color.PURPLE

QUIT_BUTTON_WIDTH = 50
QUIT_BUTTON_HEIGHT = 35


class InvalidQuestionFile(Exception):
    def __init__(self, message) -> None:
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return f"INVALID QUESTION FILE: {self.message}"


class Board(arcade.View):
    def __init__(self, question_file_path, num_teams, main_menu_view):
        super().__init__()
        self.teams = [Team(f"Team {i+1}") for i in range(num_teams)]
        self.main_menu_view = main_menu_view
        self.categories = []
        self.question_boxes = []
        self.setup_boxes(question_file_path)
        self.window.show_view(main_menu_view)
        quit_button = ViewButton(main_menu_view, 'Quit', WINDOW_WIDTH - QUIT_BUTTON_WIDTH / 2 - BOX_PADDING,
                                 WINDOW_HEIGHT - QUIT_BUTTON_HEIGHT / 2 - BOX_PADDING, QUIT_BUTTON_WIDTH, QUIT_BUTTON_HEIGHT)
        self.buttons = [quit_button]

    def setup_boxes(self, question_file_path):
        file_parser = FileParser(question_file_path)
        if file_parser.get_line_indicator() == "NUM_CATEGORIES":
            num_categories = int(file_parser.parse_line())
        else:
            raise InvalidQuestionFile(
                "Missing NUM_CATEGORIES, indicating the number of categories for this board...")

        if file_parser.get_line_indicator() == "NUM_QUESTIONS_PER_CATEGORY":
            num_questions = int(file_parser.parse_line())
        else:
            raise InvalidQuestionFile(
                "Missing NUM_QUESTIONS_PER_CATEGORY, indicating the number of questions for each category...")

        BOX_WIDTH = (WINDOW_WIDTH - BOX_PADDING *
                     (num_categories + 1)) / num_categories
        BOX_HEIGHT = (WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - TEAM_DISPLAY_HEIGHT -
                      (BOX_PADDING * num_questions + 2)) / num_questions
        x = BOX_WIDTH / 2 + BOX_PADDING
        y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT
        points = 100

        for category_num in range(num_categories):
            if file_parser.get_line_indicator() == "C":
                category = file_parser.parse_line()
                self.categories.append(f'Category {category_num + 1}')

            for question_num in range(num_questions):
                question = Question(
                    f'Question {question_num + 1}', f'Answer for question {question_num + 1}', points)
                box = Box(question, str(points), x, y,
                          width=BOX_WIDTH, height=BOX_HEIGHT)
                self.question_boxes.append(box)
                y -= box.height + BOX_PADDING
                points += 100
            x += box.width + BOX_PADDING
            y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT
            points = 100

    def check_game_over(self):
        if (len(self.question_boxes) == 0):
            gameOverView = GameOver(self.teams, self.main_menu_view)
            self.window.show_view(gameOverView)

    def on_mouse_motion(self, x, y, dx, dy):
        all_buttons = self.buttons + self.question_boxes
        for button in all_buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        for button in self.buttons:
            if button.hovered:
                button.on_click()

        for box in self.question_boxes:
            if box.hovered:
                question = box.on_click()
                self.question_boxes.remove(box)
                self.ask_question(question)

    def ask_question(self, question):
        question_view = QuestionView(question, self)
        self.window.show_view(question_view)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"Please select a question...", WINDOW_WIDTH / 2, WINDOW_HEIGHT -
                         MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", font_size=20)
        all_buttons = self.buttons + self.question_boxes
        for button in all_buttons:
            button.draw()

        team_display_string = '     '.join(
            [f"{team.name}: {team.score:<5g}" for team in self.teams])
        arcade.draw_text(team_display_string, WINDOW_WIDTH / 2, TEAM_DISPLAY_HEIGHT /
                         2, font_size=15, anchor_x="center", anchor_y="center")


class GameOver(arcade.View):
    def __init__(self, teams, main_menu_view):
        super().__init__()
        self.team_strings = self.get_team_string(teams)
        main_menu_button = ViewButton(main_menu_view, 'Main Menu', BOX_PADDING + (DEFAULT_BUTTON_WIDTH/2),
                                      DEFAULT_BUTTON_HEIGHT + BOX_PADDING, DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT)
        self.buttons = [main_menu_button]

    def get_team_string(self, teams):
        teams.sort(key=lambda team: team.score, reverse=True)
        return [f'{team.name} : {team.score}' for team in teams]

    def on_draw(self):
        arcade.start_render()
        y = WINDOW_HEIGHT - 50
        for string in self.team_strings:
            arcade.draw_text(string, WINDOW_WIDTH / 2, y,
                             font_size=20, anchor_x="center", anchor_y="center")
            y -= 50

        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, dx, dy):
        for button in self.buttons:
            if button.hovered:
                button.on_click()
