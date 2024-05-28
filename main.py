#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 木羽Cheney
@Date: 2024-05-23
@Description: 版本v6：增加RAG文件对话
"""

import gradio as gr
from utils import llm_reply, show_user_input
from config import LLM_MODELS
import pandas as pd
from file_process.load_upload_files import load_file

"""
需求1：优化前端页面
      - 添加系统名称
      - 调整页面排布样式
需求2：优化用户体验
      - 当点击提交按钮后，用户的输入先行输出在Chatbot中
      - 当点击提交按钮后，输入框的内容置空
"""


with gr.Blocks() as demo:
    # 标题行
    gr.Markdown("&#8203;")  # 这里添加一个透明的空字符作为间隔
    gr.Markdown("""
    <h1 style='text-align: center; 
               color: #333; 
               font-size: 40px; 
               text-shadow: 2px 2px 4px #AAA;
               background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet); 
               -webkit-background-clip: text; 
               -webkit-text-fill-color: transparent;'>
    欢迎使用智能对话系统
    </h1>
    """)
    gr.Markdown("&#8203;")  # 这里添加一个透明的空字符作为间隔

    with gr.Row(equal_height=True):
        # 左侧对话栏
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="智能聊天机器人", height=820, bubble_full_width=False)
            user_input = gr.Textbox(label="输入框", placeholder="您好，请在这里输入你的问题")
            with gr.Row():
                user_submit = gr.Button("提交")
                clear = gr.Button("清除")


        # 右侧参数栏
        with gr.Column(scale=1):
            chat_mode_radio = gr.Radio(
                choices=[
                    "普通对话",
                    "文档问答"],
                label="对话模式",
                value="普通对话",)

            model_dropdown = gr.Dropdown(
                choices=LLM_MODELS,
                value=LLM_MODELS[0],
                label="选择模型",
                interactive=True
            )

            stream_radio = gr.Radio(label="是否采用流式输出",
                                    choices=[True, False],
                                    value=True,
                                    )

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
            file_upload_path_dataframe = gr.Dataframe(value=pd.DataFrame({'已完成上传': []}), height=100)


            temperature_slider = gr.Slider(label="Temperature",
                                           minimum=0,
                                           maximum=2,
                                           value=0.8,
                                           )
            maximum_token_slider = gr.Slider(label="Max_tokens",
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
            fn=show_user_input,
            inputs=[chatbot, user_input],
            outputs=[chatbot],

        ).then(
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
            outputs=[chatbot, user_input]
        )

        clear.click(lambda: None, None, chatbot, queue=False)

        # 绑定用户上传事件
        file_upload_path.upload(
            fn=load_file,
            inputs=[file_upload_path],
            outputs=[file_upload_path_dataframe]
        )

if __name__ == '__main__':

    demo.queue().launch()
