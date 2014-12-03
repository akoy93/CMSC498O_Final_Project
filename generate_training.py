# Usage: python generate_training.py {NUMBER_OF_DAYS} {NUM_DAYS_IN_WINDOW} {DIRECTORY} {OUTPUT_FILE}

import numpy as np
import pandas as pd
import glob
import sys

NUM_DATA_POINTS = 5

if len(sys.argv) != 5:
  print "Incorrect usage. Use: \"python generate_training.py {NUMBER_OF_DAYS} {NUM_DAYS_IN_WINDOW} {DIRECTORY} {OUTPUT_FILE}\""
  sys.exit()

num_days_to_train = int(sys.argv[1])
num_days_in_window = int(sys.argv[2])
directory = sys.argv[3]
output_file = sys.argv[4]

# get all csv files in the given directory
files = glob.glob("%s/*.csv" % directory)
i = 0

results = []

# process all files
for f in files:
  i += 1
  print "(%d/%d) - Normalizing %s..." % (i, len(files), f[len(directory) + 1:])
  try:
    data = pd.read_csv(f)

    if data.shape[0] >= num_days_to_train:
      data = data[0:num_days_to_train]

      # drop unnecessary columns and move into one line
      data = data.set_index('Date')
      data = data.drop('Adj Close', 1)

      # convert into numpy array
      data = np.array(data)[::-1]

      result = []
      for r in range(num_days_in_window):
        result.append(data[r:(r + data.shape[0] - num_days_in_window + 1),:])

      results.append(np.hstack(result))
  except:
    print "ERROR: Unable to generate training data for %s" % f[len(directory) + 1:]

results = np.vstack(results)
np.savetxt(output_file, results, delimiter=",", header=','.join([str(i) for i in range(1,num_days_in_window * NUM_DATA_POINTS + 1)]))