# -*- coding: utf-8 -*-

"""
# @File: gunicorn.conf.py
# @Project: health-bot
# @Author: Cheng Zuo
# @Time: 5月 24, 2023
"""
import multiprocessing

# ip和端口
bind = "0.0.0.0:8000"
# 并行进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
# 使用uvicorn的worker
worker_class = "uvicorn.workers.UvicornWorker"
# 每个worker的线程数
threads = 1
# 等待服务的client数量
backlog = 128
# 超过多少秒后重新启动
timeout = 30
# 最大并发
worker_connections = 1000
daemon = False
debug = False
# 日志等级
loglevel = "info"
# 记录打印信息
capture_output = True
# 进程文件目录
pidfile = "./pid/gunicorn.pid"
# 访问日志文件
accesslog = "./logs/access.log"
# 错误日志文件
errorlog = "./logs/error.log"
# 预加载资源
preload_app = True
autorestart = True
reload = True
# 日志格式
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" " "%(a)s"'
