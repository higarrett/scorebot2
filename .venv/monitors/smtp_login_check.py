import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText

def check_smtp(host, port=587, username='', password=''):
    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            #server.set_debuglevel(1)
            server.connect(host, port)
            server.ehlo()
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()

            server.login(username, password)
            print("Login successful")
            return True

    except smtplib.SMTPAuthenticationError:
        print("Failed to log in")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP connection failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python smtp_check.py <hostname> [port]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    username = "gold@test.lab"
    password = "goldteam"
    result = check_smtp(host, port, username, password)
    if result:
        print("SMTP service is good")
    else:
        print("SMTP service failed")

if __name__ == "__main__":
    main()