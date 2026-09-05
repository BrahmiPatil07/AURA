import json
import os

MEMORY_FILE = "memory.json"

# Keep only the 10 most recent messages
MAX_MEMORY = 10


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return []


conversation_history = load_memory()


def add_message(role, content):

    conversation_history.append({
        "role": role,
        "content": content
    })

    # Keep only recent messages
    if len(conversation_history) > MAX_MEMORY:
        del conversation_history[:-MAX_MEMORY]

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            conversation_history,
            file,
            indent=2
        )


def get_memory():
    return conversation_history