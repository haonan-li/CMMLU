#!/bin/bash
#SBATCH --job-name=gpt4
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH -q cpu-4

cd ../src

python gpt4.py \
    --save_dir ../results/GPT4 \
    --num_few_shot 0

python gpt4.py \
    --save_dir ../results/GPT4 \
    --num_few_shot 5

