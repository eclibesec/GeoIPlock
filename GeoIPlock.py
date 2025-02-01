import requests
import threading
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)
def get_location(ip):
    url = f"https://api.iplocation.net/?ip={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
def filter_ips(ip_list, country, output_file, thread_count):
    lock = threading.Lock()
    def worker(ip):
        location = get_location(ip)
        if location:
            country_name = location.get("country_name", "").lower()
            if country_name == country.lower():
                with lock:
                    with open(output_file, 'a') as file:
                        file.write(ip + '\n')
                print(f"{Fore.GREEN}[+] {ip} » {country_name}")
            else:
                print(f"{Fore.RED}[-] {ip} » {country_name}")
    threads = []
    for ip in ip_list:
        ip = ip.strip()
        if ip:
            while threading.active_count() > thread_count:
                pass
            thread = threading.Thread(target=worker, args=(ip,))
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()
    print(f"{Fore.CYAN}\ncomplete result saved to {output_file}")
if __name__ == "__main__":
    print("""
  _____           _______    __            __          
 / ___/__ ___    /  _/ _ \  / /  ___  ____/ /_____ ____
/ (_ / -_) _ \  _/ // ___/ / /__/ _ \/ __/  '_/ -_) __/
\___/\__/\___/ /___/_/    /____/\___/\__/_/\_\\__/_/   
                                                                                                             
- Made By Eclipse Security Labs Team
- GeoIPlocker
    """)
    file_path = input("$ Give me yout ip list: ")
    country = input("$ Lock Country [ ex : indonesia ] : ")
    thread_count = int(input("Thread [ex : 100 ]: "))
    output_file = input("Save to [ex results.txt]: ")
    with open(file_path, 'r') as file:
        ip_list = file.readlines()
    filter_ips(ip_list, country, output_file, thread_count)
