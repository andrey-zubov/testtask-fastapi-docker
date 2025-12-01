import os
import boto3
import uuid


class DBLogger:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-west-2",
            endpoint_url=os.getenv("DYNAMO_ENDPOINT", "http://localhost:8001"),  # todo for debug only
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "local"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "local"),
        )
        self.logs_table = self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        client = self.dynamodb.meta.client
        existing_tables = client.list_tables()["TableNames"]
        table_name = os.getenv("LOGS_TABLE_NAME", "locallogs")
        if table_name not in existing_tables:
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            table.wait_until_exists()
        return self.dynamodb.Table(table_name)

    def log(self, task: dict, filename: str):
        message = f"{task['city']}; {task['timestamp']}; {filename}"

        self.logs_table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "message": message,
                "timestamp": int(task['timestamp']),
            }
        )
