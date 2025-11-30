from typing import Any

def postprocess_data(data: dict[str, Any]):
    keys_to_keep = ['name', 'main', 'wind', 'clouds']
    cleaned_data = {k: data.get(k) for k in keys_to_keep}
    return cleaned_data
