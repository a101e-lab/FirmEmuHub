import logging
import argparse
import json
import time
import subprocess
import random
import string
import yaml
import requests
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[+] %(message)s",
)
logger = logging.getLogger("emulator")

def run_docker_command(command, log_message):
    """Runs a Docker command and handles errors."""
    logger.info(f"Executing command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during {log_message}: {e}")
        raise e

def emulate(benchmark_dir):
    benchmark_config_file = Path(benchmark_dir) / "benchmark.yml"
    config_file = benchmark_config_file.resolve()
    with open(benchmark_config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    image_tag = config["info"]["serial"].lower()
    context = (config_file.parent / config["emulation"]["context"]).resolve()

    container_name = f"{image_tag}_{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))}"

    build_command = [
        "docker", "build",
        "-f", str(context / "Dockerfile"),
        "--tag", image_tag,
        str(context)
    ]

    try:
        logger.info(f"Executing build command: {' '.join(build_command)}")
        subprocess.run(build_command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during build: {e}")
        raise e

    run_command = [
        "docker", "run", "-it", "-d",
        "-e", f"REMOTE_IP={config['emulation']['ip']}",
        "-e", f"REMOTE_PORT={config['emulation']['port']}",
        "--privileged", "-P",
        "--name", container_name,
        image_tag
    ]

    try:
        logger.info(f"Executing run command: {' '.join(run_command)}")
        subprocess.run(run_command, check=True, capture_output=True, text=True)

        logger.info(f"Firmware container '{container_name}' started successfully.")
        inspect_command = ["docker", "inspect", container_name]
        inspect_result = subprocess.run(inspect_command, check=True, capture_output=True, text=True)

        if not inspect_result.stdout:
            logger.error("Docker inspect returned empty result.")
            return
        
        ports = json.loads(inspect_result.stdout)[0]['NetworkSettings']['Ports']
        host_fuzz_port = [
            int(mapping['HostPort']) for port, mappings in ports.items() 
            if mappings for mapping in mappings if mapping['HostIp'] == '0.0.0.0'
        ][0]
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during run: {e}")
        return

    is_started = False
    for attempt in range(20):
        try:
            response = requests.get(f"http://0.0.0.0:{host_fuzz_port}", timeout=5)
            if response.status_code:
                is_started = True
                break
        except requests.exceptions.RequestException:
            print(f"\r[+] Attempt {attempt + 1}/20: Waiting for service to start... (retrying)", end='')
            time.sleep(20)
    print()

    if is_started:
        logger.info("Service started successfully.")
        logger.info(f"The firmware emulation is running at 0.0.0.0:{host_fuzz_port}")
    else:
        logger.info("Service failed to start.")
        logger.info(f"The firmware emulation failed at 0.0.0.0:{host_fuzz_port}")

def print_gradient_banner():
    ascii_art_lines = [            
        " _    _______ ______                    _      ______ _       ",
        "| |  (_______|____  \                  | |    / _____|_)      ",
        "| | ___  _    ____)  )_____ ____   ____| |__ ( (____  _       ",
        "| |/ _ \| |  |  __  (| ___ |  _ \ / ___)  _ \ \____ \| |      ",
        "| | |_| | |  | |__)  ) ____| | | ( (___| | | |_____) ) |_____ ",
        "|_|\___/|_|  |______/|_____)_| |_|\____)_| |_(______/|_______)",
        "--------------------------------------------------------------",
        "Developed by CyberUnicorn.                                    " 
    ]

    colors = [
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255)
    ]

    num_chars = max(len(line) for line in ascii_art_lines)
    num_segments = len(colors) - 1
    segment_length = num_chars // num_segments

    def interpolate_color(start, end, factor):
        return int(start + (end - start) * factor)

    for line in ascii_art_lines:
        for i, char in enumerate(line):
            segment_index = min(i // segment_length, num_segments - 1)
            start_color = colors[segment_index]
            end_color = colors[segment_index + 1]
            factor = (i % segment_length) / segment_length
            r = interpolate_color(start_color[0], end_color[0], factor)
            g = interpolate_color(start_color[1], end_color[1], factor)
            b = interpolate_color(start_color[2], end_color[2], factor)
            color = f"\033[38;2;{r};{g};{b}m"
            print(f"{color}{char}", end="")
        print("\033[0m") 

if __name__ == "__main__":
    print_gradient_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--benchmark', help="Set the benchmark directory")
    args = parser.parse_args()
    
    emulate(args.benchmark)
