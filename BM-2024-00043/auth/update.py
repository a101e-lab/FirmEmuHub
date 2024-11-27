import requests
import argparse
import re

def get_new_token(target_ip,target_port):
    burp0_url = "http://"+target_ip+":"+str(target_port)+"/userRpm/LoginRpm.htm?Save=Save"
    burp0_cookies = {"Authorization": "Basic%20YWRtaW46MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%3D"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux aarch64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Referer": "http://192.168.0.1/", "Upgrade-Insecure-Requests": "1"}
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
