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
def readwff(listoflines):
  d = listoflines.rsplit(" ")
  c = d.pop(0)
  ProbNum = d.pop(0)
  while (c != 'c'):
  	parse until find another c

  return tuple of output values
     

f = open(FILENAME, "r").readlines()

f = readwff(f, 1)
print f
