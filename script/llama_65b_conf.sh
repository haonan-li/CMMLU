#!/bin/bash
#SBATCH --job-name=llama_65b_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:4
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd ../src

# 0-shot
for i in {0..1}; do
python hf_causal_model.py \
    --model_name_or_path huggyllama/llama-65b \
    --save_dir ../results/LLaMA-65B-conf \
    --load_in_8bit \
    --with_conf \
    --num_few_shot $i
done
