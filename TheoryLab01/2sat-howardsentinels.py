#!/usr/bin/env python2.7
# 2sat-howardsentinels.py
# Lauren Tucker, Jacob Knutson
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
    return [probNum, maxLit, satVal, numVar, numClauses, L]
    
# Check if wff assignment is valid or not
def verify(v, assignment, stack):
    copyassignment = list(assignment)
    copystack = list(stack)
    numUnknown = 0
    clauses = list(v[5])
    i = 0
    track = 0
    wrong = False
    while len(clauses) > 0:
        if track > len(clauses):
            wrong = True
            break
        # Check each clause in list
        if i >= len(clauses): i = 0
        if i < 0: i = 0

        track = track + 1
        curClause = clauses[i]
        # Get values from current clause
        lit1 = int(curClause[0])
        value1 = int( assignment[abs(lit1)-1] )
        lit2 = int(curClause[1])
        value2 = int( assignment[abs(lit2)-1] )

        # If known literal has a negative, flip value
        if lit1 < 0:
            if value1 == 0:
                value1 = 1
            elif value1 == 1:
                value1 = 0
        if lit2 < 0:
            if value2 == 0:
                value2 = 1
            elif value2 == 1:
                value2 = 0

        if DEBUG: 
            print "Clause" + str(i) + "= ",
            print curClause 
            print "Lit1: " + str(lit1) + " has a value of " + str(value1)
            print "Lit2: " + str(lit2) + " has a value of " + str(value2)


        # Lit1 and Lit2 are undefined
     
        # Lit1 is defined as 1 or Lit2 is defined as 1
        if value1 == 1 or value2 == 1:
            track = 0
            clauses.pop(i)
            i = i - 1
            continue  # clause is already true, so go to next iteration
        
        # Lit1 is defined as 0 but Lit2 is not defined
        if value1 == 0 and value2 == 9:
            track = 0
            if DEBUG: print "Changing " + str(abs(lit2)) + " to ",
            if lit2 < 0:
                # if not of 2nd var, value = 0
                copystack.append((abs(lit2), 0))
                assignment[abs(lit2)-1] = 0
                if DEBUG: print "0"
            else:
                copystack.append((lit2, 1))
                assignment[lit2-1] = 1
                if DEBUG: print "1"
            clauses.pop(i)
            i = i - 1

        # Lit2 is defined as 0 but Lit1 is not defined
        if value1 == 9 and value2 == 0:
            track = 0
            if DEBUG: print "Changing " + str(abs(lit1)) + " to ",
            if lit1 < 0:
                # if not of 1st var, value = 0
                copystack.append((abs(lit1), 0))
                assignment[abs(lit1)-1] = 0
                if DEBUG: print "0"
            else:
                copystack.append((lit1, 1))
                assignment[lit1-1] = 1
                if DEBUG: print "1"
            clauses.pop(i)
            i = i - 1

        # Lit1 and Lit2 values are both defined as 0
        if value1 == 0 and value2 == 0:
            # Reset assignment variable
            for t in range(len(copystack)-1):
                q = copystack.pop()
                assignment[q[0]-1] = "9"
            return -1
        i = i + 1
    # If no other assumptions can be made, create new wff
    if wrong == True:
        v[5] = []
        v[5] = clauses
        x = stack.pop()
        # Add one variable to stack (variable, value, boolean of if othervaluetried)
        first = int(v[5][0][0])
        if first > 0:
            firstVal = 1
            v[6] = firstVal
            assignment[abs(first)-1] = firstVal
        else:
            firstVal = 0
            v[6] = firstVal
            assignment[abs(first)-1] = firstVal
        stack.append((abs(first),assignment[abs(first)-1]))
        return 0

    # If it made it out of the for loop, all clauses must be true 
    return 1

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
            if assignment[i] != '9':
                output += ',' + str(assignment[i])
            else:
                output += ',' + "-1"
    
    
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
reg = FILENAME + "-2sat.csv"
newF = open(reg, "w")
newF.close()

while True:
    # Get tuple that contains all the necessary variables from the wff
    v = readwff(f)

    # If false is returned, end of file is reached
    if v == False:
        break

    numWiffs += 1
    numVar = v[3]

    # Create initial assignment string
    assignment = list("9" * int(numVar))

    # Add one variable to stack (variable, value, boolean of if othervaluetried)
    stack = []
    first = int(v[5][0][0])
    if first > 0:
        firstVal = 1
        assignment[abs(first)-1] = firstVal
    else:
        firstVal = 0
        assignment[abs(first)-1] = firstVal
    v.append(firstVal)
    dt = time.time()
    if DEBUG:
        print assignment
        print "lit: " + str(abs(first)) + " value: " + str(assignment[abs(first)-1])
    stack.append((abs(first),assignment[abs(first)-1]))
    # Go through stack until empty
    while len(stack) > 0:

	#print "assignment: " + "".join(assignment)
        if DEBUG == True:
            print "STACK: "
            print stack
            print "\n"

        # Check if assignment is correct
        t = verify(v, assignment, stack)
        if t == 1:
            satVal = "S"
            break
        elif t == 0:
            satVal = "?"
        else:
            satVal = "U"

        if DEBUG == True: 
	    print satVal + " Assignment: ", 
            print assignment
            print
        
        # If unsatisfied, must flip last variable added to stack
        if t == -1:
            x = stack.pop()
            if x[1] != v[6]:
                satVal = "U"
                break
            #  If value was 0, flip to 1 and push to stack
            if x[1] == 0:
                stack.append((x[0], 1))
                assignment[x[0]-1] = "1"
            elif x[1] == 1:
                stack.append((x[0], 0))
                assignment[x[0]-1] = "0"   
        
        # If wff is partially solved
        if t == 0:
	    if DEBUG: print "PARTIALLY SOLVED"
            continue
        # If satisfied, break out because we are done
        if t == 1:
            satVal = "S"
            break

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
    if DEBUG: 
        print "END STACK: "
        print stack

# Final output line
output2 = FILENAME + ",howardsentinels," + str(numWiffs)
output2 += "," + str(numSat) + "," + str(numUnsat) + "," 
output2 += str(numWithAnswers) + "," + str(numCorrect)

newF = open(reg, 'a')
print >> newF, output2
newF.close()


f.close()
