import pandas as pd
import numpy as np
import operator
import sklearn.linear_model as lm
import sys
from itertools import chain

def normalize10day(stocks):
  def process_column(i):
    if operator.mod(i, 5) == 1:
      return stocks[:,i] * 0
    if operator.mod(i, 5) == 2:
      return stocks[:,i] * 0
    if operator.mod(i, 5) == 4:
      return stocks[:,i] * 0
      #return np.log(stocks[:,i] + 1)
    else:
      return stocks[:,i] / stocks[:,0]

  stocks_dat = np.array([process_column(i) for i in range(46)]).transpose()
  return stocks_dat

def normalizeRow(stocks):
  def process_column(i):
    if operator.mod(i, 5) == 1:
      return stocks[i] * 0
    if operator.mod(i, 5) == 2:
      return stocks[i] * 0
    if operator.mod(i, 5) == 4:
      return stocks[i] * 0
      #return np.log(stocks[:,i] + 1)
    else:
      return stocks[i] / stocks[0]

  stocks_dat = np.array([process_column(i) for i in range(46)]).transpose()
  return stocks_dat

train = np.array(pd.read_table(sys.argv[1], sep = ","))

if train.shape[0] == 94: # if we're using the kaggle training data
  n_windows = 490
  windows = range(n_windows)
  
  # we convert the 500 day data into a stack of 10 day data.
  X_windows = [train[:,range(1 + 5*w, 47 + 5*w)] for w in windows]
  print X_windows[0].shape
  X_windows_normalized = [normalize10day(w) for w in X_windows]
  
  print len(X_windows_normalized)

  X = np.vstack(X_windows_normalized)
  print X[0]
  print X.shape

  # read in the response variable and convert to indicators
  y_stockdata = np.vstack([train[:, [46 + 5*w, 49 + 5*w]] for w in windows])
  y = (y_stockdata[:,1] > y_stockdata[:,0]) + 0

  model = lm.LogisticRegression(penalty="l2").fit(X, y)
  print model.score(X, y)

  results = []
  data = pd.read_csv(sys.argv[2])
  data = data.set_index('Date')
  data = np.array(data)
  data = np.delete(data, np.s_[-1:], 1)
  result = []
  for i in range(10):
    result.append(data[i:(i+data.shape[0]-9),:])
  results.append(np.hstack(result))
  formatted = np.vstack(results)

  print formatted[0]

  X = np.array([normalizeRow(l) for l in formatted[:,:-4]])
  y = (formatted[:, 48] > formatted[:, 45]) + 0

  print model.score(X, y)