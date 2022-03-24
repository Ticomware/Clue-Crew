from abc import ABC, abstractmethod
import arcade
from constants import DEFAULT_FOREGROUND_COLOR, DEFAULT_TEXT_COLOR
from point import Point

######################################### 
#               Constants               #
######################################### 
DEFAULT_BOX_COLOR = DEFAULT_FOREGROUND_COLOR
DEFAULT_BOX_TEXT_COLOR = DEFAULT_TEXT_COLOR
DEFUALT_BOX_FONT_SIZE = 12

######################################################################################################
#                                              Buttons                                               #
######################################################################################################
class Button(ABC):
    """
    Abstract base class for all other buttons.
    The button consists of a rectangle and text. The colors of the button are altered when it is hovered.
    All derived buttons must define an on_click method.
    """
    def __init__(self, text, x, y, width, height, color=DEFAULT_BOX_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFUALT_BOX_FONT_SIZE):
        self.text = text
        self.center = Point(x, y)
        self.width = width
        self.height = height
        self.hovered = False
        self.color = color
        self.text_color = text_color
        self.font_size = font_size

    def check_hovered(self, mouse_x, mouse_y):
        """
        Determines if this button is being hovered.

        Arguments:
            mouse_x
                Current x-coordinate of the mouse.
            mouse_y
                Current y-coordinate of the mouse.
        """
        if (abs(mouse_x - self.center.x) <= self.width // 2) and (abs(mouse_y - self.center.y) <= self.height // 2):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self):
        """ Displays this button. """
        # Colors are exchanged when button is hovered
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
  """
    Representation of a box containing an item.
    The item is returned when the box is clicked.
    """
    def __init__(self, item, text, x, y, width, height, color=DEFAULT_BOX_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFUALT_BOX_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color, font_size)
        self.item = item

    def on_click(self):
        """ Returns this boxes' item. """
        return self.item

class FunctionButton(Button):
  """ Representation of a button that executes a function when it is clicked. """
    def __init__(self, function, text, x, y, width, height, color=DEFAULT_BOX_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFUALT_BOX_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color, font_size)
        self.function = function

    def on_click(self):
        """ Executes this boxes' function. """
        self.function()

class ViewButton(Button):
    """
    Representaion of a navigation button.
    Alters the current view when it is clicked.
    """
    def __init__(self, view, text, x, y, width, height, color=DEFAULT_BOX_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFUALT_BOX_FONT_SIZE):
        super().__init__(text, x, y, width, height, color, text_color, font_size)
        self.view = view

    def on_click(self):
        """ Displays this button's view. """
        self.view.window.show_view(self.view)

class ExitButton(FunctionButton):
    """ 
    Representation of an exit button. 
    The main arcade window is closed when this button is clicked. 
    """
    def __init__(self, x, y, width, height, color=DEFAULT_BOX_COLOR, text_color=DEFAULT_TEXT_COLOR, font_size=DEFUALT_BOX_FONT_SIZE):
        super().__init__(arcade.close_window, 'Exit', x, y,
                         width, height, color, text_color, font_size)
