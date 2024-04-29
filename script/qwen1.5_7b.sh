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

python qwen1.5.py \
    --model_name_or_path /mnt/storage/qwen/Qwen1.5-7B \
    --save_dir ../results/Qwen1.5-7B \
    --num_few_shot 0

python qwen1.5.py \
    --model_name_or_path /mnt/storage/qwen/Qwen1.5-7B \
    --save_dir ../results/Qwen1.5-7B \
    --num_few_shot 5

