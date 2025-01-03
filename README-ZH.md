# 自动 SS 配置

- [English README](README.md)
- [中文说明](README-ZH.md)

一个工具，用于自动生成和上传 Shadowsocks 或 Clash 订阅 URL 从 Shadowsocks URL。每当我的 Shadowsocks 服务器被封锁时，我使用 Outline Manager 创建一个新的服务器并获取一个新的地址。然后，我直接使用 Mac 应用程序导入此 URL 以绕过防火墙（GFW）限制。接下来，我运行 `python upload_configs.py` 从这个项目更新我的订阅 URL。最后，我将 Android 和 iOS 设备与更新的订阅 URL 同步，以确保所有数字设备保持功能网络连接。

## 特点

- 将 Shadowsocks URL 转换为 Clash 配置
- 支持多个 Shadowsocks 服务器
- 自动将配置上传到 Google Cloud Storage
- 使配置公开可访问
- 使用缓存控制以实现立即更新

## 文件

- `app_config.yaml` - 应用程序配置（存储桶名称，SS URL）
- `clash_config_tmp.yaml` - 临时 Clash 配置文件
- `upload_configs.py` - 生成 Clash 配置并将配置上传到 Google Cloud Storage 的脚本
- `requirements.txt` - Python 依赖项

## 设置

1. 安装依赖项：
```bash
pip install -r requirements.txt
```

2. 设置 Google Cloud 凭据：
   - 安装 Google Cloud SDK
   - 运行 `gcloud auth application-default login`
   - 或设置 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量

3. **将 `app_config_tmp.yaml` 复制到 `app_config.yaml` 并配置**：
```yaml
bucket_name: your-bucket-name
ss_urls:
    - ss://method:password@server:port
```

## 使用

1. 将您的 Shadowsocks URL 添加到 `app_config.yaml` 中的 `ss_urls` 列表：
```yaml
ss_urls:
    - ss://method:password@server:port
```

2. 上传配置：
```bash
python upload_configs.py
```

脚本将输出两个配置的公共 URL。

## 开发

- Python 3.6+
- 使用 `ruamel.yaml` 处理 YAML
- 使用 `google-cloud-storage` 进行 GCS 操作

## 许可证

MIT