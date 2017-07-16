import win32api

from board import Board
from moves import MoveType

board = Board()

while True:
    board.start_new_game()
    previous_move = None

    while board.is_game_enabled():
        if win32api.GetAsyncKeyState(113) != 0:
            raise Exception()

        next_move = board.get_next_move(previous_move)

        if isinstance(next_move.type, MoveType):
            board.move(next_move)

        previous_move = next_move
