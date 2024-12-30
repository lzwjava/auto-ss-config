import unittest
from unittest.mock import patch, mock_open, MagicMock
from auto_ss_config.update_config import decode_ss_url, update_config_yaml, update_config
from ruamel.yaml import YAML

class TestUpdateConfig(unittest.TestCase):
    def test_decode_ss_url(self):
        # Test valid SS URL
        test_url = "ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@server.com:8388"
        expected = {
            'server': 'server.com',
            'port': 8388,
            'cipher': 'aes-256-gcm',
            'password': 'password'
        }
        self.assertEqual(decode_ss_url(test_url), expected)

        # Test invalid SS URL
        self.assertIsNone(decode_ss_url("invalid_url"))

    @patch('builtins.open', new_callable=mock_open, read_data="ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@server.com:8388\n")
    def test_update_config_yaml(self, mock_file):
        # Mock the YAML operations
        mock_yaml = MagicMock()
        mock_yaml.load.return_value = {
            'proxies': [],
            'proxy-groups': [
                {
                    'name': 'Proxy',
                    'type': 'select',
                    'proxies': []
                }
            ],
            'rules': [
                'MATCH,DIRECT'
            ]
        }
        mock_yaml.preserve_quotes = True
        mock_yaml.indent = MagicMock()

        # Set up the mock file handler for config.yaml
        mock_file_handle = mock_file()
        mock_file_handle.write = MagicMock()
        
        with patch('ruamel.yaml.YAML', return_value=mock_yaml):
            # Run the function
            update_config_yaml('ssconfig')

            # Verify file operations
            mock_file.assert_any_call('ssconfig', 'r')
            mock_file.assert_any_call('config.yaml', 'r')
            mock_file.assert_any_call('config.yaml', 'w')

            # Verify YAML operations
            self.assertTrue(mock_yaml.dump.called)

    @patch('update_config.update_config_yaml')
    @patch('google.cloud.storage.Client')
    def test_update_config(self, mock_client_class, mock_update_yaml):
        # Mock dependencies
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_acl = MagicMock()
        mock_user = MagicMock()

        # Setup mock chain
        mock_client_class.return_value = mock_client
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.acl = mock_acl
        mock_acl.user.return_value = mock_user

        # Run the function
        update_config('test-bucket', 'ssconfig')

        # Verify update_config_yaml was called
        mock_update_yaml.assert_called_once_with('ssconfig')

        # Verify GCS operations
        mock_client.bucket.assert_called_once_with('test-bucket')
        mock_bucket.blob.assert_any_call('ssconfig')
        mock_bucket.blob.assert_any_call('config.yaml')
        self.assertEqual(mock_blob.upload_from_filename.call_count, 2)
        self.assertEqual(mock_blob.patch.call_count, 2)
        self.assertEqual(mock_acl.save.call_count, 2)
        mock_acl.user.assert_has_calls([
            unittest.mock.call('allUsers'),
            unittest.mock.call('allUsers')
        ])
        mock_user.grant_read.assert_has_calls([
            unittest.mock.call(),
            unittest.mock.call()
        ])

if __name__ == '__main__':
    unittest.main()
