import numpy as np
import sys
import pickle

NUMBER_OF_DAYS_IN_WINDOW = 10
NUM_DATA_POINTS_PER_DAY = 2

if len(sys.argv) != 3:
  print "Incorrect usage. Use: \"python test_model.py {MODEL_FILE_NAME} {TESTING_FILE_NAME}\""
  sys.exit()

model_file = sys.argv[1]
test_file = sys.argv[2]
num_days_in_window = NUMBER_OF_DAYS_IN_WINDOW
points_per_day = NUM_DATA_POINTS_PER_DAY
points_in_window = num_days_in_window * points_per_day

# load testing data
testing = np.genfromtxt(test_file, delimiter=",")

# normalize
for row in testing:
  for i in range(points_in_window - points_per_day + 1):
    row[i] = row[i] / row[0]

# pull X and y
X = np.array([p[range(points_in_window - 1)] for p in testing])
y = (testing[:, points_in_window - points_per_day + 1] > testing[:, points_in_window - points_per_day]) + 0

# test model
with open(model_file, "rb") as f:
  model = pickle.load(f)
  print model.score(X, y)