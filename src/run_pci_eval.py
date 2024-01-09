import os
import argparse
import time
import json
from tqdm import tqdm
from collections import defaultdict
import pandas as pd

from pci_utils import load_json, save_json, load_data, extract_choice
from pci_model import LLM
from categories import name_en2zh, subcategories, categories
from mp_utils import format_example, gen_prompt

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
    resp_hist, id_hist, resp_dir = create_or_load_data("../responses", model_name+f"/{num_few_shot}_shot", resp_file)
    test_data = load_data(test_item)
    with open(os.path.join(resp_dir, resp_file), mode='a', encoding='utf8') as f:
        for samp in tqdm(test_data):
            samp_id = samp['id']
            if id_hist is not None and samp_id in id_hist:
                continue
            resp_dict = samp.copy()

            q1 = samp['question'].replace(test_item,name_en2zh[test_item])
            if num_few_shot > 0:
                prompt_end = format_example(test_df, int(samp_id), test_item, include_answer=False, cot=False)
                prompt = gen_prompt(dev_df, test_item, prompt_end, num_few_shot, tokenizer=None, max_length=2048, cot=False)
                usr_cont = prompt
            elif num_few_shot == 0:
                usr_cont = q1
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
    for root, dirs, files in os.walk(f'../responses/pci_transgpt/{num_few_shot}_shot'):
        for i in files:
            eval_item = i.replace("pci_transgpt-","").replace(".jsonl","")
            if eval_item in category2subject['STEM']:
                with open(os.path.join(f'../responses/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict1 = json.loads(line)
                        if dict1["extract_answer"] == dict1["right"]:
                            STEM_TRUE.append(1)
                        else:
                            STEM_FALSE.append(0)
            if eval_item in category2subject['Humanities']:
                with open(os.path.join(f'../responses/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict2 = json.loads(line)
                        if dict2["extract_answer"] == dict2["right"]:
                            Humanities_TRUE.append(1)
                        else:
                            Humanities_FALSE.append(0)
            if eval_item in category2subject['Social Science']:
                with open(os.path.join(f'../responses/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict3 = json.loads(line)
                        if dict3["extract_answer"] == dict3["right"]:
                            Social_Science_TRUE.append(1)
                        else:
                            Social_Science_FALSE.append(0)
            if eval_item in category2subject['Other']:
                with open(os.path.join(f'../responses/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
                    for line in f:
                        dict4 = json.loads(line)
                        if dict4["extract_answer"] == dict4["right"]:
                            Other_TRUE.append(1)
                        else:
                            Other_FALSE.append(0)
            if eval_item in category2subject['China specific']:
                with open(os.path.join(f'../responses/pci_transgpt/{num_few_shot}_shot/',f'{i}'),encoding='utf-8', mode='r') as f:
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
    save_json(Overall_SCORES, os.path.join(f"../responses/pci_transgpt/{num_few_shot}_shot/", f"Overall_SCORES_{num_few_shot}_shot.json"), multi=False, indent=4)
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
    for root, dirs, files in os.walk('../data/PCI-TransGPT'):
        for i in files:
            item = i.replace(".jsonl","")
            dev_df = pd.read_csv(os.path.join(args.data_dir, "dev", item + ".csv"), header=0, index_col=0)
            test_df = pd.read_csv(os.path.join(args.data_dir, "test", item + ".csv"), header=0, index_col=0)
            print(item)
            llm_responses = run_test(dev_df,test_df,item, test_model, model_key=model_key, num_few_shot=args.num_few_shot, **model_hyparam)
    run_eval(test_model,num_few_shot=args.num_few_shot)
    t2 = time.time()
    print("test cost time: {:.2f} min".format((t2-t1)/60))
    time.sleep(1)

