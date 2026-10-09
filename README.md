# Network Scanner

A simple Python-based network scanner using the `scapy` library to discover active devices on a local network.

---

## Prerequisites

- Python 3.x
- `pip` (Python package manager)
- Linux, macOS, or Windows Subsystem for Linux (WSL)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository_url>
cd net-scanner
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt, confirming it is active.

### 4. Install Dependencies

```bash
pip install scapy
```

> You can also create a `requirements.txt` file containing `scapy` and run `pip install -r requirements.txt` if one is provided.

---

## Usage

The scanner sends raw ARP packets to discover devices and **requires root privileges** to open raw network sockets.

Run the script using the Python binary inside your virtual environment to ensure all dependencies are accessible:

```bash
sudo .venv/bin/python3 scanner.py <target_ip_range>
```

### Example

```bash
sudo .venv/bin/python3 scanner.py 172.27.240.0/24
```

Replace `172.27.240.0/24` with your actual network range (e.g., `192.168.1.0/24`).

---

## Troubleshooting & Common Issues

### ❌ `ModuleNotFoundError: No module named 'scapy'`

**Cause:** Python cannot find the `scapy` library. This typically happens when:
- You forgot to install `scapy`.
- You ran the script with `sudo python3` which uses the **system Python** instead of your virtual environment.

**Solution:**

Make sure your virtual environment is active and `scapy` is installed:

```bash
source .venv/bin/activate
pip install scapy
```

Then run using the venv's Python binary:

```bash
sudo .venv/bin/python3 scanner.py <target_ip_range>
```

---

### ❌ `PermissionError: [Errno 1] Operation not permitted`

**Cause:** The scanner crafts and sends raw Layer 2 network packets using `scapy`. Standard user accounts are not permitted to open raw sockets on Linux/WSL systems.

**Solution:**

Run the script with `sudo`:

```bash
sudo .venv/bin/python3 scanner.py <target_ip_range>
```

> ⚠️ **Important:** Always use the full path to the venv's Python binary (`.venv/bin/python3`) when running with `sudo`. Omitting this causes `sudo` to fall back to the system Python, where `scapy` is not installed, triggering a `ModuleNotFoundError`.

---

### ❌ `sudo: python3: command not found`

**Cause:** `sudo` does not inherit your shell's `PATH`, so it cannot find `python3`.

**Solution:**

Use the absolute path to the virtual environment's Python binary:

```bash
sudo /full/path/to/net-scanner/.venv/bin/python3 scanner.py <target_ip_range>
```

---

### ❌ No devices found / Empty results

**Cause:** The target range may be incorrect, the network interface may not be available, or the ARP scan timed out.

**Solutions:**
- Verify the correct network range using `ip a` or `ifconfig`.
- Ensure you are scanning the correct subnet.
- Try increasing the timeout in `scanner.py` if your network is slow.

---

## Notes

- This tool is intended for use on networks you own or have explicit permission to scan.
- Running network scanners on unauthorized networks may be illegal.
