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

def parse_ping_output(output, scores, service_key):
    if "ping check good" in output:
        scores[service_key] +=1
    else:
        scores[service_key] +=0

def parse_smtp_output(output, scores):
    if "SMTP connection successful" in output:
        scores['smtp'] += 10
    else:
        scores['smtp'] += 0

def parse_smtp_login_output(output, scores):
    if "SMTP service is good" in output:
        scores['smtp-587'] += 10
    else:
        scores['smtp-587'] += 0

def parse_ad_output(output, scores):
    if "ad good" in output:
        scores['ad'] += 10
    else:
        scores['ad'] += 0

def parse_ftp_output(output, scores):
    if "FTP service check good" in output:
        scores['ftp'] += 10
    else:
        scores['ftp'] += 0

def check_services(host_smtp, host_ad, host_ftp):
    scores = {
        'smtp': 0,
        'smtp-587': 0,
        'ad': 0,
        'ftp': 0,
        'dns': 0
    }

    with ThreadPoolExecutor() as executor:
        future_smtp = executor.submit(run_service_check, 'smtp_check.py', host_smtp)
        #future_ad = executor.submit(run_service_check, 'ad_check.py', host_ad)
        future_ftp = executor.submit(run_service_check, 'ftp_check.py', host_ftp)
        future_smtp_login = executor.submit(run_service_check, 'smtp_login_check.py', host_smtp)

        for future in as_completed([future_smtp, future_ad, future_ftp]):
            output = future.result()
            if future == future_smtp:
                parse_smtp_output(output, scores)
            elif future == future_ad:
                parse_ad_output(output, scores)
            elif future == future_ftp:
                parse_ftp_output(output, scores)
            elif future == future_smtp_login:
                parse_smtp_login_output(output, scores)

    total_score = sum(scores.values())
    print(f"Scores: {scores}")
    print(f"Total Score: {total_score}")

def main():
    smtp_ip = '10.20.30.18'
    ad_ip = '10.20.30.11'
    ftp_ip = '10.20.30.19'
    while True:
        check_services(smtp_ip, ad_ip, ftp_ip)
        time.sleep(10)

if __name__ == "__main__":
    main()
