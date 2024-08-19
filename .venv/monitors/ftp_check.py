import ftplib
import sys

def check_ftp(host, port=21, username='anonymous', password='guest'):
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(host, port, timeout=10)
            print(f"Connected to FTP server at {host}:{port}")
            ftp.login(username, password)
            print(f"Logged in as {username}")
            ftp.cwd('/')
            contents = ftp.nlst()
            return True
    except ftplib.all_errors as e:
        print(f"FTP check failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python ftp_check.py <hostname> [port] [username] [password]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv)> 2 else 21
    username = sys.argv[3] if len(sys.argv) > 3 else 'anonymous'
    password = sys.argv[4] if len(sys.argv) > 4 else 'guest'
    result = check_ftp(host, port, username, password)
    if result:
        print("FTP service check good")
    else:
        print("FTP service check failed")

if __name__ == "__main__":
    main()