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
#Agregar Vehículo
@bot.message_handler(regexp=r"(^)agregar vehiculo|agv placa ([a-zA-Z0-9_ ]*) tipo ([0-9]{1,})($)")
def on_reg_vehicle(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)agregar vehiculo|agv placa ([a-zA-Z0-9_ ]*) tipo ([0-9]{1,})($)", message.text, re.IGNORECASE)

    #Ejemplos: Carro: AGV PLACA UES070 TIPO 2     Moto: agv placa NAN208 tipo 1 
              
    placa = parts.group(2)
    tipo = float (parts.group(3))

    idUsuario = message.from_user.id
    
    tipoVehiculo = None

    if tipo == 1 : 
        tipoVehiculo = "Carro"

    if tipo == 2 : 
        tipoVehiculo = "Moto"    

    if tipo not in [1, 2]:
	    bot.reply_to(message, f"Error, tipo de registro inválido: {tipo} Digite 1 para Carro ó 2 para Moto")
	    return 

    control = logic.add_vehiculo (tipoVehiculo, placa, idUsuario)

    bot.reply_to(
        message,
        f"🚗 Vehículo Registrado con Placa:  {placa}" if control == True
        else "🙈 Tuve problemas registrando el Vehiculo, ejecuta /start y vuelve a intentarlo")  

######################################################### 
# Listar Vehículos
@bot.message_handler(regexp=r"^(listar vehiculos|lsv)$")
def on_list_vehiculos(message):
	bot.send_chat_action(message.chat.id, 'typing')

	text = ""	
	vehiculos = logic.list_vehiculos()

	text = "``` Listado de vehiculos:\n\n"

	for vehiculo in vehiculos:
		text += f"| Tipo:  {vehiculo.tipo_vehiculo} | Placa: {vehiculo.placa} | ID: {vehiculo.id_vehiculo}|\n"

	text += "```"
	
	bot.reply_to(message, text, parse_mode="Markdown")
    
#########################################################     
# Eliminar Vehiculo
@bot.message_handler(regexp=r"(^)remover vehiculo|rmv placa ([a-zA-Z0-9_ ]*)($)")
def on_remove_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)remover vehiculo|rmv placa ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)
    
    #Ejemplo: rmv placa UES071

    placaVehiculo = parts.group(2)
    
    control = logic.remove_vehiculo(message.from_user.id, placaVehiculo)
    
    bot.reply_to(message, f"🚗 Vehículo con placa {placaVehiculo} removido." if control else f"🚨 No se pudo remover el vehículo con placa: {placaVehiculo}")

######################################################### 
# Registrar Ingreso del Vehiculo
@bot.message_handler(regexp=r"(^)registrar ingreso|ingreso|ring placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)")
def on_in_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)registrar ingreso|ingreso|ring placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)

    placaVehiculo = parts.group(2)
    zonaVehiculo = parts.group(3)
    
    #Ejemplo: ring placa UES070 en la zona ZN02

    try:
        disponibilidad = logic.get_disponibilidad_zona(zonaVehiculo)

        estado = float(0); 

        if disponibilidad == True:
            control = logic.ingresar_vehiculo(message.from_user.id, placaVehiculo, zonaVehiculo)
            logic.update_dispo_zona(zonaVehiculo, estado)
            bot.reply_to(
            message,
            f"🚗 Vehículo Ingrezado a la Zona:  {zonaVehiculo}" if control == True
            else "🙈 Tuve problemas ingresando el Vehiculo, ejecuta /start y vuelve a intentarlo") 
        else:    
            bot.reply_to(message, f"😔 Zona: {zonaVehiculo} no se encuentra disponible") 
    except:
            bot.reply_to(message, f"💩 Tuve problemas ingresando el Vehiculo, valida la zona, ejecuta /start y vuelve a intentarlo")

######################################################### 
# Registrar Salida del Vehiculo 
@bot.message_handler(regexp=r"(^)registrar salida|salida|rsal placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)")
def on_out_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)registrar salida|salida|rsal placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)

    placaVehiculo = parts.group(2)
    zonaVehiculo = parts.group(3)
        
    #Ejemplo: rsal placa UES070 en la zona ZN02

    try:
        estado = float(1)

        control = logic.reg_salida_vehiculo(message.from_user.id, placaVehiculo)
        logic.update_dispo_zona(zonaVehiculo, estado)
        bot.reply_to(
            message,
            f"🚗 Salida exitosa de Vehículo:  {placaVehiculo}" if control == True
            else "🙈 Tuve problemas con la salida del Vehiculo, ejecuta /start y vuelve a intentarlo") 
    except:
            bot.reply_to(message, f"💩 Tuve problemas ingresando el Vehiculo, valida la zona y placa, ejecuta /start y vuelve a intentarlo")

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