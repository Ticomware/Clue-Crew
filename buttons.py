from abc import ABC, abstractmethod
import arcade
from point import Point

DEFAULT_COLOR = arcade.color.GREEN
DEFAULT_TEXT_COLOR = arcade.color.PURPLE
DEFAULT_FONT_SIZE = 12


class Button(ABC):
    def __init__(self, text, x, y, width, height, color=DEFAULT_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFAULT_FONT_SIZE):
        self.text = text
        self.center = Point(x, y)
        self.width = width
        self.height = height
        self.hovered = False
        self.color = color
        self.text_color = text_color
        self.font_size = font_size

    def check_hovered(self, mouse_x, mouse_y):
        if (abs(mouse_x - self.center.x) <= self.width // 2) and (abs(mouse_y - self.center.y) <= self.height // 2):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self):
        if not self.hovered:
            arcade.draw_rectangle_filled(
                self.center.x, self.center.y, self.width, self.height, self.color)
            arcade.draw_text(self.text, self.center.x, self.center.y, self.text_color,
                             anchor_x="center", anchor_y="center", font_size=self.font_size)
        else:
            arcade.draw_rectangle_filled(
                self.center.x, self.center.y, self.width, self.height, self.text_color)
            arcade.draw_text(self.text, self.center.x, self.center.y, self.color,
                             anchor_x="center", anchor_y="center", font_size=self.font_size)

    @abstractmethod
    def on_click(self):
        pass


class Box(Button):
    def __init__(self, item, text, x, y, width, height, color=DEFAULT_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFAULT_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color)
        self.item = item

    def on_click(self):
        return self.item


class FunctionButton(Button):
    def __init__(self, function, text, x, y, width, height, color=DEFAULT_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFAULT_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color, font_size)
        self.function = function

    def on_click(self):
        self.function()


class ViewButton(Button):
    def __init__(self, view, text, x, y, width, height, color=DEFAULT_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFAULT_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color, font_size)
        self.view = view

    def on_click(self):
        self.view.window.show_view(self.view)


class ExitButton(FunctionButton):
    def __init__(self, x, y, width, height, color=DEFAULT_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFAULT_FONT_SIZE):
        super().__init__(arcade.close_window, 'Exit', x, y,
                         width, height, color, text_color, font_size)
