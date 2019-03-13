# coding=utf-8
"""
发送邮件
"""
from email.mime.text import MIMEText
from email.header import Header
import smtplib

from myCelery.celery import app
from myCelery.Mytask import MyTask

@app.task(base=MyTask)
def send_mail(content=""):
    print("send_mail")
    smtphost = 'smtp.exmail.qq.com' # smtp服务器
    port = 465                      # smtp服务器端口
    sender = "***@tbkt.cn"     # 发件人
    pwd = "***"     # 邮箱密码
    receivers = ['***@163.com', '***@tbkt.cn']  # 收件人
    subject = "celery test"  # 主题
    content = content or "***"
    msg = MIMEText(content, 'plain', 'utf-8')   # 参数分别是邮件内容、文本格式、编码
    msg['from'] = Header(sender)          # 谁发
    msg['to'] = Header("celery_tasks_maintenance_group")  # 发给谁
    msg['subject'] = Header(subject)    # 邮件主题
    try:
        smtpObj = smtplib.SMTP_SSL(smtphost, port)  # SSL加密
        smtpObj.login(sender, pwd)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print("send mail successfully")
    except smtplib.SMTPException as e:
        print(e)
    return 1

if __name__ == '__main__':
    # 测试发送邮件
    content = '''
        秦时明月汉时关，万里长征人未还。
        但是龙城飞将在，不教胡马度阴山。
    '''
    send_mail(content=content)