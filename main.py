#!/Users/noah/opt/anaconda3/envs/work/bin python
# -*- coding: utf-8 -*-

"""
# @File: main.py
# @Project: health-bot
# @Author: Cheng Zuo
# @Time: 5月 23, 2023
"""
import os
import gradio as gr
from fastapi import FastAPI
from typing import List, Tuple
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from chains import summarize_chain, qa_chain


CUSTOM_PATH = "/chat"
app = FastAPI(description="Health Chatbot")
vectordb = Chroma(persist_directory="./chroma", collection_name="health")
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def gen_summary(texts: List[str]) -> str:
    docs = [Document(page_content=f"用户提问：{t[0]}\nAI客服：{t[1]}") for t in texts]
    return summarize_chain.run(docs)


def get_qa(query: str, department: str) -> List[Document]:
    if department == "通用":
        docs = vectordb.similarity_search(query)
    else:
        docs = vectordb.similarity_search(query, filter={"source": department})

    return docs


def chat(inputs: str, department: str, history: List[Tuple[str, str]]):
    history = history or []
    docs = get_qa(inputs, department)
    try:
        output = qa_chain.run(input_documents=docs, human_input=inputs)
    except Exception as e:
        output = e
    history += [(inputs, output)]
    return history, history, docs


with gr.Blocks(css="style.css", title="ChatGPT") as demo:
    gr.Markdown("""<h1><center>医疗问答聊天机器人 Demo</center></h1>""")
    scenario = gr.Dropdown(choices=["儿科", "内科", "外科", "妇产科", "男科", "肿瘤科", "通用"], value="通用", label="请选择科室")
    with gr.Row():
        chatbot1 = gr.Chatbot(elem_id="chatbot", show_label=False).style(color_map=("blue", "green"))
        retrieved_docs = gr.Textbox(label="检索的相似问答")
    state = gr.State([])
    message = gr.Textbox(placeholder="请在此处输入", label="输入: ")
    message.submit(chat, inputs=[message, scenario, state], outputs=[chatbot1, state, retrieved_docs])

    submit = gr.Button("提交")
    submit.click(chat, inputs=[message, scenario, state], outputs=[chatbot1, state, retrieved_docs])

    summarize = gr.Button("生成摘要")
    summary = gr.Textbox(label="摘要", interactive=False)
    summarize.click(gen_summary, inputs=[state], outputs=[summary])


@app.get("/")
def read_main():
    return {"message": "Please refer to /chat page."}


demo.queue()
app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)
