import pandas as pd
import chess
from chess_winner.board import Board64
from chess_winner.engine import Engine
import os


def transform_dataset(X:pd.DataFrame,y:pd.DataFrame,min_moves:int=10,max_moves:int=150):
    """
    Transform the dataset into readable board 64 dataset
    """
    # init new engine
    engine = Engine()
    # init empty nd array
    positions=[]
    # for each values in the game dataset
    for i in range(len(X)):
        # new Board64 with target
        board = Board64(y[i],engine)
        # get moves from the pgn
        moves = board.get_moves(X.loc[i, "pgn"])
        # if enough moves
        if (len(moves)>=min_moves)&(len(moves)<=max_moves):
            positions = positions + board.get_all_grid(moves)

    # return a new dataset
    return pd.DataFrame.from_dict(positions)

def fen_to_input_columns(fen):
    """
    This function reorganizes the order of the rows in the FEN string so it matches the order in the columns of the input of the model
    after this reorganization, this function translates the ASCII characters in the FEN to a numerical classification
    For the record:
    FEN string begins from the eighth rank (row) and ending with the first. For each rank (row), squares begin from the first file (column a) and go to the eighth (column h).
    while the input needs to be organized as:
    begin from the first rank (row) and ending with the eigth one. Within each rank (row) the order is the same as in a FEN (begin from the first file (column a) and go to the eighth (column h))
    """
    #separate FEN elements
    splits = fen.split(' ')
    #line positions
    elements = splits[0].split('/')
 	# invert their order
    elements.reverse()
 	# join it
    result = ''.join(elements)
	# remove "/"
    result_clean = result.replace('/', '')
	# create dictionary for turn
    turn_map={'w': 1,'b': 0 }
	# loop through characters in inverted, cleaned string, and reassign their value according to dict
    translated_string = []
    for char in result_clean:
		# if character is a number substitute by the specific number of zeros (representing empty squares)
        if char.isdigit():
            translated_string += [0 for i in range(int(char))]
		# otherwise use dict
        else:
            translated_string.append(char)

    # user turn
    if len(splits)>1:
        turn = splits[1]
    # default white
    else:
        turn = 'w'
    # add turn to dataframe
    translated_string.append(turn_map[turn])

    # new chess engine
    engine = Engine()

    # test if a side is checked
    fen = fen.split(' ')[0]
    # and if yes for the fen side
    if is_check(fen + ' b'):
        fen = fen + ' b'
    if is_check(fen + ' w'):
        fen = fen + ' w'
    # analyse result (get score)
    score = engine.analyse(chess.Board(fen))
    # add turn to dataframe
    translated_string.append(score)

    # now create df with 64 columns
    df = pd.DataFrame(data=[translated_string])

    return df

def input_columns_to_fen(input_columns):
    '''
    input columns to fen
    '''
    appstr=''
	# for each columns do
    for ic in input_columns.columns[0:64]:
        appstr += str(input_columns.iloc[0][ic])
	# define the replacement list
    rep = [''.join(['0' for y in range(i+1)]) for i in reversed(range(8))]
    lines=[]
    # for each lines do
    for i in range(8):
        line = appstr[(i*8):(i+1)*8]
        for r in rep:
           line = line.replace(r, str(len(r)))
        lines.append(line)

    # reverse the line (to fit the dataset format)
    lines.reverse()
    # return the fen
    return '/'.join(lines)+' '+ ('w' if input_columns.iloc[0][64]==1 else 'b')

def symbols_to_dict(symbols):
    '''
    transform symbols into mapped values
    '''
    #define the mapped values
    translation_map = {'R': 4,'r': 14,'N': 2,'n': 12,'B': 3,'b': 13,'Q': 5,'q': 15,'K': 6,'k': 16,'P': 1,'p': 11}
    #return the new 64 mapped values columns
    symbols.iloc[:,0:64]=symbols.iloc[:,0:64].map(lambda x: int(translation_map[x])  if x in translation_map else 0)
    return symbols

def dict_to_symbols(symbols):
    '''
    transform symbols into mapped values
    '''
    #define the mapped values
    translation_map = {4 : 'R', 14 : 'r', 2 : 'N', 12 : 'n', 3 : 'B', 13 : 'b',5 : 'Q', 15 : 'q', 6 : 'K',16 : 'k',1 : 'P', 11 :'p'}
    #return the new 64 mapped values columns
    symbols.iloc[:,0:64]=symbols.iloc[:,0:64].map(lambda x: translation_map[x] if x in translation_map else 0)
    return symbols

def revert_fen(fen):
    '''
    revert chess board fen
    '''
    splits = fen.split(' ')
    splits[0]=splits[0][::-1]
    return ' '.join(splits)

def to_revert(fen):
    '''
    detect chess board side
    '''
    splits = fen.split('/')
    cntupper=cntlower=0
    # check the upper side only
    side = ' '.join(fen.split('/')[0:4])
    for char in side:
        if ~char.isdigit() & char.isupper():
            cntupper+=1
        if ~char.isdigit() & char.islower():
            cntlower+=1
    return True if cntupper>cntlower else False

def is_checkmate(fen):
    return chess.Board(fen).is_checkmate()

def is_check(fen):
    return chess.Board(fen).is_check()
