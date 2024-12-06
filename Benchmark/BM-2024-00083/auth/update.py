import requests
import argparse
import re
import hmac
import hashlib
import time
from xml.etree import ElementTree as ET

def initialize_login(target_ip, target_port):
    # 构造请求的URL
    url = f"http://{target_ip}:{target_port}/HNAP1/"

    # 构造请求的头部
    headers = {
        "Host": f"{target_ip}:{target_port}",
        "Content-Length": "310", 
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "HNAP_AUTH": "99101A3727957BF5756F1D559E0E38CE 1722495232", 
        "SOAPAction": "\"http://purenetworks.com/HNAP1/SetIgnoreWizardConfig\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Content-Type": "text/xml; charset=UTF-8",
        "Origin": f"http://{target_ip}:{target_port}",
        "Referer": f"http://{target_ip}:{target_port}/Wizard.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": f"uid=ujcI4DPmyw; PrivateKey=C8B843B87E7C03EF5F224D6D4949A7F1",
        "Connection": "close"
    }

    # 构造请求的XML数据
    xml_data = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <SetIgnoreWizardConfig xmlns="http://purenetworks.com/HNAP1/" />
        </soap:Body>
    </soap:Envelope>"""

    # 发送POST请求
    response = requests.post(url, headers=headers, data=xml_data)

def hex_hmac_md5(key, message):
    """Compute HMAC-MD5 for the given key and message, returning the hex digest."""
    return hmac.new(key.encode(), message.encode(), hashlib.md5).hexdigest().upper()

def calculate_login_password(public_key, password, challenge):
    """Calculate the LoginPassword using the provided public key, password, and challenge."""
    private_key = hex_hmac_md5(public_key + password, challenge)
    login_password = hex_hmac_md5(private_key, challenge)
    return login_password

def calculate_hnap_auth(public_key, private_key, challenge):
    """Calculate the HNAP_AUTH header value."""
    timestamp = str(int(time.time()))
    combined = public_key + private_key + timestamp
    return hex_hmac_md5(combined, challenge) + ' ' + timestamp

def get_new_token(target_ip, target_port):
    # 登录初始化
    initialize_login(target_ip, target_port)

    url = f"http://{target_ip}:{target_port}/HNAP1/"
    
    # First request to get the challenge and public key
    headers = {
        "Content-Type": "text/xml; charset=UTF-8",
        "SOAPAction": "\"http://purenetworks.com/HNAP1/Login\""
    }
    data = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <Login xmlns="http://purenetworks.com/HNAP1/">
                <Action>request</Action>
                <Username>Admin</Username>
                <LoginPassword></LoginPassword>
                <Captcha></Captcha>
            </Login>
        </soap:Body>
    </soap:Envelope>"""
    
    response = requests.post(url, headers=headers, data=data)
    response_xml = ET.fromstring(response.content)
    
    challenge = response_xml.find('.//{http://purenetworks.com/HNAP1/}Challenge').text
    public_key = response_xml.find('.//{http://purenetworks.com/HNAP1/}PublicKey').text
    cookie = response_xml.find('.//{http://purenetworks.com/HNAP1/}Cookie').text
    
    password = ""  # Assuming the password is empty as per the example
    private_key = hex_hmac_md5(public_key + password, challenge)
    login_password = calculate_login_password(public_key, password, challenge)
    
    # Calculate HNAP_AUTH header for the second request
    hnap_auth = calculate_hnap_auth(public_key, private_key, challenge)
    
    # Second request to log in with the calculated LoginPassword
    headers["Cookie"] = f"uid={cookie}; PrivateKey={private_key}"
    headers["HNAP_AUTH"] = hnap_auth
    data = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <Login xmlns="http://purenetworks.com/HNAP1/">
                <Action>login</Action>
                <Username>Admin</Username>
                <LoginPassword>{login_password}</LoginPassword>
                <Captcha></Captcha>
            </Login>
        </soap:Body>
    </soap:Envelope>"""
    
    response = requests.post(url, headers=headers, data=data)
    response_xml = ET.fromstring(response.content)
    
    login_result = response_xml.find('.//{http://purenetworks.com/HNAP1/}LoginResult').text
    if login_result == "SUCCESS":
        return cookie
    else:
        raise Exception("Login failed")

def set_new_token(seed, new_token):
    return re.sub(r'Cookie: uid=\w+', f'Cookie: uid={new_token}', seed)

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
