import re

from telegram import Update
from telegram.ext import CallbackContext
import datetime
from escupidobot.logger import BotLogger
from escupidobot.persistence import DataEngine


initial_text = "Para /enviar solo tienes que mencionar el nombre de la persona a la que amas con " \
               "@nick y escribirle una carta de amor. Por ejemplo:\n" \
               "/enviar @nick eres lo más hermoso que pisa la tierra, si pudiera, a besos te comería\n\n" \
               "Escribe /recibir y te llegarán los mensajes que han dejado para tí en el buzón del amor"


# Definition of command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


class BotController:

    the_logger = BotLogger.get_logger('./escupidobot.log')

    @staticmethod
    def hello(update: Update, context: CallbackContext):
        user = update.message.from_user
        update.message.reply_text(f"¡Hola {user['first_name']}!")

    @staticmethod
    def help(update: Update, context: CallbackContext):
        update.message.reply_text(initial_text)

    @staticmethod
    def message(update: Update, context: CallbackContext):
        text = update.message.text
        user = update.message.from_user
        BotController.__process_message_text(text, update, user)

    @staticmethod
    def echo(update: Update, context: CallbackContext):
        text = update.message.text
        text = re.sub("[aeou]", "i", text)
        text = re.sub("[áéóú]", "í", text)
        text = re.sub("[AEOU]", "I", text)
        text = re.sub("[ÁÉÓÚ]", "Í", text)
        update.message.reply_text(text)

    @staticmethod
    def error(update: Update, context: CallbackContext):
        BotController.the_logger.warning('Update "%s" caused error "%s"', update, context.error)

    @staticmethod
    def letterbox(update: Update, context: CallbackContext):
        now = datetime.datetime.now()
        if now.day == 14 and now.month == 2:
            user = update.message.from_user
            messages = DataEngine.read(user)
            final_text = BotController.__letterbox_text(messages, user)
            update.message.reply_text(final_text)
        else:
            update.message.reply_text("Hoy Cupido no está trabajando, tendrás que esperar")

    @staticmethod
    def __process_message_text(text, update, user):
        fields = text.split(" ", 2)
        if len(fields) != 3 or not fields[1].startswith("@"):
            update.message.reply_text(f"Vaya, no esperaba ese formato para enviar un mensaje. "
                                      f"Prueba con /enviar @user texto.")
        else:
            DataEngine.save(user, fields[1], fields[2])
            update.message.reply_text("El mensaje ha sido almacenado hasta su entrega!")

    @staticmethod
    def __letterbox_text(messages, user):
        if len(messages) == 0:
            final_text = f"Lo siento {user['first_name']}, Cupido no tiene ningun mensaje para tí"
        elif len(messages) == 1:
            final_text = user['first_name'] + ", tienes 1 mensaje:\n\n" + messages[0].text;
        else:
            texts = [str(index + 1) + ': ' + m.text for index, m in enumerate(messages)]
            greeting = f"{user['first_name']}, tienes {len(messages)}  mensajes:\n\n"
            final_text = greeting + '\n'.join(texts)
        return final_text




