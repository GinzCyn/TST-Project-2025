"""
collect_results.py - Collect TST benchmark results with correct format parsing
"""

import os
import glob
import re
import pandas as pd
from pathlib import Path

def collect_results(results_dir):
    """Collect results from all benchmark files"""
    results = []
    
    # Pattern to match benchmark result files
    pattern = os.path.join(results_dir, "benchmark_size_*.txt")
    files = glob.glob(pattern)
    
    if not files:
        print(f"No benchmark files found in {results_dir}")
        print(f"Looking for pattern: benchmark_size_*.txt")
        
        # Debug: show what files are actually there
        print(f"\nFiles in directory:")
        try:
            all_files = os.listdir(results_dir)
            for f in sorted(all_files)[:10]:  # Show first 10 files
                print(f"  {f}")
            if len(all_files) > 10:
                print(f"  ... and {len(all_files) - 10} more files")
        except:
            print("  Could not list directory contents")
        
        return []
    
    print(f"Found {len(files)} benchmark files")
    
    for filename in sorted(files):
        try:
            with open(filename, 'r') as f:
                content = f.read()
                
                # Extract metrics - your format
                size_match = re.search(r"Size: (\d+)", content)
                insert_time_match = re.search(r"Insert time: ([\d.]+)s", content)
                search_time_match = re.search(r"Search time: ([\d.]+)s", content)
                
                # Also try to extract the provided rates (optional)
                insert_rate_match = re.search(r"Insert rate: ([\d.]+) words/sec", content)
                search_rate_match = re.search(r"Search rate: ([\d.]+) words/sec", content)
                
                if not all([size_match, insert_time_match, search_time_match]):
                    print(f"Warning: Could not extract all metrics from {filename}")
                    print(f"  Content preview: {content[:200]}...")
                    continue
                
                size = int(size_match.group(1))
                insert_time = float(insert_time_match.group(1))
                search_time = float(search_time_match.group(1))
                
                result = {
                    'size': size,
                    'insert_time': insert_time,
                    'search_time': search_time,
                    'filename': os.path.basename(filename)
                }
                
                # Add provided rates if available
                if insert_rate_match:
                    result['provided_insert_rate'] = float(insert_rate_match.group(1))
                if search_rate_match:
                    result['provided_search_rate'] = float(search_rate_match.group(1))
                
                results.append(result)
                print(f"✓ {os.path.basename(filename)}: size={size}, insert={insert_time:.4f}s, search={search_time:.6f}s")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    return results

def save_csv(results, output_dir):
    """Save results to CSV for further analysis"""
    if not results:
        print("No results to save")
        return None
    
    df = pd.DataFrame(results)
    
    # Sort by size
    df = df.sort_values('size')
    
    # Calculate our own rates for verification
    df['calculated_insert_rate'] = df['size'] / df['insert_time']
    df['calculated_search_rate'] = 1000 / df['search_time']  # Assuming 1000 searches
    
    # If we have provided rates, compare them
    if 'provided_insert_rate' in df.columns:
        print("\nRate Comparison (Provided vs Calculated):")
        comparison = df[['size', 'provided_insert_rate', 'calculated_insert_rate']].copy()
        comparison['insert_rate_diff'] = comparison['provided_insert_rate'] - comparison['calculated_insert_rate']
        print(comparison.to_string(index=False))
    
    # Reorder columns for better readability
    base_cols = ['size', 'insert_time', 'search_time']
    rate_cols = [col for col in df.columns if 'rate' in col.lower()]
    other_cols = [col for col in df.columns if col not in base_cols and col not in rate_cols]
    
    df = df[base_cols + rate_cols + other_cols]
    
    csv_path = os.path.join(output_dir, 'benchmark_results.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nResults saved to {csv_path}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    numeric_cols = ['size', 'insert_time', 'search_time'] + [col for col in df.columns if 'rate' in col.lower()]
    summary_df = df[numeric_cols]
    print(summary_df.describe())
    
    # Show all results in a clean format
    print(f"\nAll Results:")
    display_cols = ['size', 'insert_time', 'search_time']
    if 'provided_insert_rate' in df.columns:
        display_cols.extend(['provided_insert_rate', 'provided_search_rate'])
    print(df[display_cols].to_string(index=False))
    
    return csv_path

def check_completeness(results_dir, expected_sizes=None):
    """Check if all expected benchmark sizes are present"""
    if expected_sizes is None:
        expected_sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    
    pattern = os.path.join(results_dir, "benchmark_size_*.txt")
    files = glob.glob(pattern)
    
    found_sizes = []
    for filename in files:
        match = re.search(r"benchmark_size_(\d+)\.txt", filename)
        if match:
            found_sizes.append(int(match.group(1)))
    
    found_sizes = sorted(found_sizes)
    missing = set(expected_sizes) - set(found_sizes)
    
    print(f"Expected sizes: {expected_sizes}")
    print(f"Found sizes: {found_sizes}")
    if missing:
        print(f"Missing sizes: {sorted(missing)}")
        return False
    else:
        print("✅ All expected sizes found!")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Collect TST benchmark data to CSV')
    parser.add_argument('results_dir', nargs='?', default='./results',
                       help='Directory containing benchmark results')
    parser.add_argument('--check-only', action='store_true', 
                       help='Only check completeness, don\'t process data')
    parser.add_argument('--expected-sizes', nargs='+', type=int,
                       help='List of expected benchmark sizes')
    args = parser.parse_args()
    
    # Ensure results directory exists
    if not os.path.exists(args.results_dir):
        print(f"Error: Results directory {args.results_dir} does not exist")
        exit(1)
    
    # Check completeness
    complete = check_completeness(args.results_dir, args.expected_sizes)
    
    if args.check_only:
        exit(0 if complete else 1)
    
    # Collect and save results
    results = collect_results(args.results_dir)
    
    if results:
        csv_path = save_csv(results, args.results_dir)
        print(f"\nSuccessfully processed {len(results)} benchmark results!")
        print(f"Data saved to: {csv_path}")
        print(f"Ready for plotting! Copy the CSV to your local machine and run:")
        print(f"    python plot_results.py {csv_path}")
    else:
        print("No valid benchmark results found")
        exit(1)