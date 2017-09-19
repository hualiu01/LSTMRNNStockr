from keras.models import load_model
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error

model = load_model('./model/data/modelMetaData.h5')

model.summary()

model_conf = model.get_config()
# print model_conf

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def RMSE(orig, predictions):
	return sqrt(mean_squared_error(orig, predictions))

def predict(filename='./static/data/aapl.csv', seq_len=50, normalise_window=True):
	f = open(filename, 'r').read()
	prices = f.split('\n')

	data = []
	for i in range(len(prices)-1)[1:]:
		data.append(prices[i].split(',')[4])
	data.reverse()

	print "testing data length: " + str(len(data))
	data.append(0)
	sequence_length = seq_len + 1
	result = []
	for index in range(len(data) - sequence_length):
		result.append(data[index: index + sequence_length])
	print "windowed testing data length: "+ str(len(result))

	if normalise_window:
		result = normalise_windows(result)

	result = np.array(result)
	x_test = result[:, :-1]
	y_test = result[:, -1]
	y_test_restorer = data[:len(y_test)]
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
	predictions = model.predict(x_test)

	if normalise_window: # restore the normalised data and predictions to the original value=
		for i in range(len(y_test)):
			y_test[i] = (y_test[i]+1) * float(y_test_restorer[i])
			predictions[i] = (predictions[i]+1) * float(y_test_restorer[i])

	return RMSE(y_test[:-1], predictions[:-1]), predictions[-1][0]

print predict()