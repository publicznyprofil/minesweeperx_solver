import math
import random
import time
import win32api
from ctypes import *


class POINT(Structure):
    _fields_ = [('x', c_ulong), ('y', c_ulong)]


class Mouse:
    def click(self, x, y, button=1):
        """Button is defined as 1 = left, 2 = right, 3 = middle."""

        self.press(x, y, button)
        self.release(x, y, button)

    def smooth_click(self, x, y, click_type=1):
        self.smooth_move(x, y)
        self.click(x, y, click_type)

    def double_click(self, x, y):
        self.press(x, y, 1)
        self.press(x, y, 2)
        self.release(x, y, 1)
        self.release(x, y, 2)

    def smooth_double_click(self, x, y):
        self.smooth_move(x, y)
        self.double_click(x, y)

    def press(self, x, y, button=1):
        button_action = 2 ** ((2 * button) - 1)
        self.move(x, y)
        win32api.mouse_event(button_action, x, y)

    def release(self, x, y, button=1):
        button_action = 2 ** ((2 * button))
        self.move(x, y)
        win32api.mouse_event(button_action, x, y)

    def move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def smooth_move(self, dst_x, dst_y):
        x, y = self.position()
        velo_x = velo_y = 0.0

        while True:
            distance = math.hypot(x - dst_x, y - dst_y)
            if distance <= 1.0:
                break

            gravity = random.uniform(5.0, 500.0)
            velo_x += (gravity * (dst_x - x)) / distance
            velo_y += (gravity * (dst_y - y)) / distance

            # Normalize velocity to get a unit vector of length 1.
            velo_distance = math.hypot(velo_x, velo_y)
            velo_x /= velo_distance
            velo_y /= velo_distance

            x += int(round(velo_x))
            y += int(round(velo_y))

            self.move(x, y)

            time.sleep(random.uniform(0.0001, 0.0003))

    def position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y
