import argparse
import os

import numpy as np
import pandas as pd
import torch
from pandas import DataFrame
from tqdm import tqdm

from transformers import AutoModelForCausalLM, Qwen2ForCausalLM, AutoTokenizer, Qwen2TokenizerFast
from transformers.generation import GenerationConfig

from src.mp_utils import choices, format_example, gen_prompt
from src.rag.pdf_retriever import PdfRetriever


class Qwen2EvalWithRag:
    def __init__(self, args):
        if not args.model_name_or_path:
            raise ValueError("--model_name_or_path not set")

        self.model_path = args.model_name_or_path
        self.is_instruct_model = "instruct" in self.model_path.lower()

        parts = self.model_path.split('/')
        if len(parts) > 1:
            self.model_name = parts[1]
        else:
            self.model_name = self.model_path

        self.model = self.__init_model(self.model_path)
        self.tokenizer = self.__get_tokenizer(self.model_path)

        self.data_dir = args.data_dir
        self.num_few_shot = args.num_few_shot
        self.save_dir = os.path.join("../results", "".join([self.model_name, "_", str(self.num_few_shot), "_shot"]))
        self.max_length = args.max_length
        self.cot = args.cot

    def run_eval(self):
        self.model.eval()

        test_files = os.listdir(os.path.join(self.data_dir, "test/"))
        subjects = sorted([f.split(".csv")[0] for f in test_files])

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        for subject in subjects:
            out_file = os.path.join(self.save_dir, f"results_{subject}.csv")
            if os.path.exists(out_file) or subject != "bmw":  # If result file exist, skip this subject
                continue

            dev_df = pd.read_csv(os.path.join(self.data_dir, "dev", subject + ".csv"), header=0, index_col=0)
            test_df = pd.read_csv(os.path.join(self.data_dir, "test", subject + ".csv"), header=0, index_col=0)

            acc, preds, confs = self.__eval_instruct(model=self.model, tokenizer=self.tokenizer, subject=subject, dev_df=dev_df,
                                 test_df=test_df, num_few_shot=self.num_few_shot, max_length=self.max_length,
                                 cot=self.cot)
            test_df['prediction'] = preds
            test_df.to_csv(path_or_buf=out_file, header=False)


    @staticmethod
    def __init_model(model_name: str) -> Qwen2ForCausalLM:
        """Initialize models"""
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map="auto",
                                                     torch_dtype=torch.float16, )
        model.generation_config = GenerationConfig.from_pretrained(model_name, trust_remote_code=True)
        return model

    @staticmethod
    def __get_tokenizer(model_name: str) -> Qwen2TokenizerFast:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        return tokenizer

    @staticmethod
    def __eval_instruct(model: Qwen2ForCausalLM, tokenizer: Qwen2TokenizerFast, subject: str, dev_df: DataFrame,
                        test_df: DataFrame, num_few_shot: int, max_length: int, cot: bool):

        cors = []
        all_preds = []
        answers = choices[: test_df.shape[1] - 2]

        retriever = PdfRetriever(file="/home/hqin/workspace/CMMLU_RAG/data/bmw_7.pdf")

        for i in tqdm(range(test_df.shape[0])):
            question = test_df.iloc[i, 0]
            context = retriever.retrieve(question)
            context = ""

            prompt_end = format_example(test_df, i, subject, include_answer=False, cot=cot, context=context)
            prompt = gen_prompt(dev_df=dev_df, subject=subject, prompt_end=prompt_end, num_few_shot=num_few_shot,
                                tokenizer=tokenizer, max_length=max_length, cot=cot)
            label = test_df.iloc[i, test_df.shape[1] - 1]

            text = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,add_generation_prompt=True)
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

            generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
            generated_ids = [output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
            pred = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            if pred and pred[0] in choices:
                cors.append(pred[0] == label)
                all_preds.append(pred.replace("\n", ""))

        acc = np.mean(cors)
        print("Average accuracy {:.3f} - {}".format(acc, subject))
        print("{} results, {} inappropriate formated answers.".format(len(cors), len(all_preds) - len(cors)))
        return acc, all_preds, None

# def eval_instruct(
#     model, tokenizer, subject, dev_df, test_df, num_few_shot, max_length, cot
# ):
#     """eval Qwen/Qwen2-72B-Instruct
#     ref: https://huggingface.co/Qwen/Qwen2-72B-Instruct#quickstart
#     """
#     cors = []
#     all_preds = []
#     answers = choices[: test_df.shape[1] - 2]
#
#     for i in tqdm(range(test_df.shape[0])):
#         prompt_end = format_example(test_df, i, subject, include_answer=False, cot=cot)
#         prompt = gen_prompt(
#             dev_df=dev_df,
#             subject=subject,
#             prompt_end=prompt_end,
#             num_few_shot=num_few_shot,
#             tokenizer=tokenizer,
#             max_length=max_length,
#             cot=cot,
#         )
#         label = test_df.iloc[i, test_df.shape[1] - 1]
#
#         text = tokenizer.apply_chat_template(
#             [{"role": "user", "content": prompt}],
#             tokenize=False,
#             add_generation_prompt=True,
#         )
#         model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
#
#         generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
#         generated_ids = [
#             output_ids[len(input_ids) :]
#             for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
#         ]
#
#         pred = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
#         # pred, history = model.chat(tokenizer, prompt, history=None)
#
#         if pred and pred[0] in choices:
#             cors.append(pred[0] == label)
#         all_preds.append(pred.replace("\n", ""))
#
#     acc = np.mean(cors)
#     print("Average accuracy {:.3f} - {}".format(acc, subject))
#     print(
#         "{} results, {} inappropriate formated answers.".format(
#             len(cors), len(all_preds) - len(cors)
#         )
#     )
#     return acc, all_preds, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str)
    parser.add_argument("--data_dir", type=str, default="../data")
    parser.add_argument("--num_few_shot", type=int, default=0)
    parser.add_argument("--max_length", type=int, default=2048)
    parser.add_argument("--cot", action="store_true")
    args = parser.parse_args()

    qwen2_eval = Qwen2EvalWithRag(args)
    qwen2_eval.run_eval()


if __name__ == "__main__":
    main()
