#!/usr/bin/env python3

import subprocess
import sys

def getResults(filters):
	results = subprocess.run(['git', 'branch', '-r'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("  ")
	results = [result[0 : len(result) - 1] for result in results]

	filteredResults = results
	if len(filters) == 0:
		return results

	filteredResults = []
	for result in results:
		if result == '':
			continue
		matches_filter = True
		for filter in filters:
			matches_filter &= filter in result
		if matches_filter:
			filteredResults.append(result)

	return filteredResults

filters = ['']
if (len(sys.argv) > 1):
	filters = sys.argv[1:]

user_input = filters

results = []
while (user_input[0] == '' and len(results) != 1) or (len(user_input) != 1 and user_input[0] != "!q" and user_input[0] != "!Q" and (len(user_input[0]) < 1) or (len(user_input[0]) > 0 and user_input[0][-1] != "!")):
	results = getResults(user_input)

	if (len(results) == 0):
		print("-")

	for i in range(0, len(results)):
		print("%d\t%s" % (i, results[i]))

	user_input = input(">> ").split(" ")

if user_input[0] in ("q!", "Q!"):
	exit (0)

if user_input[0] == '':
	user_input[0] = "0!"

index = user_input[0][0 : -1]

branch = results[int(index)][7:]
subprocess.run(['git', 'checkout', branch], stdout=subprocess.PIPE)