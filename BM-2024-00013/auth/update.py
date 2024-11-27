import requests
import argparse
import re
import hashlib
import hmac
import json

def generate_digest(user, passwd, challenge):
    mix = (user + challenge).encode()
    key = passwd.encode()
    hmac_digest = hmac.new(key, mix, hashlib.md5)
    digest = hmac_digest.hexdigest().upper()
    return digest

def get_new_token(target_ip, target_port):
    # 第一次请求，根据返回包算出cookie、password
    burp0_url = f"http://{target_ip}:{target_port}/authentication.cgi?captcha=&dummy=1721377888183"
    burp0_cookies = {"uid": "dNKq2CsbKs"}
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": f"http://{target_ip}:{target_port}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    
    response0 = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    
    try:
        response0_json = response0.json()  # 尝试解析json
        print(response0.text)
    except json.JSONDecodeError:
        print("Failed to decode json from response. Response text was:")
        print(response0.text)  # 打印响应文本，以供调试
        raise
    
    challenge = response0_json["challenge"]
    uid = response0_json['uid']
    password = generate_digest('Admin', '', challenge)
    
    # 第二次请求，根据计算出的password和得到的uid发送第二次登录请求
    burp1_url = f"http://{target_ip}:{target_port}/authentication.cgi"
    burp1_cookies = {"uid": uid}
    burp1_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Origin": f"http://{target_ip}:{target_port}",
        "Referer": f"http://{target_ip}:{target_port}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    burp1_data = {
        "id": "Admin", 
        "password": password
        }
    response1=requests.post(burp1_url, headers=burp1_headers, cookies=burp1_cookies, data=burp1_data)
    print('-----------')
    print(burp1_data)
    print('~~~~~~~~~~~')
    return burp1_cookies

def set_new_token(seed_lines, new_token):
    new_uid = new_token["uid"]
    updated_seed_lines = []
    
    for line in seed_lines:
        if "uid=" in line:
            line = re.sub(r"uid=[^;]+", f"uid={new_uid}", line)
        updated_seed_lines.append(line)

    return updated_seed_lines

def update_seed(seed_content, target_ip, target_port):
    new_token = get_new_token(target_ip, target_port)
    seed_lines = seed_content.splitlines()
    updated_seed_lines = set_new_token(seed_lines, new_token)
    return "\n".join(updated_seed_lines)

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
