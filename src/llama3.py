import os
import torch
import numpy as np
import argparse
from mp_utils import choices, format_example, gen_prompt, softmax, get_results
from tqdm import tqdm
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import re
import pandas as pd


def run_eval(model, tokenizer, eval, args, is_pipline):
    if model and not is_pipline:
        model.eval()
    subjects=sorted([f.split(".csv")[0] for f in os.listdir(os.path.join(args.data_dir, "test/"))])
    args.save_dir = f"{args.save_dir}_{args.num_few_shot}_shot"
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    for subject in subjects:
        out_file = os.path.join(args.save_dir, f"results_{subject}.csv")
        if os.path.exists(out_file):  # If result file exist, skip this subject
            continue
        dev_df = pd.read_csv(os.path.join(args.data_dir, "dev", subject + ".csv"), header=0, index_col=0)
        test_df = pd.read_csv(os.path.join(args.data_dir, "test", subject + ".csv"), header=0, index_col=0)

        acc, preds, confs = eval(model=model,
                                 tokenizer=tokenizer,
                                 subject=subject,
                                 dev_df=dev_df,
                                 test_df=test_df,
                                 num_few_shot=args.num_few_shot,
                                 max_length=args.max_length,
                                 cot=args.cot if 'cot' in args else False)
        test_df['prediction'] = preds
        if 'with_conf' in args and args.with_conf:
            test_df['conf'] = confs

        test_df.to_csv(out_file, header=None)

    # print result
    get_results(args.save_dir)

def is_eval_success(args) -> bool:
    """judege if eval task is success by checking the result dir"""
    subjects = sorted(
        [f.split(".csv")[0] for f in os.listdir(os.path.join(args.data_dir, "test/"))]
    )
    abs_save_dir = f"{args.save_dir}_{args.num_few_shot}_shot"
    if not os.path.exists(abs_save_dir):
        return False
    for subject in subjects:
        out_file = os.path.join(abs_save_dir, f"results_{subject}.csv")
        if not os.path.exists(out_file):
            # If any result file NOT exist, the eval isn't finished
            return False
    return True


def eval_chat(
    model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot
):
    """eval meta-llama/Meta-Llama-3-70B
    ref: https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct#use-with-transformers
    """
    pipeline=model
    cors = []
    all_preds = []
    answers = choices[: test_df.shape[1] - 2]

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

        messages = [
            {"role": "user", "content": prompt},
        ]
        terminators = [
            pipeline.tokenizer.eos_token_id,
            pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        outputs = pipeline(
            messages,
            max_new_tokens=max_length,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        pred = outputs[0]["generated_text"][-1]["content"]
        if pred and pred[0] in choices:
            cors.append(pred[0] == label)
        all_preds.append(pred.replace("\n", ""))

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
    parser.add_argument("--model_name_or_path", type=str, default="Meta-Llama-3-8B-Instruct")
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--save_dir", type=str, default="../results/Meta-Llama-3-8B-Instruct")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--cot", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path, trust_remote_code=True
    )
    
    if "instruct" in args.model_name_or_path.lower():
        model=transformers.pipeline(
            "text-generation",
            model=args.model_name_or_path,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )
        run_eval(model, tokenizer, eval_chat, args, True)
    else:
        # Todo
        raise NotImplementedError(f"Direct inference with llama3_base_model is currently not supported.")
