"""
Parse a .blt file of ranked choice cast vote records.
Print counts of who wins between each pair of candidates
Thanks to ChatGPT for a starting point
"""

import sys

def index_with_default(list, key, default=None):
    try:
        return list.index(key)
    except:
        return default

def process_input(input_data):
    n = 4
    lines = input_data.strip().split("\n")
    lines = lines[1:]  # Skip the first line

    # Initialize a dictionary to store the count of pairs
    candidates = range(1, n+1)
    pair_counts = {(i, j): 0 for i in candidates for j in candidates if i != j}

    for line in lines:
        if line.strip() == '0':
            break

        numbers = [int(n) for n in line.split() if n.isdigit() and 1 <= int(n)]
        numbers = numbers[1:]
        indices = [None] + [index_with_default(numbers, c, n+2) for c in candidates]

        # go thru pairs and figure out if the first in the pair beat the other

        for first, second in pair_counts.keys():
            if indices[first] < indices[second]:
                pair_counts[(first, second)] += 1
            # If they're equal, neither...

    return pair_counts

# Example input
input_data = """
1 1 2
1 3 4
1 1
1 2
0
ignore me
"""

input_data = open('output.blt').read()
# input_data = sys.stdin.read()

# Process the input and print the results
pair_counts = process_input(input_data)
for pair, count in pair_counts.items():
    print(f"Pair {pair} appeared {count} times.")
