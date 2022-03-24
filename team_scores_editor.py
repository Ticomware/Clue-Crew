import arcade

from buttons import Button, ViewButton
from constants import BOX_PADDING

ADJUST_BUTTON_WIDTH = 20
ADJUST_BUTTON_HEIGHT = 20
ADJUST_BUTTON_FONT_SIZE = 12
ADJUST_BUTTON_Y_OFFSET = 150
ADJUST_BUTTON_WIDTH_OFFSET = 75
ADJUST_BUTTON_POINTS_INCREMENT = 50

DONE_BUTTON_WIDTH = 100
DONE_BUTTON_HEIGHT = 50

# TeamAdjustScoreButton - Button
# purpose - make buttons that add or subtract from team score
class TeamAdjustScoreButton(Button):
    def __init__(self, team, is_add_button, x, y, color, text_color):
        #is.add.button determines text and function
        self.is_add_button = is_add_button
        text = '+' if self.is_add_button else '-'
        super().__init__(text, x, y, ADJUST_BUTTON_WIDTH, ADJUST_BUTTON_HEIGHT, color, text_color, font_size=ADJUST_BUTTON_FONT_SIZE)
        self.team = team
    
    # on_click
    # purpose - adjust team score by 50 per click
    def on_click(self):
        if self.is_add_button:
            self.team.score += ADJUST_BUTTON_POINTS_INCREMENT
        else:
            self.team.score -= ADJUST_BUTTON_POINTS_INCREMENT

# EditTeamScoresView - arcade.View
# purpose - open team score editor 
class EditTeamScoresView(arcade.View):
    def __init__(self, board_view):
        super().__init__()
        self.board_view = board_view
        self.title_text = arcade.Text('Edit Team Scores', self.window.width // 2, self.window.height - 75, font_size=50, anchor_x="center")
        
        self.team_texts = []

        self.done_button = ViewButton(self.board_view, 'Done', self.window.width / 2, self.window.height / 2 - DONE_BUTTON_HEIGHT - 10, DONE_BUTTON_WIDTH, DONE_BUTTON_HEIGHT)
        self.buttons = [self.done_button]
        
        y = self.window.height - ADJUST_BUTTON_Y_OFFSET
        for team in self.board_view.teams:
            team_text = arcade.Text(f'{team.name}', self.window.width // 2, y, font_size=12, anchor_x="center", anchor_y='center')
            self.team_texts.append(team_text)
            subtract_button = TeamAdjustScoreButton(team, False, self.window.width / 2 - ADJUST_BUTTON_WIDTH_OFFSET, y, self.board_view.colors['foreground'], self.board_view.colors['text'])
            add_button = TeamAdjustScoreButton(team, True, self.window.width / 2 + ADJUST_BUTTON_WIDTH_OFFSET, y, self.board_view.colors['foreground'], self.board_view.colors['text'])
            self.buttons.append(add_button)
            self.buttons.append(subtract_button)
            y -= ADJUST_BUTTON_HEIGHT + BOX_PADDING

    def update(self, delta_time: float):
        for text, team in zip(self.team_texts, self.board_view.teams):
            text.value = f'{team.name} : {team.score}'

    def on_draw(self):
        arcade.start_render()

        self.title_text.draw()
        for text in self.team_texts:
            text.draw()

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