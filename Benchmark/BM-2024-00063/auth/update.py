import requests
import argparse
import re

def get_new_token(target_ip,target_port):
   
    burp0_url = "http://"+target_ip+":"+str(target_port)+"/userRpm/LoginRpm.htm?Save=Save"
    burp0_cookies = {"Authorization": "Basic%20YWRtaW46MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%3D"}
    burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"}

    results = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    results_str = results.text

    new_token = results_str[results_str.find('userRpm')-17:results_str.find('userRpm')-1]
    #print(new_token)
    return new_token

def set_new_token(seed,new_token):
    seed_begin = seed[:seed.find('/')+1]
    seed_end = seed[seed.find('userRpm')-1:]
    updated_seed = seed_begin + new_token + seed_end
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
