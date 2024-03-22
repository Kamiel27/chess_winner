import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # Ignore Tensorflow INFO debug messages
import tensorflow as tf
import numpy as np


def load_graph(frozen_graph_filepath):
    # Load and parse the protobuf file to retrieve the unserialized graph_def.
    with tf.io.gfile.GFile(frozen_graph_filepath, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    # Import graph def and return.
    with tf.Graph().as_default() as graph:
        # Prefix every op/nodes in the graph.
        tf.import_graph_def(graph_def, name="tcb")
    return graph

class ChessboardPredictor(object):
    """ChessboardPredictor using saved model"""
    def __init__(self, frozen_graph_path='saved_models/frozen_graph.pb'):
        # Restore model using a frozen graph.
        print("\t Loading model '%s'" % frozen_graph_path)
        graph = load_graph(frozen_graph_path)
        self.sess = tf.compat.v1.Session(graph=graph)

        # Connect input/output pipes to model.
        self.x = graph.get_tensor_by_name('tcb/Input:0')
        self.keep_prob = graph.get_tensor_by_name('tcb/KeepProb:0')
        self.prediction = graph.get_tensor_by_name('tcb/prediction:0')
        self.probabilities = graph.get_tensor_by_name('tcb/probabilities:0')
        print("\t Model restored.")

    def getPrediction(self, tiles):
        """Run trained neural network on tiles generated from image"""
        if tiles is None or len(tiles) == 0:
            print("Couldn't parse chessboard")
            return None, 0.0

        # Reshape into Nx1024 rows of input data, format used by neural network
        validation_set = np.swapaxes(np.reshape(tiles, [32*32, 64]),0,1)

        # Run neural network on data
        guess_prob, guessed = self.sess.run(
            [self.probabilities, self.prediction],
            feed_dict={self.x: validation_set, self.keep_prob: 1.0})

        # Prediction bounds
        a = np.array(list(map(lambda x: x[0][x[1]], zip(guess_prob, guessed))))
        tile_certainties = a.reshape([8,8])[::-1,:]

        # Convert guess into FEN string
        # guessed is tiles A1-H8 rank-order, so to make a FEN we just need to flip the files from 1-8 to 8-1
        labelIndex2Name = lambda label_index: ' KQRBNPkqrbnp'[label_index]
        pieceNames = list(map(lambda k: '1' if k == 0 else labelIndex2Name(k), guessed)) # exchange ' ' for '1' for FEN
        fen = '/'.join([''.join(pieceNames[i*8:(i+1)*8]) for i in reversed(range(8))])
        return fen, tile_certainties

    def close(self):
        print("Closing session.")
        self.sess.close()
