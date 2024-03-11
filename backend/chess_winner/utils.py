import pandas as pd
from chess_winner.board import Board64

def transform_dataset(X:pd.DataFrame,y:pd.DataFrame,min_moves:int=10,max_moves:int=150):
    """
    Transform the dataset into readable board 64 dataset
    """
    # init empty nd array
    positions=[]
    # for each values in the game dataset
    for i in range(len(X)):
        # new Board64 with target
        board = Board64(y[i])
        # get moves from the pgn
        moves = Board64.get_moves(X.loc[i, "pgn"])
        # if enough moves
        if (len(moves)>=min_moves)&(len(moves)<=max_moves):
            positions = positions + board.get_all_grid(moves)
    # return a new dataset
    return pd.DataFrame.from_dict(positions)
