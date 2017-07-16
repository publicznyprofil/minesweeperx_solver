import random
import win32gui

from PIL import ImageGrab

from fields import (
    FieldType,
    FIELD_BY_COLOR,
)
from moves import (
    MoveType,
    NextMove,
)
from utils import chunks
from windows import Mouse

mouse = Mouse()


class Board:
    def __init__(self):
        self.field_size = 16
        self.bomb_pos_list = []
        self.set_game_size()

    def start_new_game(self):
        self.bomb_pos_list = []
        x, y = self.get_new_game_button_pos()
        mouse.click(x, y, 1)

    def get_new_game_button_pos(self):
        return self.first_x + (self.game_x * self.field_size) // 2, self.first_y - 25

    def is_game_enabled(self):
        box = (
            self.first_x,
            self.first_y - 38,
            self.first_x + (self.game_x * self.field_size),
            self.first_y - 15
        )

        # new game button pixel position
        y = 13
        x = (self.game_x * self.field_size) // 2

        screenshot = ImageGrab.grab(box)
        screenshot_pixels = list(screenshot.getdata())
        screenshot_pixels = chunks(screenshot_pixels, self.game_x * self.field_size)
        return screenshot_pixels[y][x] == (255, 255, 0)

    def set_game_size(self):
        hwnd = win32gui.FindWindow(None, 'Minesweeper X')
        rect = win32gui.GetWindowRect(hwnd)

        x, y = rect[0], rect[1]
        window_size = rect[2] - x, rect[3] - y
        x += 15
        y += 100

        expert, intermediate, beginner = (510, 371), (286, 371), (158, 243)

        if window_size == expert:
            game_x, game_y = 30, 16
        elif window_size == intermediate:
            game_x, game_y = 16, 16
        else:
            game_x, game_y = 8, 8

        self.first_x = x
        self.first_y = y
        self.game_x = game_x
        self.game_y = game_y

    def refresh_map(self):
        box = (
            self.first_x,
            self.first_y,
            self.first_x + (self.game_x * self.field_size),
            self.first_y + (self.game_y * self.field_size)
        )
        screenshot = ImageGrab.grab(box)
        screenshot_pixels = list(screenshot.getdata())
        screenshot_pixels = chunks(screenshot_pixels, self.game_x * self.field_size)

        self.map = self.get_map(screenshot_pixels)
        self.add_bombs_to_map()

    def get_map(self, screenshot_pixels):
        return [self.get_row(screenshot_pixels, y) for y in range(8, self.game_y * self.field_size, self.field_size)]

    def get_row(self, screenshot_pixels, y):
        row = []
        # iterate over center pixel of fields
        for x in range(8, self.game_x * self.field_size, self.field_size):
            # first pixel of field is white if field is empty
            if screenshot_pixels[y - 8][x - 8] == (255, 255, 255):
                row.append(FieldType.EMPTY)
            else:
                color = screenshot_pixels[y][x]
                row.append(FIELD_BY_COLOR[color])
        return row

    def add_bombs_to_map(self):
        for x, y in self.bomb_pos_list:
            self.map[y][x] = FieldType.BOMB

    def move(self, move):
        if move.type == MoveType.DOUBLE_CLICK:
            self.double_click(move.x, move.y)
        elif move.type == MoveType.MARK_BOMBS:
            self.mark_bombs(move.bombs)
        elif move.type == MoveType.SINGLE_CLICK:
            self.single_click(move.x, move.y)

    def single_click(self, x, y):
        mouse_x, mouse_y = self.change_pos_to_mouse_pos(x, y)
        mouse.smooth_click(mouse_x, mouse_y, 1)

    def double_click(self, x, y):
        mouse_x, mouse_y = self.change_pos_to_mouse_pos(x, y)
        mouse.smooth_double_click(mouse_x, mouse_y)

    def mark_bombs(self, bombs):
        for x, y in bombs:
            self.map[y][x] = FieldType.BOMB
            self.bomb_pos_list.append((x, y))
            mouse_x, mouse_y = self.change_pos_to_mouse_pos(x, y)
            mouse.smooth_click(mouse_x, mouse_y, 2)

    def change_pos_to_mouse_pos(self, x, y):
        """In map we are not based on desktop pos."""
        x = (x * self.field_size) + self.first_x + random.randint(2, 14)
        y = (y * self.field_size) + self.first_y + random.randint(2, 14)
        return x, y

    def get_next_move(self, previous_move):
        return NextMove(self.game_x, self.game_y, self.map).get_closest_move(previous_move)
