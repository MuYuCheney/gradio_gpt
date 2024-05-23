#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 绑定点击事件的函数
"""

from gpt_chat_handler import create_chat_response
from loguru import logger


def llm_reply(chat_history,
              user_input,
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

    # messages = [{"role": "user", "content": user_input}]

    # 用户消息在前端对话框展示
    chat_history.append([user_input, None])

    # 初始化 messages 为空列表
    messages = []
    # 如果对话历史长度超过1，则遍历历史记录构建 messages
    if len(chat_history) > 1:
        for user_msg, assistant_msg in chat_history:
            if user_msg is not None:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg is not None:
                messages.append({"role": "assistant", "content": assistant_msg})
    else:
        # 如果没有有效的历史记录，则直接使用用户输入
        messages = [{"role": "user", "content": user_input}]

    # 去调用大模型
    gpt_reponse = create_chat_response(messages, model, temperature, max_tokens, frequency_penalty, presence_penalty)

    chat_history[-1][1] = gpt_reponse
    logger.info(f"对话历史: {chat_history}")

    return chat_history


