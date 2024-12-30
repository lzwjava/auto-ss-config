import unittest
from unittest.mock import patch
from auto_ss_config.update_config import update_config

class TestUpdateConfig(unittest.TestCase):
    @patch('auto_ss_config.update_config.run_shell_command')
    @patch('auto_ss_config.update_config.storage.Client')
    def test_update_config(self, mock_client, mock_run_shell_command):
        # Add your test cases here
        update_config()
        mock_run_shell_command.assert_called_once_with("python update-config.py")
        mock_client.assert_called_once()

if __name__ == '__main__':
    unittest.main()
