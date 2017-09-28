#!/usr/bin/env python2.7
# backtrack-howardsentinels.py
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
    return (probNum, maxLit, satVal, numVar, numClauses, L)
    
# Check if wff assignment is valid or not
def verify(v, assignment):
    numUnknown = 0
    clauses = v[5]
    
    # Check each clause in list
    for i in range(len(clauses)):

        # Keeps track if clause is satisfied(-1), unsatisfied(=lenofclause), 
        # or unknown(<lenofclause)
        track = 0
       
        curClause = clauses[i]
        # Iterate through each clause and look for a 1 (True)
        for x in range(len(curClause)):
            lit = int(curClause[x])
            value = int( assignment[abs(lit)-1] )
            if DEBUG: print "Lit: " + str(lit) + " has a value of " + str(value)
            # If known literal has a negative, flip value
            if lit < 0:
                if value == 0:
                    value = 1
                elif value == 1:
                    value = 0

            # If value is 1, clause is satisfied, break
            if value == 1:
                track = -1
                break
            # If value is 0, literal is not satisfied, add 1 to track var
            if value == 0:
                track += 1
 
        # If track == lenofclause, then each literal is 0, i.e. unsatisfied
        if track == len(curClause):
            if DEBUG: print "Clause " + str(i) + " is unsatisfied"
            return -1
        # If track isnt -1, the clause must be unknown
        elif track >= 0 and track < len(curClause):
            if DEBUG: print "Clause " + str(i) + " is unknown"
            return 0

    # If it made it out of the for loop, all clauses must be true 
    return 1

def output(v, satVal, exTime, assignment):
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
    newFile = open('output-backtrack.csv', 'a')
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


f = open(FILENAME, "r")
newF = open("output-backtrack.csv", "w")
newF.close()

while True:
    # Get tuple that contains all the necessary variables from the wff
    v = readwff(f)
    
    # If false is returned, end of file is reached
    if v == False:
        break

    numVar = v[3]

    # Create initial assignment string
    assignment = list("9" * int(numVar))
    assignment[0] = "0"

    # Add one variable to stack (variable, value), value always goes 0 -> 1
    stack = []
    dt = time.time()
    stack.append((1,0))
    
    # Go through stack until empty
    while len(stack) > 0:

	#print "assignment: " + "".join(assignment)
        if DEBUG == True:
            print "STACK: "
            print stack
            print "\n"

        # Check if assignment is correct
        t = verify(v, "".join(assignment))
        if t == 1:
            satVal = "S"
            break
        elif t == 0:
            satVal = "?"
        else:
            satVal = "U"

        if DEBUG == True: print satVal + " " + "".join(assignment)
        
        # If unsatisfied, must flip last variable added to stack
        if t == -1:
            changed = False
            while changed == False:
                x = stack.pop()
                # If value was 0, flip to 1 and push to stack
                if x[1] == 0:
                    stack.append((x[0], 1))
                    assignment[x[0]-1] = "1"
                    changed = True
                elif x[1] == 1:
                    assignment[x[0]-1] = "9"
                if len(stack) == 0:
                    break
        
        # If unknown, another variable must be added to the stack
        if t == 0:
            num = len(stack)
            # values go from 0 -> 1
            stack.append((num+1, 0))
            assignment[num] = "0"

        # If satisfied, break out because we are done
        if t == 1:
            break

    # End the execution time
    dt = time.time() - dt
    dt = 1E6*dt

    # Create output for wff
    output(v, satVal, round(dt,2), assignment)
    if DEBUG: 
        print "END STACK: "
        print stack
    #print "FINISHED: #" + v[0] + satVal + v[2] + " " + "".join(assignment)
f.close()

# Create output line
