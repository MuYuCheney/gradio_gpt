#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 版本v6：增加RAG文件对话
"""

import gradio as gr
from utils import llm_reply
from config import LLM_MODELS
import pandas as pd
from file_process.load_upload_files import load_file

"""
<<<<<<< HEAD
需求1：在输入框输入内容，点击提交按钮后，能够连接OpenAI的GPT模型，将输入的Query送入大模型，得到回复，并返回到前端
需求2: 如何把前端的全部参数拿过来做成变量？
需求3：如何让大模型的对话具备记忆功能？
需求4：功能优化
    - 如何添加流式输出
    - 
=======
需求1：前端增加文件上传按钮
需求2: 前端增加普通对话与文档对话两种模式
需求3：添加Qdrant向量数据库
      - 创建集合功能
      - 向集合添加数据功能
      - 检索功能
需求4：添加基于LangChain的文档切分过程
需求5：构建RAG的对话Prompt
>>>>>>> new-feature-branch
    

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

            chat_mode_radio = gr.Radio(
                choices=[
                    "普通对话",
                    "文档问答"],
                label="对话模式",
                value="普通对话",
                interactive=True)

            # 添加文件上传按钮
            file_upload_path = gr.Files(
                label="请在这里上传你的文件",
                file_types=[  # 要上传的文件扩展名或文件类型列表
                    ".pdf",
                ],

                # 允许用户上传多个文件
                file_count="multiple",
            )

            # 显示上传成功的文件
            file_upload_path_dataframe = gr.Dataframe(
                value=pd.DataFrame({'已完成上传': []}))


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

            stream_radio = gr.Radio(label="Stream",
                                    choices=[True, False],
                                    value=False,
                                    )
        # 用户点击事件
        user_submit.click(
            fn=llm_reply,
            inputs=[
                chat_mode_radio,
                file_upload_path_dataframe,
                chatbot,
                user_input,
                model_dropdown,
                temperature_slider,
                maximum_token_slider,
                frequency_penalty_slider,
                presence_penalty_slider,
                stream_radio,
            ],
            outputs=[chatbot]
        )


        # 绑定用户上传事件
        file_upload_path.upload(
            fn=load_file,
            inputs=[file_upload_path],
            outputs=[file_upload_path_dataframe]
        )

demo.launch()
