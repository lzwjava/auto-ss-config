# Auto SS Config

- [English README](README.md)
- [中文说明](README-ZH.md)

A tool to automatically generate and upload Shadowsocks or Clash subscription URLs from Shadowsocks URLs. Whenever my Shadowsocks server is blocked, I use Outline Manager to create a new server and obtain a fresh address. I then import this URL directly using the Mac app to bypass the Great Firewall (GFW) restrictions. Next, I run `python upload_configs.py` from this project to update my subscription URLs. Finally, I sync my Android and iOS devices with the updated subscription URL to ensure all my digital devices maintain functional network connections.

## Features

- Converts Shadowsocks URLs to Clash configuration
- Supports multiple Shadowsocks servers
- Automatically uploads configurations to Google Cloud Storage
- Makes configurations publicly accessible
- Uses cache control for immediate updates

## Files

- `app_config_tmp.yaml` - Application configuration (bucket name, SS URLs)
- `clash_config_tmp.yaml` - Temporary Clash configuration file
- `upload_configs.py` - Script to generate Clash config and upload configs to Google Cloud Storage
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud credentials:
   - Install Google Cloud SDK
   - Run `gcloud auth application-default login`
   - Or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

3. **Copy `app_config_tmp.yaml` to `app_config.yaml` and configure**:
```yaml
bucket_name: your-bucket-name
ss_urls:
    - ss://method:password@server:port
```

## Usage

1. Add your Shadowsocks URLs to the `ss_urls` list in `app_config.yaml`:
```yaml
ss_urls:
    - ss://method:password@server:port
```

2. Upload configurations:
```bash
python upload_configs.py
```

The script will output the public URLs for both configurations.

## Development

- Python 3.6+
- Uses `ruamel.yaml` for YAML handling
- Uses `google-cloud-storage` for GCS operations

## License

MIT
