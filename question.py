from buttons import Box
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, MESSAGE_BOX_HEIGHT
import arcade

CHOICE_HEIGHT = 50
CHOICE_WIDTH = 200

class Question:
    def __init__(self, question_text, choices, correct_answer_index, points):
        self.question_text = question_text
        self.choices = choices
        self.correct_answer_index = correct_answer_index
        self.points = points
    
    def check_correct(self, answer_index):
        return self.correct_answer_index == answer_index

class QuestionView(arcade.View):
    def __init__(self, board_view, question, answering_team):
        super().__init__()
        self.board_view = board_view
        self.question = question
        self.answering_team = answering_team
        self.choice_boxes = []
        self.setup_choices()

    def setup_choices(self):
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - CHOICE_HEIGHT / 2 - BOX_PADDING 
        for i,choice in enumerate(self.question.choices):
            choice_box = Box(chr(65+i) + ". " + choice, x, y, i, width = CHOICE_WIDTH, height=CHOICE_HEIGHT, font_size=10)
            self.choice_boxes.append(choice_box)
            y -= CHOICE_HEIGHT + BOX_PADDING
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(self.question.question_text, WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", font_size=20)
        for box in self.choice_boxes:
            box.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.choice_boxes:
            box.check_hovered(x, y)
    
    def on_mouse_release(self, x, y, button, modifiers):
        for box in self.choice_boxes:
            if box.hovered:
                selection = box.on_click()
                if (self.question.check_correct(selection)):
                    self.answering_team.score += self.question.points
                self.window.show_view(self.board_view)
                self.board_view.switch_teams()
                self.board_view.check_game_over()