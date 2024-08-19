from ping3 import ping
import statistics
import sys

def check_ping(host, count=30, threshold=0.75):
    successful_pings = []

    for _ in range(count):
        response = ping(host)
        if response is not None:
            successful_pings.append(response)

    success_rate = len(successful_pings) / count

    return success_rate > threshold, successful_pings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping_check.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    is_successful, ping_times = check_ping(host)
    if is_successful:
        print("ping check good")
    else:
        print("ping check bad")

