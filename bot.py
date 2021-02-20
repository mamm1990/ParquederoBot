#########################################################
from sqlalchemy.sql.functions import func
from telebot.types import Message
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
#   4. Agregar, Listar y Eliminar Vehiculo y PRuebas
#	5. Registrar Ingreso y Salidad del Vehiculo y Pruebas
@bot.message_handler(commands=['about'])
def on_command_about(message):
    
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
    message.chat.id,
    logic.get_about_this(config.VERSION), parse_mode="Markdown")

#########################################################
#   4. Agregar, Listar y Eliminar Vehiculo y PRuebas
#	5. Registrar Ingreso y Salidad del Vehiculo y Pruebas
#@bot.message_handler(regexp=r"(^)(agregar vehiculo|agv) ([+-]?([0-9]*[.])?[0-9]+) ([A-Z0-9\-]+)$")
@bot.message_handler(regexp=r"(^)agregar vehiculo|agv ([a-zA-Z0-9_ ]*) tipo ([0-9]{1,})($)")
def on_reg_vehicle(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)agregar vehiculo|agv ([a-zA-Z0-9_ ]*) tipo ([0-9]{1,})($)", message.text)

    # print (parts.groups())
    placa = parts.group(2)
    tipo = float (parts.group(3))

    idUsuario = message.from_user.id
    
    tipoVehiculo = None

    if tipo == 1 : 
        tipoVehiculo = "Moto"

    if tipo == 2 : 
        tipoVehiculo = "Carro"     

    control = logic.add_vehiculo (tipoVehiculo, placa, idUsuario)

    bot.reply_to(
        message,
        f"\U0001F6FB Vehículo Registrado con Placa:  {placa}" if control == True
        else "\U0001F4A9 Tuve problemas registrando el Vehiculo, ejecuta /start y vuelve a intentarlo")  


        #parts = re.match(
     #   r"(^)(agregar vehiculo|agv) ([+-]?([0-9]*[.])?[0-9]+) ([a-zA-Z0-9_ ]*)$",          
      #  message.text,
      #  re.IGNORECASE) 

    

    #print (parts.groups())         
    #placa = parts.group(4) 
    #tipo = parts.group(3) 
    #tipo = float(parts[4]) 

    #@bot.message_handler(regexp=r"(^)agregar ([a-zA-Z0-9_ ]*) prioridad ([0-9]{1,})($)")

    #parts = re.match(r"(^)agregar ([a-zA-Z0-9_ ]*) prioridad ([0-9]{1,})($)", message.text)

	# print (parts.groups())
	#task = parts.group(2)
	#priority = parts.group(3)  
    


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