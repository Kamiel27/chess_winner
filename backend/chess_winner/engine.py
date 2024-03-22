import os
import chess.engine
from chess.engine import Cp, Mate, MateGiven, PovScore

class Engine:

    def __init__(self):
        """
        Init a new engine
        """
        self.engine = chess.engine.SimpleEngine.popen_uci(os.environ.get("ENGINE_PATH"))

    def analyse(self,board):
        """
        Return the score in white point of view
        """
        # analysis the game using the engine
        analysis = self.engine.analyse(chess.Board(board.fen()), chess.engine.Limit(time=float(os.environ.get("ENGINE_TIMEOUT")),depth=int(os.environ.get("ENGINE_DEPTH"))))
        # return the score
        return analysis['score'].white().score(mate_score=int(os.environ.get("ENGINE_MATE_SCORE")))

    def quit(self):
        """
        Quit the chess engine
        """
        self.engine.quit()
