# Usage: python normalize_volume.py {DIRECTORY}

import numpy as np
import pandas as pd
import talib
import glob
import sys
from subprocess import call

if len(sys.argv) == 2:
  directory = sys.argv[1]
  new_directory = "%s_normalized_volume" % directory

  # create new directory
  call(["rm", "-rf", new_directory])
  call(["mkdir", new_directory])

  # get all csv files in the give directory
  files = glob.glob("%s/*.csv" % directory)
  symbols = []
  i = 0

  # normalize volume
  for f in files:
    i += 1
    print "(%d/%d) - Normalizing volume for %s..." % (i, len(files), f[len(directory) + 1:])
    try:
      data = pd.read_csv(f)
      data = data.set_index('Date')
      cols = {'open': np.array(data['Open'])[::-1], 'high': np.array(data['High'])[::-1], 'low': np.array(data['Low'])[::-1], 'close': np.array(data['Close'])[::-1], 'volume': np.array(data['Volume'], dtype=np.float64)[::-1]}
      data['Volume'] = data['Volume'] / talib.SMA(cols['volume'], timeperiod=50)[::-1]

      # write dataframe to new file
      data.to_csv(f.replace(directory, new_directory), sep=',', encoding='utf-8')
      symbols.append(f[len(directory) + 1:-4])
    except:
      print "ERROR: Unable to normalize volume for %s" % f[len(directory) + 1:]

  # write symbols to file
  f = open("%s/symbol_list.txt" % new_directory, "w")
  for s in symbols:
    f.write(s + "\n")
  f.close()
else:
  print "Incorrect usage. Use: \"python normalize_volume.py {DIRECTORY}\""