#!/usr/bin/env python2.7

import time
import sys

# parse command line arguments for filename and binary argument
args = sys.argv[1:]
arg = args.pop(0)
FILENAME = arg
arg = args.pop(0)
if arg == '0':
  DEBUG = False
else:
  DEBUG = True

# reads in the next wff from the specified input file
def readwff(f):
  
    # Get first line of wff, store each value in a list
    line = f.readline().rstrip().split(" ")

    probNum = line[1]
    maxLit = line[2]
    satVal = line[3]

    line = f.readline().rstrip().split(" ")
    numVar = line[2]
    numClauses = line[3]

    # Iterate through clauses and store into list
    L = []
    for i in range(int(numClauses)):
	#0 is actually the delimeter but project document says to assume on 1 line
        line = f.readline().rstrip().split(",")
        # We want each literal of the clause but not the delimeter 0
        L.append(line[0:len(line)-1])
        
    # Return values in a tuple
    return (probNum, maxLit, satVal, numVar, numClauses, L)
    
# Generates next possible assignment recursively 
def genassignment(numVar, a):
    if (numVar < 1):
        yield str()
    else:
        for i in range(2):
            m = a[i]
            for p in genassignment(numVar-1, a):
                yield str(m+p)

f = open(FILENAME, "r")

# Get tuple that contains all the necessary variables from the wff
v = readwff(f)
numVar = v[3]

# Generate all possible assignment
genObject = genassignment(int(numVar), '01')


# Pop off one possible assignment
print next(genObject)


# Check if assignment is correct



# Create output line

