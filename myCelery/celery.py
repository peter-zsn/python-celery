# coding=utf-8
from celery import Celery

"""
celery 主文件
"""

# 创建celery 应用
app = Celery('test')
# # 引入celery配置参数， 详情见myCelery.celeryConfig文件
app.config_from_object("myCelery.celeryConfig")
