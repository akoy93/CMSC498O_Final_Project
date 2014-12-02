# Usage: python normalize.py {NUMBER_OF_DAYS} {DIRECTORY} {OUTPUT_FILE}

import numpy as np
import pandas as pd
import glob
import sys

def normalize_row(row, open_price):
  def process_value(i):
    if i == 4:
      return np.log(row[i] + 1)
    else:
      return row[i] / open_price
  return [process_value(i) for i in range(len(row))]

if len(sys.argv) == 4:
  num_days = int(sys.argv[1])
  directory = sys.argv[2]
  output_file = sys.argv[3]

  # get all csv files in the given directory
  files = glob.glob("%s/*.csv" % directory)
  i = 0

  results = []

  # normalize all files
  for f in files:
    i += 1
    print "(%d/%d) - Normalizing %s..." % (i, len(files), f[len(directory) + 1:])
    try:
      data = pd.read_csv(f)

      if data.shape[0] >= num_days:
        data = data[0:num_days]

        # drop unnecessary columns and move into one line
        data = data.drop('Date', 1)
        data = data.drop('Adj Close', 1)

        # get open_price value
        open_price = data.iloc[[data.shape[0] -1]]['Open'].values[0]

        # convert to numpy array
        data = np.array(data)

        # normalize rows and concatenate data into one line
        normalized = [normalize_row(r, open_price) for r in data]
        normalized = normalized[::-1]
        normalized = np.hstack(normalized)

        arrstr = np.char.mod('%f', normalized)
        str = ",".join(arrstr)

        results.append(str)
    except:
      print "ERROR: Unable to normalize %s" % f[len(directory) + 1:]

  # write data to file
  with open(output_file, "w") as f:
    for row in results:
      f.write(row + "\n")
else:
  print "Incorrect usage. Use: \"python normalize.py {NUMBER_OF_DAYS} {DIRECTORY} {OUTPUT_FILE}\""