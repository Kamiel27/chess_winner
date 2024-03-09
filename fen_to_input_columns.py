def fen_to_input_columns(fen):
	# this function reorganizes the order of the rows in the FEN string so it matches the order in the columns of the input of the model
	# after this reorganization, this function translates the ASCII characters in the FEN to a numerical classification
	
	# For the record:
	# FEN string begins from the eighth rank (row) and ending with the first. For each rank (row), squares begin from the first file (column a) and go to the eighth (column h).
	# while the input needs to be organized as:
	# begin from the first rank (row) and ending with the eigth one. Within each rank (row) the order is the same as in a FEN (begin from the first file (column a) and go to the eighth (column h))
	
	# separate FEN elements
    elements = s.split('/')
	#invert their order
    inverted_elements = reversed(elements)
    result = ''.join(inverted_elements)
	# remove "/"
    result_clean = result.replace('/', '')

	# now translate corrected string into numerical system to match the needed input
	# create dictionary for pieces
	translation_dict = {
        'R': '4',
        'r': '4',
        'N': '2',
        'n': '2',
        'B': '3',
        'b': '3',
        'Q': '5',
        'q': '5',
        'K': '6',
        'k': '6',
		'P': '1',
		'p': '1'
    }
	
	# loop through characters in inverted, cleaned string, and reassign their value according to dict
    translated_string = ''
    for char in result_clean:
		# if character is a number substitute by the specific number of zeros (representing empty squares)
        if char.isdigit():
            translated_string += '0' * int(char)
		# otherwise use dict
        elif char in translation_map:
            translated_string += translation_map[char]
        else:
            translated_string += char

	# now create df with 64 columns
	df = pd.DataFrame(columns=[f'col{i+1}' for i in range(64)])
	
    # populate df with characters from string, make sure character is an integer
    for i, char in enumerate(translated_string):
        df.loc[0, f'col{i+1}'] = int(char)

	return df



