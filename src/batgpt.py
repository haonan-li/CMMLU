import os
import numpy as np
import requests
import argparse
from time import sleep
from mp_utils import choices, format_example, gen_prompt, run_eval
from chatgpt import eval

url = 'http://47.100.14.205:6022/eval/chat/BATGPT-chat-batgpt'
def get_response(inputs):
    timeout_counter = 0
    while timeout_counter<=10:
        try:
            data = {
                    'utterance': inputs,
            }
            response = requests.post(url, json=data)

            return response.json()['response']
        except Exception as msg:
            timeout_counter+=1
            sleep(5)
            continue
            print("Some error occured when getting gpt output.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-d", type=str, default="../data")
    parser.add_argument("--save_dir", "-s", type=str, default="../results/BatGPT")
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--num_few_shot", "-n", type=int, default=0)
    parser.add_argument("--cot", action='store_true')
    args = parser.parse_args()

    run_eval(None, None, eval, args)

