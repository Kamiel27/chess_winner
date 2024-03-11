import pandas as pd

def fen_to_input_columns(fen):
	# this function reorganizes the order of the rows in the FEN string so it matches the order in the columns of the input of the model
	# after this reorganization, this function translates the ASCII characters in the FEN to a numerical classification
	
	# For the record:
	# FEN string begins from the eighth rank (row) and ending with the first. For each rank (row), 
	# squares begin from the first file (column a) and go to the eighth (column h).
	#
	# While the input needs to be organized as:
	# begin from the first rank (row) and ending with the eigth one. Within each rank (row) the order is the 
	# same as in a FEN (begin from the first file (column a) and go to the eighth (column h)).
	
	# check if input contains only valid characters
	valid_characters = set('RrNnBbQqKkPp12345678/')
	invalid_characters = [char for char in fen if char not in valid_characters]
	if invalid_characters:
		print(f"Error: FEN string contains the following invalid characters: {', '.join(invalid_characters)}")
		print("Valid characters are: R r N n B b Q q K k P p 1 2 3 4 5 6 7 8 /")
		print("Please revise input FEN and try again.")
		return
	
	# separate FEN elements
	elements = fen.split('/')
	#invert their order
	inverted_elements = reversed(elements)
	result = ''.join(inverted_elements)
	# remove "/"
	result_clean = result.replace('/', '')
	
	# now translate corrected string into numerical system to match the needed input
	# create dictionary for pieces
	translation_dict = {
		'R': '4',
		'r': '10',
		'N': '2',
		'n': '8',
		'B': '3',
		'b': '9',
		'Q': '5',
		'q': '11',
		'K': '6',
		'k': '12',
		'P': '1',
		'p': '7'
		}
	
	# loop through characters in result_clean and reassign their value according to dict
	translated_string = ''
	for char in result_clean:
		# if character is a number substitute by the specific number of zeros (representing empty squares)
		if char.isdigit():
			translated_string += '0' * int(char)
		# otherwise use dict
		elif char in translation_dict:
			translated_string += translation_dict[char]
	
	# check if translated_string has exactly 64 characters
	if len(translated_string) != 64:
		print("Error: FEN string is incomplete. Please revise and try again.")
		return

	# now create df with 64 columns
	df = pd.DataFrame(columns=[f'col{i+1}' for i in range(64)])
	
	# populate df with characters from string, make sure character is an integer
	for i, char in enumerate(translated_string):
		df.loc[0, i] = int(char)

	return df


def from_number_to_player(x):
	if x == 0:
		return "white"
	elif x == 1:
		return "black"