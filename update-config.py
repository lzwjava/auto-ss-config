from ruamel.yaml import YAML
import base64
import re

# Function to decode Shadowsocks URL
def decode_ss_url(ss_url):
    match = re.match(r'ss://(.+)@(.+):(\d+)/?', ss_url)
    if match:
        encoded_part = match.group(1)
        server = match.group(2)
        port = match.group(3)
        decoded_part = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
        method, password = decoded_part.split(':')
        return {
            'server': server,
            'port': int(port),
            'cipher': method,
            'password': password
        }
    return None

# Read Shadowsocks URLs from ssconfig file
with open('ssconfig', 'r') as file:
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
