import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText

def check_smtp(host, port=25):
    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            #server.set_debuglevel(1)
            response = server.helo('test.lab')
            print("SMTP connection successful:", response)
            server.quit()
            return True
    except Exception as e:
        print("Failed to connect to SMTP server:", e)
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python smtp_check.py <hostname> [port]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    result = check_smtp(host, port)

if __name__ == "__main__":
    main()