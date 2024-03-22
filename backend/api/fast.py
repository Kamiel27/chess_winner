from fastapi import FastAPI

from chess_winner.data import load_model
from chess_winner.utils import fen_to_input_columns

app = FastAPI()
app.state.model = load_model()

@app.get("/predict")
def predict(
        fen: str
    ):
    """
    Make a chess prediction.
    """
    # predicts from a converted fen
    predicts = app.state.model.predict_proba(fen_to_input_columns(fen))
    return {'white': round(predicts[0][0],4),'black': round(predicts[0][1],4)}

@app.get("/")
def root():
    return {'greeting':'Welcome to the chess winner prediction API'}
