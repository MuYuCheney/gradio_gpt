#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 绑定点击事件的函数
"""


from gpt_chat_handler import create_chat_response


def llm_reply(user_input):
    messages = [{"role": "user", "content": user_input}]
    # 调用大模型
    gpt_reponse = create_chat_response(messages)

    # chabot 接收的是列表形式的输入
    return [[user_input, gpt_reponse]]