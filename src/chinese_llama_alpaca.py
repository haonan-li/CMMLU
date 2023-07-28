import os
import torch
import argparse
from mp_utils import choices, format_example, gen_prompt, softmax, run_eval
from hf_causal_model import eval

from peft import PeftModel
from transformers import LlamaForCausalLM, LlamaTokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer


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

    # TODO: better handle
    tokenizer_class = LlamaTokenizer if 'llama' in args.model_name_or_path else AutoTokenizer
    model_class = LlamaForCausalLM if 'llama' in args.model_name_or_path else AutoModelForCausalLM
    tokenizer = tokenizer_class.from_pretrained(args.lora_weights) # Specific for Chinese_llama_alpaca
    model = model_class.from_pretrained(args.model_name_or_path,
                                        torch_dtype=torch.float16, # Follow https://github.com/ymcui/Chinese-LLaMA-Alpaca/blob/main/scripts/inference_hf.py
                                        load_in_8bit=args.load_in_8bit,
                                        device_map="auto"
                                        )
    if args.lora_weights != "":
        # Specific for Chinese_llama_alpaca
        tokenzier_vocab_size = len(tokenizer)
        model.resize_token_embeddings(tokenzier_vocab_size)

        model = PeftModel.from_pretrained(
                        model,
                        args.lora_weights,
                        torch_dtype=torch.float16,
                        )

    run_eval(model, tokenizer, eval, args)
