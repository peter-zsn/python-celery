# coding=utf-8
from myCelery.tasks import *
import time

# countdown 等待时间默认S， 执行任务。  （先接受任务，再等待，时间到了执行任务）
# 启动重试， 最大重试3次
relA = taskA.apply_async(args=(1, 2), countdown=0, retry=True, retry_policy={
    'max_retries': '3'
})
while not relA.ready():
    time.sleep(1)
    # print(relA.get(timeout=10))
print(relA.state)           # 查看任务的状态，若是不配置结果后端，一直为pending。
print(relA.id)              # 查看任务的id
#
relb = taskB.delay(1, 2, 3)
while not relb.ready():
    time.sleep(1)
print("b %s" % relb.result)     # 查看任务的结果，若是不保存结果后端，此项为None
