from predict import predict 
from performance import performance
from lstm import plot_results, plot_results_multiple

import numpy as np

import matplotlib  
matplotlib.use('WebAgg')
import matplotlib.pyplot as plt

def exp_batchsize(layers_candidates, batchsize_candidates):
	results = "nb_epoch = 70, timestep=30 \n"
	for layers in layers_candidates:
		results += "layers: " + str(layers) + "---------------------\n"
		results += "batch_size\tRMSE\tTPA\tTPPA\n"
		for batch_size in batchsize_candidates:
			y_test, predictions = predict(batch_size = batch_size, nb_epoch = 70, timestep=30, hidden_state=50, layers = layers)
			rmse,tp_acc,tpp_acc,cm1,cm2 = performance(y_test, predictions)
			results += str(batch_size)+"\t"+str(rmse)+"\t"+str(tp_acc)+"\t"+str(tpp_acc )+"\n"

	with open("./exp/batchsize.txt","w") as file:
		file.write(results)

def exp_epoch(layers_candidates, timesteps_candidates, epoch_candidates):
	results = "batch_size = 512 \n"
	for layers in layers_candidates:
		for timesteps in timesteps_candidates:
			results += "layers: " + str(layers) + "; timesteps: " + str(timesteps) + "-------------------\n"
			results += "number of epoch\tRMSE\tTPA\tTPPA\n"
			for epoch in epoch_candidates:
				y_test, predictions = predict(batch_size = 512, nb_epoch = epoch, timestep = timesteps, hidden_state = 50, layers = layers)
				rmse,tp_acc,tpp_acc,cm1,cm2 = performance(y_test, predictions)
				results += str(epoch)+"\t"+str(rmse)+"\t"+str(tp_acc)+"\t"+str(tpp_acc )+"\n"
	with open("./exp/epoch.txt","w") as file:
		file.write(results)

def exp_timesteps(hidden_state_candidates, timestep_candidates):
	results = "batch_size = 512,nb_epoch = 70 \n"
	for hidden_state in hidden_state_candidates:
		results += "hidden state size: " + str(hidden_state) +"------------------\n"
		results += "timestep size\tRMSE\tTPA\tTPPA\n"
		for timestep in timestep_candidates:
			y_test, predictions = predict(512,70,timestep,hidden_state)
			rmse,tp_acc,tpp_acc,cm1,cm2 = performance(y_test, predictions)
			results += str(timestep)+"\t"+str(rmse)+"\t"+str(tp_acc)+"\t"+str(tpp_acc )+"\n"

	with open("./exp/timestep.txt","w") as file:
		file.write(results)

def exp_hidden_state(hidden_state_candidates):
	results = "batch_size = 512,nb_epoch = 70,timestep=50 \n"
	results += "hidden state size\tRMSE\tTPA\tTPPA\n"	
	for hidden_state in hidden_state_candidates:
		y_test, predictions = predict(512,70,50, hidden_state) # !!!!!!!!!!!!timestep
		rmse, tp_acc, tpp_acc,cm1,cm2 = performance(y_test, predictions)
		results += str(hidden_state)+"\t"+str(rmse)+"\t"+str(tp_acc)+"\t"+str(tpp_acc )+"\n"

	with open("./exp/hiddenstate.txt","w") as file:
		file.write(results)


def exp_layer_depth(layers):
	prediction_len = 20
	predict(batch_size = 512, nb_epoch = 70,timestep = 50,hidden_state = 50, layers = layers, save = True,
		predict_multiple = True, prediction_len = prediction_len, predict_full = True)

	# Plot the predictions 
	orig = np.load("./data/y_test.npy")
	predictions = np.load("./data/predictions.npy")

	rmse,tp_acc,tpp_acc,cm1,cm2 = performance(orig, predictions)
	print "Tendency Prediction Confusion Matrix (0:down; 1:up or equal): "
	print cm1
	print "Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): "
	print cm2
	print "rmse: " + str(rmse) + "TPA: " + str(tp_acc) + "TPPA: " + str(tpp_acc)

	predictions_multi = np.load("./data/predictions_multi.npy")
	predictions_full = np.load("./data/predictions_full.npy")
	fig = plt.figure(facecolor='white')
	plot_results(predictions, orig, fig, sublocation = 121, show = False)
	# plot_results(predictions_full, orig, fig, sublocation = 222, show = False)
	plot_results_multiple(predictions_multi, orig, prediction_len = prediction_len, 
		fig = fig, sublocation = 122, show = True)

# 1.1 exp_batchsize
# exp_batchsize(layers_candidates = [[1,50,1],[1,50,50,1]], 
# 	batchsize_candidates = [32,64,128,256,512])
# 1.2 exp_epoch
# exp_epoch(layers_candidates = [[1,100,1],[1,50,100,1]], 
# 	timesteps_candidates = [10,50], 
# 	epoch_candidates = [1,5,10,15,20,25,30,35,50,70,100,150,200])


# 2.1 exp_timesteps : estimate running time ____
# exp_timesteps(hidden_state_candidates = [10,25,50,75,100], 
# 	timestep_candidates = [5,10,15,20,35,50,75,90,100,110,120,150])
# 2.2 exp_hiddenstates : estimate running time ____
# exp_hidden_state(hidden_state_candidates = [1,3,5,7,10,15,20,25,30,35,40,50,70,80,100])

# 3. exp_LSTM_layer_depth : estimate running time ____
# exp_layer_depth([1,30,1])
"""
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  88.  118.]
 [  98.  109.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 136.   24.   28.]
 [  90.    1.   21.]
 [  89.   23.    0.]]
 rmse: 26.3269746028TPA: 0.476997578692TPPA: 0.332524271845
"""
# exp_layer_depth([1,60,1])
"""
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  86.  120.]
 [ 101.  106.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 125.   29.   34.]
 [  81.    0.   31.]
 [  77.   35.    0.]]
rmse: 22.1483220029TPA: 0.464891041162TPPA: 0.303398058252
"""

# exp_layer_depth([1,30,30,1])
"""
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  89.  117.]
 [  96.  111.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 138.   23.   27.]
 [  95.    1.   16.]
 [  90.   20.    2.]]
rmse: 27.4761089593TPA: 0.484261501211TPPA: 0.342233009709
"""

exp_layer_depth([1,20,20,20,1])
"""
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  84.  122.]
 [ 101.  106.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 161.   14.   13.]
 [  99.    1.   12.]
 [  95.   13.    4.]]
rmse: 32.0570884719TPA: 0.46004842615TPPA: 0.402912621359
"""

# exp_layer_depth([1,50,50,50,1])
"""
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  88.  118.]
 [ 101.  106.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 155.   17.   16.]
 [  93.    2.   17.]
 [  93.   16.    3.]]
rmse: 31.1416397512TPA: 0.469733656174TPPA: 0.388349514563

epoch 50
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  91.  115.]
 [  99.  108.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 135.   26.   27.]
 [  82.    4.   26.]
 [  86.   24.    2.]]
rmse: 23.9289568118TPA: 0.481840193705TPPA: 0.342233009709

epoch 100
Tendency Prediction Confusion Matrix (0:down; 1:up or equal): 
[[  93.  113.]
 [ 104.  103.]]
Turning Point Prediction Confusion Matrix (0:not a turning point; 1:summit; 2:vale): 
[[ 106.   37.   45.]
 [  73.    0.   39.]
 [  66.   46.    0.]]
rmse: 25.9057863944TPA: 0.474576271186TPPA: 0.257281553398
"""

# exp_layer_depth([1,100,1])

# todo:
# 4. plot axi label
# 5. start writting
