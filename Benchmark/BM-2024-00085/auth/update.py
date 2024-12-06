import hashlib
import hmac
import json
import re
import requests
import argparse

def md5_hash(data):
    """计算数据的MD5散列值"""
    md5_obj = hashlib.md5()
    md5_obj.update(data.encode('utf-8'))
    return md5_obj.hexdigest()

def hmac_md5(key, data):
    """创建HMAC-MD5散列"""
    return hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.md5).hexdigest()

def generate_digest(username, password, challenge):
    """生成DIGEST"""
    key = password
    mix = username + challenge
    digest = hmac_md5(key, mix)
    DIGEST = digest.upper()
    return DIGEST

def send_request(url, headers, method='GET', data=None):
    """发送HTTP请求并返回响应内容"""
    if method == 'POST':
        response = requests.post(url, headers=headers, data=data)
    else:
        response = requests.get(url, headers=headers)
    return response.text

def get_new_token(target_ip, target_port):
    # 发送GET请求获取cookie和challenge
    get_url = f"http://{target_ip}:{target_port}/authentication.cgi?captcha=&dummy=1721624885522"
    get_headers = {
        "Host": f"{target_ip}:{target_port}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    get_response = send_request(get_url, get_headers)
    get_data = json.loads(get_response)
    
    # 账号密码
    username = "Admin"
    password = ""
    
    # 生成DIGEST
    digest = generate_digest(username, password, get_data['challenge'])
    
    # 发送POST请求获取key
    post_url = f"http://{target_ip}:{target_port}/authentication.cgi"
    post_headers = {
        "Host": f"{target_ip}:{target_port}",
        "Content-Length": str(len(f"id={username}&password={digest}")),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Origin": f"http://{target_ip}:{target_port}",
        "Referer": f"http://{target_ip}:{target_port}/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": f"uid={get_data['uid']}",
        "Connection": "close"
    }
    post_data = {
        "id": username,
        "password": digest
    }
    post_response = send_request(post_url, post_headers, method='POST', data=post_data)
    post_data = json.loads(post_response)
    
    return post_data['key']

def set_new_token(seed, new_token):
    # Update the seed file with the new token
    updated_seed = re.sub(r'Cookie: uid=[^\s]+', f'Cookie: uid={new_token}', seed)
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

    # Write the updated seed back to the original file
    with open(args.seed, 'w') as file:
        file.write(updated_seed)

    print("Seed file updated successfully.")

if __name__ == '__main__':
    main()
