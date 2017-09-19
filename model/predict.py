from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import lstm, time

import numpy as np 

def predict(batch_size,nb_epoch,timestep,hidden_state, layers = [1], save = False, 
	predict_multiple = False, prediction_len = 1, predict_full = False):
	# Load Data 
	normalise = True
	X_train, y_train, X_test, y_test, y_test_restorer = lstm.load_data('./input/sp500.csv', timestep, normalise) 
	print "X_train length" + str(len(X_train))
	print "X_test length" + str(len(X_test))

	# Build Model 
	if(len(layers) == 3):
		model = lstm.build_model_single_layer_LSTM(layers)
	elif(len(layers) == 4):
		model = lstm.build_model_double_layer_LSTM(layers)
	elif(len(layers) == 5):
		model = lstm.build_model_triple_layer_LSTM(layers)
	else:
		model = lstm.build_model_single_layer_LSTM([1,hidden_state,1])

	model.compile(loss='mse', optimizer='rmsprop')

	# Train the model 
	model.fit(
	    X_train,
	    y_train,
	    batch_size=batch_size,
	    nb_epoch=nb_epoch,
	    validation_split=0.05)

	model.save('./data/modelMetaData.h5')

	# Predict test data with trained model 
	predictions = lstm.predict_point_by_point(model, X_test)
	if predict_multiple:
		predictions_multiple = lstm.predict_sequences_multiple(model, X_test, window_size = timestep, prediction_len = prediction_len)
	if predict_full:
		predictions_full = lstm.predict_sequence_full(model, X_test, window_size = timestep)
	if normalise: # restore the normalised data and predictions to the original value=
		for i in range(len(y_test)):
			y_test[i] = (y_test[i]+1) * float(y_test_restorer[i])
			predictions[i] = (predictions[i]+1) * float(y_test_restorer[i])
		if predict_multiple:
			col = len(predictions_multiple[0])
			tmp = np.asarray(predictions_multiple).reshape(1,-1)
			for i in range(len(tmp)):
				tmp[i] = (tmp[i]+1) * float(y_test_restorer[i])
			predictions_multiple = tmp.reshape(-1,col).tolist()
		if predict_full:
			for i in range(len(predictions_full)):
				predictions_full[i] = (predictions_full[i]+1) * float(y_test_restorer[i])

	# save predictions and the test data for further experiments 
	if save:
		np.save('./data/y_test', y_test)
		np.save('./data/predictions', predictions)
		if predict_multiple:
			np.save('./data/predictions_multi', predictions_multiple)
		if predict_full:
			np.save('./data/predictions_full', predictions_full)

	return y_test, predictions
