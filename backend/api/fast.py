from fastapi import FastAPI
from chess_winner.data import load_model,load_model_CP
from chess_winner.utils import fen_to_input_columns,symbols_to_dict,to_revert,revert_fen,is_checkmate,is_check
import os
import pandas as pd

app = FastAPI()
app.state.model = load_model()
app.state.model_CP = load_model_CP()

@app.get("/predict")
def predict(
        fen: str
    ):
    """
    Make a chess prediction.
    """
    # if wrong side we revert the fen
    if to_revert(fen):
        fen = revert_fen(fen)
    # test if checkmated
    checkmated_b = is_checkmate(fen.split(' ')[0]+ ' b')
    checkmated_w = is_checkmate(fen.split(' ')[0]+ ' w')

    # test if not checkmated
    if checkmated_b==False & checkmated_w==False :
        # convert a fen into predictable dataframe
        input = symbols_to_dict(fen_to_input_columns(fen))
        # predict probas
        predicts = app.state.model.predict_proba(input)
        # get centi-pawns value
        CP = input.iloc[0,65].tolist()
        # predict CP probas
        predicts_CP = app.state.model_CP.predict_proba(input[[64,65]])
        white_CP = predicts_CP[0][1]
        black_CP = predicts_CP[0][0]

        # use centipawns probas when the model failed
        if  ( (CP>0) & (predicts_CP[0][1]<predicts[0][0]) ) or (CP<0) & (predicts_CP[0][1]>predicts[0][0]):
            white = round(white_CP,2)
            black = round(black_CP,2)
        else:
            white = round(predicts[0][1],2)
            black = round(predicts[0][0],2)
    # if checkmated force win/loose result
    else:
        white = white_CP = 0 if checkmated_w else 1
        black =  black_CP = 0 if checkmated_b else 1
        CP = 10000 * (-1 if checkmated_w else 1)

    return {'white': white,
            'black': black,
            'CP':CP,
            'white_CP': white_CP,
            'black_CP': black_CP,
            }


@app.get("/")
def root():
    return {'greeting':'Welcome to the chess winner prediction API'}
