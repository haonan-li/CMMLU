import os
import torch
import numpy as np
import argparse
from hf_causal_model import eval
from mp_utils import choices, format_example, gen_prompt, softmax, run_eval

from huggingface_hub import snapshot_download
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
from accelerate import init_empty_weights, load_checkpoint_and_dispatch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="")
    parser.add_argument("--lora_weights", type=str, default="")
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--save_dir", type=str, default="../results/not_specified")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--load_in_8bit", action='store_true')
    args = parser.parse_args()

    # Initialize models
    # Verified support models: llama, bloom, bactrian,
    hf_home = os.environ.get('HF_HOME')
    model_path = os.path.join(hf_home, args.model_name_or_path)
    if not os.path.exists(model_path):
        model_path = snapshot_download(args.model_name_or_path)
    config = AutoConfig.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    with init_empty_weights():
        model = AutoModelForCausalLM.from_config(config, torch_dtype=torch.float16, trust_remote_code=True)
    model.tie_weights()
    model = load_checkpoint_and_dispatch(model, model_path, device_map="auto", no_split_module_classes=["MossBlock"], dtype=torch.float16)

    run_eval(model, tokenizer, eval, args)
