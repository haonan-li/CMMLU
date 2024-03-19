import os
import re
import time
import json
import asyncio
import logging
import requests
import csv
import argparse
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

from categories import name_en2zh, subcategories, categories
from mp_utils import format_example, gen_prompt


pci_url = "http://123.249.36.167:19203"

def pci_generate(usr_contents, model_name=None, stream=False, model_key=None,
                 max_length=4096, top_p=0.8, top_k=30, repetition_penalty=1.2, temperature=0.05):
    """PCI TransGPT
    url: 地址
    usr_contents: 用户输入
    """
    # URI处理
    if stream:
        url_tail = "/api/gpt/chat/completions/stream"
    else:
        url_tail = "/api/gpt/chat/completions"

    if model_key is None:
        model_key = pci_url

    url = model_key + url_tail

    # Message处理
    messages = []

    # 用户输入
    if isinstance(usr_contents, str):
        messages.append({"role": "user", "content": usr_contents})
    else:
        raise ValueError(f"Contents type error for single turn chat, "
                         f"user:{type(usr_contents)}, assistant: {type(asis_contents)}")

    # body处理
    body = {
        "model": "PCI-TransGPT",
        "max_tokens": max_length,
        "top_p": top_p,
        "temperature": temperature,
        "top_k": top_k,
        "repetition_penalty": repetition_penalty,
        "messages": messages
    }

    # header处理
    headers = {
        "Content-Type": "application/json",
    }

    # 设置10次重连
    retry_counter = 0
    max_retries = 10
    delay = 15  #

    while retry_counter < max_retries:
        try:
            response = requests.post(url=url, json=body, headers=headers)
            response_dict = response.json()

            if "choices" in response_dict:
                return response_dict['choices'][0]['message']['content']
            else:
                raise f"PCI generate failure: {str(response_dict)}"
        except Exception as error:
            retry_counter += 1
            logging.warning(f"PCI generate failure: {repr(error)}")
            if retry_counter <= max_retries:
                logging.warning(f"Waiting for retry: {retry_counter} ...")
                time.sleep(delay)
            else:
                logging.warning(f"Exceed maximum retries number!")
                raise error


class LLM:
    def __init__(self, model_name, model_key, **kwargs):
        self.model_name = model_name
        self.model_key = model_key
        self.kwargs = kwargs
        self.usr_contents = None

    def run(self, usr_contents):
        self.usr_contents = usr_contents
        return self.call_llm()

    def get_model_type(self):
        model_type = {
            **{k: "pci" for k in ["pci_transgpt"] },
        }
        if self.model_name in model_type:
            return model_type.get(self.model_name)
        raise ValueError(f"LLM model name not supported: '{self.model_name}'")

    def call_llm(self):
        generate_funcs = {
            "pci": pci_generate,
        }

        model_type = self.get_model_type()
        generate_func = generate_funcs.get(model_type)
        if generate_func:
            self.kwargs.update({
                'usr_contents': self.usr_contents,
                'model_name': self.model_name,
                'model_key': self.model_key
            })

            response = generate_func(**self.kwargs)
            return response

        raise KeyError(f"LLM model type not supported: '{model_type}'")


class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def load_json(json_file, multi=True):
    if not os.path.exists(json_file):
        raise FileNotFoundError("json file not found: {}".format(json_file))
    if multi:
        with open(json_file, encoding='utf-8', mode='r') as f:
            data = [json.loads(line) for line in f]
        return data
    else:
        with open(json_file, encoding='utf-8', mode='r') as f:
            data = json.load(f)
        return data

def save_json(json_data, json_file, multi=True, indent=None):
    if multi:
        with open(json_file, encoding='utf-8', mode='w') as f:
            for item in json_data:
                json.dump(item, f, ensure_ascii=False, indent=indent)
                f.write('\n')
    else:
        with open(json_file, encoding='utf-8', mode='w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=indent)

def extract_choice(response, choice_desc):
    # choice_desc: 选项信息，包括选项字母和描述
    if choice_desc is not None:
        ref_letters = [c[0] for c in choice_desc]
        ref_desc = [c[2:] for c in choice_desc]
    else:
        ref_letters = ["A", "B", "C", "D"]
        ref_desc = None
    if len(response) == 0:
        return None
    if ref_desc is not None:
        pattern = '|'.join(re.escape(desc) for desc in ref_desc)
        match = re.findall(pattern, response)
        if len(set(match)) == 1:
            return ref_letters[ref_desc.index(match[0])]
    # 关键字匹配
    # 1. Single match
    patterns = [
            (r'答案(选项)?(是|为)：? ?([A-Z]+)', 3),
            (r'答案(是|为)选项 ?([A-Z]+)', 2),
            (r'故?选择?：? ?([A-Z]+)', 1),
            (r'([A-Z]+) ?选?项(是|为)?正确', 1),
            (r'正确的?选项(是|为) ?([A-Z]+)', 2),
            (r'答案(应该)?(是|为)([A-Z]+)', 3),
            (r'选项 ?([A-Z]+) ?(是|为)?正确', 1),
            (r'选择答案 ?([A-Z]+)', 1),
            (r'答案?：?([A-Z]+)', 1),
            (r'([A-Z]+)(选?项)?是?符合题意', 1),
            (r'答案选项：? ?([A-Z]+)', 1),  # chatglm
            (r'答案(选项)?为(.*?)([A-Z]+)', 3),  # chatgpt
    ]
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            return answer
    # 2. Recursive match
    patterns = [
            (r'([A-Z]+)(.*?)当选', 1),
            (r'([A-Z]+)(.*?)正确', 1),
            (r'(综上)(.*?)([A-Z]+)(.*?)最', 3),
            (r'(因此)(.*?)([A-Z]+)(.*?)最', 3),
    ]
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            while m:
                answer = m.group(idx)
                m = re.search(pattern, m.group(0)[1:], re.M)
            return answer
    # 3. Weak single match
    patterns = [
            (r'[^不]是：? ?([A-Z]+)', 1),
    ]
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            return answer
    # 4. Check the only mentioend choices
    pattern = r'^[^ABCD]*([ABCD])[^ABCD]*$'
    m = re.match(pattern, response)
    if m:
        answer = m.group(1)
        return answer
    # 最后
    pattern = re.compile(r'[A-Z]+')
    answer = pattern.findall(response)
    if len(set(answer)) > 0:
        return list(set(answer))[0]
    return None

def create_or_load_data(data_dir, model_name, file_name):
    data_dir = os.path.join(data_dir, model_name)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data_path = os.path.join(data_dir, file_name)
    if os.path.exists(data_path):
        data_hist = load_json(data_path)
        id_hist = [i['id'] for i in data_hist]
    else:
        data_hist = []
        id_hist = None
    return data_hist, id_hist, data_dir

def run_test(dev_df, test_df, test_item, model_name, model_key="", num_few_shot=0, **kwargs):
    # 模型
    llm_model = LLM(model_name=model_name, model_key=model_key, **kwargs)
    # LLM回复处理
    resp_file = f"{model_name}-{test_item}.jsonl"
    resp_hist, id_hist, resp_dir = create_or_load_data("../results", model_name+f"/{num_few_shot}_shot", resp_file)
    resp_dict = {}
    with open(os.path.join(resp_dir, resp_file), mode='a', encoding='utf8') as f:
        filename = os.path.join('../data/test/',f'{test_item}.csv')
        with open(filename,'r',encoding=u'utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            #跳过表头
            next(csvreader)
            for samp in tqdm(csvreader):
                samp_id = samp[0]
                if id_hist is not None and samp_id in id_hist:
                    continue
                resp_dict["id"] = samp[0]
                resp_dict["question"] = f"以下是关于{name_en2zh[test_item]}的单项选择题，请直接给出正确答案的选项。只能用字母A、B、C、D作答，不要给出多余的内容。\n"+ samp[1] + "\n" + "A " + samp[2] + "\n" +  "B " + samp[3] + "\n" + "C " + samp[4] + "\n" + "D " + samp[5] + "\n答案:"
                resp_dict["answer"] = ""
                resp_dict["right"] = samp[6]

                if num_few_shot > 0:
                    prompt_end = format_example(test_df, int(samp_id), test_item, include_answer=False, cot=False)
                    prompt = gen_prompt(dev_df, test_item, prompt_end, num_few_shot, tokenizer=None, max_length=2048, cot=False)
                    usr_cont = prompt
                elif num_few_shot == 0:
                    usr_cont = resp_dict["question"]
                resp_dict.update({'question': usr_cont})
                a1 = llm_model.run(usr_contents=usr_cont)
                resp_dict.update({'answer': a1})
                extract_answer = extract_choice(a1,choice_desc=None)
                resp_dict.update({'extract_answer': extract_answer})
                resp_hist.append(resp_dict)
                json.dump(resp_dict, f, ensure_ascii=False)
                f.write('\n')
                time.sleep(0.1)
    return resp_hist

def run_eval(test_model,num_few_shot):
    """评测得分计算"""
    category2subject = defaultdict(list)
    for k,v in categories.items():
        for subject, subcat in subcategories.items():
            for c in subcat:
                if c in v:
                    category2subject[k].append(subject)
    Overall_SCORES = {}
    STEM_TRUE, STEM_FALSE, Humanities_TRUE, Humanities_FALSE, Social_Science_TRUE, Social_Science_FALSE, Other_TRUE, Other_FALSE, China_specific_TRUE, China_specific_FALSE = [], [], [], [], [], [], [], [], [], []
    for root, dirs, files in os.walk(f'../results/pci_transgpt/{num_few_shot}_shot'):
        for i in files:
            eval_item = i.replace("pci_transgpt-","").replace(".jsonl","")
            if eval_item in category2subject['STEM']:
                with open(os.path.join(f'../results/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict1 = json.loads(line)
                        if dict1["extract_answer"] == dict1["right"]:
                            STEM_TRUE.append(1)
                        else:
                            STEM_FALSE.append(0)
            if eval_item in category2subject['Humanities']:
                with open(os.path.join(f'../results/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict2 = json.loads(line)
                        if dict2["extract_answer"] == dict2["right"]:
                            Humanities_TRUE.append(1)
                        else:
                            Humanities_FALSE.append(0)
            if eval_item in category2subject['Social Science']:
                with open(os.path.join(f'../results/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict3 = json.loads(line)
                        if dict3["extract_answer"] == dict3["right"]:
                            Social_Science_TRUE.append(1)
                        else:
                            Social_Science_FALSE.append(0)
            if eval_item in category2subject['Other']:
                with open(os.path.join(f'../results/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict4 = json.loads(line)
                        if dict4["extract_answer"] == dict4["right"]:
                            Other_TRUE.append(1)
                        else:
                            Other_FALSE.append(0)
            if eval_item in category2subject['China specific']:
                with open(os.path.join(f'../results/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict5 = json.loads(line)
                        if dict5["extract_answer"] == dict5["right"]:
                            China_specific_TRUE.append(1)
                        else:
                            China_specific_FALSE.append(0)
    STEM_SCORE = len(STEM_TRUE) / (len(STEM_TRUE) + len(STEM_FALSE)) * 100
    Humanities_SCORE = len(Humanities_TRUE) / (len(Humanities_TRUE) + len(Humanities_FALSE)) * 100
    Social_Science_SCORE = len(Social_Science_TRUE) / (len(Social_Science_TRUE) + len(Social_Science_FALSE)) * 100
    Other_SCORE = len(Other_TRUE) / (len(Other_TRUE) + len(Other_FALSE)) * 100
    China_specific_SCORE = len(China_specific_TRUE) / (len(China_specific_TRUE) + len(China_specific_FALSE)) * 100
    All_SCORE = (len(STEM_TRUE) + len(Humanities_TRUE) + len(Social_Science_TRUE) + len(Other_TRUE) + len(China_specific_TRUE)) / (len(STEM_TRUE) + len(Humanities_TRUE) + len(Social_Science_TRUE) + len(Other_TRUE) + len(China_specific_TRUE) + len(STEM_FALSE) + len(Humanities_FALSE) + len(Social_Science_FALSE) + len(Other_FALSE) + len(China_specific_FALSE)) * 100
    Overall_SCORES['平均分'] = All_SCORE
    Overall_SCORES['STEM'] = STEM_SCORE
    Overall_SCORES['人文学科'] = Humanities_SCORE
    Overall_SCORES['社会科学'] = Social_Science_SCORE
    Overall_SCORES['其他'] = Other_SCORE
    Overall_SCORES['中国特定主题'] = China_specific_SCORE
    #保存得分
    save_json(Overall_SCORES, os.path.join(f"../results/pci_transgpt/{num_few_shot}_shot/", f"Overall_SCORES_{num_few_shot}_shot.json"), multi=False, indent=4)
    print (f"{test_model} {num_few_shot}_shot评测结果得分：")
    print (f"STEM得分：{STEM_SCORE}")
    print (f"Humanities得分：{Humanities_SCORE}")
    print (f"Social_Science得分：{Social_Science_SCORE}")
    print (f"Other得分：{Other_SCORE}")
    print (f"China_specific得分：{China_specific_SCORE}")
    print (f"平均分：{All_SCORE}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", "-d", type=str, default="../data")
    parser.add_argument("--num_few_shot", "-n", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=4096)
    parser.add_argument("--cot", action='store_true')
    args = parser.parse_args()

    test_model = "pci_transgpt"
    model_key = "http://123.249.36.167:19203"
    model_hyparam = {"max_length": 4096, "top_p": 0.8, "top_k": 30, "repetition_penalty": 1.2, "temperature": 0.05}
    t1 = time.time()
    for root, dirs, files in os.walk('../data/test'):
        for i in files:
            item = i.replace(".csv","")
            dev_df = pd.read_csv(os.path.join(args.data_dir, "dev", item + ".csv"), header=0, index_col=0)
            test_df = pd.read_csv(os.path.join(args.data_dir, "test", item + ".csv"), header=0, index_col=0)
            print(item)
            llm_responses = run_test(dev_df,test_df,item, test_model, model_key=model_key, num_few_shot=args.num_few_shot, **model_hyparam)
    run_eval(test_model,num_few_shot=args.num_few_shot)
    t2 = time.time()
    print("test cost time: {:.2f} min".format((t2-t1)/60))
    time.sleep(1)

