#!/bin/bash
#SBATCH --job-name=bactrian_llama_13b_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:1
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd /l/users/haonan.li/mygit/CMMLU/src

for i in {0..5}; do
python gpt_model.py \
    --model_name_or_path decapoda-research/llama-13b-hf \
    --lora_weights MBZUAI/bactrian-x-llama-13b-lora \
    --load_in_8bit \
    --save_dir ../results/Bactrian-LLaMA-13B \
    --max_length 768 \
    --num_few_shot $i
done
