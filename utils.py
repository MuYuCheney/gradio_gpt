#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 绑定点击事件的函数
"""


from gpt_chat_handler import create_chat_response
from loguru import logger

def llm_reply(user_input,
              model,
              temperature,
              max_tokens,
              frequency_penalty,
              presence_penalty
              ):

    logger.info(f"\n用户输入：{user_input},"
                f"\n模型：{model},"
                f"\n温度：{temperature}"
                f"\n最大输入Token：{max_tokens}"
                f"\n惩罚频率：{frequency_penalty}"
                f"\n惩罚值：{presence_penalty}")

    messages = [{"role": "user", "content": user_input}]
    # 去调用大模型
    gpt_reponse = create_chat_response(messages, model, temperature, max_tokens, frequency_penalty, presence_penalty)

    # chabot 接收的是列表形式的输入
    return [[user_input, gpt_reponse]]