#!/usr/bin/env python2.7
# brute-howardsentinels.py
# Lauren Tucker
# Jacob Knutson
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

    # Check if at end of file
    if len(line) == 1:
        return False

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

def output(v, satVal, exTime, assignment, reg):
    counter = 0
    for i in range(len(v[5])):
        counter += len(v[5][i])	# adds number of literals in each clause
    # compare satVal to actaul S/U value in problem
    if v[2] != 'S' and v[2] != 'U':
        correctness = 0
    elif v[2] == satVal:
        correctness = 1
    else: 
        correctness = -1
    
    output = v[0] + ',' + v[3] + ',' + v[4] + ',' + v[1] + ','
    output += str(counter) + ',' + satVal + ',' + str(correctness) + ','
    output += str(exTime)
    if satVal == "S":
        for i in range(len(assignment)):
            output += ',' + assignment[i]
    
    # print output
    newFile = open(reg, 'a')
    print >> newFile, output
    newFile.close()

#####MAIN#####

# parse command line arguments for filename and binary argument
args = sys.argv[1:]
arg = args.pop(0)
FILENAME = arg
arg = args.pop(0)
if arg == '0':
  DEBUG = False
else:
  DEBUG = True

numWiffs = 0
numSat = 0
numUnsat = 0
numWithAnswers = 0
numCorrect = 0
f = open(FILENAME, "r")
FILENAME = FILENAME[:len(FILENAME)-4]
reg = FILENAME + "-brute.csv"
newF = open(reg, 'w')
newF.close()


while True:
    # Get tuple that contains all the necessary variables from the wff
    v = readwff(f)
    
    # If false is returned, end of file is reached
    if v == False:
        break

    numVar = v[3]
    numWiffs += 1
    # Create generator object of all possible assignment
    genObject = genassignment(int(numVar), '01')

    # Loop through all possible assignments
    for i in xrange(2**int(numVar)):

        # Start execution time
        if i == 0:
            dt = time.time()
        # Pop off one possible assignment
        assignment = next(genObject)
    
        # Check if assignment is correct
        t = verify(v, assignment)
        if t == True:
            satVal = "S"
            break
        else:
            satVal = "U"

    # End the execution time
    dt = time.time() - dt
    dt = 1E6*dt

    # Create output for wff
    if v[2] == "S" or v[2] == "U":
        numWithAnswers += 1
    if satVal == "U":
        numUnsat += 1
        if v[2] == "U":
            numCorrect += 1
    elif satVal == "S":
        numSat += 1
        if v[2] == "S":
            numCorrect += 1
    output(v, satVal, round(dt,2), assignment, reg)

# Final output line
output2 = FILENAME + ",howardsentinels," + str(numWiffs)
output2 += "," + str(numSat) + "," + str(numUnsat) + ","
output2 += str(numWithAnswers) + "," + str(numCorrect)

newF = open(reg, 'a')
print >> newF, output2
newF.close()

f.close()

