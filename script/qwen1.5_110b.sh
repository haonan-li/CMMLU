set -x
cd ../src

python qwen1.5.py \
    --model_name_or_path /qwen/Qwen1.5-110B \
    --save_dir ../results/Qwen1.5-110B \
    --num_few_shot 5
python qwen1.5.py \
    --model_name_or_path /qwen/Qwen1.5-110B \
    --save_dir ../results/Qwen1.5-110B \
    --num_few_shot 0
