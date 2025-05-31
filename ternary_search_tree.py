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