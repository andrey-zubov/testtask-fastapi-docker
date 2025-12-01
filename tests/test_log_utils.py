import unittest
from unittest.mock import patch, MagicMock

from log_utils import DBLogger


class TestLogUtils(unittest.TestCase):
    def setUp(self):
        DBLogger._instance = None

    @patch("boto3.resource")
    def test_db_logger_initialization(self, mock_boto):
        mock_instance = MagicMock()
        mock_boto.return_value = mock_instance
        mock_instance.meta.client.list_tables.return_value = {"TableNames": []}

        logger = DBLogger()

        assert logger.logs_table is not None
        assert mock_boto.called


    @patch("boto3.resource")
    def test_db_logger_log(self, mock_boto):
        mock_table = MagicMock()
        mock_dynamo = MagicMock()
        mock_dynamo.Table.return_value = mock_table
        mock_dynamo.meta.client.list_tables.return_value = {"TableNames": []}

        mock_boto.return_value = mock_dynamo

        logger = DBLogger()
        task = {"city": "minsk", "timestamp": 123}
        logger.log(task, "file.json")
