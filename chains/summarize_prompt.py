#!/Users/noah/opt/anaconda3/envs/work/bin python
# -*- coding: utf-8 -*-

"""
# @File: summarize_prompt.py
# @Project: health-bot
# @Author: Cheng Zuo
# @Time: 5月 23, 2023
"""
from langchain import PromptTemplate


summarize_template = """请针对用户和AI客服关于病情的对话记录，了解患者的基本信息，包括病情、症状等，总结患者的基本情况和需求，以及AI客服的答复，供医生查看。
你可以总结有关儿科，妇产科，男科，内科，外科，肿瘤科的对话记录。如果对话记录与上述内容不相关，则告知用户你能够总结的范围。
对话记录用---隔开

---
{text}
---

SUMMARY:"""

summarize_prompt = PromptTemplate(template=summarize_template, input_variables=["text"])
