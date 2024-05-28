#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: B站 木羽Cheney
@Timie: 2024-05-27
@file: mutli_file_process
@description: 
"""

import pdfplumber
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class MultiFile():
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name


    def file_to_chunks(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=20,
        )
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        docs = text_splitter.create_documents(texts, metadatas=metadatas)
        return docs



    @ staticmethod
    def load_pdf(file_path, file_name):
        """
        读取一整个PDF文件
        :param file_path:
        :param file_name:
        :return:
        """

        docs = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    doc = Document(
                        page_content=page_text,
                        metadata=dict(
                            {
                                "file_name": file_name,
                            },
                            **{
                                k: pdf.metadata[k]
                                for k in pdf.metadata
                                if isinstance(pdf.metadata[k], (str, int))
                            },
                        ),
                    )
                    docs.append(doc)
        return docs


