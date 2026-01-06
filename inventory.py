def add_item(user, item: str):
    if item not in user["inventory"]:
        user["inventory"].append(item)

def inventory_text(user):
    if not user["inventory"]:
        return "🎒 Инвентарь пуст."
    return "🎒 Инвентарь:\n\n" + "\n".join(f"• {item}" for item in user["inventory"])

def remove_item(user, item):
    if item in user.get("inventory", []):
        user["inventory"].remove(item)
        return True
    return False
