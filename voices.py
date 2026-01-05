voices = {}

def save_voice(key: str, file_id: str):
    voices[key] = file_id

def get_voice(key: str):
    return voices.get(key)
