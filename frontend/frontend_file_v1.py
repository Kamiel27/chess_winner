import streamlit as st
import requests
import chess
from fentoimage.board import BoardImage
#from utils_fronted import fen_to_input_columns, from_number_to_player

# Title

st.title("Chess winner predictor app")
st.text("") # this add empty lines to the display, so can use it to space out elements



# This following section is commented out because it is not part of the MVP

## Description/Instructions
#
#st.text("Given a snapshot of an on-going chess game (picture of the chess board depicting current pieces positions), this app predicts which player (black or white) has a higher probability of winning the game")
#
## User input
## might have to specify the format of the file (jpeg, png, etc) depending on how the image recognition model works
#
#user_image = st.file_uploader("Choose an image file") # this will only accept one file at a time
#
## FIRST MODEL - Image convertion to FEN
#
#if user_image is not None:   # if the the image needs to be in a specific file format add another condition to the if statement to check that it has the right format
#	response = requests.get(f"https://URL_FOR_MODEL_ON_CLOUD_RUN/predict?image={user_image}").json()
#
#fen = response['prediction']
#
#if fen:
#   # Generate a chess board image given a FEN, à la Lichess style
#
#   st.text("This is your current board")
#
#   renderer = BoardImage(fen)
#   board_image = renderer.render()
#   st.image(board_image, width=400)
#
#   st.text("and its corresponding FEN string")
#   st.text(fen)




######################
# For the MVP

st.text("""Given a snapshot of an on-going chess game (FEN string), this app predicts
which player (black or white) has a higher probability of winning the game""")
st.text("(Current features displayed here were adapted to fit the MVP of this project)")
st.text("") # add blank space

# FEN manual input

fen = st.text_input("Please enter your FEN string")

if fen:
    # Generate a chess board image given a FEN, à la Lichess style

    st.text("This is your current board")

    renderer = BoardImage(fen)
    board_image = renderer.render()
    st.image(board_image, width=400)

#Once the mdel for image convertion to FEN is working, remove this whole MVP section
######################




# SECOND MODEL - Winner prediction

st.text("")
st.text("")
st.markdown("***")

st.text("Winning predictions")

#st.text("""Button for prediction is currently de-activated.
#Waiting for best model to be deployed to the cloud :)""")

if st.button('Predict'):

	# prediction
	response = requests.get(f"https://chesswinner-wjazvss5bq-ew.a.run.app/predict?fen={fen}").json()
	st.write(f"""Probability of win for white: {response['white']}
          Probability of win for black: {response['black']}""")
