import json
import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from telegram import InlineQueryResultPhoto, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
from telegram.ext.filters import Command

load_dotenv()

whitelist = os.environ["OLSZEBOT_ALLOWED_USERS"].split(",")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi!")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or str(update.effective_user.id) not in whitelist:
        return
    query = update.inline_query.query.strip().lower()
    if query == "":
        return

    requested_tags = [tag.strip() for tag in query.split()]
    matching = []
    found = []
    for sticker in stickers:
        for tag in sticker["tags"]:
            for requested in requested_tags:
                if requested in tag:
                    if sticker["file"] not in found:
                        found.append(sticker["file"])
                        matching.append(sticker)
    results = []
    for sticker in matching:
        result = InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url=base_url+sticker["file"],
            thumb_url=base_url+sticker["file"],
        )
        results.append(result)

    await update.inline_query.answer(results)


with open("./stickers.json") as f:
    config = json.load(f)
    stickers = config["stickers"]
    base_url = config["base_url"]


def main() -> None:
    application = Application.builder().token(os.environ["TELEGRAM_API_TOKEN"]).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.run_polling()

if __name__ == "__main__":
    main()

