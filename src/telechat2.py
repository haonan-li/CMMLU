import os
import torch
import numpy as np
import argparse
from mp_utils import choices, format_example, gen_prompt, softmax, run_eval
from tqdm import tqdm

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig


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


def init_model(args):
    """Initialize models"""
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


def get_input_ids(tokenizer,history_input_list,history_output_list,input_str):
    sentence_ids = [1]
    assert len(history_input_list) == len(history_output_list)
    for i in range(len(history_input_list)):
        input_ids = [4] + tokenizer(history_input_list[i])["input_ids"]
        output_ids = [5] + tokenizer(history_output_list[i])["input_ids"] + [2]
        sentence_ids += input_ids + output_ids
    sentence_ids += [4]+tokenizer(input_str)["input_ids"]+[5]
    return torch.tensor([sentence_ids])


def eval_instruct(
    model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot
):
    """eval TeleAI/TeleChat2-115B
    ref: https://modelscope.cn/models/TeleAI/TeleChat2-115B
    """
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

        pred, history = model.chat(tokenizer, prompt)


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
    parser.add_argument("--model_name_or_path", type=str, default="")
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--save_dir", type=str, default="../results/TeleChat2-115B")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--cot", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path, trust_remote_code=True
    )
    if is_eval_success(args):
        # eval finished, no need load model anymore, just show the result
        model = None
    else:
        model = init_model(args)

    run_eval(model, tokenizer, eval_instruct, args)

