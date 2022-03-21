from buttons import Box, FunctionButton, ViewButton
from constants import DEFAULT_BUTTON_HEIGHT, DEFAULT_BUTTON_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, MESSAGE_BOX_HEIGHT
import arcade

#######################################
#              Constants              # 
#######################################
BACK_BUTTON_WIDTH = 50
BACK_BUTTON_HEIGHT = 35
BUTTON_WIDTH = DEFAULT_BUTTON_WIDTH
BUTTON_HEIGHT = DEFAULT_BUTTON_HEIGHT
TEAM_CHOICE_HEIGHT = 50
TEAM_CHOICE_WIDTH = 200


class Question:
    def __init__(self, question_text, answer_text, points):
        self.question_text = question_text
        self.answer_text = answer_text
        self.points = points

################################################################################################
#                                            Views                                             #
################################################################################################
class QuestionView(arcade.View):
    """ Representation of a view that asks a question and allows it to be answered. """
    def __init__(self, question_box, board_view):
        super().__init__()
        # Initialization
        self.question_box = question_box
        self.board_view = board_view
        self.question = self.question_box.on_click()

        # Create texts
        self.question_text = arcade.Text(self.question.question, WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", align='center', font_size=15, width=WINDOW_WIDTH - 2 * BOX_PADDING, multiline=True)
        self.answer_text = arcade.Text('', WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2 - 75, anchor_x="center", anchor_y="center", align='center', font_size=15, width=WINDOW_WIDTH - 2 * BOX_PADDING, multiline=True)
        
        # Initilaize answering team options buttons
        self.teams_boxes = []

        # Create buttons
        back_button = ViewButton(self.board_view, 'Back', BACK_BUTTON_WIDTH / 2 + BOX_PADDING, WINDOW_HEIGHT - BACK_BUTTON_HEIGHT / 2 - BOX_PADDING, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT, color=self.board_view.colors['foreground'], text_color=self.board_view.colors['text'])
        show_answer_button = FunctionButton(self.show_answer, 'Show Answer', WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT, color=self.board_view.colors['foreground'], text_color=self.board_view.colors['text'])
        self.buttons = [back_button, show_answer_button]

    def setup_teams_boxes(self):
        """ 
        Creates answering team options buttons. 
        
        Returns
            List of boxes each representing a team option.
        """
        # Determine coordinates
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT / 2 + TEAM_CHOICE_HEIGHT + BOX_PADDING

        # Create options buttons
        teams_boxes = []
        for team in self.board_view.teams:
            teams_box = Box(team, team.name, x, y, width=TEAM_CHOICE_WIDTH, height=TEAM_CHOICE_HEIGHT, font_size=10, color=self.board_view.colors['foreground'], text_color=self.board_view.colors['text'])
            teams_boxes.append(teams_box)
            y -= TEAM_CHOICE_HEIGHT + BOX_PADDING
        # Create additional option button indicating no correct answer
        no_team_box = Box(None, 'No correct answer', x, y, width=TEAM_CHOICE_WIDTH, height=TEAM_CHOICE_HEIGHT, font_size=10, color=self.board_view.colors['foreground'], text_color=self.board_view.colors['text'])
        teams_boxes.append(no_team_box)
        return teams_boxes

    def show_answer(self):
        """ Displays the answer, creates answering team options buttons, and removes display answer button. """
        # Display aswer
        self.answer_text.value = f'Answer: {self.question.answer}'
        # Create answering team options buttons. 
        self.teams_boxes = self.setup_teams_boxes()
        # Remove display answer button
        self.buttons = []

    def on_draw(self):
        # Clear window
        arcade.start_render()

        # Draw question
        self.question_text.draw()
        self.answer_text.draw()

        # Draw boxes
        for box in self.teams_boxes:
            box.draw()

        # Draw buttons
        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Determine if any boxes are being hovered
        for box in self.teams_boxes:
            box.check_hovered(x, y)

        # Determine if any buttons are being hovered
        for button in self.buttons:
            button.check_hovered(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        # Determine if any boxes are being clicked
        for box in self.teams_boxes:
            if box.hovered:
                team_correct = box.on_click()
                if team_correct is not None:
                    team_correct.score += self.question.pointValue
                self.window.show_view(self.board_view)
                self.board_view.question_answered(self.question_box)

        # Determine if any buttons are being clicked
        for button in self.buttons:
            if button.hovered:
                button.on_click()
