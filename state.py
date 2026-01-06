# хранение состояния пользователей
USERS = {}

def get_user_state(user_id):
    if user_id not in USERS:
        USERS[user_id] = {"inventory": [], "node": "start", "wait_voice": None}
    return USERS[user_id]

def reset_user(user_id):
    USERS[user_id] = {"inventory": [], "node": "start", "wait_voice": None}

def wait_for_voice(user, key):
    user["wait_voice"] = key
