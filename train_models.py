# Usage: python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {OPEN_INDEX} {CLOSE_INDEX} {NUM_DATA_POINTS_PER_DAY} {TRAINING_FILE_NAME}

# We're training a model to determine if a stock will close above its open on the next day.
# We're given the stock's data for a variable window and its opening price on the last day.

import numpy as np
import sys
import pickle
import sklearn.linear_model as lm

if len(sys.argv) != 6:
  print "Incorrect usage. Use: \"python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {NUM_DATA_POINTS_PER_DAY} {TRAINING_FILE_NAME}\""
  sys.exit()

num_days_in_window = int(sys.argv[1])
open_index = int(sys.argv[2])
close_index = int(sys.argv[3])
points_per_day = int(sys.argv[4])
training_file = sys.argv[5]

# load training and testing data
training = np.genfromtxt(training_file, delimiter=",")

# compute number of windows
num_days_data = training.shape[1] / points_per_day
num_windows = num_days_data - num_days_in_window
num_data_points_in_window = points_per_day * (num_days_in_window - 1) + open_index + 1

if num_windows == 0:
  print "Window is too large. Not enough training data."
  sys.exit()

# create {num_days_in_windows} length windows
X_windows = [training[:,range(i * points_per_day, i * points_per_day + num_data_points_in_window)] for i in range(num_windows)]
# stack data so each window is its own row
X = np.vstack(X_windows)

final_open_index = num_data_points_in_window - 1
final_close_index = final_open_index + close_index

# compute boolean values for whether stock price increased
y_open_close = np.vstack([training[:,[final_open_index + points_per_day * i, final_close_index + points_per_day * i]] for i in range(num_windows)])
y = (y_open_close[:,1] > y_open_close[:,0]) + 0
