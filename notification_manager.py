# notification_manager.py
"""
notification_manager.py
manage email notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class NotificationManager:
    """email notification manager class"""
    
    def __init__(self):
        """initialize notification manager"""
        email_user = Config.EMAIL_USER
        email_pass = Config.EMAIL_PASS
        
        
        self.email_user: str = email_user # type: ignore
        self.email_pass: str = email_pass # type: ignore
    
    def send_email(self, message, recipient_emails):
        """
        send email notification to users
        
        parameters:
            message: 
            recipient_emails: list of recipient email addresses
        """
        if not recipient_emails:
            print(" No recipient emails provided. Skipping email notification.")
            return
        
        try:
            #  create email message
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = ", ".join(recipient_emails)
            msg["Subject"] = " Flight Price Notification"
            
            # attach the message body
            msg.attach(MIMEText(message, "plain", "utf-8"))
            
            # send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=self.email_user, password=self.email_pass)
                connection.send_message(msg)
            
            print(f" Email sended!")
            
        except Exception as e:
            print(f" Failed to send email: {e}")
