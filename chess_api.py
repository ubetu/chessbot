import chess
import chess.svg
import os
import cairocffi
from cairosvg import svg2png
class Game:
    def __init__(self):
        self.board = chess.Board()
    def is_legal_move(self, move: str) -> bool:
        try:
            return self.board.is_legal(self.board.parse_san(move))
        except chess.InvalidMoveError:
            return False
    def create_image(self) -> None:
        board_svg_code = chess.svg.board(board=self.board)
        svg2png(bytestring=board_svg_code, write_to='board.png')
        #board_svg_file = open('boardsvg.svg', 'w')
        #board_svg_file.write(chess.svg.board(board=self.board, size=350))
        #board_svg_file.close()
        #drawing = svg2rlg('boardsvg.svg')
        #renderPM.drawToFile(drawing, 'board.png', fmt='PNG')
        #os.remove('boardsvg.svg')

game = Game()
game.create_image()