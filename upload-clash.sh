gsutil cp  config.yaml gs://lzwjava1/

gsutil acl ch -u allUsers:R gs://lzwjava1/config.yaml
