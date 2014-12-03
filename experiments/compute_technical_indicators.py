# Usage: python compute_technical_indicators.py {DIRECTORY}

import numpy as np
import pandas as pd
import talib
import glob
import sys
from subprocess import call

if len(sys.argv) == 2:
  directory = sys.argv[1]
  new_directory = "%s_with_technicals" % directory

  # create new directory
  call(["rm", "-rf", new_directory])
  call(["mkdir", new_directory])

  # get all csv files in the give directory
  files = glob.glob("%s/*.csv" % directory)
  symbols = []
  i = 0

  # compute techincal indicators for all files
  for f in files:
    i += 1
    print "(%d/%d) - Computing techinicals for %s..." % (i, len(files), f[len(directory) + 1:])
    try:
      data = pd.read_csv(f)
      cols = {'open': np.array(data['Open'])[::-1], 'high': np.array(data['High'])[::-1], 'low': np.array(data['Low'])[::-1], 'close': np.array(data['Close'])[::-1], 'volume': np.array(data['Volume'], dtype=np.float64)[::-1]}
      data['50DayAvgVol'] = talib.SMA(cols['volume'], timeperiod=50)[::-1]
      data['30DaySMA'] = talib.SMA(cols['close'], timeperiod=30)[::-1]
      data['4WeekSMA'] = talib.SMA(cols['close'], timeperiod=20)[::-1]
      data['10WeekSMA'] = talib.SMA(cols['close'], timeperiod=50)[::-1]
      data['30WeekSMA'] = talib.SMA(cols['close'], timeperiod=150)[::-1]
      data['20.2UpperBB'], data['20.2MiddleBB'], data['20.2LowerBB'] = [bb[::-1] for bb in talib.BBANDS(cols['close'], 20, 2, 2)]
      data['12.26.9MACD'], data['12.26.9MACDSignal'], data['12.26.9MACDHist'] = [macd[::-1] for macd in talib.MACD(cols['close'], fastperiod=12, slowperiod=26, signalperiod=9)]
      data['RSI14'] = talib.RSI(cols['close'], timeperiod=14)[::-1]
      data['10.4STOC'], data['10.4.4STOC'] = [s[::-1] for s in talib.STOCH(cols['high'], cols['low'], cols['close'], fastk_period=10, slowk_period=4, slowk_matype=0, slowd_period=4, slowd_matype=0)]

      # write dataframe to new file
      data.to_csv(f.replace(directory, new_directory), sep=',', encoding='utf-8')
      symbols.append(f[len(directory) + 1:-4])
    except:
      print "ERROR: Unable to compute technicals for %s" % f[len(directory) + 1:]

  # write symbols to file
  f = open("%s/symbol_list.txt" % new_directory, "w")
  for s in symbols:
    f.write(s + "\n")
  f.close()
else:
  print "Incorrect usage. Use: \"python compute_technical_indicators.py {DIRECTORY}\""