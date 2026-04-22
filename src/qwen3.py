import argparse
import os
import re

import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

from mp_utils import choices, format_example, gen_prompt, run_eval, softmax


def is_eval_success(args) -> bool:
    """Judge if eval task is finished by checking output files."""
    subjects = sorted(
        [f.split(".csv")[0] for f in os.listdir(os.path.join(args.data_dir, "test/"))]
    )
    abs_save_dir = f"{args.save_dir}_{args.num_few_shot}_shot"
    if not os.path.exists(abs_save_dir):
        return False
    for subject in subjects:
        out_file = os.path.join(abs_save_dir, f"results_{subject}.csv")
        if not os.path.exists(out_file):
            return False
    return True


def init_model(args):
    """Initialize model."""
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        trust_remote_code=True,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    model.generation_config = GenerationConfig.from_pretrained(
        args.model_name_or_path, trust_remote_code=True
    )
    return model


def eval(model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot):
    """Logit-based multiple choice evaluation (base model style)."""
    choice_ids = [tokenizer(choice)["input_ids"][0] for choice in choices]
    cors = []
    all_conf = []
    all_preds = []

    for i in range(test_df.shape[0]):
        prompt_end = format_example(test_df, i, subject, include_answer=False, cot=cot)
        prompt = gen_prompt(
            dev_df=dev_df,
            subject=subject,
            prompt_end=prompt_end,
            num_few_shot=num_few_shot,
            tokenizer=tokenizer,
            max_length=max_length,
            cot=cot,
        )
        label = test_df.iloc[i, test_df.shape[1] - 1]

        with torch.no_grad():
            input_ids = tokenizer([prompt], padding=False)["input_ids"]
            input_ids = torch.tensor(input_ids, device=model.device)
            logits = model(input_ids)["logits"]
            last_token_logits = logits[:, -1, :]
            if last_token_logits.dtype in {torch.bfloat16, torch.float16}:
                last_token_logits = last_token_logits.to(dtype=torch.float32)
            choice_logits = last_token_logits[:, choice_ids].detach().cpu().numpy()
            conf = softmax(choice_logits[0])[choices.index(label)]
            pred = {0: "A", 1: "B", 2: "C", 3: "D"}[np.argmax(choice_logits[0])]

        all_preds += pred
        all_conf.append(conf)
        cors.append(pred == label)

    acc = np.mean(cors)
    print("Average accuracy {:.3f} - {}".format(acc, subject))
    return acc, all_preds, None


def _extract_choice(text: str) -> str:
    """Extract first A/B/C/D from generated answer."""
    if not text:
        return ""
    m = re.search(r"\b([ABCD])\b", text.upper())
    if m:
        return m.group(1)
    first = text.strip().upper()[:1]
    return first if first in choices else ""


def eval_instruct(
    model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot
):
    """Eval for Qwen3 Instruct chat models."""
    cors = []
    all_preds = []

    for i in tqdm(range(test_df.shape[0])):
        prompt_end = format_example(test_df, i, subject, include_answer=False, cot=cot)
        prompt = gen_prompt(
            dev_df=dev_df,
            subject=subject,
            prompt_end=prompt_end,
            num_few_shot=num_few_shot,
            tokenizer=tokenizer,
            max_length=max_length,
            cot=cot,
        )
        label = test_df.iloc[i, test_df.shape[1] - 1]

        text = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True,
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0,
        )
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        pred_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        pred = _extract_choice(pred_text)

        if pred:
            cors.append(pred == label)
        all_preds.append(pred_text.replace("\n", ""))

    acc = np.mean(cors)
    print("Average accuracy {:.3f} - {}".format(acc, subject))
    print(
        "{} results, {} inappropriate formated answers.".format(
            len(cors), len(all_preds) - len(cors)
        )
    )
    return acc, all_preds, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="Qwen/Qwen3-4B-Instruct")
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--save_dir", type=str, default="../results/Qwen3-4B-Instruct")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--cot", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path, trust_remote_code=True
    )
    if is_eval_success(args):
        model = None
    else:
        model = init_model(args)

    if "instruct" in args.model_name_or_path.lower():
        run_eval(model, tokenizer, eval_instruct, args)
    else:
        run_eval(model, tokenizer, eval, args)
