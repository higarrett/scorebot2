import sys
import logging
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.header import Header
import time
import uuid
from tabnanny import check

result_smtp = ()
result_imap = ()


def send_email(smtp_server, smtp_port, username, password, recipient, subject):
    # Create a MIMEText message
    msg = MIMEText('This is a test email.', 'plain', 'utf-8')
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, [recipient], msg.as_string())
            print("Email sent successfully.")
            result_smtp = True
            return True
    except Exception as e:
        print(f"Failed to send email")
        return False

def check_inbox(imap_server, username, password, subject):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select('inbox')
        # Search for the email by subject
        status, data = mail.search(None, '(SUBJECT "{}")'.format(subject))
        if data[0]:
            print("Email received!")
            return True
        else:
            print("No new email received.")
            return False
    except Exception as e:
        print(f"Failed to check inbox")
        return False

def check_inbox_2(imap_server, username, password):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select('inbox')
        print("Inbox check good")
        return True
    except Exception as e:
        print(f"Failed to check inbox")
        return False

def run(smtp_server, smtp_port, imap_server, username, password, recipient):
    # Generate a unique subject using UUID
    unique_subject = f"Test Email {uuid.uuid4()}"
    email_sent = send_email(smtp_server,smtp_port,username,password,recipient,unique_subject)

    if email_sent:
        # Wait a bit for the email to be delivered
        time.sleep(5)
    email_received = check_inbox(imap_server, username, password, unique_subject)
    if email_received:
        time.sleep(1)

    inbox_check = check_inbox_2(imap_server, username, password)

    if email_sent and email_received:
        print("Success: Email sent and received.")
        return True
    elif inbox_check:
        print("Partial Success: Email not sent, but inbox good.")
        return False
    else:
        #print("Failure: Email sending and receiving failed.")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    smtp_server = host
    smtp_port = 587
    imap_server = host
    username = 'bot@test.lab'
    password = 'botpass'
    recipient = 'bot@test.lab'
    run(smtp_server, smtp_port, imap_server, username, password, recipient)

if __name__ == '__main__':
    main()
