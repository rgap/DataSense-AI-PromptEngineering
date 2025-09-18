def clean_json_keys(obj):
    """
    Clean JSON keys by removing unwanted characters and whitespace.
    """
    if isinstance(obj, dict):
        return {
            k.strip().replace('\n', '').replace('"', '').replace("'", ''):
            clean_json_keys(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [clean_json_keys(item) for item in obj]
    return obj
