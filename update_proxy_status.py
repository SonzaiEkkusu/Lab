import requests
import csv
import shutil
import os

def main():
    input_file = os.getenv('IP_FILE', 'ip.txt')
    output_file = 'ip_updated.txt'
    api_url_template = os.getenv('API_URL', 'https://apix.sonzaix.us.kg/?ip={ip}:{port}')

    alive_proxies = []

    try:
        with open(input_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                ip = row[0].strip()
                port = row[1].strip()
                api_url = api_url_template.format(ip=ip, port=port)
                try:
                    response = requests.get(api_url, timeout=10)
                    response.raise_for_status()  # Memastikan respons HTTP sukses
                    data = response.json()
                    status = data.get("proxyStatus", "").upper()
                    if status == "✅ ALIVE ✅":
                        alive_proxies.append(row)
                        print(f"{ip}:{port} is ALIVE")
                    else:
                        print(f"{ip}:{port} is DEAD")
                except requests.exceptions.RequestException as e:
                    print(f"Error checking {ip}:{port}: {e}")
    except FileNotFoundError:
        print(f"File {input_file} tidak ditemukan.")
        return

    try:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(alive_proxies)
    except Exception as e:
        print(f"Error menulis ke {output_file}: {e}")
        return

    try:
        shutil.move(output_file, input_file)
        print(f"{input_file} telah diperbarui dengan proxy yang ALIVE.")
    except Exception as e:
        print(f"Error menggantikan {input_file}: {e}")

if __name__ == "__main__":
    main()
