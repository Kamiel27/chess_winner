####
# Frontend file for full project
####

import streamlit as st
import requests
from fentoimage.board import BoardImage

# Title
st.title("Chess Winner Predictor")
st.text("") # this add empty lines to the display, so can use it to space out elements


# Description/Instructions

st.markdown("""
Given a snapshot of an on-going online chess game (e.g. from chess.com or lichess.org), this app predicts
which player has a higher probability of winning the game
""")


# User input

user_image = st.file_uploader("Your image (png or jpeg)") # this will only accept one file at a time

if user_image is not None:

     # FIRST MODEL - Image convertion to FEN

     file = {'file': user_image}
     response = requests.post("https://chessfenbot-reduced-q5iz3btp5a-ew.a.run.app/predict", files=file).json()
     fen = response['fen']

     # Check if the request was successful
     if response is not None:
          fen = response['fen']
          certainty = response['certainty']

          # Generate a chess board image given a FEN, à la Lichess style

          renderer = BoardImage(fen)
          board_image = renderer.render()

          # Display user image and board image side by side
          col1, col2 = st.columns(2)
          with col1:
               st.text("Your input image")
               st.image(user_image, width=300)

          with col2:
               st.text("Chess board confirmation")
               st.image(board_image, width=300)

          st.text(f"FEN string: {fen}")
          st.text("")


          # SECOND MODEL - Winner prediction
          #st.markdown("***")
          col1, col2 = st.columns(2)

          with col1:
                st.markdown("<h3 style='text-align: center;'>Winning predictions</h3>", unsafe_allow_html=True)

          with col2:
                # prediction
                # Probas for white turn
                response_white = requests.get(f"https://chesswinner-wjazvss5bq-ew.a.run.app/predict?fen={fen + ' w'}").json()
                # Probas for black turn
                response_black = requests.get(f"https://chesswinner-wjazvss5bq-ew.a.run.app/predict?fen={fen + ' b'}").json()
                # Display tabs
                tab1, tab2 = st.tabs(["♘ white turn to play", "♞ black turn to play"])
                tab1.write(f"Probability of win for white ♘: {response_white['white']}")
                tab1.write(f"Probability of win for black ♞: {response_white['black']}")

                tab2.write(f"Probability of win for white ♘: {response_black['white']}")
                tab2.write(f"Probability of win for black ♞: {response_black['black']}")
