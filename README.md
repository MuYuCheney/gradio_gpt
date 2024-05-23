# 1. 项目介绍

- 基于 Gradio 实现了一个静态的类GPT Playground 页面

    - Gradop Docs:官https://www.gradio.app/docs/interface
    - GPT Playground 源地址：https://platform.openai.com/playground/chat?models=gpt-3.5-turbo-16k
- 新增功能点：
  - v2.0：在输入框输入内容，点击提交按钮后，能够连接OpenAI的GPT模型，将输入的Query送入大模型，得到回复，并返回到前端

# 2. 环境配置

- 创建Python虚拟环境并安装依赖

   - pip install gradio==4.31.5
   - pip install openai
   - pip install logru

- 修改配置项：
  - 在config配置文件中填写正确的OpenAI Keys
    
# 3. 项目启动

- python main.py
- 打开地址访问：http://127.0.0.1:7865

