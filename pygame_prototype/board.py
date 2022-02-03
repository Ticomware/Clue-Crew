import arcade
from buttons import Button, Box
from question import Question, QuestionView
from team import Team
from constants import NUM_CATEGORIES, NUM_QUESTIONS_PER_CATEGORY, WINDOW_HEIGHT, WINDOW_WIDTH, BOX_PADDING, MESSAGE_BOX_HEIGHT, TEAM_DISPLAY_HEIGHT

BOX_WIDTH = (WINDOW_WIDTH - BOX_PADDING * (NUM_CATEGORIES + 1)) / NUM_CATEGORIES
BOX_HEIGHT = (WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT - TEAM_DISPLAY_HEIGHT - (BOX_PADDING * NUM_QUESTIONS_PER_CATEGORY + 2)) / NUM_QUESTIONS_PER_CATEGORY
BOX_COLOR = arcade.color.GREEN
BOX_TEXT_COLOR = arcade.color.PURPLE

QUIT_BUTTON_WIDTH = 50
QUIT_BUTTON_HEIGHT = 35

class QuitButton(Button):
    def __init__(self, main_menu_view, x, y):
        super().__init__("Quit", x, y, width=QUIT_BUTTON_WIDTH, height=QUIT_BUTTON_HEIGHT)
        self.main_menu_view = main_menu_view
    
    def on_click(self):
        self.main_menu_view.window.show_view(self.main_menu_view)

class Board(arcade.View):
    def __init__(self, main_menu_view):
        super().__init__()
        self.team_1 = Team("Team 1")
        self.team_2 = Team("Team 2")
        self.answering_team = self.team_1
        self.main_menu_view = main_menu_view
        self.categories = []
        self.question_boxes = []
        self.setup_boxes()
        self.buttons = [QuitButton(self.main_menu_view, WINDOW_WIDTH - QUIT_BUTTON_WIDTH / 2 - BOX_PADDING, WINDOW_HEIGHT - QUIT_BUTTON_HEIGHT / 2 - BOX_PADDING)]

    
    def setup_boxes(self):
        x = BOX_WIDTH / 2 + BOX_PADDING
        y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT
        points = 100
        for category_num in range(NUM_CATEGORIES):
            self.categories.append(f"Category {category_num + 1}")
            for question_num in range (NUM_QUESTIONS_PER_CATEGORY):
                question= Question(f"{self.categories[category_num]} - Quesiton {question_num + 1}", ["One", "Two", "Three", "Four", "Five"], question_num, points)
                box = Box(str(points), x, y, question, width=BOX_WIDTH, height=BOX_HEIGHT)
                self.question_boxes.append(box)
                y -= box.height + BOX_PADDING
                points += 100
            x += box.width + BOX_PADDING
            y = WINDOW_HEIGHT - BOX_HEIGHT // 2 - MESSAGE_BOX_HEIGHT
            points = 100

    def switch_teams(self):
        if self.answering_team == self.team_1:
            self.answering_team = self.team_2
        else:
            self.answering_team = self.team_1

    
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
        question_view = QuestionView(self, question, self.answering_team)
        self.window.show_view(question_view)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"{self.answering_team.name} please select a question...", WINDOW_WIDTH / 2, WINDOW_HEIGHT - MESSAGE_BOX_HEIGHT / 2, anchor_x="center", anchor_y="center", font_size=20)
        all_buttons = self.buttons + self.question_boxes 
        for button in all_buttons:
            button.draw()

        arcade.draw_text(f"{self.team_1.name}: {self.team_1.score}", BOX_PADDING, TEAM_DISPLAY_HEIGHT / 2, font_size=20, anchor_y="center")
        arcade.draw_text(f"{self.team_2.name}: {self.team_2.score}", WINDOW_WIDTH - BOX_PADDING, TEAM_DISPLAY_HEIGHT / 2, font_size=20, anchor_x = "right", anchor_y="center")