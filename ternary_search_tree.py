#!/usr/bin/env python
# coding: utf-8

# A ternary search tree has nodes with the following attributes:
# * a character, can be `None`;
# * a Boolean flag that indicates whether the character represented
#   by this node has been the last in a string that was inserted in the
#   tree;
# * the "less-than" child;
# * the "equals" child and
# * the "larger-than" child.
# 
# The data structure should support the following operations:
# * string insert
# * string search
# * prefix string search
# * return the number of strings stored in the data structure
# * return all strings stored in the data structure
# 
# Also ensure that an instance of the data structure can be visualy represented, e.g., in aSCII format.

# Implementation

# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')

# The data structure has been implemented as a class.

#from ternary_search_tree import TernarySearchTree


class TSTNode:
	def __init__(self, char):
		self.char = char
		self.left = None
		self.middle = None
		self.right = None
		self.is_end_of_string = False


class TernarySearchTree:
	def __init__(self):
		self.root = None

	def insert(self, word):
		if word:
			self.root = self._insert(self.root, word)


	def _insert(self, node, word):
		if not node:
			node = TSTNode(word[0])
			
		if word[0] < node.char:
			node.left = self._insert(node.left, word)
		elif word[0] > node.char:
			node.right = self._insert(node.right, word)
		else:
			if len(word) > 1:
				node.middle = self._insert(node.middle, word[1:])
			else:
				node.is_end_of_string = True
		return node

	def all_strings(self):
		result = []
		buffer = [''] * 100
		self._traverse(self.root, buffer, 0, result)
		return result

	def _traverse(self, node, buffer, depth, result):
		if node is None:
			return

		self._traverse(node.left, buffer, depth, result)
		buffer[depth] = node.char
		if node.is_end_of_string:
			result.append("".join(buffer[:depth + 1]))
		self._traverse(node.middle, buffer, depth + 1, result)
		self._traverse(node.right, buffer, depth, result)


	def __len__(self):
		return self._count_words(self.root)

	def _count_words(self, node):
		if node is None:
			return 0

		count = 0
		if node.is_end_of_string:
			count += 1

		count += self._count_words(node.left)
		count += self._count_words(node.middle)
		count += self._count_words(node.right)
		return count

	def search(self, word, exact=False):
		if not word and not exact:
			return self.root is not None and len(self) > 0
		return self._search(self.root, word, exact)

	def _search(self, node, word, exact):
		if not node or not word:
			return False

		if word[0] < node.char:
			return self._search(node.left, word, exact)
		elif word[0] > node.char:
			return self._search(node.right, word, exact)
		else:
			if len(word) > 1:
				return self._search(node.middle, word[1:], exact)
			else:
				if exact:
					return node.is_end_of_string
				else:
					# If we're doing a prefix search, return True if this node exists
					# or if there are any words extending from here
					return True


# # Example usage

print('##############################################################')
print('Testing the Ternary Search Tree implementation with simple data.')
print('##############################################################\n')
# Create a new empty ternery search tree.
print('Create a new empty ternery search tree.\n')
tst = TernarySearchTree()

# Insert the string `'abc'` into the tree.
print('Insert the string \'abc\' into the tree.\n')
tst.insert('abc')

# Display the tree.
print('Display the tree.\n')
print(tst)

# Insert another string `'aqt'`.
print('Insert another string \'aqt\'.\n')
tst.insert('aqt')

print('Display the tree again.\n')
print(tst)

# The tree should now contain two strings.
print('The tree should now contain two strings.\n')
print('Tree length: ' + str(len(tst)))
print('Tree content: ' + str(tst.all_strings()))

# Search for the string `'ab'`, it should be found since it is a prefix of `'abc'`.
print('Search for the string \'ab\', it should be found since it is a prefix of \'abc\'.')
print('Result: ' + str(tst.search('ab')))

# The string `'ac'` should not be found.
print('The string \'ac\' should not be found.')
print('Result: ' + str(tst.search('ac')))

# The tree can also contain the empty string.
print('Insert an empty string.\n')
tst.insert('')

print('Display the tree again.\n')
print('Tree length: ' + str(len(tst)))
print(tst)
print('Tree content: ' + str(tst.all_strings()))

# Testing
print('###########################################################################')
print('Testing the Ternary Search Tree implementation with the provided sample data.')
print('###########################################################################\n')
# The file `data/search_trees/insert_words.txt` contains words that we can insert into a tree.
print('Create a new empty ternery search tree.')
tst = TernarySearchTree()
print('Insert words from the file `data/search_trees/insert_words.txt` into the tree.')
with open('data/search_trees/insert_words.txt') as file:
    words = [
        line.strip() for line in file
    ]

for word in words:
    tst.insert(word)
unique_words = set(words)
print(f'Inserted {len(unique_words)} unique words into the tree.')
# Verify the length of the data stucture.
print('Verify that the tree contains as many words. No error should be thrown.')
assert len(tst) == len(unique_words), \
       f'{len(tst)} in tree, expected {len(unique_words)}'


# Verify that all words that were inserted can be found.
print('Verify that all words that were inserted can be found.')
print('Inserted words: ' + str(unique_words))
print('Tree content: ' + str(tst.all_strings()))
print('Search for the word "bomb". It should be found.')
print('Result: ' + str(tst.search("bomb")))
print('Verify that all unique words are found in the tree. No error should be thrown.')
for word in unique_words:
    assert tst.search(word), f'{word} not found'


# Verify that all prefixes can be found.
print('Verify that all prefixes can be found. No error should be thrown.')
for word in unique_words:
    for i in range(len(word) - 1, 0, -1):
        prefix = word[:i]
        assert tst.search(prefix), f'{prefix} not found'


# Chack that when searching for a exact match, only the inserted words are found, and no prefixes.
print('Check that when searching for an exact match, only the inserted words are found, and no prefixes. No error should be thrown.')
for word in unique_words:
    for i in range(len(word), 0, -1):
        prefix = word[:i]
        if prefix not in unique_words:
            assert not tst.search(prefix, exact=True), \
                   f'{prefix} found'


# Check that the empty string is in the tree (since it is a prefix of any string).
print('Verify that the empty string is in the tree (since it is a prefix of any string). No error should be thrown.')
assert tst.search(''), 'empty string not found'


# Check that the empty string is not in the tree for an exact search.
print('Check that the empty string is not in the tree for an exact search. No error should be thrown.')
assert not tst.search('', exact=True), 'empty string found'


# Check that words in the file `data/search_trees/not_insert_words.txt` can not be found in the tree.
print('Check that words in the file `data/search_trees/not_insert_words.txt` can not be found in the tree. No error should be thrown.')
with open('data/search_trees/not_insert_words.txt') as file:
    for line in file:
        word = line.strip()
        assert not tst.search(word), f'{word} should not be found'


# Check that all strings are returned.
print('Check that all strings are returned.')
all_strings = tst.all_strings()
print('Number of all strings in the tree: ' + str(len(all_strings)))

assert len(all_strings) == len(unique_words), \
       f'{len(all_strings)} words, expected {len(unique_words)}'
assert sorted(all_strings) == sorted(unique_words), 'words do not match'
print('All strings match the inserted words. No error should be thrown.')
# If not output was generated, all tests have passed.
