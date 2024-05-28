#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: B站 木羽Cheney
@Timie: 2024-05-27
@file: Qdrant
@description: 
"""

from qdrant_client import QdrantClient

from config import QDRANT_HOST, QDRANT_SIZE, QDRANT_POPT
from qdrant_client.http.models import Distance, VectorParams, Batch
from loguru import logger
from qdrant_client.http.exceptions import UnexpectedResponse  # 捕获错误信息
from file_process.mutli_file_process import MultiFile
from models.embeddings import get_embeddings
import os


class Qdrant_conn():

    def __init__(self, host=QDRANT_HOST, port=QDRANT_POPT):
        # 连接客户端
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_POPT)
        self.size = QDRANT_SIZE


    def get_collection_points_counts(self, collection_name):
        """
        检查集合是否存在。

        - 如果集合存在，返回该集合的 points_count （集合中确切的points_count）
        - 如果集合不存在，创建集合。
            - 创建集合成功，则返回 points_count （0: 刚创建完points_count就是0）
            - 创建集合失败，则返回 points_count （-1: 创建失败了，定义points_count为-1）
        :param collection_name:
        :return:
        """

        try:
            # 获取当前的集合信息
            collection_info = self.client.get_collection(collection_name=collection_name)
        except (UnexpectedResponse, ValueError) as e:
            if self.create_collection(collection_name):
                logger.success(f"创建一个新集合成功，集合的名称为:{collection_name}")
                return 0
            else:
                logger.error(f"创建一个新集合失败，错误信息为:{e}")
                return -1
        else:
            collect_points_count = collection_info.points_count
            logger.success(f"当前向量数据库中已有该集合:{collection_name}")
            return collect_points_count


    def create_collection(self, collection_name):
        """
        创建一个集合
        :param collection_name:
        :return:
        """
        return self.client.create_collection(collection_name=collection_name,
                                             vectors_config=VectorParams(size=self.size, distance=Distance.COSINE))


    def add_points(self, collection_name, vectors, payloads):
        # 执行数据插入过程
        self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=Batch(
                ids=list(range(1, len(vectors) + 1)),
                payloads=payloads,
                vectors=vectors
            )
        )
        return True


    def search(self, collection_name, query_vector, limit=3):
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

def file_to_vs(file_path, file_name):

    # 在往集合中插入信息的时候，是不是先需要判断是否已经存在该集合？

    # 1. 创建一个Qdrant 实例
    qdrant = Qdrant_conn()

    # 2. 查询一下当前集合中是否有数据
    collect_points_count = qdrant.get_collection_points_counts(file_name)

    # 说明是新进来的文件，需要存储Chunk
    if collect_points_count == 0:

        # 加载文件的全部内容（pdf）
        docs = MultiFile.load_pdf(file_path, file_name)

        # 切分成Chunks
        multi_file = MultiFile(file_path, file_name)
        docs = multi_file.file_to_chunks(docs)

        # 构造Qdrant的payloads
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]

        payloads = [
            {
                "page_content": text,
                "metadata": metadata,
            }
            for text, metadata in zip(texts, metadatas)
        ]

        # 向量化
        embeddings = get_embeddings(texts)

        # 插入向量数据库中的Collection中
        if qdrant.add_points(file_name, embeddings, payloads):
            return file_path

    elif collect_points_count > 0:
        return file_path

    else:
        return ""



def query_retrival(user_input, collection_names, chat_history):

    # 先获取用户的Embedding
    query_embedding = get_embeddings(user_input)

    # 实例化向量数据库

    qdrant = Qdrant_conn()

    # 去向量数据库中检索
    similarity_points = []

    for collection_name in collection_names:
        file_name = os.path.basename(collection_name)

        scored_points_by_current_collection = qdrant.search(
            file_name, query_embedding[0], )
        similarity_points.extend(scored_points_by_current_collection)

    # 将 ScoredPoint 对象列表转换为字典列表
    points = []
    for scored_point in similarity_points:
        point = {
            "id": scored_point.id,
            "score": scored_point.score,
            "payload": scored_point.payload
        }
        points.append(point)

    # 字典列表按分数降序排序
    points.sort(key=lambda x: x['score'], reverse=True)
    points = points[:3]

    # 构建上下文
    contexts = []
    for index, point in enumerate(points, start=1):
        # 获取每个点的页面内容
        context = point['payload']['page_content']
        # 为每个段落添加标题，如 "背景信息 1"
        titled_context = f"## 背景信息 {index}\n{context}"
        contexts.append(titled_context)

    # 使用两个换行符将所有段落连接成一个字符串
    context = "\n\n".join(contexts)

    chat_history_str = ""
    for chat in chat_history[:-1]:
        # 检查是否是用户消息
        if chat[0]:
            chat_history_str += f'user:{chat[0]}\n'
        if chat[1]:
            chat_history_str += f'assistant:{chat[1]}\n'
    chat_history_str = chat_history_str[:-1]  # 去掉最后一个'\n'


    # 构建 prompt
    prompt = f"""你善于根据文档内容和历史对话进行分析总结，可以基于`文档内容`和`对话历史`回答user的问题。但请注意：如果user提出的问题与`文档内容`无关，你可以不参考`文档内容`直接进行回答。

文档内容：```
{context}```

对话历史：```
{chat_history_str}```

user: ```{user_input}```
assistant: """

    return prompt
