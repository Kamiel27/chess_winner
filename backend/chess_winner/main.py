import pandas as pd
import numpy as np
import re
import chess

from sklearn.model_selection import train_test_split, GridSearchCV

# import from chess winner package
from chess_winner.board import Board64
from chess_winner.utils import transform_dataset

data = pd.read_csv('../raw_data/club_games_data.csv')
data = data[['white_result','black_result','pgn']]

status = ['timeout','repetition','timevsinsufficient','stalemate','insufficient','agreed','threecheck','kingofthehill','50move']
sample = data[(~data['white_result'].isin(status))&(~data['black_result'].isin(status))].sample(frac=1).reset_index(drop=True)

sample['result'] = sample['white_result'].map(lambda X: 1 if X=='win' else 0)

X_game = sample.drop(columns='result')
y_game = sample['result']

# define the train and test split
X_train_game, X_test_game, y_train_game, y_test_game = train_test_split(X_game,y_game,test_size=0.80,random_state=42)
# reset index (necessary for png extraction)
X_train_game = X_train_game.reset_index(drop=True)
y_train_game = y_train_game.reset_index(drop=True)

df = transform_dataset(X_train_game[0:20],y_train_game[0:20],50,100)

print(df)
