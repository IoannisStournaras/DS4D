import numpy as np
import matplotlib.pyplot as plt
import scipy.io


def logistic_regression(X,w):
    X = np.concatenate([np.ones((X.shape[0],1)),X],axis=1)
    a = np.dot(X,w)
    return 1/(1+np.exp(-a))


def sqrt_mean_error(X,y,weights):
    X = np.concatenate([np.ones((X.shape[0],1)),X],axis=1)
    f = np.dot(X,weights)
    f = np.rint(f)
    error = (y-f)*(y-f)
    return np.sqrt(np.sum(error)/error.shape[0])


def find_cluster(xtest,w1,w2,K=6):
    predict_test = np.zeros([1,K])
    for kk in range(K):
        predict_test[:,kk] =logistic_regression(xtest.reshape(1,44),w1[kk,:])
    print(predict_test)
    X = np.concatenate([np.ones((predict_test.shape[0],1)),predict_test],axis=1)
    f = np.dot(X,w2)
    return int(np.rint(f))   

#find_cluster(x.iloc[23],w1,w2)


