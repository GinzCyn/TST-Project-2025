# Ternary Search Tree Implementation

A Python implementation of a Ternary Search Tree (TST) data structure.

## Features

- String insertion
- Exact string search

## Usage

```python
# Create a new TST
tst = TernarySearchTree()

# Insert words
tst.insert("cat")
tst.insert("cats")
tst.insert("bug")
tst.insert("up")

# Search for words
print(tst.search("cat", exact=True))  # True
print(tst.search("ca", exact=False))  # True (prefix search)

# Get all strings
print(tst.all_strings())  # ['bug', 'cat', 'cats', 'up']

# Get total word count
print(len(tst))  # 4
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

## Space Complexity

