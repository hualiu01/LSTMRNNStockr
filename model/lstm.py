import time
import warnings
import numpy as np
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

import matplotlib  
matplotlib.use('WebAgg')
import matplotlib.pyplot as plt

font = {'family' : 'normal',
        'size'   : 14}

matplotlib.rc('font', **font)

warnings.filterwarnings("ignore")

def plot_results_multiple(predicted_data, true_data, prediction_len, fig, sublocation, show):
    # fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(sublocation)
    ax.plot(true_data, label='True Data')
    ax.set_xlabel('stock samples')
    ax.set_ylabel('stock prices')
    print 'ploting predicted_data'
    #Pad the list of predictions to shift it in the graph to it's correct start
    onetime = True
    for i, data in enumerate(predicted_data):
        plt.plot(range(i*prediction_len, (i+1)*prediction_len),data, label='Prediction', color='orange')
        if onetime:
        	plt.legend(fontsize=13,loc=3)
        	onetime = False
    if show:
    	plt.show()

def plot_results(predicted_data, true_data, fig, sublocation, show):
    # fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(sublocation)
    ax.plot(true_data, label='True Data')
    ax.set_xlabel('stock samples')
    ax.set_ylabel('stock prices')
    print 'ploting predicted_data'
    plt.plot(predicted_data, label='Prediction')
    plt.legend(fontsize=13,loc=3)
    if show:
    	plt.show()

def load_data(filename, seq_len, normalise_window):
    f = open(filename, 'r').read()
    data = f.split('\n')

    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])
    
    if normalise_window:
        result = normalise_windows(result)

    result = np.array(result)

    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))  

    y_test_restorer = data[int(row):int(row)+len(y_test)]
    return [x_train, y_train, x_test, y_test, y_test_restorer]

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def build_model_single_layer_LSTM(layers): 
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[2]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print "Compilation Time : ", time.time() - start
    return model

def build_model_double_layer_LSTM(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print "Compilation Time : ", time.time() - start
    return model

def build_model_triple_layer_LSTM(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        input_dim=layers[1],
        output_dim=layers[2],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[3],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[4]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print "Compilation Time : ", time.time() - start
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted

def predict_sequence_full(model, data, window_size):
    #Shift the window by 1 new prediction each time, re-run predictions on new window
    curr_frame = data[0]
    predicted = []
    for i in xrange(len(data)):
        predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
    return predicted

def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in xrange(len(data)/prediction_len):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in xrange(prediction_len):
            predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs