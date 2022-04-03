from re import compile
import markov_chain
from random import choice

# regex for removing numbers from te beginning of lines
REG_NUM = compile(r'^-?\d+\s+')

chain = markov_chain.MarkovChain()

with open('./magical_effects.txt') as f:
	lines = []
	for line in f:
		lines.append(REG_NUM.sub(repl='', string=line))
#		chain.train(text=REG_NUM.sub(repl='', string=line))
	chain.train(text=''.join(lines))
with open('./magical_durations.txt') as f:
	lines = []
	for line in f:
		lines.append(REG_NUM.sub(repl='', string=line))
#		chain.train(text=REG_NUM.sub(repl='', string=line))
	chain.train(text=''.join(lines))

#chain.save_training(filename='./magical_effects.bin')
#chain.load_training(filename='./magical_effects.bin')

#keys = sorted(chain.tree.keys(), key=lambda k: len(chain.tree[k]['next_words']), reverse=True)
#for i in range(0,50):
#	print(keys[i])

#TOP_KEYS = [('caster', 'is'), ('target', 'is'), ('the', 'caster'), ('caster', 'can'),
#			('someone', 'nearby'), ('the', 'target'), ('the', 'nearest'),
#			("target's", 'weapon'), ('target', 'can'), ('caster', 'must'), ('the', "caster's"),
#			('caster', "can't"), ('this', 'area'), ("target's", 'hands'), ("target's", 'feet'),
#			('the', 'ground'), ("target's", 'skin'), ("target's", 'clothes'), ('caster', 'wakes'),
#			("target's", 'head'), ('the', "target's"), ('her', 'target'), ('her', 'weapon'),
#			('target', 'has'), ('the', 'air'), ("target's", 'allies'), ('caster', 'has'),
#			("caster's", 'home'), ('target', "can't"), ("caster's", 'presence'), ("target's", 'limbs'),
#			('caster', 'speaks'), ('caster', 'feels'), ("caster's", 'arms'), ("target's", 'body'),
#			('caster', 'suffers'), ('caster', 'becomes')]
#CASTER_KEYS = [('caster', 'is'), ('the', 'caster'), ('caster', 'can'), ('caster', 'must'),
#			('the', "caster's"), ('caster', "can't"), ('caster', 'wakes'), ('caster', 'has'),
#			("caster's", 'home'), ("caster's", 'presence'), ('caster', 'speaks'), ('caster', 'feels'),
#			("caster's", 'arms'), ('caster', 'suffers'), ('caster', 'becomes')]

#keys = []
#for key in chain.tree.keys():
#	if key[0] == 'target' or key[0] == 'target\'s':
#	if key[0] == 'someone':
#	if key[0] == 'caster' or key[0] == 'caster\'s':
#		keys.append(key)

def generate_effect():
	"""Generate a new effect."""

#	key = choice(keys)
#	key = ('someone', 'nearby')
#	effect = chain.generate_sentences(sentences=1, key=key, newlines=False)
	effect = chain.generate_sentences(sentences=1, key=None, newlines=False)
	while 'caster' not in effect:
		print('.', end='')
		effect = chain.generate_sentences(sentences=1, key=None, newlines=False)
	print(effect)

