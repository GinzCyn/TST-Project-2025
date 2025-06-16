#!/bin/bash
#SBATCH --job-name=tst_benchmark
#SBATCH --output=benchmark_%A_%a.out
#SBATCH --error=benchmark_%A_%a.err
#SBATCH --array=0-5
#SBATCH --time=02:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1
#SBATCH --clusters=genius
#SBATCH --account=lp_h_ds_students

cd $SLURM_SUBMIT_DIR

# Load Python module available on your cluster
module purge
module load Python/3.13.1-GCCcore-14.2.0

# Activate existing virtual environment (do NOT create it here!)
source ~/venvs/benchmark_env/bin/activate

# Create results directory
RESULTS_DIR="benchmark_results_${SLURM_ARRAY_JOB_ID}"
mkdir -p $RESULTS_DIR

# Define sizes to test
SIZES=(100 500 1000 5000 10000 50000)
SIZE=${SIZES[$SLURM_ARRAY_TASK_ID]}

# Run benchmark
python performance_test.py --size $SIZE --output-dir $RESULTS_DIR