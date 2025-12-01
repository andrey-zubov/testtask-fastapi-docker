from typing import Any

from app.datastorage import StorageData
from app.log_utils import DBLogger


storage = StorageData()
db_logger = DBLogger()

# i think it is more readable than as deco in this case
def postprocess_response(data: dict[str, Any], task: dict[str, Any]):
    file_name = f'data/{task["city"]}_{task["timestamp"]}.json'

    storage.save_data(data, task['city'], file_name)
    db_logger.log(task, file_name)
    keys_to_keep = ['name', 'main', 'wind', 'clouds']
    cleaned_data = {k: data.get(k) for k in keys_to_keep}
    return cleaned_data
