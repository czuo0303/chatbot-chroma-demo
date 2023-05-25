# -*- coding: utf-8 -*-

"""
# @File: dataloader.py
# @Project: health-bot
# @Author: Cheng Zuo
# @Time: 5月 23, 2023
"""
import os
import random
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from utils.config import config

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma"
))
collection = client.get_or_create_collection("health")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

files = os.listdir(config["data_path"])
for file in files:
    if not file.endswith("txt"):
        continue
    documents = []
    questions = []
    fname = file.split(".")[0]
    fpath = os.path.join(config["data_path"], file)
    with open(fpath) as f:
        data = f.readlines()
    # 内存不足，每科随机保存10000条
    random.shuffle(data)
    for line in data[:10000]:
        split_text = line.strip().split(",")
        if len(split_text) != 4:
            continue
        dpt, title, question, answer = split_text
        documents.append(f"用户提问：{question}\n医生回答：{answer}")
        questions.append(question)

    # 只用问题做embedding
    embeddings = sentence_transformer_ef(questions)
    metadatas = [{"source": fname}] * len(documents)
    ids = [f"doc{i}" for i in range(len(documents))]
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
