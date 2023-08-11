# Measuring massive multitask language understanding in Chinese

<p align="center"> <img src="fig/banner.jpg" style="width: 100%;" id="title-icon">       </p>

<h4 align="center">
    <p>
        <a href="https://github.com/haonan-li/CMMLU/">简体中文</a> |
        <b>English</b> 
    <p>
</h4>

<p align="center" style="display: flex; flex-direction: row; justify-content: center; align-items: center">
📄 <a href="https://arxiv.org/abs/2306.09212" target="_blank" style="margin-right: 15px; margin-left: 10px">Paper</a> • 
🏆 <a href="https://github.com/haonan-li/CMMLU/#leaderboard" target="_blank"  style="margin-left: 10px">Leaderboard</a> •
🤗 <a href="https://huggingface.co/datasets/haonan-li/cmmlu" target="_blank" style="margin-left: 10px">Dataset</a> 
</p>

## Introduction

CMMLU is a comprehensive evaluation benchmark specifically designed to evaluate the knowledge and reasoning abilities of LLMs within the context of Chinese language and culture. 
CMMLU covers a wide range of subjects, comprising 67 topics that span from elementary to advanced professional levels. It includes subjects that require computational expertise, such as physics and mathematics, as well as disciplines within humanities and social sciences. 
Many of these tasks are not easily translatable from other languages due to their specific contextual nuances and wording. 
Furthermore, numerous tasks within CMMLU have answers that are specific to China and may not be universally applicable or considered correct in other regions or languages.
<p align="center"> <img src="fig/logo.jpg" style="width: 85%;" id="title-icon">       </p>

## Leaderboard

The following table displays the performance of models in the five-shot and Zero-shot setting. If you wish to contribute your model's results, kindly contact us or submit a pull request to update this section. 
#### Five-shot

| Model               | STEM | Humanities | Social Science | Other | China-specific | Average |
|---------------------|------|------------|----------------|-------|----------------|---------|
| Multilingual-oriented                                             |
| [GPT4](https://openai.com/gpt4)                                   | **65.23** | **72.11** | **72.06** | **74.79** | **66.12** | **70.95** |
| [ChatGPT](https://openai.com/chatgpt)                             |   47.81   |   55.68   |   56.50   |   62.66   |   50.69   |   55.51   |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   33.33   |   43.46   |   44.28   |   44.75   |   39.46   |   41.45   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   34.47   |   40.24   |   41.55   |   42.88   |   37.00   |   39.80   |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   30.56   |   39.10   |   38.59   |   40.32   |   37.15   |   37.04   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   27.52   |   32.47   |   32.27   |   35.77   |   31.56   |   31.88   |
| Chinese-oriented                                                  |
| [MiLM-6B](https://github.com/XiaoMi/MiLM-6B/)                     | **46.85** |   61.12   | **61.68** |   58.84   | **59.39** | **57.17** |
| [Baichuan-13B](https://github.com/baichuan-inc/Baichuan-13B)      |   42.38   | **61.61** |   60.44   | **59.26** |   56.62   |   55.82   |
| [ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)           |   42.55   |   50.98   |   50.99   |   50.80   |   48.37   |   48.80   |
| [Baichuan-7B](https://github.com/baichuan-inc/baichuan-7B)        |   35.25   |   48.07   |   47.88   |   46.61   |   44.14   |   44.43   |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.35   |   39.22   |   39.65   |   38.62   |   37.70   |   37.48   |
| [BatGPT-15B](https://arxiv.org/abs/2307.00360)                    |   34.96   |   35.45   |   36.31   |   42.14   |   37.89   |   37.16   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   27.12   |   33.18   |   34.87   |   35.10   |   32.97   |   32.63   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   27.23   |   30.41   |   28.84   |   32.56   |   28.68   |   29.57   |
| [Chinese-GLM-10B](https://github.com/THUDM/GLM)                   |   25.49   |   27.05   |   27.42   |   29.21   |   28.05   |   27.26   |
| Random                                                            |   25.00   |   25.00   |   25.00   |   25.00   |   25.00   |   25.00   |


#### Zero-shot
| Model               | STEM | Humanities | Social Science | Other | China-specific | Average |
|---------------------|------|------------|----------------|-------|----------------|---------|
| Multilingual-oriented                                             | 
| [GPT4](https://openai.com/gpt4)                                   | **63.16** | **69.19** | **70.26** | **73.16** | **63.47** | **68.90** |
| [ChatGPT](https://openai.com/chatgpt)                             |   44.80   |   53.61   |   54.22   |   59.95   |   49.74   |   53.22   |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   33.03   |   45.74   |   45.74   |   46.25   |   41.58   |   42.80   |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   31.11   |   41.30   |   40.87   |   40.61   |   36.05   |   38.50   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   31.09   |   34.45   |   36.05   |   37.94   |   32.89   |   34.88   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   26.46   |   29.36   |   31.81   |   31.55   |   29.17   |   30.06   |
| Chinese-oriented                                                  |
| [MiLM-6B](https://github.com/XiaoMi/MiLM-6B/)                     | **48.88** | **63.49** | **66.2**  | **62.14** | **62.07** | **60.37** |
| [Baichuan-13B](https://github.com/baichuan-inc/Baichuan-13B)      |   42.04   |   60.49   |   59.55   |   56.60   |   55.72   |   54.63   |
| [ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)           |   41.28   |   52.85   |   53.37   |   52.24   |   50.58   |   49.95   |
| [Baichuan-7B](https://github.com/baichuan-inc/baichuan-7B)        |   32.79   |   44.43   |   46.78   |   44.79   |   43.11   |   42.33   |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.22   |   42.91   |   44.81   |   42.60   |   41.93   |   40.79   |
| [BatGPT-15B](https://arxiv.org/abs/2307.00360)                    |   33.72   |   36.53   |   38.07   |   46.94   |   38.32   |   38.51   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   26.76   |   26.57   |   27.42   |   28.33   |   26.73   |   27.34   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   25.68   |   26.35   |   27.21   |   27.92   |   26.70   |   26.88   |
| [Chinese-GLM-10B](https://github.com/THUDM/GLM)                   |   25.57   |   25.01   |   26.33   |   25.94   |   25.81   |   25.80   |

## Data Format
Each question in the dataset is a multiple-choice questions with 4 choices and only one choice as the correct answer.  The data is comma saperated .csv file. The data can be found in [data](https://github.com/haonan-li/CMMLU/data) 
Here is an example of the data format:
```
    同一物种的两类细胞各产生一种分泌蛋白，组成这两种蛋白质的各种氨基酸含量相同，但排列顺序不同。其原因是参与这两种蛋白质合成的,tRNA种类不同,同一密码子所决定的氨基酸不同,mRNA碱基序列不同,核糖体成分不同,C
    Translation:"Two types of cells within the same species each produce a secretion protein. The various amino acids that make up these two proteins have the same composition but differ in their arrangement. The reason for this difference in arrangement in the synthesis of these two proteins is,Different types of tRNA,Different amino acids determined by the same codon,Different mRNA base sequences,Different ribosome components,C"
```

## Usage

To use our code in your project, clone the repository to your local machine:

```shell
    git clone https://github.com/haonan-li/CMMLU.git
    cd CMMLU/src
```
#### Data
We provide development and test dataset according to each subject in the [data/dev](https://github.com/haonan-li/CMMLU/tree/master/data/dev) and [data/test](https://github.com/haonan-li/CMMLU/tree/master/data/test) directory.

#### Prompt
We provide the preprocessing code in [src/mp_utils](https://github.com/haonan-li/CMMLU/tree/master/src/mp_utils.py) directory. It includes apporach we used to generate direct answer prompt and chain-of-thought (COT) prompt.

Here is an example of data after adding direct answer prompt:
```
    以下是关于(高中生物)的单项选择题，请直接给出正确答案的选项。
    (Here are some single-choice questions about(high school biology), please provide the correct answer choice directly.)
    题目：同一物种的两类细胞各产生一种分泌蛋白，组成这两种蛋白质的各种氨基酸含量相同，但排列顺序不同。其原因是参与这两种蛋白质合成的：
    (Two types of cells within the same species each produce a secretion protein. The various amino acids that make up these two proteins have the same composition but differ in their arrangement. The reason for this difference in arrangement in the synthesis of these two proteins is)
    A. tRNA种类不同(Different types of tRNA)
    B. 同一密码子所决定的氨基酸不同(Different amino acids determined by the same codon)
    C. mRNA碱基序列不同(Different mRNA base sequences)
    D. 核糖体成分不同(Different ribosome components)
    答案是：C(Answer: C)

    ... [other examples] 

    题目：某种植物病毒V是通过稻飞虱吸食水稻汁液在水稻间传播的。稻田中青蛙数量的增加可减少该病毒在水稻间的传播。下列叙述正确的是：
    (Question: A certain plant virus, V, is transmitted between rice plants through the feeding of rice planthoppers. An increase in the number of frogs in the rice field can reduce the spread of this virus among the rice plants. The correct statement among the options provided would be)
    A. 青蛙与稻飞虱是捕食关系(Frogs and rice planthoppers have a predatory relationship)
    B. 水稻和病毒V是互利共生关系(Rice plants and virus V have a mutualistic symbiotic relationship)
    C. 病毒V与青蛙是寄生关系(Virus V and frogs have a parasitic relationship)
    D. 水稻与青蛙是竞争关系(Rice plants and frogs have a competitive relationship)
    答案是： (Answer:)
```
For the COT prompt we modified the prompt from“请直接给出正确答案的选项 (please provide the correct answer choice directly)” to “逐步分析并选出正确答案 (Analyze step by step and select the correct answer).”

#### Evaluation
The code for evaluation of each model we used is in [src](https://github.com/haonan-li/CMMLU/tree/master/src), and the code to run them is listed in [script](https://github.com/haonan-li/CMMLU/tree/master/script) directory.

## Citation
```
@misc{li2023cmmlu,
      title={CMMLU: Measuring massive multitask language understanding in Chinese}, 
      author={Haonan Li and Yixuan Zhang and Fajri Koto and Yifei Yang and Hai Zhao and Yeyun Gong and Nan Duan and Timothy Baldwin},
      year={2023},
      eprint={2306.09212},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## License

The CMMLU dataset is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
