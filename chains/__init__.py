# -*- coding: utf-8 -*-

"""
# @File: __init__.py.py
# @Project: health-bot
# @Author: Cheng Zuo
# @Time: 5月 23, 2023
"""
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
from chains.summarize_prompt import summarize_prompt
from chains.qa_prompt import qa_prompt


load_dotenv()
summarize_chain = load_summarize_chain(llm=ChatOpenAI(temperature=0),
                                       chain_type="stuff",
                                       prompt=summarize_prompt)

memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")
qa_chain = load_qa_chain(llm=ChatOpenAI(temperature=0), chain_type="stuff", memory=memory, prompt=qa_prompt)
