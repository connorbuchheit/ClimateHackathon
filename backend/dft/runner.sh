#!/bin/bash

# Configuration
INPUT_DIR="/path/to/INPUT_DIR"   # Path to your input directory
STEADY_STATE_JOB_COUNT=50       # Max jobs to run concurrently
USER_EMAIL="your_email@example.com" # Email for SLURM notifications

# Function to check the job status
check_status() {
    if [ -f "$1/IN_PROGRESS" ]; then
        return 1  # Job is in progress
    elif [ -f "$1/ERRORED_OUT" ]; then
        return 2  # Job errored out
    elif [ -f "$1/COMPLETED" ]; then
        return 3  # Job completed
    else
        return 0  # Job not yet submitted
    fi
}

# Get current job count
CURRENT_JOB_COUNT=$(squeue -u $USER | grep -c "R")  # Count running jobs

# Calculate how many jobs to submit
JOBS_TO_SUBMIT=$((STEADY_STATE_JOB_COUNT - CURRENT_JOB_COUNT))
echo "Current running jobs: $CURRENT_JOB_COUNT. Submitting $JOBS_TO_SUBMIT jobs."

# Loop over each directory in INPUT_DIR
for dir in "$INPUT_DIR"/*; do
    # Skip if we've reached the steady-state job count
    if [ "$JOBS_TO_SUBMIT" -le 0 ]; then
        break
    fi

    # Check job status
    check_status "$dir"
    STATUS=$?

    if [ $STATUS -eq 0 ]; then
        # Job not yet submitted. Submit it.
        echo "Submitting job for $dir"
        sbatch --mail-user=$USER_EMAIL --mail-type=END,FAIL --output="$dir/output.log" "$dir/submit.sh"
        touch "$dir/IN_PROGRESS"
        JOBS_TO_SUBMIT=$((JOBS_TO_SUBMIT - 1))
    elif [ $STATUS -eq 1 ]; then
        echo "Job for $dir is in progress."
    elif [ $STATUS -eq 2 ]; then
        echo "Job for $dir has errored out."
    elif [ $STATUS -eq 3 ]; then
        echo "Job for $dir is completed."
    fi
done
