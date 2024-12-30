import unittest
from unittest.mock import patch, mock_open
from auto_ss_config.decode_ss_url import decode_ss_url, update_config_yaml

class TestDecodeSSUrl(unittest.TestCase):
    def test_decode_ss_url(self):
        ss_url = "ss://YWVzLTI1Ni1nY206dGVzdDpzc291cmNl@example.com:8388"
        expected = {
            'server': 'example.com',
            'port': 8388,
            'cipher': 'aes-256-gcm',
            'password': 'test'
        }
        self.assertEqual(decode_ss_url(ss_url), expected)

    @patch('builtins.open', new_callable=mock_open, read_data='ss://YWVzLTI1Ni1nY206dGVzdDpzc291cmNl@example.com:8388')
    def test_update_config_yaml(self, mock_file):
        update_config_yaml()
        mock_file.assert_called_with('ssconfig', 'r')
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
