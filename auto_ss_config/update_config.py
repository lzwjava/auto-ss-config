import subprocess
from google.cloud import storage
from ruamel.yaml import YAML
import base64
import re

def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    else:
        print(result.stdout)

def decode_ss_url(ss_url):
    match = re.match(r'ss://(.+)@(.+):(\d+)/?', ss_url)
    if match:
        encoded_part = match.group(1)
        server = match.group(2)
        port = match.group(3)
        decoded_part = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
        parts = decoded_part.split(':')
        method = parts[0]
        password = ':'.join(parts[1:])
        return {
            'server': server,
            'port': int(port),
            'cipher': method,
            'password': password
        }
    return None

def update_config_yaml(ssconfig_path):
    # Read Shadowsocks URLs from ssconfig file
    with open(ssconfig_path, 'r') as file:
        ss_urls = file.readlines()

    # Decode Shadowsocks URLs
    proxies = []
    for ss_url in ss_urls:
        ss_url = ss_url.strip()
        if ss_url:
            proxy_config = decode_ss_url(ss_url)
            if proxy_config:
                proxies.append(proxy_config)

    # Read existing config.yaml
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open('config.yaml', 'r') as file:
        config = yaml.load(file)

    # Ensure config is a dictionary
    if not isinstance(config, dict):
        raise ValueError("config.yaml is not a valid YAML dictionary")

    # Update proxies in config.yaml
    config['proxies'] = [
        {
            'name': f"My SS Proxy {i+1}",
            'type': 'ss',
            'server': proxy['server'],
            'port': proxy['port'],
            'cipher': proxy['cipher'],
            'password': proxy['password'],
            'udp': True,
            'plugin': "",
            'plugin-opts': {}
        }
        for i, proxy in enumerate(proxies)
    ]

    # Write updated config.yaml
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

    print("config.yaml has been updated with the new Shadowsocks proxies.")

def update_config(bucket_name, ssconfig_path):
    # Run the update_config_yaml function
    update_config_yaml(ssconfig_path)

    # Initialize a Google Cloud Storage client
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Upload ssconfig to the bucket with no-cache header
    blob = bucket.blob('ssconfig')
    blob.upload_from_filename(ssconfig_path)
    blob.cache_control = 'no-cache'
    blob.patch()

    # Make ssconfig publicly readable
    blob.acl.user('allUsers').grant_read()
    blob.acl.save()

    # Upload config.yaml to the bucket with no-cache header
    blob = bucket.blob('config.yaml')
    blob.upload_from_filename('config.yaml')
    blob.cache_control = 'no-cache'
    blob.patch()

    # Make config.yaml publicly readable
    blob.acl.user('allUsers').grant_read()
    blob.acl.save()

    # Print the URLs
    print(f"https://storage.googleapis.com/{bucket_name}/ssconfig")
    print(f"https://storage.googleapis.com/{bucket_name}/config.yaml")

if __name__ == "__main__":
    # Example usage
    update_config(bucket_name='lzwjava1', ssconfig_path='ssconfig')
