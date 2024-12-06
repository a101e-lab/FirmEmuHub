import requests
import argparse
import re

def get_new_token(target_ip, target_port):
    url = f"http://{target_ip}:{target_port}/login.php"
    headers = {
        "Host": f"{target_ip}:{target_port}",
        "Content-Length": "78",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": f"http://{target_ip}:{target_port}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": f"http://{target_ip}:{target_port}/login.php",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "session_uid=bqgvkrckpo",
        "Connection": "close"
    }
    data = {
        "ACTION_POST": "LOGIN",
        "f_date": "",
        "f_time": "",
        "LOGIN_USER": "admin",
        "LOGIN_PASSWD": "",
        "login": "+Login+"
    }
    response = requests.post(url, headers=headers, data=data)
    new_token = headers.get('Cookie', '').split(';')[0].split('=')[1]
    return new_token

def set_new_token(seed, new_token):
    pattern = r"(Cookie: session_uid=)[^\s;]+"
    updated_seed = re.sub(pattern, rf"\1{new_token}", seed)
    return updated_seed

def update_seed(seed, target_ip, target_port):
    new_token = get_new_token(target_ip, target_port)
    if new_token:
        updated_seed = set_new_token(seed, new_token)
        return updated_seed
    else:
        return seed

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
