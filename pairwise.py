"""
Print counts of who wins between each pair of candidates
"""

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
    # TODO: consider all valid numbers
    candidates = range(1, n+1)
    pair_counts = {(i, j): 0 for i in candidates for j in candidates if i != j}

    for line in lines:
        if line.strip() == '0':
            break

        numbers = [int(n) for n in line.split() if n.isdigit() and 1 <= int(n)]
        numbers = numbers[1:]
        indices = [None] + [index_with_default(numbers, c, n+2) for c in candidates]

        # go thru pairs and figure out which wins: lower index
        #  Get index of each number, then for each pair look up the two and compare
        # or go thru numbers and accumulate pairs with that number first, discarding matches with that number second

        for first, second in pair_counts.keys():
            if indices[first] < indices[second]:
                pair_counts[(first, second)] += 1
            # If they're equal, neither...

            #import pdb; pdb.set_trace()

    """
        if len(numbers) == 1:
            num = numbers[0]
            for other_num in range(1, 5):
                if num != other_num:
                    pair_counts[(num, other_num)] += 1
        else:
            for i in range(0, len(numbers), 2):
                pair = (numbers[i], numbers[i + 1] if i + 1 < len(numbers) else None)
                if pair[1] is not None:
                    pair_counts[pair] += 1
    """

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

import sys
input_data = open('output.blt').read()
# input_data = sys.stdin.read()

# Process the input and print the results
pair_counts = process_input(input_data)
for pair, count in pair_counts.items():
    print(f"Pair {pair} appeared {count} times.")
