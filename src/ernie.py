import argparse
import numpy as np
import requests
import json
from tqdm import tqdm
from time import sleep
from mp_utils import choices, format_example, gen_prompt, run_eval

encoding = None

API_KEY = "ERNIE_API_KEY"
SECRET_KEY = "ERNIE_SECRET_KEY"


def get_first_wanted_character(content, targets):
    # 遍历字符串的每个字符
    ret = ""
    for char in content:
        # 判断当前字符是否为英文字母
        if char in targets:
            ret = char
            break
    return ret


def get_res(input):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()

    payload = json.dumps({  # 上下文信息，最后一个dict为当前请求
        "messages": [
            {"role": "user", "content": input},
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["result"]


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_response(inputs):
    timeout_counter = 0
    completion = None
    while completion is None and timeout_counter<=30:
        try:
            ret = get_res(inputs)
            return ret
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
            choice = pred[0]
            cors.append(choice == label)
        elif pred:
            choice = get_first_wanted_character(pred, choices)
            if choice:
                cors.append(choice == label)

        all_preds.append(pred.replace("\n", "") if pred is not None else "")

    acc = np.mean(cors)
    print("Average accuracy {:.3f} - {}".format(acc, subject))
    print("{} results, {} inappropriate formated answers.".format(len(cors), len(all_preds)-len(cors)))
    return acc, all_preds, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-d", type=str, default="../data")
    parser.add_argument("--save_dir", "-s", type=str, default="../results/Ernie")
    parser.add_argument("--num_few_shot", "-n", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=4096)
    parser.add_argument("--cot", action='store_true')
    args = parser.parse_args()

    run_eval(None, None, eval, args)
