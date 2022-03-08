from buttons import Box, FunctionButton
from constants import DEFAULT_BUTTON_HEIGHT, DEFAULT_BUTTON_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, MESSAGE_BOX_HEIGHT
import arcade

BUTTON_WIDTH = DEFAULT_BUTTON_WIDTH
BUTTON_HEIGHT = DEFAULT_BUTTON_HEIGHT
TEAM_CHOICE_HEIGHT = 50
TEAM_CHOICE_WIDTH = 200


class Question:
    def __init__(self, question_text, answer_text, points):
        self.question_text = question_text
        self.answer_text = answer_text
        self.points = points


class QuestionView(arcade.View):
    def __init__(self, question, board_view):
        super().__init__()
        self.board_view = board_view
        self.question = question

        self.question_text = arcade.Text(self.question.question, WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", align='center', font_size=15, width=WINDOW_WIDTH - 2 * BOX_PADDING, multiline=True)
        self.answer_text = arcade.Text('', WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2 - 75, anchor_x="center", anchor_y="center", align='center', font_size=15, width=WINDOW_WIDTH - 2 * BOX_PADDING, multiline=True)

        self.teams_boxes = []
        show_answer_button = FunctionButton(
            self.show_answer, 'Show Answer', WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.buttons = [show_answer_button]

    def setup_teams_boxes(self):
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT / 2 + TEAM_CHOICE_HEIGHT + BOX_PADDING
        teams_boxes = []
        for team in self.board_view.teams:
            teams_box = Box(team, team.name, x, y, width=TEAM_CHOICE_WIDTH,
                            height=TEAM_CHOICE_HEIGHT, font_size=10)
            teams_boxes.append(teams_box)
            y -= TEAM_CHOICE_HEIGHT + BOX_PADDING
        no_team_box = Box(None, 'No correct answer', x, y,
                          width=TEAM_CHOICE_WIDTH, height=TEAM_CHOICE_HEIGHT, font_size=10)
        teams_boxes.append(no_team_box)
        return teams_boxes

    def show_answer(self):
        self.answer_text.value = f'Answer: {self.question.answer}'
        self.teams_boxes = self.setup_teams_boxes()
        self.buttons = []

    def on_draw(self):
        arcade.start_render()

        self.question_text.draw()
        self.answer_text.draw()

        for box in self.teams_boxes:
            box.draw()

        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.teams_boxes:
            box.check_hovered(x, y)

        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        for box in self.teams_boxes:
            if box.hovered:
                team_correct = box.on_click()
                if team_correct is not None:
                    team_correct.score += self.question.pointValue
                self.board_view.update_team_display()
                self.window.show_view(self.board_view)
                self.board_view.check_game_over()

        for button in self.buttons:
            if button.hovered:
                button.on_click()
