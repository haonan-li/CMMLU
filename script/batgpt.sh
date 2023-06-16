#!/bin/bash
#SBATCH --job-name=batgpt
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH -q cpu-4

cd /l/users/haonan.li/MISC/CMMLU/src

# Slow, only test 0, 5

python batgpt.py \
    --save_dir ../results/BatGPT-15B \
    --num_few_shot 0

python batgpt.py \
    --save_dir ../results/BatGPT-15B \
    --num_few_shot 5

python batgpt.py \
    --save_dir ../results/BatGPT-15B-cot \
    --cot \
    --num_few_shot 0
