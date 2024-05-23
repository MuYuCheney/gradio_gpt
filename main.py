#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 版本二：接收前端页面中的所有参数作为变量传递到的后端
"""

import gradio as gr
from utils import llm_reply
from config import LLM_MODELS

"""
需求1：在输入框输入内容，点击提交按钮后，能够连接OpenAI的GPT模型，将输入的Query送入大模型，得到回复，并返回到前端
需求2: 如何把前端的全部参数拿过来做成变量？
需求3：如何让大模型的对话具备记忆功能

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
            model_dropdown = gr.Dropdown(
                choices=LLM_MODELS,
                value=LLM_MODELS[0],
                label="LLM Model",
                interactive=True
            )
            temperature_slider = gr.Slider(label="Temperature",
                                           minimum=0,
                                           maximum=2,
                                           value=0.8,
                                           )
            maximum_token_slider = gr.Slider(label="Maximum Tokens",
                                             minimum=0,
                                             maximum=8192,
                                             value=4096,
                                             )
            frequency_penalty_slider = gr.Slider(label="Frequency penalty",
                                                 minimum=-2,
                                                 maximum=2,
                                                 value=0,
                                                 )
            presence_penalty_slider = gr.Slider(label="Presence penalty",
                                                minimum=-2,
                                                maximum=2,
                                                value=0,
                                                )
        # 用户点击事件
        user_submit.click(
            fn=llm_reply,
            inputs=[
                chatbot,
                user_input,
                model_dropdown,
                temperature_slider,
                maximum_token_slider,
                frequency_penalty_slider,
                presence_penalty_slider
            ],
            outputs=[chatbot]
        )

demo.launch()
