# coding=utf-8

from kombu import Queue, Exchange
from celery.schedules import crontab
from datetime import timedelta

# broker中间人地址， 可用redis或rabbitmq, 下面用rabbitmq中间人和结果存放设置
broker_url = "amqp://{}:{}@{}:{}".format("guest", "guest", "192.168.7.142", "5672")
result_backend = "amqp://{}:{}@{}:{}".format("guest", "guest", "192.168.7.142", "5672")

# # redis 连接方式， 中间人和结果存放设置
# broker_url = "redis://root:jxtbkt2013!@192.168.7.250:6379/1"
# result_backend = "redis://root:jxtbkt2013!@192.168.7.250:6379/1"

# 指定时区，默认是utc
timezone = 'Asia/Shanghai'
enable_utc = True

# 结果后端不起作用，或者一直处于pending状态
# task_ignore_result = True

# 序列化方法的字符串
task_serializer = 'json'

# 读取任务结果, 一般性能要求不高，所以使用可读性更好的JSON
result_serializer = 'json'

# 只有当worker完成了这个task时，任务才被标记为ack状态. 注意：这意味着如果工作程序在执行过程中崩溃，任务可能会多次执行
task_acks_late = True

# (安装使用中，发现用topic， 部分版本的python，re的源码与celery的命名冲突，需要根据产生的错误信息进行修改)
default_exchange = Exchange("default", type="direct")           # direct完全匹配，直接转发对等的routing_key
taskA_exchange = Exchange("taskA", type="topic")                # topic 正则匹配。发送给匹配成功的routing_key
taskB_exchange = Exchange("taskB", type="direct")               # fanout 发送给与exchange 绑定的所有队列


# 定义默认队列，交换机，key
task_default_queue = "default"
task_default_exchange = "direct"
task_default_routing_key = ""

# 绑定交换机和队列
task_queues = (
    Queue("default", default_exchange, routing_key=""),
    Queue("task_A", taskA_exchange, routing_key="task.#"),          # 路由键以task.开头的进入task_A队列
    Queue("task_B", taskB_exchange, routing_key="btask"),          # 路由是btask的进入task_B队列
)

# 路由配置
# work taskA 使用task_A队列
task_routes = {
    'myCelery.tasks.taskA': {
        'queue': 'task_A',
        'routing_key': 'task.A'
    },
    'myCelery.tasks.taskB': {
        'queue': "task_B",
        'routing_key': 'btask'
    },
}

# 定时任务， 不支持windows系统， 启动命令加-B
beat_schedule = {
    'send_mail': {
        'task': 'myCelery.send_mail.send_mail',
        'schedule': crontab(hour=18, minute=0),             # 每天18点执行
        'args': ("下班了！！！",),
        'options': {'queue': 'default'}
    }
}

# # 注册tasks
imports = (
    "myCelery.tasks",
    "myCelery.send_mail"
)
