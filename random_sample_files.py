# Selects a random sample of prediction files from a directory
# and copies them to an output directory
# Creates a file 'sample_symbols.txt' that contains the copied symbols
# Run as: ./random_sample_files {INPUT_FOLDER} {OUTPUT_FOLDER}

import sys
import shutil
import os
import glob
import codecs
from random import randrange

input_directory = sys.argv[1]
output_folder = sys.argv[2]
limit = int(sys.argv[3])

os.chdir(input_directory)
files = glob.glob("*.csv")

# create a file to store symbols for this file
file = codecs.open(output_folder + '/sample_symbols.txt','w','utf-8')
file.write("symbol\n")
if limit <= len(files):
	symbols = []
	for i in range(limit):
		index = randrange(len(files))
		print(files[index])
		symbols.append(files[index][:-4])
		shutil.copy(files[index], output_folder)

	file.write("\n".join(symbols))

file.close()


