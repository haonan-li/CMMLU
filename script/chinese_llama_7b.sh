#!/bin/bash
#SBATCH --job-name=chinese_llama_7b_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:2
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd /l/users/haonan.li/mygit/CMMLU/src

for i in {0..5}; do
python chinese_llama_alpaca.py \
    --model_name_or_path decapoda-research/llama-7b-hf \
    --lora_weights ziqingyang/chinese-llama-plus-lora-7b \
    --save_dir ../results/Chinese-LLaMA-7B \
    --num_few_shot $i
done
