# Sending Email Agent -> send_email

import smtplib          # This module defines an SMTP client session object that can be used to send mail to any Internet machine 
from email.mime.multipart import MIMEMultipart      # This module provides a way to create MIME objects of the multipart/* type. It is used to combine multiple parts (like text and attachments) into a single email message.
from email.mime.text import MIMEText                # This module provides a way to create MIME objects of the text/* type. It is used to represent the text content of an email message.
from langchain.tools import tool

# 1. Define configuration variables
smtp_server = "smtp.gmail.com"
smtp_port = 587              
sender_email = "youremail@gmail.com"
password = "your gmail app password" 


# 2. Define a function to send email using Gmail's SMTP server:
def send_email_by_gmail(to:str, subject:str, body_text:str):
    message = MIMEMultipart()           # Create a "MIMEMultipart" object to represent the email message. This allows us to include multiple parts (like text and attachments) in the email.
    message["From"] = sender_email      # Set the "From" field of the email message to the sender's email address.
    message["To"] = to                  # Set the "To" field of the email message to the recipient's email address.
    message["Subject"] = subject        # Set the "Subject" field of the email message to the provided subject line.

    message.attach(MIMEText(body_text, "plain"))    # Attach the body text to the email message as a plain text MIME part. This allows the recipient to read the email content.


# 3. Establish a connection to the SMTP server and send the email:
    try:    
        server = smtplib.SMTP(smtp_server, smtp_port)       # Create an SMTP client session object with the specified SMTP server and port. This establishes a connection to the Gmail SMTP server.
        server.starttls()           # This creates a secure connection to the SMTP server using TLS (Transport Layer Security). 
    
        server.login(sender_email, password)        # This logs in to the SMTP server using the sender's email address and password. 
        
        server.sendmail(sender_email, to, message.as_string())      # THis will send the email message to the recipient's email address using the SMTP server.
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 6. Clean up and close connection safely
        server.quit()


# 4. Define a tool function to send email using the above function:
@tool
def send_email(to:str, subject:str, body:str):
    """
     Send Email to any email address by providing the correct email address, subject and body.
     Args:
        to - email address
        subject - email subject in one line
        body - email body in plane text
    """
    send_email_by_gmail(to, subject, body_text=body)
    return "Email Send Successfully..."

ALL_TOOLS = [send_email]