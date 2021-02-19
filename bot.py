#########################################################
from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

#########################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    logic.insert_admins()

#########################################################
@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
    message.chat.id,
    logic.get_welcome_message(bot.get_me()),
    parse_mode="Markdown")
    bot.send_message(
    message.chat.id,
    logic.get_help_message(),
    parse_mode="Markdown")

#########################################################
@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
    message.chat.id,
    logic.get_help_message(),
    parse_mode="Markdown")

#########################################################
@bot.message_handler(commands=['about'])
def on_command_about(message):
    
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
    message.chat.id,
    logic.get_about_this(config.VERSION), parse_mode="Markdown")

#########################################################
#*Consultar Ubicacion del Vehiculo en la zona de parqueo 
# y pruebas, 
#*Casos de refactorizacion
#*Ubicar vehiculo|ubicar|ubv {placa}* - Ubicar Vehículo\n"

@bot.message_handler(regexp=r"^(ubicar vehiculo|placa) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_earnings(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    parts = re.match(
    r"^(ubicar vehiculo|placa) en ([0-9]{1,2}) de ([0-9]{4})$",
    message.text)
    
    zona = logic.get_zona (message.from_user.id)
    text=""  
    
    if not zona:
        text = f"\U0001F633 El vehiculo no está parqueado en ninguna zona"
    else:
        text = "``` La zona en que se encuentra ubicado el vehiculo es:\n\n"
        zona
        
        bot.reply_to(message, text, parse_mode="Markdown")

#########################################################
# Default cuando se ingresa un valor invalido:
@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)

    bot.send_message(
        message.chat.id,
        logic.get_help_message(),
        parse_mode="Markdown")
        
########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################