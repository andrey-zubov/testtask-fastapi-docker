import os


from typing import Any


class StorageData:
    def __init__(self):
        self.storage = os.getenv('STORAGE')

        if self.storage == 's3':
            pass  # todo add s3 init with boto

    def save_data(self, data: Union[str, dict[str, Any]]):
        if isinstance(data, dict):
            data = str(data)

        if self.storage == 'local':
            with open(file_name, 'w') as file:
                file.write(data + '\n')
        elif self.storage == 's3':
            pass
