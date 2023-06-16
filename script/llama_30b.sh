#!/bin/bash
#SBATCH --job-name=llama_30b_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:4
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd /l/users/haonan.li/MISC/CMMLU/src

for i in {0..5}; do
python gpt_model.py \
    --model_name_or_path decapoda-research/llama-30b-hf \
    --save_dir ../results/LLaMA-30B \
    --num_few_shot $i
done
