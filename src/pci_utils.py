import json
import os
import re
import logging
import time
from pci_model import LLM

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


def load_data(item, data_dir="../data/PCI-TransGPT/"):
    if data_dir is None:
        data_dir = "../data/PCI-TransGPT/"
    files = [f for f in os.listdir(data_dir) if f.endswith(".jsonl") and item+".jsonl" == f]
    if len(files) != 1:
        raise ValueError(f"Data files do not match: {len(files)}")

    data_file = files[0]
    data = load_json(data_dir + data_file, )
    return data

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
