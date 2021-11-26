## CS 121 Assignment 1 Part B
## Ha Quang Tran
## 53409673

import sys
import re
from collections import defaultdict
from PartA import no_file, no_tokens, no_map, invalid_arg, A1_A

## Creating the 2 "A1_A" objects would take O(1) time.
## Tokenizing both objects take O(n).
## Computing the Word Frequencies would take O(n) time as mentioned in PartA.py
## Obtaining keys of a dictionary is O(1) constant time.
## Creating a set of the dictionary keys is O(len(dict)).
## Intersecting the 2 set is O(len(a) * len(b)) in worse case, but O(min(len(a), len(b)) average case
## Overall: O(M + N) because tokenizing 2 different inputs dominates the program.

if __name__ == "__main__":
	if (len(sys.argv) > 3 or len(sys.argv) <= 2):
		raise invalid_arg("You must enter only 2 text file arguments")
	D1 = A1_A(sys.argv[1])
	D2 = A1_A(sys.argv[2])
	D1.tokenize()
	D2.tokenize()
	Token1 = set(D1.computeWordFrequencies().keys())
	Token2 = set(D2.computeWordFrequencies().keys())
	same = Token1 & Token2
	for x in same:
		print(x)
	print(len(same))
