# 🌊 FloodPY - Powerfull FLOOD DDoS Tool

⚠️ **WARNING**: This tool may be **illegal** to use on unauthorized targets. Use it **only for educational, ethical testing**, or **your own infrastructure**. You are fully responsible for your actions.

---

## 🚀 What is FloodPY?

**FloodPY** is a fast, multi-threaded HTTP flooder made with Python.

Made for stress testing or just learning how flooding tools work. 🧠💥

---

## 🧰 Features

- 🔫 **High Thread Support** — Up to thousands of threads
- 🧅 **Proxy Support** — Use HTTP/HTTPS proxies
- 🌀 **Random Headers** — Rotate User-Agents and Referers
- 📟 **Live Stats** — See requests per second, error count, and status codes in real-time
- 💻 **Cross-Platform** — Works on Windows, macOS, and Linux
- ⚙️ **Custom Threads** — Choose how many threads you wanna use

---

## 📦 Requirements

- Python 3.6+
- `requests`
- `colorama` (optional on Linux/macOS)

Install dependencies with:

```bash
pip install requests colorama
```

---

## 📂 Setup

1. Clone or download this repo:
   ```bash
   git clone https://github.com/kyrazzx/floodpy
   cd floodpy
   ```

2. (Optional) Add your proxy list to `proxies.txt`:
   ```
   127.0.0.1:8080
   192.168.1.1:3128
   ```

---

## 🛠️ Usage

Run the tool with:

```bash
python main.py
```

You’ll be prompted to enter:

- Number of threads (e.g., 500+ for flood)
- Target URL (must start with `http://` or `https://`)
- If you wanna use proxies

🧠 Tip: The more threads, the more intense the attack.

---

## 📊 Example Output

```
[*] Launching FLOOD on https://example.com with 500 threads...
[!] WARNING: This is EXTREMELY AGGRESSIVE and potentially ILLEGAL.
[!] Press Ctrl+C to stop.

Target: https://example.com           | Threads: 500  | Sent: 15023    | Errors: 421    | RPS: 1083 | Status: 200
```

---

## ☠️ Disclaimer

> This project is **for educational purposes only**. Do not use it on networks or servers without explicit authorization.  
> I'm **not responsible** for any damage or legal consequences.

---

---

## 🖥️ FloodPY v0.1.0 (BETA)

> FloodPY is currently in a beta phase, this version may be unstable.

---

## 🧠 Author

Made by Kyra

---

## 🧃 License

MIT — *do whatever you want, I wont charge you I promise.*
