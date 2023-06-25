# 多维语言理解评估---中文大规模多任务测量

<p align="center"> <img src="fig/banner_zh.jpg" style="width: 100%;" id="title-icon">       </p>

<h4 align="center">
    <p>
        <a href="https://github.com/haonan-li/CMMLU/">English</a> |
        <b>简体中文</b> 
    <p>
</h4>

论文：[CMMLU: Measuring Chinese Massive Multitask Language Understanding](https://arxiv.org/abs/2306.09212)
数据：[github](https://github.com/haonan-li/CMMLU/tree/master/data), [Hugging Face Hub](https://huggingface.co/datasets/haonan-li/cmmlu)


## 目录

- [简介](#introduction)
- [排行榜](#leaderboard)
- [数据格式](#data-format)
- [使用方法](#usage)
- [引用](#citation)
- [许可证](#license)

## 简介

CMMLU是一个综合性的中文评估套件，专门用于评估语言模型在中文语境下的高级知识和推理能力。CMMLU涵盖了广泛的主题，包括从基础到高级专业水平的67个主题。它包括需要计算专业知识的学科，如物理和数学，以及人文和社会科学学科。由于特定的语境细微差别和措辞，其中许多任务在其他语言中不容易翻译。此外，CMMLU中的许多任务具有中国特定的答案，可能在其他地区或语言中并不普遍适用或被认为是正确的。

<p align="center"> <img src="fig/logo.jpg" style="width: 85%;" id="title-icon">       </p>

## 排行榜

以下表格显示了模型在五次迭代和零次迭代设置中的表现。如果您想贡献您的模型结果，请与我们联系或提交拉取请求以更新本节。


#### 五次迭代

| 模型                 | STEM  | 人文学科 | 社会科学 | 其他  | 中国特定主题 | 平均分  |
|---------------------|------|------------|----------------|-------|----------------|---------|
| 多语言向 |
| [ChatGPT](https://openai.com/chatgpt)                             | **47.81** | **55.68** | **56.50** | **62.66** | **50.69** | **55.51** |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   33.33   |   43.46   |   44.28   |   44.75   |   39.46   |   41.45   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   34.47   |   40.24   |   41.55   |   42.88   |   37.00   |   39.80   |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   30.56   |   39.10   |   38.59   |   40.32   |   37.15   |   37.04   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   27.52   |   32.47   |   32.27   |   35.77   |   31.56   |   31.88   |
| 中文向 |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.35   | **39.22** | **39.65** |   38.62   | **37.70** | **37.48** |
| [BatGPT-15B]()                                                    | **33.49** |   35.38   |   36.31   | **42.14** |   37.00   |   36.72   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   27.12   |   33.18   |   34.87   |   35.10   |   32.97   |   32.63   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   27.23   |   30.41   |   28.84   |   32.56   |   28.68   |   29.57   |
| [Chinese-GLM-10B](https://github.com/THUDM/GLM)                   |   25.49   |   27.05   |   27.42   |   29.21   |   28.05   |   27.26   |
| Random              | 25.00 | 25.00      | 25.00          | 25.00 | 25.00          | 25.00   |


#### 零次迭代
| 模型                 | STEM  | 人文学科 | 社会科学 | 其他  | 中国特定主题 | 平均分  |
|---------------------|------|------------|----------------|-------|----------------|---------|
| 多语言向 |
| [ChatGPT](https://openai.com/chatgpt)                             | **44.80** | **53.61** | **54.22** | **59.95** | **49.74** | **53.22** |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   33.03   |   45.74   |   45.74   |   46.25   |   41.58   |   42.80   |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   31.11   |   41.30   |   40.87   |   40.61   |   36.05   |   38.50   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   31.09   |   34.45   |   36.05   |   37.94   |   32.89   |   34.88   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   26.46   |   29.36   |   31.81   |   31.55   |   29.17   |   30.06   |
| 中文向 |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.22   | **42.91** | **44.81** |   42.60   | **41.93** | **40.79** |
| [BatGPT-15B]()                                                    | **33.72** |   36.53   |   38.07   | **46.94** |   38.32   |   38.51   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   26.76   |   26.57   |   27.42   |   28.33   |   26.73   |   27.34   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   25.68   |   26.35   |   27.21   |   27.92   |   26.70   |   26.88   |
| [Chinese-GLM-10B](https://github.com/THUDM/GLM)                   |   25.57   |   25.01   |   26.33   |   25.94   |   25.81   |   25.80   |
| Random              | 25.00 | 25.00      | 25.00          | 25.00 | 25.00          | 25.00   |

## 数据格式
数据集中的每个问题都是一个多项选择题，有4个选项，只有一个选项是正确答案。数据以逗号分隔的.csv文件形式存在。数据可以在以下位置找到：
这里是数据格式的示例：

```
    同一物种的两类细胞各产生一种分泌蛋白，组成这两种蛋白质的各种氨基酸含量相同，但排列顺序不同。其原因是参与这两种蛋白质合成的,tRNA种类不同,同一密码子所决定的氨基酸不同,mRNA碱基序列不同,核糖体成分不同,C
```
## 使用方法
要在您的项目中使用我们的代码，请将存储库克隆到本地计算机：

```shell
    git clone https://github.com/haonan-li/CMMLU.git
    cd CMMLU/src
```
## 数据
我们根据每个主题在[data/dev](https://github.com/haonan-li/CMMLU/data/dev)和[data/test](https://github.com/haonan-li/CMMLU/data/test)目录中提供了开发和测试数据集。

## 提示
我们在src/mp_utils目录中提供了预处理代码。其中包括我们用于生成直接回答提示和思路链 (COT) 提示的方法。

以下是添加直接回答提示后的数据示例：

```
    以下是关于(高中生物)的单项选择题，请直接给出正确答案的选项。
    题目：同一物种的两类细胞各产生一种分泌蛋白，组成这两种蛋白质的各种氨基酸含量相同，但排列顺序不同。其原因是参与这两种蛋白质合成的：
    A. tRNA种类不同
    B. 同一密码子所决定的氨基酸不同
    C. mRNA碱基序列不同
    D. 核糖体成分不同
    答案是：C

    ... [其他例子] 

    题目：某种植物病毒V是通过稻飞虱吸食水稻汁液在水稻间传播的。稻田中青蛙数量的增加可减少该病毒在水稻间的传播。下列叙述正确的是：
   
    A. 青蛙与稻飞虱是捕食关系
    B. 水稻和病毒V是互利共生关系
    C. 病毒V与青蛙是寄生关系
    D. 水稻与青蛙是竞争关系
    答案是： 
```

对于思路链提示，我们将提示从“请直接给出正确答案的选项”修改为“逐步分析并选出正确答案”。

#### 评估
我们使用的每个模型的评估代码位于[src](https://github.com/haonan-li/CMMLU/src)中，运行它们的代码列在[script](https://github.com/haonan-li/CMMLU/script)目录中。

## 引用

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
## 许可证

CMMLU数据集采用
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
