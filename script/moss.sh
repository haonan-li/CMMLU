#!/bin/bash
#SBATCH --job-name=moss_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:2
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd ../src

for i in {0..5}; do
python moss.py \
    --model_name_or_path fnlp/moss-moon-003-base \
    --save_dir ../results/MOSS-SFT-16B \
    --num_few_shot $i
done
