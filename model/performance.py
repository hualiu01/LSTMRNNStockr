from __future__ import  division
import numpy as np 
from sklearn.metrics import mean_squared_error
from math import sqrt

# this function calculated the Root Mean Squre Error (RMSE) of the predictions
def RMSE(orig, predictions):
	return sqrt(mean_squared_error(orig, predictions))
	
# this function returns the percentage and confusion matrix of correct tendency predictions
def calculate_confusion_matrix(list1, list2, class_num):
	cm = np.zeros((class_num, class_num))
	for i,j in zip(list1,list2):
		cm[i][j] += 1
	total = len(list1)
	acc = sum(cm[i][i] for i in range(class_num)) / total
	return cm,acc

def tendency_acc(orig, predicts):
	tendency_orig = []
	tendency_predicts = []
	for i in range(len(orig)-1):
		tendency_orig.append(1 if orig[i+1]>=orig[i] else 0)
		tendency_predicts.append(1 if predicts[i+1]>=predicts[i] else 0)
	return calculate_confusion_matrix(tendency_orig,tendency_predicts,2)

# this function returns the percentage and confusion matrix of correct turning points predictions 
def tp(pre, cur, thenext):
	if pre<=cur and cur > thenext:
		return 1
	elif pre > cur and cur<= thenext:
		return 2
	else:
		return 0
def turning_point_acc(orig, predicts):
	orig_turning_points = []
	pred_turning_points = []
	for i in range(len(orig)-1)[1:]:
		orig_turning_points.append(tp(orig[i-1], orig[i], orig[i+1]))
		pred_turning_points.append(tp(predicts[i-1], predicts[i], predicts[i+1]))
	return calculate_confusion_matrix(orig_turning_points,pred_turning_points,3)

# external api returns the performance results
def performance(orig, predictions):
	rmse = RMSE(orig, predictions)
	cm1, acc1 = tendency_acc(orig, predictions) # cm1 is the Confusion Matrix (0:down; 1:up or equal)"
	cm2, acc2 = turning_point_acc(orig, predictions) # cm1 is the Confusion Matrix (0:not a turning point; 1:summit; 2:vale)
	return rmse,acc1,acc2,cm1,cm2
