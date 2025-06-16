import time
import random
import string
import matplotlib.pyplot as plt
import os
import argparse
import sys
from typing import List, Tuple
import logging

try:
    from ternary_search_tree import TernarySearchTree
except ImportError:
    print("Error: ternary_search_tree module not found")
    sys.exit(1)

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('tst_test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_word_list(filename: str) -> List[str]:
    """Load words from file with error handling"""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.info(f"Warning: {filename} not found, will use random words")
        return []
    except Exception as e:
        logger.info(f"Error reading {filename}: {e}")
        return []

def generate_random_word(length: int) -> str:
    """Generate a random word of given length"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_test_data(num_words: int, word_length: int = 5, word_list: List[str] = None) -> List[str]:
    """Generate list of words - use provided list or generate random ones"""
    if word_list and len(word_list) >= num_words:
        return random.sample(word_list, num_words)
    else:
        return [generate_random_word(word_length) for _ in range(num_words)]

def measure_insert_performance(words: List[str]) -> Tuple[float, TernarySearchTree]:
    """Measure time taken to insert words into empty TST"""
    try:
        tst = TernarySearchTree()
        start_time = time.time()
        for word in words:
            tst.insert(word)
        end_time = time.time()
        return end_time - start_time, tst
    except Exception as e:
        logger.error(f"Error during insertion: {e}")
        raise

def measure_search_performance(tst: TernarySearchTree, words: List[str]) -> float:
    """Measure time taken to search words in TST"""
    try:
        start_time = time.time()
        for word in words:
            tst.search(word, exact=True)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise

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
        
        logger.info(f"Benchmark completed for size {size}")
        logger.info(f"Insert time: {insert_time:.6f}s, Search time: {search_time:.6f}s")
        
        return insert_time, search_time
        
    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        raise

def measure_performance_with_samples(sizes: List[int], word_list: List[str], nr_runs: int = 10) -> dict:
    """
    Measure performance across different sizes with multiple runs.
    
    For each size:
    - Creates a TST with 'size' number of words
    - Measures insertion time for a fixed set of test words into empty TSTs
    - Measures search time for the same test words in the populated TST
    
    This provides consistent comparison across different tree sizes.
    """
    logger.info(f"Starting performance measurement for sizes: {sizes}")
    
    if len(word_list) < max(sizes) + 100:  # Extra buffer for test operations
        raise ValueError("Word list too small for requested sizes")
    
    # Create samples for each size (for populating TSTs)
    logger.info("Creating word samples for each size...")
    samples = {}
    for size in sizes:
        samples[size] = random.sample(word_list, k=size)
        logger.info(f"Created sample of {len(samples[size])} words for size {size}")
    
    # Fixed sample for testing insertion/search (separate from population data)
    used_words = set()
    for sample in samples.values():
        used_words.update(sample)
    
    available_words = [w for w in word_list if w not in used_words]
    if len(available_words) < 50:
        logger.warning(f"Only {len(available_words)} words available for testing, using 20 instead")
        test_sample = random.sample(available_words, k=min(20, len(available_words)))
    else:
        test_sample = random.sample(available_words, k=50)
    
    logger.info(f"Created test sample of {len(test_sample)} words")
    
    # Store average times for each size
    times = {}
    
    for size in sizes:
        logger.info(f"Benchmarking size {size}...")
        times[size] = {'insert': 0.0, 'search': 0.0}
        
        for run in range(nr_runs):
            if run % 5 == 0:  # Log progress every 5 runs
                logger.info(f"  Run {run + 1}/{nr_runs} for size {size}")
            
            # Create TST populated with 'size' words
            populated_tst = TernarySearchTree()
            for word in samples[size]:
                populated_tst.insert(word)
            
            # Measure insertion performance on empty TST
            empty_tst = TernarySearchTree()
            start_time = time.time()
            for word in test_sample:
                empty_tst.insert(word)
            end_time = time.time()
            times[size]['insert'] += end_time - start_time
            
            # Measure search performance on populated TST
            # First insert test words so they can be found
            for word in test_sample:
                populated_tst.insert(word)
            
            start_time = time.time()
            for word in test_sample:
                result = populated_tst.search(word, exact=True)
            end_time = time.time()
            times[size]['search'] += end_time - start_time
        
        # Calculate averages
        times[size]['insert'] /= nr_runs
        times[size]['search'] /= nr_runs
        
        logger.info(f"Completed size {size}: insert={times[size]['insert']:.6f}s, search={times[size]['search']:.6f}s")
    
    logger.info("Performance measurement completed for all sizes")
    return times

def run_multiple_benchmarks(sizes: List[int], output_dir: str, word_list: List[str], nr_runs: int = 10):
    """Run benchmarks for multiple sizes with averaging"""
    try:
        logger.info(f"Starting benchmarks for sizes: {sizes}")
        logger.info(f"Word list size: {len(word_list) if word_list else 0}")
        logger.info(f"Number of runs: {nr_runs}")
        
        # Validate word list size
        if not word_list:
            logger.error("No word list available for benchmarking")
            raise ValueError("Word list is empty")
        
        if len(word_list) < max(sizes) + 100:
            logger.error(f"Word list too small. Need at least {max(sizes) + 100} words, have {len(word_list)}")
            raise ValueError("Word list too small for requested sizes")
        
        logger.info("Starting performance measurement...")
        times = measure_performance_with_samples(sizes, word_list, nr_runs)
        logger.info("Performance measurement completed")
        
        
        # Save detailed results
        results_file = os.path.join(output_dir, "benchmark_results.txt")
        logger.info(f"Writing results to: {results_file}")
        
        with open(results_file, 'w') as f:
            f.write(f"Benchmark Results (averaged over {nr_runs} runs)\n")
            f.write("=" * 50 + "\n\n")
            f.write("Note: Insert times measured on empty TSTs\n")
            f.write("      Search times measured on TSTs with specified number of words\n\n")
            for size in sizes:
                f.write(f"Tree Size: {size} words\n")
                f.write(f"Insert time: {times[size]['insert']:.6f}s\n")
                f.write(f"Search time: {times[size]['search']:.6f}s\n")
                f.write(f"Insert rate: {50/times[size]['insert']:.2f} words/sec\n")
                f.write(f"Search rate: {50/times[size]['search']:.2f} words/sec\n")
                f.write("-" * 30 + "\n")
        
        logger.info("Multiple benchmarks completed successfully")
        logger.info(f"Results saved to: {results_file}")
        
    except Exception as e:
        logger.error(f"Error in benchmarking: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Run TST performance benchmarks')
    parser.add_argument('--size', type=int, help='Number of words to test (single benchmark)')
    parser.add_argument('--sizes', type=int, nargs='+', help='Multiple sizes to test')
    parser.add_argument('--output-dir', type=str, default='benchmark_results', help='Output directory for results')
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
        logger.error(f"Error creating output directory: {e}")
        sys.exit(1)
    
    # Load word list
    word_list = load_word_list(args.word_file)
    
    try:
        if args.size:
            # Single benchmark
            if not word_list:
                logger.warning("No word list available, using random words")
            run_benchmark(args.size, args.output_dir, word_list)
        else:
            # Multiple benchmarks
            run_multiple_benchmarks(args.sizes, args.output_dir, word_list, args.runs)
            
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()