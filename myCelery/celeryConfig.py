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

# --------- task_acks_late，task_reject_on_worker_lost 同为true 保证消费者意外退出，任务不被消费，消费者重启后，继续执行 ---------
# 当worker进程意外退出时，task会被放回到队列中(警告：启用此功能可能会导致错误消息循环执行)，默认是False
task_reject_on_worker_lost = True

# 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
# task_time_limit = 60

# celery与borker的连接池连接数
broker_pool_limit = 10

# 每个worker执行了多少任务就会死掉，防止长时间运行内存泄漏， 建议每个worker最多执行一个任务就销毁
worker_max_tasks_per_child = 200

# (安装使用中，发现用topic， 部分版本的python，re的源码与celery的命名冲突，需要根据产生的错误信息进行修改)
default_exchange = Exchange("default", type="direct")           # direct完全匹配，直接转发对等的routing_key
taskA_exchange = Exchange("taskA", type="topic")                # topic 正则匹配。发送给匹配成功的routing_key
taskB_exchange = Exchange("taskB", type="direct")               # fanout 发送给与exchange 绑定的所有队列


# 定义默认队列，交换机，key
task_default_queue = "default"
task_default_exchange = "direct"
task_default_routing_key = ""

# 绑定交换机和队列
# delivery_mode参数(决定tasks发送到RabbitMQ后，是否存储到磁盘中)（celery默认使用２：持久化方式）：
# １表示rabbitmq不存储celery发送的tasks到磁盘,RabbitMQ重启后，任务丢失（建议使用这种方式）
# ２表示rabbitmq可以存储celery发送的tasks到磁盘，RabbitMQ重启后，任务不会丢失（磁盘IO资源消耗极大，影响性能）
task_queues = (
    Queue("default", default_exchange, routing_key="", delivery_mode=1),
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
