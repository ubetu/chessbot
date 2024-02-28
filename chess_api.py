import chess
import chess.svg
import wand.image
from typing import Any

from random import choice

class GameManager:
    MOVE_SYNTAX_ERROR = -1
    MOVE_ILLEGAL = -2
    MOVE_AMBIGUOUS = -3

    RES_WIN = 1
    RES_PLAYING = 0
    RES_DRAW = 2
    def __init__(self):
        self.board = chess.Board()
        self.move_log = []

    @staticmethod
    def random_color() -> (chess.COLORS, str, str):
        color = choice((chess.WHITE, chess.BLACK))
        (color_me_str, color_opponent_str) = ('Белые','Черные') if color == chess.WHITE else ('Черные','Белые')
        return color, color_me_str, color_opponent_str

    def is_legal_move(self, move: str) -> int:
        try:
            return self.board.is_legal(self.board.parse_san(move))
        except chess.InvalidMoveError:
            return self.MOVE_SYNTAX_ERROR
        except chess.IllegalMoveError:
            return self.MOVE_ILLEGAL
        except chess.AmbiguousMoveError:
            return self.MOVE_AMBIGUOUS

    def create_image(self) -> bytes:
        with wand.image.Image(blob=chess.svg.board(board=self.board).encode('utf-8'), format="svg") as image:
            png_image = image.make_blob("png")
            #with open("board.png", 'wb') as board_image:
                #board_image.write(png_image)
        return png_image

    def is_our_turn(self, color) -> bool:
        return color == self.board.turn

    def is_finished(self) -> (int, Any(None,chess.COLORS)):
        res = self.board.outcome(claim_draw=True)
        if res is None:
            return self.RES_PLAYING, None
        if res.winner:
            return self.RES_WIN, res.winner
        return self.RES_DRAW, None

    def get_move_log(self) -> list[str]:
        return self.move_log
    def do_move(self, move) -> None:
        self.board.push_san(move)
        self.move_log.append(move)






