import sys
import dns.resolver

MACHINE_NAMES = ["mail.test.lab", "windc1.test.lab", "WinSrv1.test.lab", "wordpress.test.lab", "windesktop1.test.lab"]

def dns_lookup(dns_server, hostnames):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    results = []
    success_count = 0
    failure_count = 0

    for hostname in hostnames:
        try:
            answer = resolver.resolve(hostname, 'A')
            ip_addresses = [ip.address for ip in answer]
            results.append(f"{hostname}: {', '.join(ip_addresses)}")
            success_count += 1
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
            results.append(f"{hostname}: No records found: {e}")
            failure_count +=1
        except dns.exception.Timeout:
            results.append(f"{hostname}: Query timed out")
            failure_count += 1
        except Exception as e:
            results.append(f"{hostname}: Error: {e}")
            failure_count += 1

    #return ' | '.join(results)
    #print(result_string)
    print(f"Successes: {success_count}, Failures: {failure_count}")

    if success_count > failure_count:
        return 10
    else:
        return 0

def main():
    dns_server = '10.20.30.11'
    score = dns_lookup(dns_server, MACHINE_NAMES)
    print(f"{score}")


if __name__ == "__main__":
    main()