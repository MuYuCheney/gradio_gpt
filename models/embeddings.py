#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: B站 木羽Cheney
@Timie: 2024-05-27
@file: embeddings
@description: 
"""

from openai import OpenAI
from config import openai_api_key

def get_embeddings(input):
    """

    :param self:
    :param input:
    :return:
    """

    client = OpenAI(api_key=openai_api_key)
    response = client.embeddings.create(
        input=input,
        model='text-embedding-ada-002',
    )
    embeddings = [data.embedding for data in response.data]
    return embeddings