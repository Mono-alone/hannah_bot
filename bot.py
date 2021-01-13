import os

from random import randint
from telegram import Update
from telegram.chat import Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.messageentity import MessageEntity


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('I am the Sexy Hannah Bot! Use /help to learn how to talk to me.')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("I'll reply to any mention in a group chat. Or just text me privately.")


def get_hannah_line():
    with open("hannah_lines.txt", "r") as hannah_text_source:
        lines = hannah_text_source.readlines()
        return lines[randint(0, len(lines)-1)]


def send_hannah_line(update: Update, context: CallbackContext) -> None:
    """
    Send a generated Hannah line. In personal chats, the bot will reply to any message.
    In group chats, the bot will only reply if mentioned
    """
    if update.message.chat.type == Chat.GROUP:
        entities = update.message.entities
        if len(entities) > 0 and entities[0].type == MessageEntity.MENTION:
            update.message.reply_text(get_hannah_line())
    else:
        update.message.reply_text(get_hannah_line())


def main():
    """Start the bot."""

    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - send a Hannah line
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_hannah_line))

    # Start the Bot
    print("Running the Hannah Bot")
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()