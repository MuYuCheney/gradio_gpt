#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 绑定点击事件的函数
"""

from gpt_chat_handler import create_chat_response
from loguru import logger
from vector_store.qdrant_store import query_retrival
import gradio as gr

def llm_reply(chat_mode_radio,
              file_upload_path_dataframe,
              chat_history,
              user_input,
              model,
              temperature,
              max_tokens,
              frequency_penalty,
              presence_penalty,
              stream,
              ):
    logger.info(f"\n用户输入：{user_input},"
                f"\n模型：{model},"
                f"\n温度：{temperature}"
                f"\n最大输入Token：{max_tokens}"
                f"\n惩罚频率：{frequency_penalty}"
                f"\n惩罚值：{presence_penalty}"
                f"\n是否流式输出：{stream}")

    # messages = [{"role": "user", "content": user_input}]
    # 因为有了前置处理，所以这里不需要重置
    # chat_history.append([user_input, None])

    # 初始化 messages 为空列表
    messages = []


    # 在这里判断 是哪种对话模式
    if chat_mode_radio == "普通对话":
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

    else:
        # 这里是文档问答
        current_file_list = file_upload_path_dataframe['已上传的文件'].values.tolist()

        # 根据用户的输入去数据库中检索
        file_prompt = query_retrival(user_input, current_file_list, chat_history)


        if file_prompt:
            messages.append({"role": "user", "content": file_prompt})
        else:
            logger.error("生成 user_prompt 失败")
            messages = []


    # 去调用大模型
    gpt_reponse = create_chat_response(messages, model, temperature, max_tokens, frequency_penalty, presence_penalty,
                                       stream)

    if stream:
        # 流式输出
        chat_history[-1][1] = ""
        for chunk in gpt_reponse:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                chat_history[-1][1] += chunk_content
                yield chat_history, ""
    else:
        chat_history[-1][1] = gpt_reponse
        logger.info(f"对话历史: {chat_history}")
        yield chat_history, ""



def show_user_input(chat_history, user_input):

    # 初始化
    chat_history = [] if not chat_history else chat_history

    # 检查输入
    if not user_input:
        gr.Warning("您必须输入需要提问的问题")
        return chat_history

    # 展示对话消息
    chat_history.append([user_input, None])

    return chat_history

def generate_response_payload(status_code, message=None, payload=None):
    """
    创建一个包含状态码、消息和负载数据的结构化字典，用于表示函数执行的结果。

    参数:
    - status_code (int): 表示执行结果的状态码，通常用于指示成功、失败等状态。
    - message (str, optional): 提供有关执行结果的详细描述性消息，可以为空。
    - payload (any type, optional): 附加数据，可以是任何类型的对象，用于提供更多上下文信息。

    返回:
    dict: 包含状态码、消息和负载数据的字典对象。
}
    """
    response = {
        'status_code': status_code,
        'message': message,
        'payload': payload
    }
    return response
