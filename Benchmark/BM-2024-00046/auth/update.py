import requests
import argparse
import re
import hashlib

def initialize_login(target_ip, target_port):
    # 构造请求的URL
    url = f"http://{target_ip}:{target_port}/HNAP1/"

    # 构造请求的头部
    headers = {
        "Host": f"{target_ip}:{target_port}",
        "Content-Length": "58",
        "Accept": "application/json",
        "HNAP_AUTH": "E5C14446F7156A0DE9E56D8ED83DAA45 1722488351042", 
        "SOAPACTION": "\"http://purenetworks.com/HNAP1/SetWizardValue\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": f"http://{target_ip}:{target_port}",
        "Referer": f"http://{target_ip}:{target_port}/Wizard.html?t=1722488212410",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": f"timeout=4; PHPSESSID=d69f2910e013b53ee0c32f2146589021",
        "Connection": "close"
    }

    # 构造请求的JSON数据
    json_data = {
        "SetWizardValue": {
            "system_root_password": "bWwxTTlyZ3o="
        }
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=json_data)

def generate_md5_key_upper(string1, string2):
    concatenatedString = string1 + string2
    return hashlib.md5(concatenatedString.encode()).hexdigest().upper()

def get_new_token(target_ip, target_port):
    # 登录初始化
    initialize_login(target_ip, target_port)
    # 第一次请求，根据返回包计算出cookie、Login_Passwd
    burp0_url = f"http://{target_ip}:{target_port}/HNAP1/"
    burp0_headers = {}
    burp0_json = {"Login": {"Action": "request", "Captcha": "", "LoginPassword": "", "PrivateLogin": "LoginPassword", "Username": "admin"}}
    response0 = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
    response0_json = response0.json()

    challenge = response0_json["LoginResponse"].get("Challenge")
    cookie = response0_json["LoginResponse"].get("Cookie")
    public_key = response0_json["LoginResponse"].get("PublicKey")

    set_cookie = response0.headers.get('Set-Cookie')

    # 提取 PHPSESSID 的值
    phpsessid = None
    if set_cookie:
        match = re.search(r'PHPSESSID=([^;]+)', set_cookie)
        if match:
            phpsessid = match.group(1)

    PrivateKey = generate_md5_key_upper(public_key, challenge)

    uid = cookie
    Login_Passwd = generate_md5_key_upper(PrivateKey, challenge)
    print(Login_Passwd)

    # 第二次请求，根据计算出的cookie和Login_Passwd发送第二次登录请求
    burp1_cookies = {"PHPSESSID": phpsessid, "uid": uid, "PrivateKey": PrivateKey}
    burp1_headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Accept-Language": "zh-CN", "SOAPAction": "\"http://purenetworks.com/HNAP1/Login\"", "Content-Type": "application/json; charset=UTF-8", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    burp1_json = {"Login": {"Action": "login", "Captcha": "", "LoginPassword": Login_Passwd, "PrivateLogin": "LoginPassword", "Username": "admin"}}
    requests.post(burp0_url, headers=burp1_headers, cookies=burp1_cookies, json=burp1_json)

    return burp1_cookies

def set_new_token(seed, new_token):
    new_phpsessid = new_token["PHPSESSID"]
    new_uid = new_token["uid"]
    new_private_key = new_token["PrivateKey"]

    new_cookie_value = f"PHPSESSID={new_phpsessid}; uid={new_uid}; PrivateKey={new_private_key}"
    
    # 使用正则表达式替换整个Cookie字段
    updated_seed = re.sub(r'Cookie:.*', f'Cookie: {new_cookie_value}', seed, flags=re.IGNORECASE)

    return updated_seed

def update_seed(seed, target_ip, target_port):
    new_token = get_new_token(target_ip, target_port)
    updated_seed = set_new_token(seed, new_token)
    return updated_seed

def main():
    parser = argparse.ArgumentParser(description="Update seed file with new authentication token.")
    parser.add_argument('--seed', required=True, help="Path to the seed file")
    parser.add_argument('--ip', required=True, help="Target IP address")
    parser.add_argument('--port', type=int, required=True, help="Target port number")
    args = parser.parse_args()

    with open(args.seed, 'r') as file:
        seed_content = file.read()

    updated_seed = update_seed(seed_content, args.ip, args.port)

    print(updated_seed)
    # Write the updated seed back to the original file
    with open(args.seed, 'w') as file:
        file.write(updated_seed)

    print("Seed file updated successfully.")

if __name__ == '__main__':
    main()
