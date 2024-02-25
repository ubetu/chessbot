import chess
import chess.svg
import os
import wand.image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
class Game:
    def __init__(self):
        self.board = chess.Board()
    def is_legal_move(self, move: str) -> bool:
        try:
            return self.board.is_legal(self.board.parse_san(move))
        except chess.InvalidMoveError:
            return False
    def create_image(self) -> None:
        with wand.image.Image(blob=chess.svg.board(board=self.board).encode('utf-8'), format="svg") as image:
            png_image = image.make_blob("png")
            with open("board.png", 'wb') as board_image:
                board_image.write(png_image)

game = Game()
game.create_image()