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

## HPC Deployment Instructions

1. SSH into the HPC cluster:
```bash
ssh username@login.hpc.kuleuven.be
```

2. Create project directory on HPC:
```bash
mkdir -p ~/projects/TST-Project-2025
```

3. Copy files to HPC (from local machine):
```bash
scp -r ./* username@login.hpc.kuleuven.be:~/projects/TST-Project-2025/
```

4. Install required virtual environment,packages and activate:
```bash
cd ~/projects/TST-Project-2025

module purge
module load Python/3.13.1-GCCcore-14.2.0

python3 -m venv ~/venvs/benchmark_env
source ~/venvs/benchmark_env/bin/activate

pip install --upgrade pip
pip install matplotlib numpy pandas

```

5. Submit benchmark job:
```bash
dos2unix run_benchmark.slurm
sbatch run_benchmark.slurm
```

6. Monitor job status:
```bash
squeue -u username
```

7. Collect Results:
```bash
python collect_results.py benchmark_results
```

8. After completion, copy results back (from local machine):
```bash
scp -r username@login.hpc.kuleuven.be:~/projects/TST-Project-2025/benchmark_results.csv ./
```

9. Plot the results on matplotlib
```bash
python plot_results.py benchmark_results/benchmark_results.csv --output-dir ./analysis
```

Replace `username` with your actual HPC credentials and cluster address.


## Time & Space Complexity
Let:  
- **n** = number of strings inserted into the TST  
- **L** = average length of the strings


### Best Case
- **Insert/Search:** O(L) - It is when the tree is perfectly balanced
- **Space:** O(n × L) - optimal packing with no wasted nodes. Remains constant across all cases because TSTs don't create redundant nodes for shared prefixes

### Average Case  
- **Insert/Search:** O(L + log n) - It is the typical performance with some imbalance
- **Space:** O(n × L) - remains consistent. Remains constant across all cases because TSTs don't create redundant nodes for shared prefixes

### Worst Case
- **Insert/Search:** O(n × L) - This occurs when strings are inserted in sorted order, creating a completely unbalanced tree.
- **Space:** O(n × L) - same as average case. Remains constant across all cases because TSTs don't create redundant nodes for shared prefixes

**Insert** O(log n + L) average case per insertion
The data shows insert times growing roughly linearly as the number grows.
The O(log n) behavior observed is typical for real-world TST implementations, not a flaw in the implementation.

**Search:** O(log n + L) average case per search
The search time per element decreases as size increases
Search time per element may decrease as dataset size increases due to 
better cache locality and improved tree balance with more diverse string patterns


## Space Complexity
Each node in a TST stores one character and three pointers (left, middle and right).
The space required is proportional to the total number of characters across all strings.
It therfore has O(n × L) space complexity.