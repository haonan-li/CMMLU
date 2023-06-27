#!/bin/bash
#SBATCH --job-name=falcon_7b
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
    --model_name_or_path tiiuae/falcon-7b \
    --save_dir ../results/Falcon-7B \
    --num_few_shot $i
done

