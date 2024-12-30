from setuptools import setup, find_packages

setup(
    name='auto-ss-config',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'google-cloud-storage',
        'ruamel.yaml',
    ],
    entry_points={
        'console_scripts': [
            'update-config=auto_ss_config.update_config:update_config',
            'decode-ss-url=auto_ss_config.update_config:update_config_yaml',
        ],
    },
    author='Zhiwei Li',
    author_email='lzwjava@example.com',
    description='A library to update Shadowsocks configuration and upload to Google Cloud Storage',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lzwjava/auto-ss-config',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
