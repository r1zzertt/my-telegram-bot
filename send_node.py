from nodes.story import NODES, CAT_ACTIONS, TREE_ACTIONS
from state import get_user_state
from inventory import add_item
from keyboards import node_keyboard

async def send_node(message, node_id: str):
    user = get_user_state(message.from_user.id)

    if node_id == "act11_branch":
        if "🐶 Щенок" in user.get("inventory", []):
            await send_node(message, "act11_with_puppy")
        else:
            await send_node(message, "act11_without_puppy")
        return

    if node_id in CAT_ACTIONS:
        await message.answer(CAT_ACTIONS[node_id])
        hub = NODES["cat_hub"]
        await message.answer(hub["text"], reply_markup=node_keyboard(hub["actions"]))
        return

    if node_id in TREE_ACTIONS:
        await message.answer(TREE_ACTIONS[node_id])
        return

    node = NODES.get(node_id)
    if not node:
        await message.answer("Что-то пошло не так… 🌫")
        return

    user["node"] = node_id

    if node_id == "cat_hub":
        add_item(user, "🌸 Цветок тишины")
    if node_id == "puppy_take":
        add_item(user, "🐶 Щенок")

    await message.answer(
        node["text"],
        reply_markup=node_keyboard(node.get("actions", {}))
    )
