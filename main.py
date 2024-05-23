#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 版本二：在输入框输入内容，点击提交按钮后，能够连接OpenAI的GPT模型，将输入的Query送入大模型，得到回复，并返回到前端
"""

import gradio as gr
from utils import llm_reply

"""
需求1：在输入框输入内容，点击提交按钮后，能够连接OpenAI的GPT模型，将输入的Query送入大模型，得到回复，并返回到前端
"""

with gr.Blocks() as demo:
    with gr.Row():
        # 左侧对话栏
        with gr.Column():
            chatbot = gr.Chatbot(label="智能聊天机器人")
            user_input = gr.Textbox(label="输入框", placeholder="您好，请在这里输入你的问题")
            with gr.Row():
                user_submit = gr.Button("提交")
                gr.Button("清除")

        # 右侧参数栏
        with gr.Column():
            gr.Dropdown(
                choices=["gpt-4", "gpt-3.5"],
                value="gpt-4",
                label="LLM Model",
                interactive=True
            )
            gr.Slider(label="Temperature")
            gr.Slider(label="Maximum Tokens")
            gr.Slider(label="Frequency penalty")
            gr.Slider(label="Presence penalty")


        # 用户点击事件
        user_submit.click(
            fn=llm_reply,
            inputs=[user_input],
            outputs=[chatbot]
        )


demo.launch()