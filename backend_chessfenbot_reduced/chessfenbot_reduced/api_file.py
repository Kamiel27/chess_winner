from fastapi import FastAPI, File, UploadFile
from .helper_functions import shortenFEN
from .helper_image_loading import loadImageFromBytes
from .chessboard_finder import findGrayscaleTilesInImage
from .chessboard_predictor import ChessboardPredictor

app = FastAPI()

# Load model
model = ChessboardPredictor()

@app.get("/")
def root():
    return {"greeting": "Hello"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Load image from file upload
    user_image = await file.read()
    img = loadImageFromBytes(user_image)

    # Look for chessboard in image, get corners and split chessboard into tiles
    tiles, corners = findGrayscaleTilesInImage(img)

    # Exit on failure to find chessboard in image
    if tiles is None:
        return {"error": "Couldn't find chessboard in image"}

    # Make prediction on input tiles
    fen, tile_certainties = model.getPrediction(tiles)

    # Use the worst case certainty as our final uncertainty score
    certainty = round(float(tile_certainties.min()),2)

    # Shorten the FEN
    short_fen = shortenFEN(fen)

    return {
        "fen": short_fen,
        "certainty": certainty
    }
