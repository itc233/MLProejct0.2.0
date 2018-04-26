import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing, metrics, model_selection
#from parse import read_data
from genetics import GA


def generate_idx(port_tr, port_vald, data_len):
	tr_len = np.int(port_tr*data_len)
	vald_len = np.int(port_vald*data_len) 
	rand_idx = np.arange(data_len)
	np.random.shuffle(rand_idx)
	tr_idx = rand_idx[:tr_len]
	vald_idx = rand_idx[tr_len:]
	np.save("train_idx.txt", tr_idx)
	np.save("vald_idx.txt", vald_idx)
	return tr_idx, vald_idx

#def feval(yhat, y):
#	fit = np.sqrt(np.mean((y-yhat)**2))
#	return fit

def feval(estimator, X, gene, nfold):
	kf = model_selection.KFold(n_splits=nfold,shuffle=True)
	RMSE = np.zeros(nfold)
	gene = np.concatenate((gene, np.array([False])), axis = 0)
	for isplit, Ind in enumerate(kf.split(X)):
		Itr, Its = Ind 
		x = X[:, gene]
		xtr = x[Itr, :]
		xts = x[Its, :]
		ytr = X[Itr, -1]
		yts = X[Its, -1]
		model = estimator.fit(xtr, ytr)
		yhat = model.predict(xts)
		RMSE[isplit] = np.sqrt(np.mean(yts-yhat)**2)
		print(RMSE[isplit])
	return np.mean(RMSE)

def sample_data(X, y, port_tr, port_vald):
	tr_idx, val_idx = generate_idx(port_tr, port_vald, len(y))
	#X = preprocessing.scale(X)
	tr_idx, vald_idx = generate_idx(port_tr, port_vald, len(y))
	Xtr = X[tr_idx, :]
	ytr = y[tr_idx]
	Xvald = X[vald_idx, :]
	yvald = y[vald_idx]
	return Xtr, ytr, Xvald, yvald

def extract_gene(X, y, gene, normal):
	if(normal):
		X = preprocessing.scale(X)
		y = preprocessing.scale(y)
	X = X[:, gene]
	y = y
	return X, y


