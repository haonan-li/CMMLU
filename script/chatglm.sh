#!/bin/bash
#SBATCH --job-name=chatglm
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

# v2
for i in {0..5}; do
python chatglm.py \
    --model_name_or_path THUDM/chatglm2-6b \
    --save_dir ../results/ChatGLM2-6B \
    --num_few_shot $i
done


for i in {0..5}; do
python chatglm.py \
    --model_name_or_path THUDM/chatglm-6b \
    --save_dir ../results/ChatGLM-6B \
    --num_few_shot $i
done

python chatglm.py \
    --model_name_or_path THUDM/chatglm-6b \
    --save_dir ../results/ChatGLM-6B-cot \
    --cot \
    --num_few_shot 0
