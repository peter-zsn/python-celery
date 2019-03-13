# coding=utf-8
from celery import Task

class MyTask(Task):
    def get_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:6]
        return super(MyTask, self).gen_task_name(name, module)

    # 任务返回后， 处理程序调用。会自动调用
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        :param status: 当前任务状态
        :param retval:任务返回值/异常
        :param task_id:任务的唯一ID
        :param args:返回任务的原始参数
        :param kwargs:返回任务的原始关键字参数
        :return:
        """
        print('after_return', status, retval, task_id, args, kwargs)
        return super(MyTask, self).after_return(status, retval, task_id, args, kwargs, einfo)

    # 当任务失败时，这由工作人员运行
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        :param exc:任务引发的异常
        :param task_id:失败任务的唯一ID
        :return:
        """
        print('after_return', exc, task_id)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    # 这是在重试任务时由工作人员运行的
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        :param exc:发送到的异常retry()。
        :param task_id:重试任务的唯一ID。
        :param args:重试任务的原始参数。
        :param kwargs: 重试任务的原始关键字参数。
        :param einfo:ExceptionInfo 实例，包含回溯。
        :return:
        """
        return super(MyTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    # 任务成功执行，则由worker运行
    def on_success(self, retval, task_id, args, kwargs):
        """
        :param retval:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        print('after_return', retval, task_id, args, kwargs)
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)