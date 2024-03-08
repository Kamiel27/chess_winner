import pandas as pd
import re
import chess

class Board64:

    def __init__(self,target:int):
        """
        Init a new board
        """
        self.board = chess.Board()
        self.target = target

    def get_grid(self):
        """
        Get the grid in 64 columns + the target
        """
        squares=[]
        for i in range(0,64):
            piece = self.board.piece_at(i)
            if piece:
                squares.append(piece.piece_type + (0 if piece.color else 6))
            else :
                squares.append(0)
        squares.append(self.target)
        return squares

    def get_all_grid(self,moves:list):
        """
        Apply a moves sequence and get all grids
        """
        # init grid list
        grid=[]
        # if moves not empty
        if len(moves):
            # for each moves try to execute and add to grid
            for move in moves:
                try:
                    self.board.push_san(move)
                    grid.append(self.get_grid())
                except:
                    nothing='wrong push'
        # return the grid
        return grid

    def get_moves(pgn:str):
        """
        Get moves list in algebraic notation from a pgn string
        """
        # split pgn by line break
        splitted = pgn.split('\n')
        # get last element
        turns = splitted[len(splitted)-2].strip()
        # clean PGN
        turns = re.sub('\{\[\%clk [0-9:\.]+\]}','', turns)
        turns = re.sub(' [0-9]+\.\.\.','', turns)
        turns = re.sub('[0-2\/]+-[0-2\/]+','', turns)
        turns=turns.replace('  ',' ')
        # init white and black list
        moves = []
        # for all turns
        for turn in re.split('[0-9]+\. ', turns):
            # extract all moves
            if turn:
                m = turn.strip().split(' ')
                moves.append(m[0])
                if len(m)==2:
                    moves.append(m[1])
        return moves
