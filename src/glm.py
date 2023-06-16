import os
import torch
import numpy as np
import argparse
from mp_utils import choices, format_example, gen_prompt, softmax, run_eval

from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def eval(model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot):
    cors = []
    all_conf = []
    all_preds = []
    answers = choices[: test_df.shape[1] - 2]

    for i in range(test_df.shape[0]):
        prompt_end = format_example(test_df, i, subject, include_answer=False)
        prompt = gen_prompt(dev_df=dev_df,
                            subject=subject,
                            prompt_end=prompt_end,
                            num_few_shot=num_few_shot,
                            tokenizer=tokenizer,
                            max_length=max_length)
        prompt += "[MASK]"
        inputs = tokenizer(prompt, return_tensors="pt")

        label = test_df.iloc[i, test_df.shape[1] - 1]

        with torch.no_grad():
            loss = []
            for t in ["A","B","C",'D']:
                inputs_ = tokenizer.build_inputs_for_generation(inputs, targets=t, max_gen_length=8, padding=False)
                inputs_ = inputs_.to('cuda')
                outputs = model(**inputs_, max_length=2048)
                loss.append(outputs.loss.detach().cpu().numpy())
            conf = softmax(loss)[choices.index(label)]
            pred = {0: "A", 1: "B", 2: "C", 3: "D"}[np.argmin(loss)]

        all_preds += pred
        all_conf.append(conf)
        cors.append(pred == label)

    acc = np.mean(cors)
    print("Average accuracy {:.3f} - {}".format(acc, subject))
    return acc, all_preds, all_conf


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="")
    parser.add_argument("--lora_weights", type=str, default="")
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--save_dir", type=str, default="../results/not_specified")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--load_in_8bit", action='store_true')
    parser.add_argument("--with_conf", action='store_true')
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    model = model.half().cuda()

    run_eval(model, tokenizer, eval, args)
