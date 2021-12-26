def solve(puzzle):
	# preset rows with nums
	rows = [set() for i in range(len(puzzle))]
	for i in range(len(puzzle)):
		for j in range(len(puzzle[0])):
			if puzzle[i][j] != '*':
				rows[i].add(puzzle[i][j])

	# preset cols with nums
	cols = [set() for i in range(len(puzzle[0]))]
	for i in range(len(puzzle)):
		for j in range(len(puzzle[0])):
			if puzzle[i][j] != '*':
				cols[j].add(puzzle[i][j])

	# preset squares with nums
	square = {}
	for start_i in range(3): # sqrt of len(puzzle) lol, was range(0, len(puzzle), 3)
		for start_j in range(3):
			square[(start_i, start_j)] = set()
			for i in range(start_i * 3, start_i * 3 + 3):
				for j in range(start_j * 3, start_j * 3 + 3):
					if puzzle[i][j] != '*':
						square[(start_i, start_j)].add(puzzle[i][j])

	attempt = dfs(puzzle, 0, 0, rows, cols, square)
	if not attempt:
		print("failed to find a solution")
	return attempt

def dfs(puzzle, r, c, rows, cols, square):
	if c == len(puzzle[0]):
		r += 1
		c = 0
	if r == len(puzzle):
		return puzzle
	if puzzle[r][c] != '*':
		return dfs(puzzle, r, c + 1, rows, cols, square)

	for digit in '123456789':
		if digit in rows[r] or digit in cols[c] or digit in square[(r // 3, c // 3)]:
			# cannot place digit in there
			continue
		# assign and dfs
		puzzle[r][c] = digit
		rows[r].add(digit)
		cols[c].add(digit)
		square[(r // 3, c // 3)].add(digit)
		attempt = dfs(puzzle, r, c + 1, rows, cols, square)
		if attempt:
			return attempt
		# reset
		puzzle[r][c] = '*'
		rows[r].remove(digit)
		cols[c].remove(digit)
		square[(r // 3, c // 3)].remove(digit)

arr = ["61*******", "**3*****2", "*4*61***3", "***9*35**", "**1******", "****879**", "*29**48**", "*7*851***", "**6*****5"]
puzzle = []
for l in arr:
	puzzle.append([x for x in l])

print(puzzle)
print(solve(puzzle))

