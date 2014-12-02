# Usage: python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {TRAINING_FILE} {TESTING_FILE}
import numpy as np
import sys
import pickle
import sklearn.linear_model as lm

if len(sys.argv) == 4:
  num_days_in_window = int(sys.argv[1])
  training_file = sys.argv[2]
  testing_file = sys.argv[3]

  training = np.genfromtxt(training_file, delimiter=",")
  testing = np.genfromtxt(testing_file, delimiter=",")

  num_days_data = training.shape[1] / 5
  num_windows = num_days_data - num_days_in_window
  windows = range(num_windows)

  
else:
  print "Incorrect usage. Use: \"python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {TRAINING_FILE} {TESTING_FILE}\""