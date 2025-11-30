from typing import Any

from app.datahandler import StorageData


storage = StorageData()


def postprocess_data(data: dict[str, Any]):
    storage.save_data(data)
    keys_to_keep = ['name', 'main', 'wind', 'clouds']
    cleaned_data = {k: data.get(k) for k in keys_to_keep}
    return cleaned_data
