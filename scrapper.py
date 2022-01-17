"""
F1 Interview Scrapper
---------------------

This module adds the latest interview experience to the existing
kaggle dataset at, https://www.kaggle.com/adiamaan/f1-visa-experiences

Workflow
--------
1. Download the latest kaggle dataset containing data from previous run
2. Get a list of new experiences that are added from the last run
3. Fetch the latest experiences, update to the existing dataset and upload
back to Kaggle

"""
import asyncio
import datetime
import logging
import os

import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from telethon import TelegramClient

logging.basicConfig(level=logging.INFO)

TELEGRAM_SESSION = str(os.getenv("TELEGRAM_SESSION"))
TELEGRAM_USER = str(os.getenv("TELEGRAM_USER"))
TELEGRAM_HASH = str(os.getenv("TELEGRAM_HASH"))
GIT_CRYPT_KEY = str(os.getenv("GIT_CRYPT_KEY"))


def decode_session_file():
    """Decodes the session file using the GIT_CRYPT_KEY from
    environment variable

    Args:
        file_path (Path): Path to the telegram session file
    """
    with open("./key", "w", encoding="utf-8") as text_file:
        text_file.write(GIT_CRYPT_KEY)

    os.system("git-crypt unlock key")
    os.remove("key")


def get_experiences(api: KaggleApi) -> pd.DataFrame:
    """Get existing experiences from Kaggle API

    Args:
        api (KaggleApi): Kaggle API instance

    Returns:
        pd.DataFrame: DataFrame of existing experiences
    """
    api.dataset_download_files(
        "adiamaan/f1-visa-experiences", path="./data", unzip=True
    )
    return pd.read_csv("./data/telegram.csv")


async def get_messages(client: TelegramClient, max_id: int) -> pd.DataFrame:
    """Get messages from Telegram API that are greater than the max_id

    Args:
        client (TelegramClient): Telegram client instance
        max_id (int): Maximum message ID to get messages from.
        Usually this is the last message ID from the previous run

    Returns:
        pd.DataFrame: New messages in a dataframe
    """
    channel = await client.get_entity("f1interviewreviews")
    messages = await client.get_messages(channel, min_id=max_id + 1, limit=10000)
    return pd.DataFrame(
        [{"msg_id": x.id, "date": x.date, "message": x.message} for x in messages]
    )


def write_experiences(experiences: pd.DataFrame, new_experiences: pd.DataFrame):
    """Combine new experiences with existing experiences and create a new dataset version

    Args:
        experiences (pd.DataFrame): Existing experiences
        new_experiences (pd.DataFrame): New experiences
    """
    all_experiences = (
        pd.concat([new_experiences, experiences])
        .sort_values("msg_id", ascending=False)
        .reset_index(drop=True)
    )
    all_experiences.to_csv("./data/telegram.csv", index=False)
    api.dataset_create_version(
        "./data/",
        version_notes=f"Updated on {datetime.datetime.now().strftime('%Y-%m-%d')}",
    )


if __name__ == "__main__":
    # Kaggle Username and password is expected to be set as environment variables
    api = KaggleApi()
    api.authenticate()

    decode_session_file()

    client = TelegramClient(TELEGRAM_SESSION, TELEGRAM_USER, TELEGRAM_HASH)
    client.start()

    experiences = get_experiences(api)
    max_msg_id = experiences.msg_id.max()

    loop = asyncio.get_event_loop()
    new_experiences = loop.run_until_complete(get_messages(client, max_msg_id))

    if new_experiences.shape[0] == 0:
        logging.info("No new experiences found")
        exit()

    write_experiences(experiences, new_experiences)
    logging.info(f"Added {len(new_experiences)} new experiences")
