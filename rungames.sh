#!/bin/bash
#SBATCH -n 10 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 0-00:05 # Runtime in D-HH:MM
#SBATCH -p serial_requeue # Partition to submit to
#SBATCH --mem=100 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o hostname_%j.out # File to which STDOUT will be written
#SBATCH -e hostname_%j.err # File to which STDERR will be written

module load python
python game.py

hostname