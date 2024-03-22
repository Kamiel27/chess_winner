import pandas as pd
import re
import os
import chess
from chess_winner import engine

class Board64:

    def __init__(self,target:int,engine:engine):
        """
        Init a new board
        """
        self.board = chess.Board()
        self.target = target
        self.engine = engine

    def get_grid(self):
        """
        Get the grid in 64 columns + the target
        """
        grid=[]
        for i in range(0,64):
            piece = self.board.piece_at(i)
            if piece:
                grid.append(chess.piece_symbol(piece.piece_type).upper() if piece.color else chess.piece_symbol(piece.piece_type))
            else :
                grid.append(0)
        # add the user turn
        grid.append(int(self.board.turn))
        # keep only the 1st parts of the fen (to calculate the same each time we see the position)
        fens = self.board.fen().split(' ')
        fen = ' '.join(fens[:-4])
        self.board.set_fen(fen)
        # add the analysed score (init a new fen)
        grid.append(self.engine.analyse(self.board))
        # add the target (win/loss)
        grid.append(self.target)
        # return the grid
        return grid

    def get_all_grid(self,moves:list):
        """
        Apply a moves sequence and get all grids
        """
        # if moves not empty
        if len(moves):
            # init initial grid
            grid=[self.get_grid()]
            # for each moves try to execute and add to grid
            for move in moves:
                try:
                    self.board.push_san(move)
                    grid.append(self.get_grid())
                except:
                    nothing='wrong push'
        # return the grid
        return grid

    def get_moves(self,pgn:str):
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
