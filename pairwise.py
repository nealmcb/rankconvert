def process_input(input_data):
    lines = input_data.strip().split("\n")
    lines = lines[1:]  # Skip the first line

    # Initialize a dictionary to store the count of pairs
    pair_counts = {(i, j): 0 for i in range(1, 5) for j in range(1, 5) if i != j}

    for line in lines:
        if line.strip() == '0':
            break

        line = line[2:]  # Remove first two characters
        numbers = [int(n) for n in line.split() if n.isdigit() and 1 <= int(n) <= 4]

        # If there's only one number in the line, consider it as a pair with each other number
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

    return pair_counts

# Example input
input_data = """
XX1 2
XX3 4
XX1
XX2
0
"""

import sys
input_data = sys.stdin.read()

# Process the input and print the results
pair_counts = process_input(input_data)
for pair, count in pair_counts.items():
    print(f"Pair {pair} appeared {count} times.")
