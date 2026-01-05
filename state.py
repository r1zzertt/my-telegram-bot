users = {}

def reset_user(user_id: int):
    users[user_id] = {
        "node": "start",
        "inventory": []
    }

def get_user_state(user_id: int):
    return users.setdefault(user_id, {
        "node": "start",
        "inventory": []
    })
