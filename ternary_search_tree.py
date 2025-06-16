class TSTNode:
    """Node class for Ternary Search Tree"""
    def __init__(self, char):
        self.char = char
        self.left = None    # Less than current character
        self.middle = None  # Equal to current character
        self.right = None   # Greater than current character
        self.is_end_of_string = False


class TernarySearchTree:
    """
    Ternary Search Tree implementation for string operations.
    """
    def __init__(self):
        self.root = None

    def insert(self, word):
        """
        Insert a word into the tree

        """
        if word:
            self.root = self._insert(self.root, word)

    def _insert(self, node, word):
        """Helper method for insertion"""
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
        """
        Return all strings stored in the tree
        """
        result = []
        buffer = [''] * 100  # Buffer for string building
        self._traverse(self.root, buffer, 0, result)
        return result

    def _traverse(self, node, buffer, depth, result):
        """Helper method for tree traversal"""
        if node is None:
            return

        self._traverse(node.left, buffer, depth, result)
        buffer[depth] = node.char
        if node.is_end_of_string:
            result.append("".join(buffer[:depth + 1]))
        self._traverse(node.middle, buffer, depth + 1, result)
        self._traverse(node.right, buffer, depth, result)

    def __len__(self):
        """
        Return the number of words in the tree
        """
        return self._count_words(self.root)

    def _count_words(self, node):
        """Helper method for counting words"""
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
        """
        Search for a word in the tree
        Args:
            word: String to search for
            exact: If True, only exact matches are returned
                  If False, prefix matches are allowed
        """
        if not word and not exact:
            return self.root is not None and len(self) > 0
        return self._search(self.root, word, exact)

    def _search(self, node, word, exact):
        """Helper method for searching"""
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

    def __str__(self):
        """Return string representation of the tree"""
        return f"TST containing {len(self)} words: {self.all_strings()}"