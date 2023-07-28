#!/bin/bash
#SBATCH --job-name=bactrian_llama_30b_eval
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

for i in {0..5}; do
python hf_causal_model.py \
    --model_name_or_path decapoda-research/llama-30b-hf \
    --lora_weights haonan-li/bactrian-x10-llama-30b-lora \
    --load_in_8bit \
    --save_dir ../results/Bactrian-LLaMA-30B \
    --max_length 1024 \
    --num_few_shot $i
done
