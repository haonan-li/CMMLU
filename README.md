# CMMLU---中文多任务语言理解评估

<p align="center"> <img src="fig/banner_zh.jpg" style="width: 100%;" id="title-icon">       </p>

<h4 align="center">
    <p>
        <b>简体中文</b> |
        <a href="https://github.com/haonan-li/CMMLU/blob/master/README_EN.md">English</a> 
    <p>
</h4>

<p align="center" style="display: flex; flex-direction: row; justify-content: center; align-items: center">
📄 <a href="https://arxiv.org/abs/2306.09212" target="_blank" style="margin-right: 15px; margin-left: 10px">论文</a> • 
🏆 <a href="https://github.com/haonan-li/CMMLU/#排行榜" target="_blank"  style="margin-left: 10px">排行榜</a> •
🤗 <a href="https://huggingface.co/datasets/haonan-li/cmmlu" target="_blank" style="margin-left: 10px">数据集</a> 
</p>


## 简介

CMMLU是一个综合性的中文评估基准，专门用于评估语言模型在中文语境下的知识和推理能力。CMMLU涵盖了从基础学科到高级专业水平的67个主题。它包括：需要计算和推理的自然科学，需要知识的人文科学和社会科学,以及需要生活常识的中国驾驶规则等。此外，CMMLU中的许多任务具有中国特定的答案，可能在其他地区或语言中并不普遍适用。因此是一个完全中国化的中文测试基准。

<p align="center"> <img src="fig/logo.jpg" style="width: 85%;" id="title-icon">       </p>

## 排行榜

以下表格显示了模型在 five-shot 和 zero-shot 下的表现。如果您想贡献您的模型结果，请与我们联系或直接提交拉取请求。


#### Five-shot

| 模型                 | STEM  | 人文学科 | 社会科学 | 其他  | 中国特定主题 | 平均分  |
|---------------------|------|------------|----------------|-------|----------------|---------|
| 多语言向 |
| [GPT4](https://openai.com/gpt4)                                   | **65.23** | **72.11** | **72.06** | **74.79** | **66.12** | **70.95** |
| [ChatGPT](https://openai.com/chatgpt)                             |   47.81   |   55.68   |   56.50   |   62.66   |   50.69   |   55.51   |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   33.33   |   43.46   |   44.28   |   44.75   |   39.46   |   41.45   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   34.47   |   40.24   |   41.55   |   42.88   |   37.00   |   39.80   |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   30.56   |   39.10   |   38.59   |   40.32   |   37.15   |   37.04   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   27.52   |   32.47   |   32.27   |   35.77   |   31.56   |   31.88   |
| 中文向 |
| [KwaiYii-13B](https://github.com/kwai)                 | 46.54 | **69.22** |   **64.49**  | **65.09** |   **63.1**   | **61.73** |
| [Qwen-7B](https://github.com/QwenLM/Qwen-7B)                      | **48.39** | 63.77 |   61.22   | 62.14 |   58.73   |   58.66 |
| [MiLM-6B](https://github.com/XiaoMi/MiLM-6B/)                     |   46.85   |   61.12   | 61.68 |   58.84   | 59.39 |   57.17   |
| [Baichuan-13B](https://github.com/baichuan-inc/Baichuan-13B)      |   42.38   |   61.61   |   60.44   |   59.26   |   56.62   |   55.82   |
| [ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)           |   42.55   |   50.98   |   50.99   |   50.80   |   48.37   |   48.80   |
| [MiLM-1.3B](https://github.com/XiaoMi/MiLM-6B/)                   |   35.59   |   49.58   |   49.03   |   47.56   |   48.17   |   45.39   |
| [Baichuan-7B](https://github.com/baichuan-inc/baichuan-7B)        |   35.25   |   48.07   |   47.88   |   46.61   |   44.14   |   44.43   |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.35   |   39.22   |   39.65   |   38.62   |   37.70   |   37.48   |
| [BatGPT-15B](https://arxiv.org/abs/2307.00360)                    |   34.96   |   35.45   |   36.31   |   42.14   |   37.89   |   37.16   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   27.12   |   33.18   |   34.87   |   35.10   |   32.97   |   32.63   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   27.23   |   30.41   |   28.84   |   32.56   |   28.68   |   29.57   |
| Random                                                            |   25.00   |   25.00   |   25.00   |   25.00   |   25.00   |   25.00   |


#### Zero-shot
| 模型                 | STEM  | 人文学科 | 社会科学 | 其他  | 中国特定主题 | 平均分  |
|---------------------|------|------------|----------------|-------|----------------|---------|
| 多语言向 |
| [GPT4](https://openai.com/gpt4)                                   | **63.16** | **69.19** | **70.26** | **73.16** | **63.47** | **68.90** |
| [ChatGPT](https://openai.com/chatgpt)                             |   44.80   |   53.61   |   54.22   |   59.95   |   49.74   |   53.22   |
| [BLOOMZ-7B](https://github.com/bigscience-workshop/xmtf)          |   33.03   |   45.74   |   45.74   |   46.25   |   41.58   |   42.80   |
| [Falcon-40B](https://huggingface.co/tiiuae/falcon-40b)            |   31.11   |   41.30   |   40.87   |   40.61   |   36.05   |   38.50   |
| [LLaMA-65B](https://github.com/facebookresearch/llama)            |   31.09   |   34.45   |   36.05   |   37.94   |   32.89   |   34.88   |
| [Bactrian-LLaMA-13B](https://github.com/mbzuai-nlp/bactrian-x)    |   26.46   |   29.36   |   31.81   |   31.55   |   29.17   |   30.06   |
| 中文向 |
| [KwaiYii-13B](https://github.com/kwai)                            |   46.82   | **69.35** |   63.42   | **64.02** | **63.26** | **61.22** |
| [MiLM-6B](https://github.com/XiaoMi/MiLM-6B/)                     | **48.88** |   63.49   | **66.20** |   62.14   |   62.07   |   60.37   |
| [Qwen-7B](https://github.com/QwenLM/Qwen-7B)                      |   46.33   |   62.54   |   60.48   |   61.72   |   58.77   |   57.57   |
| [Baichuan-13B](https://github.com/baichuan-inc/Baichuan-13B)      |   42.04   |   60.49   |   59.55   |   56.60   |   55.72   |   54.63   |
| [MiLM-1.3B](https://github.com/XiaoMi/MiLM-6B/)                   |   40.51   |   54.82   |   54.15   |   53.99   |   52.26   |   50.79   |
| [ChatGLM2-6B](https://huggingface.co/THUDM/chatglm2-6b)           |   41.28   |   52.85   |   53.37   |   52.24   |   50.58   |   49.95   |
| [Baichuan-7B](https://github.com/baichuan-inc/baichuan-7B)        |   32.79   |   44.43   |   46.78   |   44.79   |   43.11   |   42.33   |
| [ChatGLM-6B](https://github.com/THUDM/GLM-130B)                   |   32.22   |   42.91   |   44.81   |   42.60   |   41.93   |   40.79   |
| [BatGPT-15B](https://arxiv.org/abs/2307.00360)                    |   33.72   |   36.53   |   38.07   |   46.94   |   38.32   |   38.51   |
| [Chinese-LLaMA-13B](https://github.com/ymcui/Chinese-LLaMA-Alpaca)|   26.76   |   26.57   |   27.42   |   28.33   |   26.73   |   27.34   |
| [MOSS-SFT-16B](https://github.com/OpenLMLab/MOSS)                 |   25.68   |   26.35   |   27.21   |   27.92   |   26.70   |   26.88   |
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
我们根据每个主题在[data/dev](https://github.com/haonan-li/CMMLU/tree/master/data/dev)和[data/test](https://github.com/haonan-li/CMMLU/tree/master/data/test)目录中提供了开发和测试数据集。

## 提示
我们在`src/mp_utils`目录中提供了预处理代码。其中包括我们用于生成直接回答提示和思路链 (COT) 提示的方法。

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
我们使用的每个模型的评估代码位于[src](https://github.com/haonan-li/CMMLU/tree/master/src)中，运行它们的代码列在[script](https://github.com/haonan-li/CMMLU/tree/master/script)目录中。

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
