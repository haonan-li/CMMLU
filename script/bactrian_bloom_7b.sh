#!/bin/bash
#SBATCH --job-name=bactrian_bloom_7b_eval
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

for i in {0..5}; do
python hf_causal_model.py \
    --model_name_or_path bigscience/bloom-7b1 \
    --lora_weights MBZUAI/bactrian-x-bloom-7b1-lora \
    --load_in_8bit \
    --save_dir ../results/Bactrian-BLOOM-7B \
    --max_length 768 \
    --num_few_shot $i
done
