#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 大模型交互函数
"""


from openai import OpenAI


def create_chat_response(messages):
    client = OpenAI()

    completion = client.chat.completions.create(
      model="gpt-4",
      messages=messages
    )

    return completion.choices[0].message.content


if __name__ == '__main__':
    messages = [{"role": "user", "content": "你好，我用来测试"}]
    response = create_chat_response(messages)
    print(response)