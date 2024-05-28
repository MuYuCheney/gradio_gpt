#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: B站 木羽Cheney
@Timie: 2024-05-27
@file: load_upload_files
@description: 
"""

from loguru import logger
import os
import pandas as pd

import config
from utils import generate_response_payload
from config import *

from vector_store.qdrant_store import file_to_vs

def load_file(file_upload_path):

    # 文件上传列表传递进来的是 List 数据格式
    # 初始化一个进行接收
    success_upload_file = []

    # 循环处理上传的文件
    for single_file in file_upload_path:
        # 判断文件后缀格式
        _, file_suffix = os.path.splitext(single_file)
        if file_suffix not in config.FILE_SUFFIX:
            return generate_response_payload(400, f"暂不支持该文件类型:{file_upload_path}")

        # 获取文件名称：
        file_name = os.path.basename(single_file)
        logger.info(f"读取到当前上传的文件名称为：{file_name}")

        # 将文件存入向量数据库
        file_to_vs(file_path=single_file, file_name=file_name)
        success_upload_file.append(single_file)

    return pd.DataFrame({'已上传的文件': success_upload_file})



