import random
import math

class Card:
	def __init__(self, v, s):
		self.val = v
		self.source = s

def solve(cards, target, process=True):
	if process:
		for i in range(len(cards)):
			for j in range(i + 1, len(cards)):
				big_i = -1
				small_i = -1
				if cards[j].val >= cards[i].val and cards[j].val % cards[i].val == 0 and cards[i].val != 1:
					big_i = j
					small_i = i
				elif cards[i].val >= cards[j].val and cards[i].val % cards[j].val == 0 and cards[j].val != 1:
					big_i = i
					small_i = j
				if big_i != -1 and small_i != -1:
					temp = cards[small_i]
					cards[small_i] = Card(cards[big_i].val // cards[small_i].val, '({} / {})'.format(cards[big_i].val, cards[small_i].val))
					output = dfs(cards[:big_i] + cards[big_i + 1:], target)
					if output:
						return output
					cards[small_i] = temp

	output = dfs(cards, target)
	if not output:
		print("no solution")
	return output

def dfs(cards, target):
	global cheats
	if len(cards) == 0:
		return
	if len(cards) == 2:
		if cards[0].val + cards[1].val == target:
			return '{} + {} = {}'.format(cards[0].source, cards[1].source, target)
		if cards[0].val - cards[1].val == target:
			return '{} - {} = {}'.format(cards[0].source, cards[1].source, target)
		if cards[1].val - cards[0].val == target:
			return '{} - {} = {}'.format(cards[1].source, cards[0].source, target)
		if cards[0].val * cards[1].val == target:
			return '{} * {} = {}'.format(cards[0].source, cards[1].source, target)
		if cards[1].val != 0 and cards[0].val // cards[1].val == target and cards[0].val % cards[1].val == 0:
			return '{} / {} = {}'.format(cards[0].source, cards[1].source, target)
		if cards[0].val != 0 and cards[1].val // cards[0].val == target and cards[1].val % cards[0].val == 0:
			return '{} / {} = {}'.format(cards[1].source, cards[0].source, target)
	if len(cards) == 1:
		if cheats:
			if cards[0].val > 1:
				int_root = math.isqrt(cards[0].val)
				if int_root * int_root == cards[0].val:
					if int_root == target:
						if cards[0].source.startswith(')'):
							return 'sqrt{} = {}'.format(cards[0].source, target)
						else:
							return 'sqrt({}) = {}'.format(cards[0].source, target)
				if cards[0].val < 10 and cards[0].val != 2: # arbitrary limit of factorial, remove infinite loop of 2! = 2
					calculated_factorial = math.factorial(cards[0].val)
					if calculated_factorial == target:
						if cards[0].source.endswith(')') or temp.source.isnumeric():
							return '{}! = {}'.format(cards[0].source, target)
						else:
							return '({})! = {}'.format(cards[0].source, target)
		return # got to a wrong answer (not target)

	for i, c1 in enumerate(cards):
		for j, c2 in enumerate(cards):
			if i != j and i < len(cards) and j < len(cards):
				# addition
				temp = cards[i]
				cards[i] = Card(c1.val + c2.val, '({} + {})'.format(temp.source, c2.source))
				addition = dfs(cards[:j] + cards[j + 1:], target)
				if addition:
					return addition
				cards[i] = temp

				# subtraction 1
				if c1.val - c2.val >= 0:
					temp = cards[i]
					cards[i] = Card(c1.val - c2.val, '({} - {})'.format(temp.source, c2.source))
					sub1 = dfs(cards[:j] + cards[j + 1:], target)
					if sub1:
						return sub1
					cards[i] = temp
				# subtraction 2
				elif c2.val - c1.val >= 0:
					temp = cards[j]
					cards[j] = Card(c2.val - c1.val, '({} - {})'.format(temp.source, c1.source))
					sub2 = dfs(cards[:i] + cards[i + 1:], target)
					if sub2:
						return sub2
					cards[j] = c2
				
				# multiplication
				temp = cards[i]
				cards[i] = Card(c1.val * c2.val, '({} * {})'.format(temp.source, c2.source))
				multiplication = dfs(cards[:j] + cards[j + 1:], target)
				if multiplication:
					return multiplication
				cards[i] = temp

				# division 1
				if c2.val != 0 and c1.val % c2.val == 0 and c1.val >= c2.val:
					temp = cards[i]
					cards[i] = Card(c1.val // c2.val, '({} / {})'.format(temp.source, c2.source))
					div1 = dfs(cards[:j] + cards[j + 1:], target)
					if div1:
						return div1
					cards[i] = temp
				# division 2
				elif c1.val != 0 and c2.val % c1.val == 0 and c2.val >= c1.val:
					temp = cards[j]
					cards[j] = Card(c2.val // c1.val, '({} / {})'.format(temp.source, c1.source))
					div2 = dfs(cards[:i] + cards[i + 1:], target)
					if div2:
						return div2
					cards[j] = temp

	# this is where the fun begins
	# - anakin skywalker, ca. 19 bby
	if cheats:
		for i, c in enumerate(cards):
			if c.val > 1:
				int_root = math.isqrt(c.val)
				if int_root * int_root == c.val:
					temp = cards[i]
					if temp.source.startswith('('): # temp.source.endswith(')'):
						cards[i] = Card(int_root, 'sqrt{}'.format(temp.source))
					else:
						cards[i] = Card(int_root, 'sqrt({})'.format(temp.source))
					sqrt = dfs(cards, target)
					if sqrt:
						return sqrt
					cards[i] = temp

				if c.val < 10 and c.val != 2: # arbitrary limit of factorial, remove infinite loop of 2! = 2
					calculated_factorial = math.factorial(c.val)
					temp = cards[i]
					if temp.source.endswith(')') or temp.source.isnumeric():
						cards[i] = Card(calculated_factorial, '{}!'.format(temp.source))
					else:
						cards[i] = Card(calculated_factorial, '({})!'.format(temp.source))
					factorial = dfs(cards, target)
					if factorial:
						return factorial
					cards[i] = temp

target = 24
cheats = False
int_cards = random.sample(range(1, 11), counts=[4] * 10, k=4)
# int_cards = [9, 7, 9, 5] # check for cheat solution (sqrt((9 / 9) + (5)!) - 7)!
# int_cards = [8, 5, 10, 4] # check for more elegant solution (8 - (10 / 5)) * 4
# int_cards = [9, 8, 5, 3] # check general bugs
# int_cards = [7, 9, 1, 5] # check (7 - 1) * (9 - 5)
# int_cards = [3, 9, 8, 4] # check for replacement with () term
# int_cards = [5, 4, 8, 10] # check for replacement with () term
# int_cards = [10, 2, 6, 6] # check for started with (x / y)
# int_cards = [3, 4, 10, 3] # check for no solution (didn't find a starting point)
cards = [Card(n, str(n)) for n in int_cards]
print("cards:", int_cards)
solution = solve(cards, target, process=True)
if solution:
	print(solution)
else:
	print("trying with cheats")
	cheats = True
	solution = solve(cards, target, process=True)
	if solution:
		print(solution)
		# print("successful cheat")
	else:
		print("no solution even with cheats")
