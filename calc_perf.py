from performance.PrecAccF1 import findmetrics
from performance.processExpected import addExpected
from performance.processTruth import processRaw
from performance.thresholdComparison import threshold
import os

if os.path.exists('./performance/expectedList1.json') == False:
    processRaw()
if os.path.exists('./performance/Actual/0.json') == False:
    threshold()
if os.path.exists('./performance/Expected/0.json') == False:
    addExpected()

findmetrics()