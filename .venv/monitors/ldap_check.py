import sys
import ldap3
from ldap3 import Server, Connection, ALL

def ldap_authenticate(server_IP, username, password, domain):
    server = Server(server_IP, get_info=ALL)
    user_dn = f"{username}@{domain}"

    try:
        with Connection(server, user=user_dn, password=password, auto_bind=True) as conn:
            if conn.bound:
                print("LDAP authentication successful")
                return True
            else:
                print("LDAP authentication failed")
                return False
    except ldap3.core.exceptions.LDAPBindError as e:
        print(f"LDAP authentication error: {e}")
        return False
    except Exception as e:
        print(f"General error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python ldap_check.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    domain = 'test.lab'
    username = 'bot'
    password = 'botpass'
    ldap_authenticate(host, username, password, domain)

if __name__ == '__main__':
    main()