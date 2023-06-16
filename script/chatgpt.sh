#!/bin/bash
#SBATCH --job-name=chatgpt
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH -q cpu-4

cd /l/users/haonan.li/MISC/CMMLU/src

python chatgpt.py \
    --save_dir ../results/ChatGPT \
    --num_few_shot 0

python chatgpt.py \
    --save_dir ../results/ChatGPT \
    --num_few_shot 5

python chatgpt.py \
    --save_dir ../results/ChatGPT-cot \
    --cot \
    --num_few_shot 0
