##  CS 121 Assignment 1 Part A
##  Ha Quang Tran
##  53409673

import re
import sys
from collections import defaultdict

## Exceptions Raised for Each Method of Part A

class no_file(Exception):
	pass

class no_tokens(Exception):
	pass

class no_map(Exception):
	pass

class invalid_arg(Exception):
	pass

class A1_A():

	def __init__(self, file):
		self.file_name = file
		self.tokens = []
		self.t_count = defaultdict(int)

## Opening file is O(1).
## read and split are both O(n), but occur only once.
## regex is O(len(string)), but since the pattern is so simple,
## I would argue that findall is near O(1).
## Adding to an internal token list is O(1).
## Therefore, Tokenize is O(n) due to the main for loop iterating through n words.
	
	def tokenize(self):
        	try:
			with open(self.file_name) as file:
				for word in file.read().split():
					m = re.findall('(\w+)', word)
					self.tokens += m
		except:
			raise no_file("File \"{}\" not found".format(self.file_name))
		else:
			return self.tokens
		finally:
			pass

## Assert is O(1).
## Main for loop is O(n).
## Lower and adding/indexing default dict is O(1).
## Therefore, computing Word Frequency is O(n).

	def computeWordFrequencies(self):
		try:
			assert(len(self.tokens) != 0)
			for word in self.tokens:
				lo_word = word.lower()
				self.t_count[lo_word] += 1
		except:
			raise no_tokens("You are trying to compute the Word Frequency on a Token List that is Empty.")
		else:
			return self.t_count
		finally:
			pass

## Assert is O(1) each.
## For loop is O(n),
## Sorting is O(n log n) in Python.
## Print statement is O(1).
## Sorting dominates the method.
## Therefore O(n log n)

	def Print(self):
		try:
			assert(bool(self.t_count) == True)
			assert(len(self.tokens) != 0)

			for key in sorted(self.t_count.items(), key = lambda k: (-k[1],k[0])):
				print("{}: {}".format(key[0], key[1]))
		except:
			raise no_map("You are attempting to print the Word Frequency of an Empty Token List or Map")
        
## Main Function        
if __name__ == "__main__":
	if (len(sys.argv) > 2):
		raise invalid_arg("There can only be 1 argument text file.")
	Test = A1_A(sys.argv[1])
	Test.tokenize()
	Test.computeWordFrequencies()
	Test.Print()
    
    
