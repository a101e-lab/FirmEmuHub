import requests
import argparse
import re

def get_new_token(target_ip, target_port):
    url = f"http://{target_ip}:{target_port}/userRpm/LoginRpm.htm?Save=Save"
    cookies = {"Authorization": "Basic%20YWRtaW46MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%3D"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN",
        "Upgrade-Insecure-Requests": "1",
        "Referer": f"http://{target_ip}:{target_port}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    response_str = response.text

    # Extract the new token
    token_start = response_str.find('userRpm') - 17
    token_end = response_str.find('userRpm') - 1
    new_token = response_str[token_start:token_end]

    if not new_token.isupper():
        raise ValueError("Failed to retrieve a valid token.")
    
    return new_token

def set_new_token(seed, new_token):
    # Replace the old token with the new token using regex
    updated_seed = re.sub(r"/[A-Z]{16}/", f"/{new_token}/", seed)
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
