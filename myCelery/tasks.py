# coding=utf-8

from myCelery.celery import app
from myCelery.Mytask import MyTask
import datetime

# work taskA, 建议给每个任务定义名字， 防止命名冲突. 默认是相对名称。
# default_retry_delay 默认重试时间
@app.task(base=MyTask, name="task.taskA")
def taskA(x, y):
    return x + y

# work taskB,
@app.task(name='task.taskB')
def taskB(x, y, z):
    return x + y + z
