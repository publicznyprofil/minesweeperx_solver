import math
import random
from enum import Enum

from fields import (
    FieldType,
    BOMBS_AROUND_FIELDS,
)


class MoveType(Enum):
    DOUBLE_CLICK = 1
    MARK_BOMBS = 2
    SINGLE_CLICK = 3


class Move:
    def __init__(self, move_type, x, y, bombs=None):
        self.type = move_type
        self.x = x
        self.y = y
        self.bombs = bombs or []


class NextMove:
    def __init__(self, game_x, game_y, map=None):
        self.map = map
        self.game_x = game_x
        self.game_y = game_y

    def get_random_field_pos(self):
        if hasattr(self, 'map'):
            return random.choice(self.get_empty_fields())
        else:
            x = random.randint(0, self.game_x)
            y = random.randint(0, self.game_y)
            return (x, y)

    def get_empty_fields(self):
        empty_fields = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == FieldType.EMPTY:
                    empty_fields.append((x, y))
        return empty_fields

    def get_closest_move(self, previous_move):
        all_possible_moves = self.get_all_possible_move()

        if not all_possible_moves:
            x, y = self.get_random_field_pos()
            return Move(MoveType.SINGLE_CLICK, x, y)
        else:
            all_possible_moves = self.sort_moves_by_distance_from_mouse(all_possible_moves, previous_move)
            return all_possible_moves[0]

    def get_all_possible_move(self):
        moves = []
        for y, row in enumerate(self.map):
            for x, field_type in enumerate(row):
                if field_type in BOMBS_AROUND_FIELDS:
                    if self.get_bomb_count_around(x, y) == field_type.value and self.get_unfilled_count_around(x, y) > 0:
                        moves.append(Move(MoveType.DOUBLE_CLICK, x, y))
                    for k in range(field_type.value):
                        if self.get_bomb_count_around(x, y) == k and self.get_unfilled_count_around(x, y) == (
                            field_type.value - k):
                            bombs = self.get_unfilled_pos_around(x, y)
                            moves.append(Move(MoveType.MARK_BOMBS, x, y, bombs))
        return moves

    def sort_moves_by_distance_from_mouse(self, moves, previous_move):
        for move in moves:
            move.distance = math.hypot(previous_move.x - move.x, previous_move.y - move.y)
        return sorted(moves, key=lambda move: move.distance)

    def get_bomb_count_around(self, x, y):
        return len(self.get_field_pos_around(x, y, FieldType.BOMB))

    def get_unfilled_count_around(self, x, y):
        return len(self.get_field_pos_around(x, y, FieldType.EMPTY))

    def get_unfilled_pos_around(self, x, y):
        return self.get_field_pos_around(x, y, FieldType.EMPTY)

    def get_field_pos_around(self, x, y, field_type):
        field_pos = []
        for x, y in self.get_pos_around(x, y):
            if self.is_field_this_type(x, y, field_type):
                field_pos.append([x, y])
        return field_pos

    def get_pos_around(self, x, y):
        for x_ in range(-1, 2):
            for y_ in range(-1, 2):
                if (x_, y_) != (0, 0):
                    yield x + x_, y + y_

    def is_field_this_type(self, x, y, field_type):
        try:
            return self.map[y][x] == field_type
        except:
            return False
