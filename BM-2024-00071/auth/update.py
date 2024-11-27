import argparse
import re
import socket

MAX_RETRIES = 5

def send_tcp_request(seed_content, ip="0.0.0.0", port=80):
    for _ in range(MAX_RETRIES):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(seed_content.encode())
                response = ""
                while True:
                    part = s.recv(4096)
                    if not part:
                        break
                    response += part.decode()
                return response
        except socket.error as e:
            print(f"Socket error: {e}")
            return None

def create_content(template, **kwargs):
    content = template.format(**kwargs)
    lines = content.split('\n')
    content = '\r\n'.join(lines) + '\r\n'
    return content

def extract_sysauth_and_stok(response):
    sysauth_match = re.search(r'Set-Cookie: sysauth=([^;]+)', response)
    sysauth = sysauth_match.group(1) if sysauth_match else None

    stok_match = re.search(r'"stok":"([^"]+)"', response)
    stok = stok_match.group(1) if stok_match else None
    
    error_code_match = re.search(r'"error_code":"([^"]+)"', response)
    error_code = error_code_match.group(1) if error_code_match else None
    
    return sysauth, stok, error_code

def get_new_token(target_ip, target_port):
    content0 = '''POST /cgi-bin/luci/;stok=/login?form=login HTTP/1.1
Host: {ip}:{port}
Content-Length: 400
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://{ip}:{port}
Referer: http://{ip}:{port}/webpages/login.html
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

data=%7B%22method%22%3A%22login%22%2C%22params%22%3A%7B%22username%22%3A%22admin%22%2C%22password%22%3A%2221dd905725bef0483f91a45c954f26dd0c6640329cf266f043d8a386855b22d2e056c0411a8f6246fcbb8e1804a5d433a92334b312a403616eb03ac17051a3f903f39c92a7e512fe5b8deac4e455fbe532cd919749a75ebf8e3ed0927cf5277c2d0304478a54efaaa1ecd05d1b760473e6bd06734075b6040998d77ee59d87bf%22%7D%2C%22type%22%3A%22default%22%7D'''
    
    response = send_tcp_request(create_content(content0, ip=target_ip, port=target_port), target_ip, target_port)
    print(response)
    
    sysauth, stok, error_code = extract_sysauth_and_stok(response)
    
    if error_code == "0":        
        content1 = '''POST /cgi-bin/luci/;stok={stok}/admin/administration?form=accountfirstset HTTP/1.1
Host: {ip}:{port}
Content-Length: 959
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://{ip}:{port}
Referer: http://{ip}:{port}/webpages/account.html
Accept-Encoding: gzip, deflate, br
Cookie: sysauth={sysauth}
Connection: keep-alive

data=%7B%22method%22%3A%22set%22%2C%22params%22%3A%7B%22old_acc%22%3A%22admin%22%2C%22old_pwd%22%3A%2221dd905725bef0483f91a45c954f26dd0c6640329cf266f043d8a386855b22d2e056c0411a8f6246fcbb8e1804a5d433a92334b312a403616eb03ac17051a3f903f39c92a7e512fe5b8deac4e455fbe532cd919749a75ebf8e3ed0927cf5277c2d0304478a54efaaa1ecd05d1b760473e6bd06734075b6040998d77ee59d87bf%22%2C%22new_acc%22%3A%22admin%22%2C%22new_pwd%22%3A%2203fd67528b8c020de57a92838fe260be64afdc0b50ada022aed0e94c724e6f38bd9d84cc94abed1671af833f79a21c969dcaeab23d406203794a617dbef0407419d3bf9d269ccf288be567f5adc9096987ab7d280c6ce2f49913c4132ce15aaa46bea085aa3d7fc8ab7e0edfdb10ceb425d44c756974293036b0c6378256f021%22%2C%22cfm_pwd%22%3A%2203fd67528b8c020de57a92838fe260be64afdc0b50ada022aed0e94c724e6f38bd9d84cc94abed1671af833f79a21c969dcaeab23d406203794a617dbef0407419d3bf9d269ccf288be567f5adc9096987ab7d280c6ce2f49913c4132ce15aaa46bea085aa3d7fc8ab7e0edfdb10ceb425d44c756974293036b0c6378256f021%22%7D%7D'''
        
        send_tcp_request(create_content(content1, ip=target_ip, port=target_port, stok=stok, sysauth=sysauth), target_ip, target_port)

    content2 = '''POST /cgi-bin/luci/;stok=/login?form=login HTTP/1.1
Host: {ip}:{port}
Content-Length: 371
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
Accept-Language: zh-CN
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://{ip}:{port}
Referer: http://{ip}:{port}/webpages/login.html
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

data=%7b%22method%22%3a%22login%22%2c%22params%22%3a%7b%22username%22%3a%22admin%22%2c%22password%22%3a%2203fd67528b8c020de57a92838fe260be64afdc0b50ada022aed0e94c724e6f38bd9d84cc94abed1671af833f79a21c969dcaeab23d406203794a617dbef0407419d3bf9d269ccf288be567f5adc9096987ab7d280c6ce2f49913c4132ce15aaa46bea085aa3d7fc8ab7e0edfdb10ceb425d44c756974293036b0c6378256f021%22%7d%7d'''
    
    response = send_tcp_request(create_content(content2, ip=target_ip, port=target_port), target_ip, target_port)
    
    sysauth, stok, error_code = extract_sysauth_and_stok(response)
    print(f"sysauth:{sysauth}, stok:{stok}, error_code:{error_code}")

    return sysauth, stok

def set_new_token(seed, sysauth, stok):
    # 替换种子文件中的sysauth和stok，保持长度不变
    new_seed = re.sub(r'sysauth=[^;]{32}', f'sysauth={sysauth}', seed)
    new_seed = re.sub(r'stok=[^/]{32}', f'stok={stok}', new_seed)
    return new_seed

def update_seed(seed, target_ip, target_port):
    sysauth, stok = get_new_token(target_ip, target_port)
    updated_seed = set_new_token(seed, sysauth, stok)
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
