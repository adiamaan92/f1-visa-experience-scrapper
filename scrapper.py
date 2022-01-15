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


def get_experiences(api: KaggleApi) -> pd.DataFrame:
    api.dataset_download_files(
        "adiamaan/f1-visa-experiences", path="./data", unzip=True
    )
    return pd.read_csv("./data/telegram.csv")


async def get_messages(client: TelegramClient, max_id: int) -> pd.DataFrame:
    channel = await client.get_entity("f1interviewreviews")
    messages = await client.get_messages(channel, min_id=max_id + 1, limit=10000)
    return pd.DataFrame(
        [{"msg_id": x.id, "date": x.date, "message": x.message} for x in messages]
    )


def write_experiences(experiences: pd.DataFrame, new_experiences: pd.DataFrame):
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
    # Username and password set as environment variables
    api = KaggleApi()
    api.authenticate()

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
