from glob import glob
from pickle import load, dump
from random import choice, choices
from re import compile
from string import capwords
from sys import getsizeof

# for splitting while preserving newlines
WORD_SPLIT = compile(r'[ \t]+')
# for replacing 2 or more newlines with just one
MANY_LINES = compile(r'\n{2,}')
# for replacing non-letters with ''
# (keep * for censoring, apostrophes, hyphens, slashes)
NORMALIZE = compile(r"[^a-z0-9*'/-]+")
# for replacing ' \n' with '\n'
EXTRA_SPACE = compile(r' \n')


class MarkovChain:
    """A bi-gram Markov Chain with weighted possible states."""

    def __init__(self):
        self.tree = dict()

    @staticmethod
    def count_common_keys(chain1, chain2):
        """Return comparison between two keys.

        Returns a tuple with length of tree1, length of tree2,
        number of keys in common, and keys in common as a percent
        of the smaller tree"""

        count = 0
        for key in chain1.tree.keys():
            if key in chain2.tree:
                count += 1
        tree1 = len(chain1.tree)
        tree2 = len(chain2.tree)
        percent = count / min((tree1, tree2))

        return (tree1, tree2, count, percent)

    def train(self, text):
        """Train on provided text."""

        text = MANY_LINES.sub(repl='\n', string=text)
        # preserve newlines
        lines = text.splitlines(keepends=True)
        words = []
        for line in lines:
            words.extend(WORD_SPLIT.split(string=line))

        # move the newline from the end of one word
        # to the beginning of the next
        for i in range(len(words)-1):
            if words[i].endswith('\n'):
                words[i] = words[i].rstrip('\n')
                words[i+1] = '\n' + words[i+1]

        words.append(None)

        for i in range(len(words) - 2):
            key0 = NORMALIZE.sub(repl='', string=words[i].lower())
            key1 = NORMALIZE.sub(repl='', string=words[i+1].lower())
            key = (key0, key1)
            alt_key = (words[i], words[i+1])
            next_word = words[i + 2]

            if key not in self.tree:
                self.tree[key] = {'alt_keys': [],
                                  'next_words': [],
                                  'next_weights': []}

            if alt_key not in self.tree[key]['alt_keys']:
                self.tree[key]['alt_keys'].append(alt_key)

            try:
                next_idx = self.tree[key]['next_words'].index(next_word)
                self.tree[key]['next_weights'][next_idx] += 1
            except ValueError:
                self.tree[key]['next_words'].append(next_word)
                self.tree[key]['next_weights'].append(1)

    def train_on_file(self, filename, verbose=False):
        """Read file and pass string to train().

        Skips directories.
        """

        if verbose:
            print(f'Training file: "{filename}"')
        try:
            with open(filename, 'r') as f:
                self.train(f.read())
        except FileNotFoundError as fnf:
            print(fnf)
        except IsADirectoryError as iad:
            print(f'{iad} (SKIPPED)')

    def train_on_directory(self, path, recursive=False, verbose=False):
        """Loop over files in path and pass filenames to train_on_file()

        Path should end with ** to include files, e.g.: './training/**'
        """

        if verbose:
            print(f'Training directory: "{path}", recursive: {recursive}')
        for filename in glob(path, recursive=recursive):
            self.train_on_file(filename, verbose)

    def save_training(self, filename):
        """Save tree to binary file."""

        with open(filename, 'wb') as f:
            dump(self.tree, f)

    def load_training(self, filename):
        """Load tree from binary file."""

        with open(filename, 'rb') as f:
            self.tree = load(f)

    def get_largest_node(self):
        """Return node with the most children."""

        max_len = 0
        max_key = None

        for key, data in self.tree.items():
            child_len = len(data['next_words'])
            if child_len > max_len:
                max_len = child_len
                max_key = key

        return (max_key, max_len)

    def find_existing_keys(self, text):
        """Return a list of bi-grams in text that exist in the tree."""

        text = MANY_LINES.sub(repl='\n', string=text)
        lines = text.splitlines(keepends=True)
        words = []
        for line in lines:
            words.extend(WORD_SPLIT.split(string=line))
        existing = set()
        for i in range(len(words) - 1):
            key0 = NORMALIZE.sub(repl='', string=words[i].lower())
            key1 = NORMALIZE.sub(repl='', string=words[i+1].lower())
            key = (key0, key1)
            if key in self.tree:
                existing.add((key0, key1, len(self.tree[key]['next_words'])))
        existing = sorted(existing, key=lambda k: k[2], reverse=True)

        # return existing
        return [e[:2] for e in existing]

    def get_tree_memory(self):
        """Return string with size of tree in KB"""

        size = getsizeof(self.tree) / 1000
        return f'{size} KB'

    # @staticmethod
    # def is_capitalized(word):
    #     """Check if word begins with capital letter."""

    #     for letter in word:
    #         if letter.isalpha():
    #             if letter.isupper():
    #                 return True
    #             else:
    #                 return False
    #     # edge case: no letters in word
    #     return False

    # @staticmethod
    # def is_sentence_end(word):
    #     """Check if word is the end of a sentence"""

    #     for i in range(len(word) - 1, -1, -1):
    #         if not word[i].isalpha():
    #             if word[i] == '.':
    #                 return True
    #             elif word[i] == '!':
    #                 return True
    #             elif word[i] == '?':
    #                 return True
    #         else:
    #             return False
    #     # edge case: no letters or .!? in word
    #     return False

    # def get_capital_key(self):
    #     """Return a random key that starts with a capital letter."""

    #     key = choice(list(self.tree.keys()))
    #     while not MarkovChain.is_capitalized(key[0]):
    #         key = choice(list(self.tree.keys()))
    #     return key

    def generate_unlimited(self, key=None, newlines=True):
        """Generate text until reaching None, then return."""

        if key is None or key not in self.tree:
            key = choice(list(self.tree.keys()))

        alt_key = choice(self.tree[key]['alt_keys'])
        # capitalize and strip newline from first word no matter what
        words = [capwords(alt_key[0].lstrip('\n')), alt_key[1]]
        if not newlines:
            words[1] = words[1].lstrip('\n')

        next_word = choices(population=self.tree[key]['next_words'],
                            weights=self.tree[key]['next_weights'],
                            k=1)[0]

        while next_word is not None:
            if not newlines:
                next_word = next_word.lstrip()

            words.append(next_word)

            key = (key[1], NORMALIZE.sub(repl='', string=next_word.lower()))
            next_word = choices(population=self.tree[key]['next_words'],
                                weights=self.tree[key]['next_weights'],
                                k=1)[0]

        result = ' '.join(words)
        if not newlines:
            return result
        else:
            # get rid of the spaces in front of newlines from the join
            return EXTRA_SPACE.sub(repl='\n', string=result)

    def generate_sentences(self, sentences=1, key=None, newlines=True):
        """Generate and return text up to number of sentences."""

        if key is None or key not in self.tree:
            key = choice(list(self.tree.keys()))

        alt_key = choice(self.tree[key]['alt_keys'])
        # capitalize and strip newline from first word no matter what
        words = [capwords(alt_key[0].lstrip('\n')), alt_key[1]]
        if not newlines:
            words[1] = words[1].lstrip('\n')

        next_word = choices(population=self.tree[key]['next_words'],
                            weights=self.tree[key]['next_weights'],
                            k=1)[0]

        count = 0
        while next_word is not None and count < sentences:
            if not newlines:
                next_word = next_word.lstrip()

            words.append(next_word)

            if next_word.endswith('.') or next_word.endswith('!') or next_word.endswith('?'):
                count += 1

            key = (key[1], NORMALIZE.sub(repl='', string=next_word.lower()))
            next_word = choices(population=self.tree[key]['next_words'],
                                weights=self.tree[key]['next_weights'],
                                k=1)[0]

        result = ' '.join(words)
        if not newlines:
            return result
        else:
            # get rid of the spaces in front of newlines from the join
            return EXTRA_SPACE.sub(repl='\n', string=result)

    def generate_words(self, words=20, key=None, newlines=True):
        """Generate and return text up to number of words."""

        if key is None or key not in self.tree:
            key = choice(list(self.tree.keys()))

        alt_key = choice(self.tree[key]['alt_keys'])
        # capitalize and strip newline from first word no matter what
        words = [capwords(alt_key[0].lstrip('\n')), alt_key[1]]
        if not newlines:
            words[1] = words[1].lstrip('\n')

        next_word = choices(population=self.tree[key]['next_words'],
                            weights=self.tree[key]['next_weights'],
                            k=1)[0]

        count = 2
        while next_word is not None and count < words:
            if not newlines:
                next_word = next_word.lstrip()

            words.append(next_word)
            count += 1

            key = (key[1], NORMALIZE.sub(repl='', string=next_word.lower()))
            next_word = choices(population=self.tree[key]['next_words'],
                                weights=self.tree[key]['next_weights'],
                                k=1)[0]

        result = ' '.join(words)
        if not newlines:
            return result
        else:
            # get rid of the spaces in front of newlines from the join
            return EXTRA_SPACE.sub(repl='\n', string=result)

    def generate_characters(self, chars=280, key=None, newlines=True):
        """Generate and return text up to number of characters."""

        if key is None or key not in self.tree:
            key = choice(list(self.tree.keys()))

        alt_key = choice(self.tree[key]['alt_keys'])
        # capitalize and strip newline from first word no matter what
        words = [capwords(alt_key[0].lstrip('\n')), alt_key[1]]
        if not newlines:
            words[1] = words[1].lstrip('\n')

        # + 1 for space
        count = len(words[0]) + len(words[1]) + 1

        next_word = choices(population=self.tree[key]['next_words'],
                            weights=self.tree[key]['next_weights'],
                            k=1)[0]

        while next_word is not None:
            if not newlines:
                next_word = next_word.lstrip()

            next_len = len(next_word)
            if not newlines or (newlines and not next_word.startswith('\n')):
                # + 1 for space
                next_len += 1
            if count + next_len > chars:
                # print(f'count would be: {count + next_len}')
                break
            count += next_len

            words.append(next_word)

            key = (key[1], NORMALIZE.sub(repl='', string=next_word.lower()))
            next_word = choices(population=self.tree[key]['next_words'],
                                weights=self.tree[key]['next_weights'],
                                k=1)[0]

        result = ' '.join(words)
        if newlines:
            # remove the extra space in front of newlines
            result = EXTRA_SPACE.sub(repl='\n', string=result)

        # print(f'count: {count}')
        # print(f'len(result): {len(result)}')
        return result


# console testing
if __name__ == '__main__':
    path = './training/tses/**'
    print(f'path: "{path}"')
    save_file = './bin/tses.bin'
    print(f'save_file: "{save_file}"')

    chain = MarkovChain()

    chain.train_on_directory(path=path, recursive=True, verbose=False)
    chain.save_training(filename=save_file)
    # chain.load_training(filename=save_file)

    print(f'len(chain.tree): {len(chain.tree)}'
          f' ({chain.get_tree_memory()})')

    largest = chain.get_largest_node()
    print(f'largest node: {largest}')

    # ht = ' #MarkovChain'

    # print('\n\ngenerate_characters(num_chars=267) + ht:')
    # tweet = chain.generate_characters(num_chars=280 - len(ht),
    #                                   key=None,
    #                                   add_lines=False) + ht
    # print(tweet)
    # print(f'({len(tweet)} characters)')

    # print('\n\ngenerate_characters(num_chars=280):')
    # chars = chain.generate_characters(num_chars=280 ,
    #                                   key=None,
    #                                   add_lines=False)
    # print(chars)
    # print(f'({len(chars)} characters)')

    # print('\n\ngenerate_words(num_words=64):')
    # words = chain.generate_words(num_words=64,
    #                              key=None,
    #                              add_lines=True)
    # print(words)

    # print('\n\ngenerate_sentences(num_sen=3):')
    # sentences = chain.generate_sentences(num_sen=3,
    #                                      key=None,
    #                                      add_lines=True)
    # print(sentences)

    # print('\n\nchain.generate_unlimited():')
    # unlimited = chain.generate_unlimited(key=largest[0],
    #                                      add_lines=False)
    # print(unlimited)
