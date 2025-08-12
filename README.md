# 🌊 FloodPY - High-Performance Stress Test Tool

⚠️ **WARNING**: This tool is for educational purposes only. Using it on targets without prior mutual consent may be **illegal**. You are fully responsible for your actions.

---

## 🚀 What is FloodPY?

**FloodPY** is a high-performance, multi-threaded, and multi-vector stress testing tool written in Python. It is designed to saturate servers by using a combination of flooding techniques to test the resilience of both the network and application layers.

Built for penetration testers, security researchers, or anyone interested in learning how modern flooding tools work. 🧠💥

---

## 🧰 Features

-   💥 **Multi-Vector Attacks** — Launch targeted or combined attacks:
    -   **HTTP GET Flood**: Saturates the server with a high volume of GET requests.
    -   **HTTP POST Flood**: Tests the server's ability to process incoming data.
    -   **TCP Connection Flood (Hit & Run)**: Exhausts the server's socket pool by rapidly opening and closing TCP connections.
    -   **TCP Connection Hold (Slowloris-like)**: Keeps connections open to exhaust concurrent connection limits.
-   🌀 **Combined "Apocalypse" Mode** — Launches all attack types simultaneously for maximum pressure, dedicating the specified thread count to each vector.
-   ⚡ **High Performance** — Utilizes an efficient multi-threaded architecture to generate a massive load from a single machine.
-   📟 **Real-Time Statistics** — Track Requests Per Second (RPS), Connections Per Second (CPS), and errors live.
-   ⚙️ **Dual Execution Mode** — Run the tool interactively or launch attacks instantly via command-line arguments.
-   💻 **Cross-Platform** — Works on Windows, macOS, and Linux.

---

## 📦 Requirements

-   Python 3.7+
-   `httpx` with HTTP/2 support
-   `colorama`

Install dependencies with:

```bash
pip install "httpx[http2]" colorama
```

---

## 📂 Setup

1.  Clone or download this repository:
    ```bash
    git clone https://github.com/kyrazzx/floodpy
    cd floodpy
    ```

---

## 🛠️ Usage

### Interactive Mode

For a guided launch, simply run:

```bash
python main.py
```

The tool will prompt you to enter:
-   The number of threads (per attack type).
-   The target URL (must start with `http://` or `https://`).
-   The attack mode (1-4).

### Command-Line (CLI) Mode

For quick use or scripting, you can pass the options as arguments.

**Syntax:**
```bash
python main.py -u <URL> -t <THREADS> -m <MODE>
```

-   `-u` or `--url`: The target's URL.
-   `-t` or `--threads`: The number of threads **per attack type**.
-   `-m` or `--mode`: The attack mode (1, 2, 3, or 4).

**Examples:**
Launch a GET flood with 2000 threads.
```bash
python main.py -u https://example.com -t 2000 -m 1
```

Launch a combined attack with 1000 threads for each vector (4000 threads total).
```bash
python main.py -u https://example.com -t 1000 -m 4
```


## 📊 Example Output (Mode 4)

```
[*] Launching flood on https://example.com with 4000 total threads...
[!] This is an aggressive test. Press Ctrl+C to stop.

Threads: 4000      | Errors: 12        | RPS: 1582    | TCP Hit/s: 2301    | Held: 998
```

---

## ☠️ Disclaimer

> This project is for **educational purposes only**. Do not use it on networks or servers without explicit authorization.  
> The author is **not responsible** for any damage or legal consequences that may arise from your use of this tool.

---

## 🧠 Author

Made by Kyra

---

## 🧃 License

MIT — *do whatever you want, I won't charge you, I promise.*