import os
import glob
import matplotlib.pyplot as plt
import re
import logging
import sys

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('hpc_tst_test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def collect_single_benchmark_results(results_dir):
    """Collect results from individual benchmark_size_*.txt files"""
    sizes = []
    insert_times = []
    search_times = []
    
    # Pattern to match benchmark result files
    pattern = os.path.join(results_dir, "benchmark_size_*.txt")
    files_found = glob.glob(pattern)
    
    logger.info(f"Found {len(files_found)} individual benchmark files")
    
    for filename in files_found:
        try:
            with open(filename, 'r') as f:
                content = f.read()
                
                # Extract data using regex
                size_match = re.search(r"Size: (\d+)", content)
                insert_match = re.search(r"Insert time: ([\d.]+)s", content)
                search_match = re.search(r"Search time: ([\d.]+)s", content)
                
                if not all([size_match, insert_match, search_match]):
                    logger.warning(f"Could not parse all data from {filename}")
                    continue
                
                size = int(size_match.group(1))
                insert_time = float(insert_match.group(1))
                search_time = float(search_match.group(1))
                
                sizes.append(size)
                insert_times.append(insert_time)
                search_times.append(search_time)
                
                logger.info(f"Parsed {filename}: size={size}, insert={insert_time}s, search={search_time}s")
                
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            continue
    
    return sorted(zip(sizes, insert_times, search_times))

def collect_multiple_benchmark_results(results_dir):
    """Collect results from benchmark_results.txt (multiple sizes file)"""
    results_file = os.path.join(results_dir, "benchmark_results.txt")
    
    if not os.path.exists(results_file):
        logger.info("No benchmark_results.txt found")
        return []
    
    logger.info(f"Processing {results_file}")
    
    sizes = []
    insert_times = []
    search_times = []
    
    try:
        with open(results_file, 'r') as f:
            content = f.read()
            
            # Split into sections for each size
            sections = re.split(r'-{20,}', content)
            
            for section in sections:
                # Look for tree size, insert time, and search time
                size_match = re.search(r"Tree Size: (\d+)", section)
                insert_match = re.search(r"Insert time: ([\d.]+)s", section)
                search_match = re.search(r"Search time: ([\d.]+)s", section)
                
                if all([size_match, insert_match, search_match]):
                    size = int(size_match.group(1))
                    insert_time = float(insert_match.group(1))
                    search_time = float(search_match.group(1))
                    
                    sizes.append(size)
                    insert_times.append(insert_time)
                    search_times.append(search_time)
                    
                    logger.info(f"Parsed section: size={size}, insert={insert_time}s, search={search_time}s")
        
        return sorted(zip(sizes, insert_times, search_times))
        
    except Exception as e:
        logger.error(f"Error processing {results_file}: {e}")
        return []

def collect_results(results_dir):
    """Collect results from all available benchmark files"""
    if not os.path.exists(results_dir):
        logger.error(f"Results directory does not exist: {results_dir}")
        return []
    
    logger.info(f"Collecting results from: {results_dir}")
    
    # Try multiple benchmark results first
    results = collect_multiple_benchmark_results(results_dir)
    
    # If no multiple results, try individual files
    if not results:
        results = collect_single_benchmark_results(results_dir)
    
    # If still no results, try both and combine
    if not results:
        logger.warning("No results found in either format")
        # List all files in directory for debugging
        all_files = os.listdir(results_dir)
        logger.info(f"Files in directory: {all_files}")
    
    logger.info(f"Total results collected: {len(results)}")
    return results

def plot_results(results, output_dir):
    """Create plots from collected results"""
    if not results:
        logger.error("No results to plot")
        return
    
    sizes, insert_times, search_times = zip(*results)
    
    logger.info(f"Plotting {len(results)} data points")
    logger.info(f"Size range: {min(sizes)} to {max(sizes)}")
    
    plt.figure(figsize=(12, 6))
    
    # Plot insertion times
    plt.subplot(1, 2, 1)
    plt.plot(sizes, insert_times, 'b-o', markersize=6, linewidth=2)
    plt.title('TST Insertion Performance (HPC)', fontsize=14)
    plt.xlabel('Number of Words', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Plot search times
    plt.subplot(1, 2, 2)
    plt.plot(sizes, search_times, 'r-o', markersize=6, linewidth=2)
    plt.title('TST Search Performance (HPC)', fontsize=14)
    plt.xlabel('Number of Words', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'performance_results.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"Plot saved to: {output_path}")
    
    # Also create a combined plot
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, insert_times, 'b-o', label='Insert', markersize=6, linewidth=2)
    plt.plot(sizes, search_times, 'r-o', label='Search', markersize=6, linewidth=2)
    plt.title('TST Performance Comparison (HPC)', fontsize=14)
    plt.xlabel('Number of Words', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    combined_path = os.path.join(output_dir, 'performance_comparison.png')
    plt.savefig(combined_path, dpi=300, bbox_inches='tight')
    logger.info(f"Combined plot saved to: {combined_path}")
    
    # Print summary statistics
    print("\n" + "="*50)
    print("PERFORMANCE SUMMARY")
    print("="*50)
    for size, insert_t, search_t in results:
        print(f"Size {size:6d}: Insert {insert_t:.6f}s, Search {search_t:.6f}s")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description='Plot TST benchmark results')
    parser.add_argument('results_dir', help='Directory containing benchmark results')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate results directory
    if not os.path.exists(args.results_dir):
        logger.error(f"Results directory does not exist: {args.results_dir}")
        sys.exit(1)
    
    # Collect and plot results
    results = collect_results(args.results_dir)
    
    if not results:
        logger.error("No valid benchmark results found")
        logger.info("Expected files:")
        logger.info("  - benchmark_results.txt (from --sizes option)")
        logger.info("  - benchmark_size_*.txt (from --size option)")
        sys.exit(1)
    
    plot_results(results, args.results_dir)
    logger.info("Plotting completed successfully")

if __name__ == "__main__":
    import argparse
    main()