
from html2text import html2text

from tornado_smtpclient.client import SMTPAsync

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Message:
    def __init__(self, subject, content, text_content = None):
        self.subject = subject
        self.content = content
        if text_content is None:
            self.text_content = html2text(content)
        else:
            self.text_content = text_content


class Mailer:
    def __init__(self, from_address, username, password):
        self.conn = SMTPAsync()
        self.username = username
        self.password = password
        self.from_address = from_address
    
    async def connect(self):
        await self.conn.connect("smtp.gmail.com", 587)
        await self.conn.starttls()
        await self.conn.login(self.username, self.password)
    
    __aenter__ = connect
    
    async def send(self, msg: Message, to: str):
        mime = MIMEMultipart('alternative')
        mime['Subject'] = msg.subject
        mime['From'] = self.from_address
        mime['To'] = to
        
        mime.attach(MIMEText(msg.text_content, 'plain'))
        mime.attach(MIMEText(msg.content, 'html'))
        
        self.conn.sendmail(self.from_address, to, mime.as_string())
    
    async def disconnect(self):
        self.conn.quit()
    
    def __aexit__(self, exc_type, exc, tb):
        self.disconnect()
