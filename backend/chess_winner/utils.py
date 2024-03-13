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

def fen_to_input_columns(fen):
    """
    This function reorganizes the order of the rows in the FEN string so it matches the order in the columns of the input of the model
    after this reorganization, this function translates the ASCII characters in the FEN to a numerical classification
    For the record:
    FEN string begins from the eighth rank (row) and ending with the first. For each rank (row), squares begin from the first file (column a) and go to the eighth (column h).
    while the input needs to be organized as:
    begin from the first rank (row) and ending with the eigth one. Within each rank (row) the order is the same as in a FEN (begin from the first file (column a) and go to the eighth (column h))
    """
    #separate FEN elements (extract only positions)
    elements = fen.split(' ')[0].split('/')
	# invert their order
    inverted_elements = reversed(elements)
    result = ''.join(elements)
	# remove "/"
    result_clean = result.replace('/', '')
	# now translate corrected string into numerical system to match the needed input
	# create dictionary for pieces
    translation_map = {
        'R': '10',
        'r': '4',
        'N': '8',
        'n': '2',
        'B': '9',
        'b': '3',
        'Q': '11',
        'q': '5',
        'K': '12',
        'k': '6',
		'P': '7',
		'p': '1'
    }

	# loop through characters in inverted, cleaned string, and reassign their value according to dict
    translated_string = []
    for char in result_clean:
		# if character is a number substitute by the specific number of zeros (representing empty squares)
        if char.isdigit():
            translated_string += ['0' for i in range(int(char))]
		# otherwise use dict
        elif char in translation_map:
            translated_string.append(translation_map[char])
        else:
            translated_string.append(char)


	# now create df with 64 columns
    df = pd.DataFrame([translated_string])

    return df
