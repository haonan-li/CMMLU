#!/bin/bash
#SBATCH --job-name=llama3
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

python llama3.py \
    --model_name_or_path meta-llama/Meta-Llama-3.1-8B-Instruct \
    --save_dir ../results/Llama-3.1-8B-Instruct\
    --num_few_shot 0

python llama3.py \
    --model_name_or_path meta-llama/Meta-Llama-3.1-8B-Instruct \
    --save_dir ../results/Llama-3.1-8B-Instruct \
    --num_few_shot 5

