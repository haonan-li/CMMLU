#!/bin/bash
#SBATCH --job-name=baichuan_13b_eval
#SBATCH --output=./stdout/slurm-%j.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4

#SBATCH --gres=gpu:2
#SBATCH -p gpu
#SBATCH --qos=gpu-8

cd ../src

for i in {0..5}; do
python hf_causal_model.py \
    --model_name_or_path baichuan-inc/Baichuan-13B-Base \
    --save_dir ../results/Baichuan-13B-Base \
    --num_few_shot $i
done
