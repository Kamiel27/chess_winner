import streamlit as st
import requests
import chess

# Title

st.title("Chess winner predictor app")

# Description/Instructions

st.text("Given a snapshot of an on-going chess game (picture of the chess board depicting current pieces positions), this app predicts which player (black or white) has a higher probability of winning the game")

# User input
# might have to specify the format of the file (jpeg, png, etc) depending on how the image recognition model works

user_image = st.file_uploader("Choose an image file") # this will only accept one file at a time

# FIRST MODEL - Image convertion to FEN

if user_image is not None:   # if the the image needs to be in a specific file format add another condition to the if statement to check that it has the right format
	response = requests.get(f"https://URL_FOR_MODEL_ON_CLOUD_RUN/predict?image={user_image}").json()

fen = response['prediction']

# Generate a chess board image given a FEN, à la Lichess style

st.text("This is your current board")

board = chess.Board(fen)
print(board)

st.text("and its corresponding FEN string")
print(fen)


# SECOND MODEL - Winner prediction

st.text("Winner prediction")

if st.button('Predict'):

	# transform FEN into correct input format for model
	X_new = fen_to_input_columns(fen)
	
	# prediction
	response = requests.get(f"https://URL_FOR_MODEL_ON_CLOUD_RUN/predict?X_new={X_new}").json()
	st.write("Most likely winner:", str(response['prediction']))
