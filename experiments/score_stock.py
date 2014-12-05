import numpy as np
import pandas as pd
import sys
import pickle
import operator
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

results = []
with open(sys.argv[1], "rb") as f:
  model = pickle.load(f)
  data = pd.read_csv(sys.argv[2])[::-1]
  data = data.set_index('Date')
  data = np.array(data)
  data = np.delete(data, np.s_[-1:], 1)
  result = []
  for i in range(10):
    result.append(data[i:(i+data.shape[0]-9),:])
  results.append(np.hstack(result))
  formatted = np.vstack(results)

  train = formatted
  print train[0]
  # np.savetxt('sp500.csv', formatted, delimiter=",", header=','.join([str(i) for i in range(1,51)]))
  # train = np.array(pd.read_table('./sp500.csv', sep = ","))
  # chain.from_iterable is basically a "flatten" function, that takes a list of lists and 
  # converts it to one list
  # columns we want are just the opening and closing prices
  columns_we_want = list(chain.from_iterable([[5 * x, 5 * x + 3] for x in range(10)]))[:-1]

  # we get our matrix of open and close prices, and normalize the data such that all data
  # is divided by the opening price on the first day
  X = np.array([l/l[0] for l in train[:, columns_we_want]])
  print X[0]

  # we make indicators of whether or not the stock went up that day.
  y = (train[:, 48] > train[:, 45]) + 0

  print model.score(X, y)