import os
import json
import uuid
import shutil

# ---------------- Folders ---------------- #

ACTIVE_FOLDER = "chat_data/active"
ARCHIVE_FOLDER = "chat_data/archived"

os.makedirs(ACTIVE_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)


# ---------------- Create Chat ---------------- #

def create_chat():

    chat_id = str(uuid.uuid4())

    data = {
        "title": "New Chat",
        "messages": [],
        "pinned": False
    }

    with open(
        os.path.join(ACTIVE_FOLDER, f"{chat_id}.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    return chat_id


# ---------------- Load Chat ---------------- #

def load_chat(chat_id):

    path = os.path.join(
        ACTIVE_FOLDER,
        f"{chat_id}.json"
    )

    if not os.path.exists(path):

        return {
            "title": "New Chat",
            "messages": [],
            "pinned": False
        }

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    # Old chats compatibility
    if "pinned" not in data:
        data["pinned"] = False

    return data


# ---------------- Save Chat ---------------- #

def save_chat(chat_id, data):

    with open(
        os.path.join(
            ACTIVE_FOLDER,
            f"{chat_id}.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# ---------------- Get Active Chats ---------------- #

def get_all_chats():

    chats = []

    for file in os.listdir(ACTIVE_FOLDER):

        if file.endswith(".json"):

            chat_id = file.replace(".json", "")

            with open(
                os.path.join(
                    ACTIVE_FOLDER,
                    file
                ),
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            chats.append(
                (
                    chat_id,
                    data.get(
                        "title",
                        "New Chat"
                    ),
                    data.get(
                        "pinned",
                        False
                    )
                )
            )

    # Pinned chats first
    chats.sort(
        key=lambda x: (
            not x[2],
            x[1]
        )
    )

    return chats


# ---------------- Rename Chat ---------------- #

def rename_chat(chat_id, new_title):

    data = load_chat(chat_id)

    data["title"] = new_title

    save_chat(
        chat_id,
        data
    )


# ---------------- Delete Chat ---------------- #

def delete_chat(chat_id):

    path = os.path.join(
        ACTIVE_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(path):

        os.remove(path)


# ---------------- Archive Chat ---------------- #

def archive_chat(chat_id):

    src = os.path.join(
        ACTIVE_FOLDER,
        f"{chat_id}.json"
    )

    dst = os.path.join(
        ARCHIVE_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(src):

        shutil.move(
            src,
            dst
        )


# ---------------- Get Archived Chats ---------------- #

def get_archived_chats():

    chats = []

    for file in os.listdir(
        ARCHIVE_FOLDER
    ):

        if file.endswith(".json"):

            chat_id = file.replace(
                ".json",
                ""
            )

            with open(
                os.path.join(
                    ARCHIVE_FOLDER,
                    file
                ),
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            chats.append(
                (
                    chat_id,
                    data.get(
                        "title",
                        "New Chat"
                    )
                )
            )

    return chats


# ---------------- Restore Chat ---------------- #

def restore_chat(chat_id):

    src = os.path.join(
        ARCHIVE_FOLDER,
        f"{chat_id}.json"
    )

    dst = os.path.join(
        ACTIVE_FOLDER,
        f"{chat_id}.json"
    )

    if os.path.exists(src):

        shutil.move(
            src,
            dst
        )


# ---------------- Pin Chat ---------------- #

def pin_chat(chat_id):

    data = load_chat(chat_id)

    data["pinned"] = True

    save_chat(
        chat_id,
        data
    )


# ---------------- Unpin Chat ---------------- #

def unpin_chat(chat_id):

    data = load_chat(chat_id)

    data["pinned"] = False

    save_chat(
        chat_id,
        data
    )