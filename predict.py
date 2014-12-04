# Usage: python generate_training.py {DIRECTORY} {MODEL_FILE_NAME}

import numpy as np
import pandas as pd
import glob
import sys
import pickle
from subprocess import call

NUM_DAYS_IN_WINDOW = 10
NUM_POINTS_PER_DAY = 2

if len(sys.argv) != 3:
  print "Incorrect usage. Use: \"python generate_training.py {DIRECTORY} {MODEL_FILE_NAME}\""
  sys.exit()

directory = sys.argv[1]
new_directory = "%s_predictions" % directory
model_file_name = sys.argv[2]

# create new directory
call(["rm", "-rf", new_directory])
call(["mkdir", new_directory])

with open(model_file_name, "rb") as f:
  model = pickle.load(f)
  print "Model loaded."

  # get all csv files in the given directory
  files = glob.glob("%s/*.csv" % directory)
  file_num = 0

  for f in files:
    file_num += 1
    print "(%d/%d) - Making predictions for %s..." % (file_num, len(files), f[len(directory) + 1:])
    try:
      data = pd.read_csv(f)
      data = data.set_index('Date')
      data['Prediction'] = np.nan
      data['Prediction Correct'] = np.nan

      # initialize window
      window = [data.loc[[0]]['Open']]
      
      i = 0
      for i in range(1, NUM_DAYS_IN_WINDOW):
        row = data.loc[[i]]
        window = [row['Open'], row['Close']] + window

      # normalize
      window_arr = np.hstack(np.asarray(window))
      normalized = window_arr / window_arr[0]

      # result
      idx = data.loc[[0]].index
      data.loc[idx, 'Prediction'] = model.predict_proba(normalized)[:,1]
      data.loc[idx, 'Prediction Correct'] = bool(model.predict(normalized)[0]) == (data.loc[idx, 'Close'] >= data.loc[idx, 'Open'])

      while i < data.shape[0] - 1:
        i += 1
        row = data.loc[[i]]
        window_arr = window_arr[:-NUM_POINTS_PER_DAY]
        window_arr = np.hstack([np.hstack([row['Open'], row['Close']]), window_arr])
        normalized = window_arr / window_arr[0]
        idx = data.loc[[i - NUM_DAYS_IN_WINDOW + 1]].index
        data.loc[idx, 'Prediction'] = model.predict_proba(normalized)[:,1]
        data.loc[idx, 'Prediction Correct'] = bool(model.predict(normalized)[0]) == (data.loc[idx, 'Close'] >= data.loc[idx, 'Open'])

      data = data.dropna()
      data.to_csv(f.replace(directory, new_directory), sep=',', encoding='utf-8')
    except:
      print "Unable to make predictions for %s." % f[len(directory) + 1:]