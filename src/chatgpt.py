import os
import argparse
import numpy as np
import openai
import tiktoken
from tqdm import tqdm
from time import sleep
from mp_utils import choices, format_example, gen_prompt, run_eval

openai.api_key = "YOUR_API_KEY"
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def get_response(inputs):
    timeout_counter = 0
    completion = None
    while completion is None and timeout_counter<=30:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": inputs}
                  ]
                )
            return completion.choices[0].message['content']
        except Exception as msg:
            if "timeout=600" in str(msg):
                timeout_counter+=1
            print(msg)
            sleep(5)
            continue
            print("Some error occured when getting gpt output.")

def eval(subject, dev_df, test_df, num_few_shot, max_length, cot, **kwargs):
    cors = []
    all_preds = []
    answers = choices[: test_df.shape[1] - 2]

    for i in tqdm(range(test_df.shape[0])):
        prompt_end = format_example(test_df, i, subject, include_answer=False, cot=cot)
        prompt = gen_prompt(dev_df, subject, prompt_end, num_few_shot, encoding, max_length, cot=cot)
        label = test_df.iloc[i, test_df.shape[1] - 1]

        pred = get_response(prompt)
        if pred and pred[0] in choices:
            cors.append(pred[0] == label)
        all_preds.append(pred.replace("\n", "") if pred is not None else "")

    acc = np.mean(cors)
    print("Average accuracy {:.3f} - {}".format(acc, subject))
    print("{} results, {} inappropriate formated answers.".format(len(cors), len(all_preds)-len(cors)))
    return acc, all_preds, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-d", type=str, default="../data")
    parser.add_argument("--save_dir", "-s", type=str, default="../results/ChatGPT")
    parser.add_argument("--num_few_shot", "-n", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=4096)
    parser.add_argument("--cot", action='store_true')
    args = parser.parse_args()

    run_eval(None, None, eval, args)

