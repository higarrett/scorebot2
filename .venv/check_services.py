import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread


def run_service_check(script_name, host, target_ip=None):
    script_path = f'monitors/{script_name}'
    cmd = ['python3', script_path, host]
    if target_ip:
        cmd.append(target_ip)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parse_email_output(output, scores):
    if "Email sent successfully" in output:
        scores['smtp'] += 10
        scores['imap'] += 10
    elif "Error: Email sent successfully" and "Failed to check inbox" in output:
        scores['smtp'] += 10
        scores['imap'] += 0
    elif "Email not sent, but inbox good" in output:
        scores['smtp'] += 0
        scores['imap'] += 10
    elif "Failed to send email" and "Failed to check inbox" in output:
        scores['smtp'] += 0
        scores['imap'] += 0
    else:
        scores['smtp'] += 0
        scores['imap'] += 0

def parse_ldap_output(output, scores):
    if "LDAP authentication successful" in output:
        scores['ldap'] += 10
    else:
        scores['ldap'] += 0

def parse_ftp_output(output, scores):
    if "FTP service check good" in output:
        scores['ftp'] += 10
    else:
        scores['ftp'] += 0

def parse_dns_output(output, scores):
    if "success" in output:
        scores['dns'] += 10
    else:
        scores['dns'] += 0

def check_services(host_email, host_ad, host_ftp):
    scores = {
        'imap': 0,
        'smtp': 0,
        'ldap': 0,
        'ftp': 0,
        'dns': 0
    }

    with ThreadPoolExecutor() as executor:
        future_email = executor.submit(run_service_check, 'email_check2.py', host_email)
        future_ldap = executor.submit(run_service_check, 'ldap_check.py', host_ad)
        future_ftp = executor.submit(run_service_check, 'ftp_check.py', host_ftp)
        future_dns = executor.submit(run_service_check, 'dns_check.py', host_ad)

        for future in as_completed([future_email, future_ldap, future_ftp, future_dns]):
            output = future.result()
            if future == future_ldap:
                parse_ldap_output(output, scores)
            elif future == future_ftp:
                parse_ftp_output(output, scores)
            elif future == future_dns:
                parse_dns_output(output, scores)
            elif future == future_email:
                parse_email_output(output, scores)

    total_score = sum(scores.values())
    print(f"Scores: {scores}")
    print(f"Total Score: {total_score}")

def main():
    email_ip = '10.20.30.18'
    ad_ip = '10.20.30.11'
    ftp_ip = '10.20.30.19'
    while True:
        check_services(email_ip, ad_ip, ftp_ip)
        time.sleep(10)

if __name__ == "__main__":
    main()
