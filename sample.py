# Usage: python sample.py {NUM_TRAINING} {NUM_TESTING} {INPUT_FILE}
import pandas as pd
import numpy as np
import sys

if len(sys.argv) == 4:
  num_training = int(sys.argv[1])
  num_testing = int(sys.argv[2])
  input_file = sys.argv[3]

  training_file = "training%d_%s" % (num_training, input_file)
  testing_file = "testing%d_%s" % (num_testing, input_file)

  total_rows = num_training + num_testing
  data = pd.read_csv(input_file)
  if data.shape[0] < total_rows:
    print "Not enough rows in input file."
  else:
    # randomly sample rows of input file
    rows = np.random.choice(data.index.values, total_rows)

    training_rows = sorted(rows[:num_training])
    testing_rows = sorted(rows[-num_testing:])

    # grab rows from dataframe
    data = np.asarray(data)
    training = data[training_rows]
    testing = data[testing_rows]

    np.savetxt(training_file, training)
    np.savetxt(testing_file, testing)
else:
  print "Incorrect usage. Use: \"python sample.py {NUM_TRAINING} {NUM_TESTING} {INPUT_FILE}\""
