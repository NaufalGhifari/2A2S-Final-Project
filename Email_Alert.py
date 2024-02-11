import os
from dotenv import load_dotenv
import smtplib

class email_alert_system:
    def __init__(self):

        # sensitive information are stored in .env
        load_dotenv()
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.app_password = os.getenv("EMAIL_PASS")
        
    def send_alert(self, recipient, flag, timestamp):
        """
        Send an email to alert the user on motion detection or object detction.
        CAUTION: Sending emails using send_alert() may lead to the sender account being disabled (Google account TOS).
        """
        
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_conn:
            # identifies with mail server
            smtp_conn.ehlo()

            # encrypt using tls encryption
            smtp_conn.starttls()
            smtp_conn.ehlo() # re-identify with encrypted connection

            # login
            smtp_conn.login(self.email_address, self.app_password)

            # write email message depending on the flag
            flag = flag.lower()
            
            if flag == "motion":
                subject = "[2A2S Notification] Motion detection"
                body = f"Motion was detected at {timestamp}"
                
            elif flag == "object":
                subject = "[2A2S ALERT] Object detection"
                body = f"Objects detected at {timestamp} include: [...]"
            
            else:
                raise ValueError("Invalid flag value. Must be 'motion' OR 'object'.")
                
            # send
            message = f"Subject: {subject}\n\n{body}"
            smtp_conn.sendmail(self.email_address, recipient, message)
    
    def send_alert_cli(self, flag, timestamp):
        """
        This function serves to emulate sending an email and print to terminal instead of sending an actual email.
        """
        
        if flag == "motion":
            subject = "[2A2S Notification] Motion detection"
            body = f"Motion was detected at {timestamp}"
            
        elif flag == "object":
            subject = "[2A2S ALERT] Object detection"
            body = f"Objects detected at {timestamp} include: [...]"
        
        else:
            raise ValueError("Invalid flag value. Must be 'motion' OR 'object'.")
            
        # send
        message = f"Subject: {subject}\n\n{body}"
        print(message)