#!/bin/bash
#SBATCH --job-name=qwen
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:1
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd ../src

python qwen.py \
    --model_name_or_path Qwen/Qwen-7B \
    --save_dir ../results/Qwen-7B \
    --num_few_shot 0

python qwen.py \
    --model_name_or_path Qwen/Qwen-7B \
    --save_dir ../results/Qwen-7B \
    --num_few_shot 5

