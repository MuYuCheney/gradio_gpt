# 版本一：实现一个静态的智能对话机器人的Gradio前端页面

import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        # 左侧对话栏
        with gr.Column():
            gr.Chatbot(label="智能聊天机器人")
            gr.Textbox(label="输入框", placeholder="您好，请在这里输入你的问题")
            with gr.Row():
                gr.Button("提交")
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

demo.launch()

