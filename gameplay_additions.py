"""CSC111 Winter 2023 Final Project: Feelin Connected
File Information
===============================
This file contains the Button class code required to display the menu of our Connect 4 implementation.

This file is Copyright (c) 2023 Ethan McFarland, Ali Shabani, Aabha Roy and Sukhjeet Singh Nar.
"""
import pygame


class Button:
    """A class which aids in the creation of all buttons used in this game.

    NOTE: This implementation of a button class has methods specific to the game implementation.

    Instance Attributes:
        - rect: a pygame object which stores and manipulates the rectangular area of the image
        _pressed: a boolean value which represents whether the button object has been
         clicked using the pygame.mouse.get_pressed method
    """
    # Private Instance Attributes:
    #   - _image: external .png file converted into a surface using pygame.image.load('') method
    #   - _elevation: int value which represents the y coordinate value of the button while not being pressed
    #   - _dynamic_elevation: int value which represents the y coordinate value of the buttomn while being pressed
    #   - _xpos: int representing the x coordinate of the image
    #   - _ypos: int representing the y coordinate of the image
    #   - _width: int representing the width of the image
    #   - _height: int representing the height of the image

    pressed: bool
    _image: any
    _elevation: int
    _dynamic_elevation: int
    _original_y: int
    _xpos: int
    _ypos: int
    _width: int
    _height: int
    rect: pygame.Rect

    def __init__(self, x: int, y: int, image: pygame.Surface, elevation: int) -> None:
        """Initialize the button with x and y positions, the image being used,
        as well as the difference in elevation wanted while being clicked"""
        self.pressed = False
        self._image = image
        # top and bottom positions for button elevation
        self._elevation = elevation
        self._dynamic_elevation = elevation

        self._xpos = x
        self._ypos = y
        self._width = image.get_width()
        self._height = image.get_height()
        self.rect = pygame.Rect(self._xpos, self._ypos, self._width, self._height)

    def display_buttons(self, surface: pygame.Surface, pvp_image: pygame.Surface, pvp_hovered: pygame.Surface,
                        pvc_image: pygame.Surface, pvc_hover: pygame.Surface) -> None:
        """Draws the images as buttons onto the surface and specifies actions for when mouse hovers over
        or clicks on the buttons. when mouse hovers over one of the buttons its color changes by switching the
        image for the button with another one only while mouse is whithin the parameters of the button.
        When button is clicked, it calls the game its specified game state and starts the game. The button visibly
        shifts down when clicked"""

        self.rect.y = self._ypos - self._dynamic_elevation
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):

            if self._image == pvp_image:
                surface.blit(pvp_hovered, (self.rect.x, self.rect.y))

            elif self._image == pvc_image:
                surface.blit(pvc_hover, (self.rect.x, self.rect.y))

            if pygame.mouse.get_pressed()[0]:
                self._dynamic_elevation = 0
                self.pressed = True
            else:
                self.pressed = False
        else:
            if self._image == pvp_image:
                surface.blit(pvp_image, (self.rect.x, self.rect.y))
            elif self._image == pvc_image:
                surface.blit(pvc_image, (self.rect.x, self.rect.y))
            self._dynamic_elevation = self._elevation


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['pygame'],
        'disable': ['too-many-branches', 'too-many-instance-attributes', 'too-many-arguments'],

    })
