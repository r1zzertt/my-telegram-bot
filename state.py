users = {}

def reset_user(user_id: int):
    users[user_id] = {
        "node": "start",
        "inventory": [],
        "wait_voice": None,
        "flags": {}
    }

def get_user_state(user_id: int):
    return users.setdefault(user_id, {
        "node": "start",
        "inventory": [],
        "wait_voice": None,
        "flags": {}
    })

def wait_for_voice(user, key):
    user["wait_voice"] = key

def clear_wait(user):
    user["wait_voice"] = None
