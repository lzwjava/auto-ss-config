python update-config.py

gsutil -h "Cache-Control:no-cache" cp  ssconfig gs://lzwjava1/

gsutil acl ch -u allUsers:R gs://lzwjava1/ssconfig

gsutil -h "Cache-Control:no-cache" cp  config.yaml gs://lzwjava1/

gsutil acl ch -u allUsers:R gs://lzwjava1/config.yaml

echo "https://storage.googleapis.com/lzwjava1/ssconfig"

echo "https://storage.googleapis.com/lzwjava1/config.yaml"

