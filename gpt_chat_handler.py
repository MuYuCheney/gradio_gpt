#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 大模型交互函数
"""


from openai import OpenAI
from config import openai_api_key


def create_chat_response(messages,
                         model,
                         temperature=0.8,
                         max_tokens=1024,
                         frequency_penalty=0,
                         presence_penalty=0
                         ):
    client = OpenAI(api_key=openai_api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return completion.choices[0].message.content


if __name__ == '__main__':
    messages = [{"role": "user", "content": "你好，我用来测试"}]
    response = create_chat_response(messages)
    print(response)
