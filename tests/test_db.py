import unittest
from unittest.mock import MagicMock
from internal import log_usage, models
ToolUsageLog = models.ToolUsageLog

class TestDatabase(unittest.TestCase):
    def test_log_usage_insertion(self):
        # Mock database session
        mock_db = MagicMock()
        
        # Call the function
        log_usage(mock_db, "test_tool")
        
        # Verify db.add was called
        mock_db.add.assert_called_once()
        # Verify it was a ToolUsageLog object
        added_obj = mock_db.add.call_args[0][0]
        self.assertIsInstance(added_obj, ToolUsageLog)
        self.assertEqual(added_obj.tool_name, "test_tool")
        
        # Verify commit and refresh
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(added_obj)

if __name__ == '__main__':
    unittest.main()
