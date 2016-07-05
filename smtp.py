#本程序实现了在邮件中添加图片附件，并在邮件的html显示中引用附件中的图片；
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib

#对邮件头部信息的格式化
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = input('From: ')
password = input('Password: ')
to_addr = input('To: ')
smtp_server = input('SMTP server: ')

msg=MIMEMultipart('alternative')
msg.attach(MIMEText('<font color="red",size=80px,face="楷体">hello</font>\
	, send by Python...<br><img src="cid:0"/>', 'html', 'utf-8'))
msg.attach(MIMEText('hello, send by Python...', 'plain', 'utf-8'))
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

#将图片附加中附件上
with open('hello.bmp','rb') as f:
	mime=MIMEBase('image','bmp',filename='hello.bmp')
	#加上必要的头信息：
	mime.add_header('Content-Disposition', 'attachment', filename='hello.bmp')
	mime.add_header('Content-ID', '<0>')
	mime.add_header('X-Attachment-Id', '0')
	mime.set_payload(f.read())
	encoders.encode_base64(mime)
	msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
