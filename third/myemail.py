import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


class Email(object):

    @classmethod
    def send_email(cls, message, Subject, sender_show, recipient_show, to_addrs, cc_show=''):
        # :param message: str 邮件内容
        # :param Subject: str 邮件主题描述
        # :param sender_show: str 发件人显示，不起实际作用如："xxx"
        # :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
        # :param to_addrs: str 实际收件人
        # :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
        # 填写真实的发邮件服务器用户名、密码
        user = os.getenv('email_user')
        password = os.getenv('email_password')
        # 邮件内容
        msg = MIMEText(message, 'plain', _charset="utf-8")
        # 邮件主题描述
        msg["Subject"] = Subject
        # 发件人显示，不起实际作用
        msg["from"] = sender_show
        # 收件人显示，不起实际作用
        msg["to"] = recipient_show
        # 抄送人显示，不起实际作用
        msg["Cc"] = cc_show
        with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())

    @classmethod
    def send_attach_email(cls, message, Subject, sender_show, recipient_show,
                          to_addrs, cc_show='', attach_path='', encoding='utf-8-sig'):
        msg = MIMEMultipart()
        msg['From'] = sender_show
        msg['To'] = recipient_show
        msg['Subject'] = Header(Subject, 'utf-8')
        # 抄送人显示，不起实际作用
        msg["Cc"] = cc_show

        # 邮件正文内容
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open(attach_path, 'rb').read(), 'base64', encoding)
        att1["Content-Type"] = 'application/octet-stream'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = f'attachment; filename="{attach_path}"'
        msg.attach(att1)
        user = '1669738430@qq.com'
        password = 'vxhduzllgqfnjiif'
        with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())

    @classmethod
    def send_error_email(cls, error: str):
        subject = 'oa异常'
        # 显示发送人
        sender_show = 'oa打卡邮件'
        # 显示收件人
        recipient_show = 'wayn'
        # 实际发给的收件人
        to_addrs = "1669738430@qq.com"
        cls.send_email(error, subject, sender_show, recipient_show, to_addrs, cc_show='oa')
