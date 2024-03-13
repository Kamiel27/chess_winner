import pickle
import bz2
import _pickle as cPickle
import os

def load_compressed_model():
    '''
    Load from the compressed model
    '''
    data = bz2.BZ2File(open(os.environ.get("MODEL_TARGET_COMPRESSED"), 'rb'))
    model = cPickle.load(data)
    return model

def load_model():
    '''
    Load model
    '''
    model = pickle.load(open(os.environ.get("MODEL_TARGET_PICKLE"), 'rb'))
    return model

def save_model(model):
    '''
    Save model in pickle format
    '''
    pickle.dump(model, open(os.environ.get("MODEL_TARGET_PICKLE"), 'wb'))

def save_compressed_model(model):
    '''
    Save model in compressed pickle format
    '''
    cPickle.dump(model, open(os.environ.get("MODEL_TARGET_COMPRESSED"), 'rb'))
