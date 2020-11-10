import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from accounts.enums import *


def sending_email(validation, receiver, sender=Email.EMAIL_ADDRESS.value, sender_password=Email.PASSWORD.value):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = 'subject'
        message["From"] = sender
        message["To"] = receiver

        # Create the plain-text (it isn't force to use it) and HTML version of your message
        html = """\
                <html>
                  <body>
                    <p>planB email verification link<br>
                       <br> your code :
                        """ + validation + """<br/>
                    </p>
                  </body>
                </html>
                """
        # Turn these into plain/html MIMEText objects
        part = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, sender_password)
            server.sendmail(
                sender, receiver, message.as_string()
            )
    except:
        return {'message': 'try again.'}
