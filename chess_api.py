import chess
import chess.svg
import wand.image
from random import choice
class GameManager:
    def __init__(self):
        self.board = chess.Board()
        self.color = choice((chess.WHITE, chess.BLACK))
        self.color_text = 'Белые' if self.color == chess.WHITE else 'Черные'

    def is_legal_move(self, move: str) -> bool:
        try:
            return self.board.is_legal(self.board.parse_san(move))
        except chess.InvalidMoveError:
            return False
    def create_image(self) -> bytes:
        with wand.image.Image(blob=chess.svg.board(board=self.board).encode('utf-8'), format="svg") as image:
            png_image = image.make_blob("png")
            #with open("board.png", 'wb') as board_image:
                #board_image.write(png_image)
        return png_image

