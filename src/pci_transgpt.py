import json
import time
import logging
import requests

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

if __name__ == '__main__':
    usr_prompt = "水的沸点是多少？"

    print(">", usr_prompt)

    asis_response = pci_generate(usr_prompt)

    print(">", asis_response)
