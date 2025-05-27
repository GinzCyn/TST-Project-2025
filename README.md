# Ternary Search Tree Implementation

A Python implementation of a Ternary Search Tree (TST) data structure. TSTs are efficient for storing and retrieving strings, combining the time efficiency of tries with the space efficiency of binary search trees.

## Features

- String insertion
- Exact string search
- Prefix search
- String enumeration
- Word count functionality

## Usage

```python
# Create a new TST
tst = TernarySearchTree()

# Insert words
tst.insert("cat")
tst.insert("cats")
tst.insert("bug")

# Search for words
print(tst.search("cat", exact=True))  # True
print(tst.search("ca", exact=False))  # True (prefix search)

# Get all strings
print(tst.all_strings())  # ['bug', 'cat', 'cats']

# Get total word count
print(len(tst))  # 3
```

## Implementation Details

The implementation uses two main classes:

1. `TSTNode`: Represents a node in the tree with:
   - Character value
   - Left, middle, and right child pointers
   - End-of-string marker

2. `TernarySearchTree`: Main class implementing:
   - String insertion
   - Search operations (exact and prefix)
   - String traversal
   - Word counting

## Time Complexity

- Insertion: O(L) where L is the length of the string
- Search: O(L) for both exact and prefix search
- Space Complexity: O(n) where n is the total number of characters in all strings

## License

This project is open source and available under the MIT License.
