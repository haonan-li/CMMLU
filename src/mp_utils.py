import os
import re
import glob
import random
import os.path as osp
import numpy as np
import pandas as pd
from collections import defaultdict
from categories import name_en2zh, subcategories, categories
choices = ["A", "B", "C", "D"]

category2subject = defaultdict(list)
for k,v in categories.items():
    for subject, subcat in subcategories.items():
        for c in subcat:
            if c in v:
                category2subject[k].append(subject)


def format_example(df, idx, subject, include_answer=True, cot=False):
    prompt_start = "题目："
    prompt = prompt_start + df.iloc[idx, 0]
    k = df.shape[1] - 2
    for j in range(k):
        prompt += "\n{}. {}".format(choices[j], df.iloc[idx, j + 1])

    # Chain-of-thought
    if cot:
        prompt += "\n逐步分析并给出答案选项。"
    else:
        prompt += "\n答案是："

    if include_answer:
        prompt += "{}\n\n".format(df.iloc[idx, k + 1])
    return prompt

def gen_prompt(dev_df, subject, prompt_end, num_few_shot=0, tokenizer=None, max_length=2048, cot=False):
    if cot: # Chain-of-thought
        prompt = "以下是关于{}的单项选择题，请分析并选出正确答案。\n\n".format(name_en2zh[subject])
    else:
        prompt = "以下是关于{}的单项选择题，请直接给出正确答案的选项。\n\n".format(name_en2zh[subject])

    # If no tokenizer, don't consider max length.
    if tokenizer==None:
        for i in range(num_few_shot):
            example = format_example(dev_df, i, subject)
            prompt += example
        return prompt + prompt_end

    start_end_token_len = len(tokenizer.encode(prompt)+tokenizer.encode(prompt_end))
    # If cannot fit in model even without training data, remove the prompt at the beginning.
    if start_end_token_len>max_length:
        return prompt_end

    prompt_list = []
    if num_few_shot > 0:
        for i in range(num_few_shot):
            example = format_example(dev_df, i, subject)
            prompt_list.append((example, tokenizer.encode(example)))

        while prompt_list != [] and sum(len(e[1]) for e in prompt_list) >= max_length - start_end_token_len:
            print(f"Warning: {len(prompt_list)} shot case exceeds max_input_length, remove 1 shot.")
            longest_length = max([len(e[1]) for e in prompt_list])
            prompt_list = [e for e in prompt_list if len(e[1]) != longest_length]
        for p in prompt_list:
            prompt += p[0]

    return prompt + prompt_end


def softmax(x):
    z = x - max(x)
    numerator = np.exp(z)
    denominator = np.sum(numerator)
    softmax = numerator/denominator
    return softmax


def run_eval(model, tokenizer, eval, args):

    if model:
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


def extract_choice(response):
    '''
        Always return a choice, even cannot match by regex,
        to ensure fair comparison to other models.
    '''
    response = str(response)
    if response[0] in choices:
        return response[0]
    # 1. Single match
    patterns = [
        (r'答案(选项)?(是|为)：? ?([ABCD])', 3),
        (r'答案(是|为)选项 ?([ABCD])', 2),
        (r'故?选择?：? ?([ABCD])',1),
        (r'([ABCD]) ?选?项(是|为)?正确',1),
        (r'正确的?选项(是|为) ?([ABCD])',2),
        (r'答案(应该)?(是|为)([ABCD])',3),
        (r'选项 ?([ABCD]) ?(是|为)?正确',1),
        (r'选择答案 ?([ABCD])',1),
        (r'答案?：?([ABCD])',1),
        (r'([ABCD])(选?项)?是?符合题意',1),
        (r'答案选项：? ?([ABCD])', 1), # chatglm
        (r'答案(选项)?为(.*?)([ABCD])', 3), # chatgpt

    ]
    for pattern,idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            assert answer in choices
            return answer

    # 2. Recursive match
    patterns = [
        (r'([ABCD])(.*?)当选', 1),
        (r'([ABCD])(.*?)正确', 1),
    ]
    for pattern,idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            while m:
                answer = m.group(idx)
                m = re.search(pattern, m.group(0)[1:], re.M)
            assert answer in choices
            return answer

    # 3. Weak single match
    patterns = [
        (r'[^不]是：? ?([ABCD])', 1),
    ]
    for pattern,idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            assert answer in choices
            return answer

    # 4. Check the only mentioend choices
    pattern = r'^[^ABCD]*([ABCD])[^ABCD]*$'
    m = re.match(pattern, response)
    if m:
        answer = m.group(1)
        assert answer in choices
        return answer

    return choices[random.randint(0,3)]


def get_results(result_dir=''):

    all_acc = defaultdict(float)
    all_df = []
    for subject in name_en2zh.keys():
        try:
            file = glob.glob(osp.join(result_dir, f"results_{subject}.csv"))[0]
        except:
            print(f"Warning, {subject} result file not found")
            continue
        df = pd.read_csv(file, names=['id','question','A','B','C','D','answer','response'], index_col=0)
        # To deal with some mismath between data and answer
        if df.iloc[0]['question'] == '1':
            df = df.drop(0)
        df['pred'] = df['response'].apply(extract_choice)
        df['acc'] = df['answer'] == df['pred']
        acc = np.mean(df['acc']) * 100
        all_acc[subject]=acc
        all_df.append(df)

    all_df = pd.concat(all_df)
    for k, v in category2subject.items():
        avg_acc = np.mean(list(map(lambda x: all_acc[x], v)))
        print(f"{k:40s} {avg_acc:.2f}")
    avg_all_acc = np.mean(list(all_acc.values()))
    print(f"{'Overall':30s} {avg_all_acc:.2f}")

    return all_acc
