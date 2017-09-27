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

# Check if wff assignment is valid or not
def verify(v, assignment):
    clauses = v[5]
    
    # Check each clause in list
    for i in range(len(clauses)):

        # boolean to keep track of if 1 is found        
        findOne = False

        # Iterate through each clause and look for a 1 (True)
        for x in range(len(clauses[i])):
            lit = int(clauses[i][x])
            value = int( assignment[abs(lit)-1] )
            
            # If literal has a negative, flip value
            if lit < 0:
                if value == 0:
                    value = 1
                else:
                    value = 0

            # If value is 1, break
            if value == 1:
                findOne = True
                break
 
        # If clause finds no 1, then clause is false, not valid
        if findOne == False:
            return False

    # If it made it out of the for loop, all clauses must be true
    return True

def output(v, satVal, exTime, assignment):
    counter = 0
    for i in range(len(v[5]):
        counter += len(v[5][i])	# adds number of literals in each clause
    # compare satVal to actaul S/U value in problem
    if v[2] ~= 'S' and v[2] ~= 'U':
        correctness = 0
    elif v[2] == satVal:
        correctness = 1
    else 
        correctness = -1
    outputFile = open('output.csv', 'w+')
    output = v[0] + ',' + v[3] + ',' + v[4] + ',' + v[1] + ','
    output += str(counter) + ',' + satVal + ',' + correctness + ','
    output += str(exTime)
    for i in range(len(assignment))
        output += ',' + assignment[i]

#MAIN

# parse command line arguments for filename and binary argument
args = sys.argv[1:]
arg = args.pop(0)
FILENAME = arg
arg = args.pop(0)
if arg == '0':
  DEBUG = False
else:
  DEBUG = True


f = open(FILENAME, "r")

# Get tuple that contains all the necessary variables from the wff
v = readwff(f)
numVar = v[3]

# Generate all possible assignment
genObject = genassignment(int(numVar), '01')


# Loop through all possible assignments
for i in xrange(2**int(numVar)):

    # Pop off one possible assignment
    assignment = next(genObject)
    
    # Check if assignment is correct
    t = verify(v, assignment)
    if t == True:
        print assignment + " S"
        break

f.close()

# Create output line
