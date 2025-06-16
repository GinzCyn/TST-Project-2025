import time
import random
import string
import matplotlib.pyplot as plt
import os
import argparse
from typing import List, Tuple
from ternary_search_tree import TernarySearchTree


def load_word_list(filename: str) -> List[str]:
    """Load words from file with error handling"""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Please check the file path or provide an alternative. Using random words instead.")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def generate_random_word(length: int) -> str:
    """Generate a random word of given length"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_test_data(num_words: int, word_length: int = 5, word_list: List[str] = None) -> List[str]:
    """Generate list of words - use provided list or generate random ones"""
    if word_list and len(word_list) >= num_words:
        return random.choices(word_list, k=num_words)
    else:
        return [generate_random_word(word_length) for _ in range(num_words)]

def measure_insert_performance(words: List[str]) -> Tuple[float, TernarySearchTree]:
    """Measure time taken to insert words"""
    try:
        tst = TernarySearchTree()
        start_time = time.time()
        for word in words:
            tst.insert(word)
        end_time = time.time()
        return end_time - start_time, tst
    except Exception as e:
        print(f"Error during insertion: {e}")
        return float('inf'), None

def measure_search_performance(tst: TernarySearchTree, words: List[str]) -> float:
    """Measure time taken to search words"""
    try:
        start_time = time.time()
        for word in words:
            tst.search(word, exact=True)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error during search: {e}")
        return -1

def plot_performance(sizes: List[int], insert_times: List[float], search_times: List[float], output_dir: str):
    """Create performance plots"""
    try:
        plt.figure(figsize=(12, 6))
        
        # Plot insertion times
        plt.subplot(1, 2, 1)
        plt.plot(sizes, insert_times, 'b-o')
        plt.title('Insertion Performance')
        plt.xlabel('Number of Words')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        
        # Plot search times
        plt.subplot(1, 2, 2)
        plt.plot(sizes, search_times, 'r-o')
        plt.title('Search Performance')
        plt.xlabel('Number of Words')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'performance_results.png')
        plt.savefig(plot_path)
        plt.close()
        print(f"Performance plot saved to {plot_path}")
    except Exception as e:
        print(f"Error creating plot: {e}")

def run_benchmark(size: int, output_dir: str, word_list: List[str] = None) -> Tuple[float, float]:
    """Run benchmark for specific size and save results"""
    try:
        words = generate_test_data(size, word_list=word_list)
        
        # Measure insert performance
        insert_time, tst = measure_insert_performance(words)
        
        # Measure search performance
        search_time = measure_search_performance(tst, words)
        
        # Save results
        results_file = os.path.join(output_dir, f"benchmark_size_{size}.txt")
        with open(results_file, 'w') as f:
            f.write(f"Size: {size}\n")
            f.write(f"Insert time: {insert_time:.6f}s\n")
            f.write(f"Search time: {search_time:.6f}s\n")
            f.write(f"Insert rate: {size/insert_time:.2f} words/sec\n")
            f.write(f"Search rate: {size/search_time:.2f} words/sec\n")
        
        print(f"Benchmark completed for size {size}")
        print(f"Insert time: {insert_time:.6f}s, Search time: {search_time:.6f}s")
        
        return insert_time, search_time
        
    except Exception as e:
        print(f"Error running benchmark: {e}")
        raise

def nanoseconds_to_milliseconds(nanoseconds: float) -> float:
    """Convert nanoseconds to milliseconds"""
    return nanoseconds / 1_000_000.0

def measure_performance_with_samples(sizes: List[int], word_list: List[str], nr_runs: int = 10) -> dict:
    """Measure performance across different sizes with multiple runs"""
    if len(word_list) < max(sizes):
        raise ValueError("Word list too small for requested sizes")
    
    # Create samples for each size
    samples = [random.sample(word_list, k=size) for size in sizes]
    
    # Sample for insertion testing (fixed size)
    insert_sample = random.sample(word_list, k=min(20, len(word_list)))
    
    # Store average times for each size
    times = {}
    
    for sample in samples:
        size = len(sample)
        times[size] = {'insert': 0.0, 'search': 0.0}
        
        for _ in range(nr_runs):
            # Test insertion
            tst = TernarySearchTree()
            for word in sample:
                tst.insert(word)
                
            # Measure insert performance
            start_time = time.time_ns()
            for word in insert_sample:
                tst.insert(word)
            end_time = time.time_ns()
            times[size]['insert'] += end_time - start_time
            
            # Measure search performance
            start_time = time.time_ns()
            for word in insert_sample:
                tst.search(word, exact=True)
            end_time = time.time_ns()
            times[size]['search'] += end_time - start_time
            
        # Calculate averages (convert to milliseconds)
        # Convert nanoseconds to milliseconds and average over the number of runs
        times[size]['insert'] = nanoseconds_to_milliseconds(times[size]['insert'] / nr_runs)
        # Convert nanoseconds to milliseconds and average over the number of runs
        times[size]['search'] = nanoseconds_to_milliseconds(times[size]['search'] / nr_runs)
    
    return times

def run_multiple_benchmarks(sizes: List[int], output_dir: str, word_list: List[str], nr_runs: int = 10):
    """Run benchmarks for multiple sizes with averaging"""
    try:
        try:
            times = measure_performance_with_samples(sizes, word_list, nr_runs)
        except ValueError as ve:
            print(f"Error: {ve}")
            return
        
        # Extract times for plotting
        insert_times = [times[size]['insert'] for size in sizes]
        search_times = [times[size]['search'] for size in sizes]
        
        # Save detailed results
        results_file = os.path.join(output_dir, "benchmark_results.txt")
        with open(results_file, 'w') as f:
            f.write(f"Benchmark Results (averaged over {nr_runs} runs)\n")
            f.write("=" * 50 + "\n\n")
            for size in sizes:
                f.write(f"Size: {size}\n")
                f.write(f"Insert time: {times[size]['insert']:.6f}ms\n")
                f.write(f"Search time: {times[size]['search']:.6f}ms\n")
                f.write("-" * 30 + "\n")
        
        # Create performance plot
        plot_performance(sizes, insert_times, search_times, output_dir)
        
    except Exception as e:
        print(f"Error in benchmarking: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Run TST performance benchmarks')
    parser.add_argument('--size', type=int, help='Number of words to test (single benchmark)')
    parser.add_argument('--sizes', type=int, nargs='+', help='Multiple sizes to test')
    parser.add_argument('--output-dir', type=str, required=True, help='Output directory for results')
    parser.add_argument('--word-file', type=str, default='data/search_trees/corncob_lowercase.txt', 
                       help='Path to word list file')
    parser.add_argument('--runs', type=int, default=10, help='Number of runs for averaging')
    
    args = parser.parse_args()
    
    if not args.size and not args.sizes:
        parser.error("Either --size or --sizes must be specified")
    
    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}")
        exit(1)
    
    # Load word list
    word_list = load_word_list(args.word_file)
    
    try:
        if args.size:
            # Single benchmark
            run_benchmark(args.size, args.output_dir, word_list)
        else:
            # Multiple benchmarks
            run_multiple_benchmarks(args.sizes, args.output_dir, word_list, args.runs)
            
    except Exception as e:
        print(f"Benchmark failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()