from fastapi import FastAPI
from chess_winner.data import load_model,load_model_CP
from chess_winner.utils import fen_to_input_columns,symbols_to_dict,to_revert,revert_fen
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
    # convert a fen into predictable dataframe
    input = symbols_to_dict(fen_to_input_columns(fen))
    # predict probas
    predicts = app.state.model.predict_proba(input)
    # get centi-pawns value
    CP = input.iloc[0,65].tolist()
    # predict CP probas
    predicts_CP = app.state.model_CP.predict_proba(input[[64,65]])
    # use centipawns probas when the model failed
    if  ( (CP>0) & (predicts_CP[0][1]<predicts[0][0]) ) or (CP<0) & (predicts_CP[0][1]>predicts[0][0]):
        white = round(predicts_CP[0][1],2)
        black = round(predicts_CP[0][0],2)
    else:
        white = round(predicts[0][1],2)
        black = round(predicts[0][0],2)

    return {'white': white,
            'black': black,
            'CP':input.iloc[0,65].tolist(),
            'white_CP': round(predicts_CP[0][1],2),
            'black_CP': round(predicts_CP[0][0],2),
            }


@app.get("/")
def root():
    return {'greeting':'Welcome to the chess winner prediction API'}
