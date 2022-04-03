"""Script for getting random magical effects and durations."""

import linecache
from random import SystemRandom
from re import compile

# regex for removing numbers from te beginning of lines
REG_NUM = compile(r'^-*\d+\s+')
SYS_RAND = SystemRandom()


def count_lines(filename):
	"""Return nuber of lines in a file."""
	
	count = 0
	with open(filename) as f:
		for _ in f:
			count += 1
	return count


# effects file
_effects = './magical_effects.txt'
# number of lines in effects file
_effects_len = count_lines(filename=_effects)

# durations file
_durations = './magical_durations.txt'
# number of lines in durations file
_durations_len = count_lines(filename=_durations)

# high weirdness file
_weirdness = './high_weirdness.txt'
# number of lines in weirdness file
_weirdness_len = count_lines(filename=_weirdness)


def get_line(filename, lines, add_lineno=False, prepend=None, append=None):
	"""Return a random line from filename."""

	lineno = SYS_RAND.randint(1,lines)
	line = linecache.getline(filename=filename, lineno=lineno)
	line = REG_NUM.sub(repl='', string=line)
	line = line.rstrip()
	
	if prepend is not None:
		line = prepend + line
	if add_lineno:
		line = f'({lineno}) {line}'
	if append is not None:
		line = line + append
	
	return line


def print_effect(add_lineno=False):
	"""Print a random line from the effects file."""
	
	effect = get_line(filename=_effects,
					  lines=_effects_len,
					  add_lineno=add_lineno)
	print(effect)


def print_duration(add_lineno=False):
	"""Print a random line from the durations file."""

	duration = get_line(filename=_durations,
						lines=_durations_len,
						add_lineno=add_lineno,
						prepend='Until ')
	print(duration)


def print_weirdness(add_lineno=False):
	"""Print a random line from the high weirdness file."""
	
	weirdness = get_line(filename=_weirdness,
						 lines=_weirdness_len,
						 add_lineno=add_lineno)
	print(weirdness)


def roll(num=1, sides=20, mod=0):
	"""Basic pseudo-random dice roller."""

	# could add number validation, but don't feel like it

	results = []
	for _ in range(num):
		results.append(SYS_RAND.randint(1, sides))
	total = sum(results) + mod
	return (total, results)


if __name__ == '__main__':
	"""Run as REPL."""

	selection = input('"e"=effect, "d"=duration, "w"=weirdness, "r"=roll, "q"=quit\ninput: ').lower()

	while selection != 'q':
		print()
		if selection == 'e':
			print_effect(add_lineno=True)

		if selection == 'w':
			print_weirdness(add_lineno=True)

		elif selection == 'd':
			print_duration(add_lineno=True)

		elif selection == 'r':
			num = int(input('Enter number of dice: '))
			sides = int(input('Enter number of sides: '))
			print('Result:', roll(num=num, sides=sides))

		selection = input('\n"e"=effect, "d"=duration, "w"=weirdness, "r"=roll, "q"=quit\ninput: ').lower()

