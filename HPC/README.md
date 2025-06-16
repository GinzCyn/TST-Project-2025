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

6. Run the benchmark:
```bash
python performance_test.py --sizes 1000 5000 10000 --output-dir benchmark_results --word-file data/search_trees/corncob_lowercase.txt --runs 5
```

Deactivate:
```bash
deactivate
```

7. Monitor job status:
```bash
squeue -u username
```

Collect Results:
```bash
source ~/venvs/benchmark_env/bin/activate

python performance_test.py --size 1000 --output-dir benchmark_results
python performance_test.py --size 5000 --output-dir benchmark_results
python performance_test.py --size 10000 --output-dir benchmark_results
python collect_results.py benchmark_results
```

8. After completion, copy results back (from local machine):
```bash
python performance_test.py --size 1000 --output-dir benchmark_results
python performance_test.py --size 5000 --output-dir benchmark_results
python performance_test.py --size 10000 --output-dir benchmark_results

python collect_results.py benchmark_results

scp -r username@login.hpc.kuleuven.be:~/projects/TST-Project-2025/benchmark_results.csv ./
```

9. Plot the results on matplotlib
```bash
python plot_results.py benchmark_results/benchmark_results.csv --output-dir ./analysis
```

Replace `username` with your actual HPC credentials and cluster address.


## Time Complexity

## Space Complexity