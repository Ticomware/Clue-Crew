import arcade

from buttons import FunctionButton, ViewButton

EXAMPLE_BUTTON_WIDTH = 150
EXAMPLE_BUTTON_HEIGHT = 50

class EditTeamScoresView(arcade.View):
    def __init__(self, board_view):
        super().__init__()
        self.board_view = board_view
        self.teams = self.board_view.teams
        self.title_text = arcade.Text('Team Scores Editor', self.window.width // 2, self.window.height - 75, font_size=50, anchor_x="center")
        self.example_text = arcade.Text('Example message text', self.window.width // 2, self.window.height / 2 + 75, font_size=12, anchor_x="center")

        self.num_clicks = 0

        self.example_button = FunctionButton(self.example_function, 'Example Button', self.window.width / 2, self.window.height / 2, EXAMPLE_BUTTON_WIDTH, EXAMPLE_BUTTON_HEIGHT)
        self.done_button = ViewButton(self.board_view, 'Done', self.window.width / 2, self.window.height / 2 - EXAMPLE_BUTTON_HEIGHT - 10, EXAMPLE_BUTTON_WIDTH, EXAMPLE_BUTTON_HEIGHT)

        self.buttons = [self.example_button, self.done_button]
    
    def example_function(self):
        self.num_clicks += 1
        self.example_text.value = f'Button clicked {self.num_clicks} times'

    def on_draw(self):
        arcade.start_render()

        self.title_text.draw()
        self.example_text.draw()

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


if __name__ == '__main__':
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    from board import Board
    from menu import Menu

    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, 'Team Scores Editor')
    saved_board_file = open('Saved Boards/test.jpd', 'rb')
    board_view = Board.load_from_saved_board_file(saved_board_file, Menu())
    window.show_view(board_view)
    arcade.run()