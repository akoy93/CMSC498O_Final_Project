CMSC498O_Final_Project
======================

CMSC498O Final Project - Predicting Directional Movement of Stock Prices

## Gathering Data

### Web Scraping Yahoo! Finance
+ Create a file with a list of stock symbols you wish to retrieve (one symbol per line - see symbols.txt)
+ Run "ruby get\_stocks.rb {SYMBOL\_LIST\_FILE\_NAME} {NUMBER\_OF\_DAYS\_TO\_RETRIEVE}"
	+ **SYMBOL\_LIST\_FILE\_NAME** - the filename of the symbols list you created (e.g. symbols.txt).
	+ **NUMBER\_OF\_DAYS\_TO\_RETRIEVE** - the number of days of stock data to scrape.

## Preparing Data

###Computing Technical Indicators
+ python compute\_technical\_indicators.py {DIRECTORY}
	+ **DIRECTORY** - the name of the directory that contains all of the raw stock data for each individual stock

###Normalizing and Aggregating Stock Data
We can produce an output file in which each row will contain a specifed number of days' worth of data for an individual stock. A stock's data will be represented as a comma-separated string of (Open1, High1, Low1, Close1, Volume1, Open2, High2, Low2, Close2, Volume2, ...). The data reads in chronological order from left to right.
+ python normalize.py {NUMBER\_OF\_DAYS} {DIRECTORY} {OUTPUT\_FILE}
	+ **NUMBER\_OF\_DAYS** - the number of days to pull from our raw stock data
	+ **DIRECTORY** - the name of the directory that contains all of the raw stock data for each individual stock
	+ **OUTPUT\_FILE** - the name of our output file

###Generating Training and Testing Sets
We can pull random samples from our normalized and aggregated data to use as training and testing sets for our models.
+ python sample.py {NUM\_TRAINING} {NUM\_TESTING} {INPUT_FILE}
	+ **NUM\_TRAINING** - The number of stock we want to use for our training set.
	+ **NUM\_TESTING** - The number of stocks we want to use for our testing set.