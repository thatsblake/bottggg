import getopt
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from escupidobot.controller import BotController
from escupidobot.model import InputBot

HELP_TEXT = "bot.py -t token [-d 14]"


def read_configuration(argv):
    try:
        opts, args = getopt.getopt(argv, "ht:", ["token="])
        token = ''

    except getopt.GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(HELP_TEXT)
            sys.exit(0)
        elif opt in ['-t', '--token']:
            token = arg

    return InputBot(token)


class TheBot:

    def __init__(self, input_bot: InputBot):
        self.token = input_bot.token

    def execute(self):
        updater = Updater(token=self.token, use_context=True)
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", BotController.help))
        dp.add_handler(CommandHandler("hello", BotController.hello))
        dp.add_handler(CommandHandler("message", BotController.message))
        dp.add_handler(CommandHandler("enviar", BotController.message))
        dp.add_handler(CommandHandler("letterbox", BotController.letterbox))
        dp.add_handler(CommandHandler("recibir", BotController.letterbox))
        dp.add_handler(CommandHandler("help", BotController.help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, BotController.echo))

        # log all errors
        dp.add_error_handler(BotController.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    input_bot = read_configuration(sys.argv[1:])
    the_bot = TheBot(input_bot)
    the_bot.execute()
