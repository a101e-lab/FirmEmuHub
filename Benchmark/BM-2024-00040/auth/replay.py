import argparse
import socket
import requests

def replay_login(ip, port):
    burp0_url = "http://"+ip+":"+str(port)+"/login.cgi"
    burp0_cookies = {"SESSIONID": "48ce56d4", "UID": "admin", "PSW": "admin"}
    burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://192.168.126.136:32770", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://192.168.126.136:32770/", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"}
    burp0_data = {"html_response_page": "login_fail.asp", "login_name": "YWRtaW4A", "login_pass": '', "graph_id": "5c6aa", "log_pass": '', "graph_code": '', "Login": "\xa0 \xa0 \xa0 Log In \xa0 \xa0 \xa0"}
    response =requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay login script')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', required=True, help='Target port')
    args = parser.parse_args()
    replay_login(args.ip, args.port)
