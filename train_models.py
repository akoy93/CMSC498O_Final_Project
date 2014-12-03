# Usage: python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {OPEN_INDEX} {CLOSE_INDEX} {NUM_DATA_POINTS_PER_DAY} {TRAINING_FILE_NAME}

# We're training a model to determine if a stock will close above its open on the next day.
# We're given the stock's data for a variable window and its opening price on the last day.

import numpy as np
import sys
# import pickle
import sklearn.linear_model as lm
from sklearn import cross_validation

def tied_rank(x):
    """
    This function is by Ben Hamner and taken from https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/auc.py

    Computes the tied rank of elements in x.

    This function computes the tied rank of elements in x.

    Parameters
    ----------
    x : list of numbers, numpy array

    Returns
    -------
    score : list of numbers
            The tied rank f each element in x

    """
    sorted_x = sorted(zip(x,range(len(x))))
    r = [0 for k in x]
    cur_val = sorted_x[0][0]
    last_rank = 0
    for i in range(len(sorted_x)):
        if cur_val != sorted_x[i][0]:
            cur_val = sorted_x[i][0]
            for j in range(last_rank, i): 
                r[sorted_x[j][1]] = float(last_rank+1+i)/2.0
            last_rank = i
        if i==len(sorted_x)-1:
            for j in range(last_rank, i+1): 
                r[sorted_x[j][1]] = float(last_rank+i+2)/2.0
    return r

def auc(actual, posterior):
    """
    This function is by Ben Hamner and taken from https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/auc.py
    
    Computes the area under the receiver-operater characteristic (AUC)

    This function computes the AUC error metric for binary classification.

    Parameters
    ----------
    actual : list of binary numbers, numpy array
             The ground truth value
    posterior : same type as actual
                Defines a ranking on the binary numbers, from most likely to
                be positive to least likely to be positive.

    Returns
    -------
    score : double
            The mean squared error between actual and posterior

    """
    r = tied_rank(posterior)
    num_positive = len([0 for x in actual if x==1])
    num_negative = len(actual)-num_positive
    sum_positive = sum([r[i] for i in range(len(r)) if actual[i]==1])
    auc = ((sum_positive - num_positive*(num_positive+1)/2.0) /
           (num_negative*num_positive))
    sys.stdout.write('.')
    return auc

def auc_scorer(estimator, X, y):
    predicted = estimator.predict_proba(X)[:,1]
    return auc(y, predicted)

if len(sys.argv) != 6:
  print "Incorrect usage. Use: \"python train_models.py {NUMBER_OF_DAYS_IN_WINDOW} {OPEN_INDEX} {CLOSE_INDEX} {NUM_DATA_POINTS_PER_DAY} {TRAINING_FILE_NAME}\""
  sys.exit()

num_days_in_window = int(sys.argv[1])
open_index = int(sys.argv[2])
close_index = int(sys.argv[3])
points_per_day = int(sys.argv[4])
training_file = sys.argv[5]

# load training data
training = np.genfromtxt(training_file, delimiter=",")

# for now, only look at open and close columns
points_in_window = num_days_in_window * points_per_day
columns = set(range(open_index, points_in_window - points_per_day + 1, points_per_day)) | set(range(close_index, points_in_window - points_per_day + 1, points_per_day))
columns = list(sorted(columns))

# normalize data and compute outcome
X = np.array([p / p[0] for p in training[:, columns]])
y = (training[:, points_in_window - points_per_day + close_index] > training[:, points_in_window - points_per_day + open_index]) + 0

# test ridge model
C = np.linspace(500, 5000, num = 10)
models = [lm.LogisticRegression(penalty = "l2", C = c) for c in C]

print "calculating cv scores"
cv_scores = [0] * len(models)
for i, model in enumerate(models):
    cv_scores[i] = np.mean(cross_validation.cross_val_score(model, X, y, cv=5, scoring = auc_scorer))
    print " (%d/%d) C = %f: CV = %f" % (i + 1, len(C), C[i], cv_scores[i])
