import socket
import platform
import os
import sys
import threading
from datetime import datetime

PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-ALT"
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(r""" 
   _____  _____   ______  ______  _   _  ______ __     __ ______ 
  / ____||  __ \ |  ____||  ____|| \ | ||  ____|\ \   / /|  ____|
 | |  __ | |__) || |__   | |__   |  \| || |__    \ \_/ / | |__   
 | | |_ ||  _  / |  __|  |  __|  | . ` ||  __|    \   /  |  __|  
 | |__| || | \ \ | |____ | |____ | |\  || |____    | |   | |____ 
  \_____||_|  \_\|______||______||_| \_||______|   |_|   |______|                                                
    """)

def pause():
    input("\nPress ENTER to continue...")
    clear()
    banner()

def get_network_base():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    base = ".".join(local_ip.split(".")[:3])
    return base, local_ip

def get_name(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown Device"

def scan_ports(ip):
    for port in PORT_SERVICES:
        s = socket.socket()
        s.settimeout(0.4)

        if s.connect_ex((ip, port)) == 0:
            print(f"      [OPEN] {port} -> {PORT_SERVICES[port]}")

        s.close()

def scan_device(ip):
    print(f"\n[DEVICE]")
    print(f"IP   : {ip}")
    print(f"NAME : {get_name(ip)}")

    scan_ports(ip)
    print("-" * 50)

def scan_local_network():
    base, local_ip = get_network_base()

    print(f"\n[INFO] Local IP: {local_ip}")
    print(f"[INFO] Scanning: {base}.1 - {base}.254\n")

    def worker(i):
        ip = f"{base}.{i}"

        try:
            socket.gethostbyaddr(ip)
            scan_device(ip)
        except:
            pass

    threads = []

    for i in range(1, 255):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

        if i % 30 == 0:
            for tt in threads:
                tt.join()
            threads.clear()

    for t in threads:
        t.join()

def resolve(target):
    try:
        return socket.gethostbyname(target)
    except:
        return None


def single_scan():
    target = input("\nEnter IP or DOMAIN: ").strip()
    ip = resolve(target)

    if ip:
        scan_device(ip)

    pause()

def creator():
    print("\n@@@@@ CREATOR @@@@@")
    print("Project: GREENEYE-SCANNER")
    print("Creator: Pyvrax")
    print("github: https://github.com/pyvrax")
    pause()


def main():
    clear()
    banner()

    while True:
        print("\n1 - IP / DOMAIN SCAN")
        print("2 - CREATOR")
        print("3 - SCAN LOCAL NETWORK (FULL)")
        print("4 - EXIT")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            single_scan()
        elif choice == "2":
            creator()
        elif choice == "3":
            scan_local_network()
            pause()
        elif choice == "4":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()