#########################################################
from sqlalchemy.sql.functions import func
from telebot.types import Message
from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

import sys

#########################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    logic.insert_admins()

#########################################################
@bot.message_handler(commands=['start', 'Start', 'START'])
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
@bot.message_handler(commands=['help','Help', 'HELP'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
    message.chat.id,
    logic.get_help_message(),
    parse_mode="Markdown")

#########################################################
@bot.message_handler(commands=['about', 'About', 'ABOUT'])
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

    try:
        placa = parts.group(2)
        tipo = float(parts.group(3))

        placaVehiculo = placa.upper()

        idUsuario = message.from_user.id

        tipoVehiculo = None
          
        obtenerPlaca = logic.get_placa (placaVehiculo)
        
        if  not obtenerPlaca:              

            tipoVehiculo=logic.getTipoVehiculo(tipo)

            control = logic.add_vehiculo (tipoVehiculo, placaVehiculo, idUsuario)

            bot.reply_to(
                message,
                f"🚗 Vehículo Registrado con Placa:  {placaVehiculo}" if control == True
                else "🙈 Tuve problemas registrando el Vehiculo, ejecuta /start y vuelve a intentarlo") 
        else: 
            bot.reply_to(message, f"🚨 El Vehículo con placa {placaVehiculo} ya se encuentra registrado.")
    except:
            bot.reply_to(message, f"💩 Tuve problemas agregando el Vehiculo, ejecuta /start valida tus datos y vuelve a intentarlo")
            #bot.reply_to(message, sys.exc_info()[0])
			
#########################################################  
# Listar Vehículos
@bot.message_handler(regexp=r"^(listar vehiculos|lsv)$")
def on_list_vehiculos(message):
    bot.send_chat_action(message.chat.id, 'typing')

    text = ""
    vehiculos = logic.list_vehiculos()

    if vehiculos:
        text = "``` Listado de vehiculos:\n\n"

        for vehiculo in vehiculos:
            text += f"| Tipo:  {vehiculo.tipo_vehiculo} | Placa: {vehiculo.placa} | ID: {vehiculo.id_vehiculo}|\n"
        text += "```"
    else:
        text = f"🚨 Aún no se encuentran vehículos registrados"
    bot.reply_to(message, text, parse_mode="Markdown")    
    
#########################################################     
# Eliminar Vehiculo
@bot.message_handler(regexp=r"(^)remover vehiculo|rmv placa ([a-zA-Z0-9_ ]*)($)")
def on_remove_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)remover vehiculo|rmv placa ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)

    #Ejemplo: rmv placa UES071

    try:
        placa = parts.group(2)

        placaVehiculo = placa.upper()

        obtenerPlaca = logic.get_placa (placaVehiculo)        
        
        if  not obtenerPlaca:  
            bot.reply_to(message, f"🚨 El vehículo con placa {placaVehiculo} no se encuentra registrado")
        else:                                   
            control = logic.remove_vehiculo(message.from_user.id, placaVehiculo)
            
            bot.reply_to(message, f"🚗 Vehículo con placa {placaVehiculo} removido." if control else f"🚨 No se pudo remover el vehículo con placa: {placaVehiculo}")
    except:
            bot.reply_to(message, f"💩 Tuve problemas removiendo el Vehiculo, ejecuta /start y vuelve a intentarlo")

#########################################################
#Agregar Zona de Parqueo
@bot.message_handler(regexp=r"(^)agregar zona|agz zona ([a-zA-Z0-9_ ]*)($)")
def on_reg_zona(message):
    bot.send_chat_action(message.chat.id, 'typing')	
        
    parts = re.match(r"(^)agregar zona|agz zona ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)
    
    try:
        id_zona = parts.group(2).upper()
        
        text=""

        if logic.check_admin(message.from_user.id): 
            obtenerZona = logic.get_IdZona(id_zona)

            if not obtenerZona:
			    #Ejemplo: agz zona ZN02
                
                disponibilidad_zona = 1
                
                control = logic.add_zona (id_zona, disponibilidad_zona)
                    
                if control == True :
                    text = f"🌳 Zona Registrada con identificacion:  {id_zona}"
                else:
                    text = f"😔 Tuve problemas registrando la zona, ejecuta /start y vuelve a intentarlo"
            else:
                text = f"🚨 La zona con identificación {id_zona} ya se encuentra registrada."
        else:
            text = f"🥺 Esta funcionalidad sólo está disponible para administradores"
            
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, f"💩 Tuve problemas agregando la Zona, ejecuta /start valida tus datos y vuelve a intentarlo")

######################################################### 
# Eliminar Zona de Parqueo
@bot.message_handler(regexp=r"(^)remover zona|rmz zona ([a-zA-Z0-9_ ]*)")
def on_remove_zona(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)remover zona|rmz zona ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)
    text = ""
    
    try:
        if logic.check_admin(message.from_user.id):
            #Ejemplo: rmz zona ZN01
            idZona = parts.group(2).upper()

            obtenerZona = logic.get_IdZona(idZona)
            
            if obtenerZona:
                
                control = logic.remove_zona(idZona)

                if control == True :
                    text = f"🌳 Zona de parqueo identicada con {idZona} removida con éxito."
                else:
                    text = f"🚨 No se pudo remover la zona identiciada: {idZona}"
            else:
                text = f"🚨 La zona con identificación {idZona} no se encuentra registrada." 
        else:
            text = f"🥺 Esta funcionalidad sólo está disponible para administradores"
            
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, f"💩 Tuve problemas eliminando la Zona, ejecuta /start valida tus datos y vuelve a intentarlo")
		
#########################################################      
# Listar Zona de Parqueo
@bot.message_handler(regexp=r"^(listar zonas|lsz)$")
def on_list_zona(message):
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    text = ""
    zona_disponible = ""
        
    Zonas = logic.list_zonas()

    if Zonas:
        text = "``` Listado de zonas de parqueo:\n\n"
            
        for Zona in Zonas:

            disponibilidad = Zona.disponible

            if disponibilidad == 1 : 
                zona_disponible = 'Disponible'
            if disponibilidad == 0 : 
                zona_disponible = 'No Disponible'
                                
            text += f"| Zona:  {Zona.id_zona}: {zona_disponible} |\n"
            
        text += "```"
    else:
        text = f"🚨 Aún no se encuentran zonas registradas"
        
    bot.reply_to(message, text, parse_mode="Markdown")

######################################################### 
# Registrar Ingreso del Vehiculo
@bot.message_handler(regexp=r"(^)registrar ingreso|ingreso|ring placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)")
def on_in_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)registrar ingreso|ingreso|ring placa ([a-zA-Z0-9_ ]*) en la zona ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)

    #Ejemplo: ring placa UES070 en la zona ZN02

    try:
        placaVehiculo = parts.group(2).upper()
        zonaVehiculo = parts.group(3).upper()

        zonaParqueo = ""

        idUsuario = message.from_user.id

        obtenerPlaca = logic.get_placa (placaVehiculo)
        zona = logic.get_IdZona(zonaVehiculo)        

        if zona:
            if  not obtenerPlaca:  
                bot.reply_to(message, f"🚨 El vehículo con placa {placaVehiculo} no se encuentra registrado")
            else:
                disponibilidad = logic.get_disponibilidad_zona(zonaVehiculo)

                estado = float(0)

                if disponibilidad == True:
                    zonaParqueo = logic.get_parking(placaVehiculo, idUsuario)        
                    if not zonaParqueo:
                        control = logic.ingresar_vehiculo(message.from_user.id, placaVehiculo, zonaVehiculo)
                        logic.update_dispo_zona(zonaVehiculo, estado)
                        bot.reply_to(
                        message,
                        f"🚗 Vehículo Ingrezado a la Zona:  {zonaVehiculo}" if control == True
                        else "🙈 Tuve problemas ingresando el Vehiculo, ejecuta /start y vuelve a intentarlo") 
                    else:
                        bot.reply_to(message, f"⚠️ El vehiculo: {placaVehiculo} ya se encuentra parqueado en zona {zonaParqueo}")
                else:    
                    bot.reply_to(message, f"⚠️ Zona: {zonaVehiculo} no se encuentra disponible")
        else:
            bot.reply_to(message, f"⚠️ Zona: {zonaVehiculo} no se encuentra registrada")        
    except:
            bot.reply_to(message, f"💩 Tuve problemas ingresando el Vehiculo, valida la zona y placa, ejecuta /start y vuelve a intentarlo")

######################################################### 
# Registrar Salida del Vehiculo 
@bot.message_handler(regexp=r"(^)registrar salida|salida|rsal placa ([a-zA-Z0-9_ ]*)")
def on_out_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)registrar salida|salida|rsal placa ([a-zA-Z0-9_ ]*)", message.text, re.IGNORECASE)
        
    #Ejemplo: rsal placa UES070

    try:
        placaVehiculo = parts.group(2).upper()       
        estado = float(1)

        obtenerPlaca = logic.get_placa (placaVehiculo)
        if  not obtenerPlaca: 
            bot.reply_to(message, f"🚨 El vehículo con placa {placaVehiculo} no se encuentra registrado")
        else:
            idUsuario = message.from_user.id
            zonaVehiculo = logic.get_parking(placaVehiculo, idUsuario)                                      
            if zonaVehiculo:
                control = logic.reg_salida_vehiculo(message.from_user.id, placaVehiculo)
                logic.update_dispo_zona(zonaVehiculo, estado)
                bot.reply_to(
                    message,
                    f"🚗 Salida exitosa de Vehículo:  {placaVehiculo}" if control == True
                    else "🙈 Tuve problemas con la salida del Vehiculo, ejecuta /start y vuelve a intentarlo") 
            else:
                bot.reply_to(message, f"⚠️ El vehiculo: {placaVehiculo} NO presena salidas pendientes")
    except:
            bot.reply_to(message, f"💩 Tuve problemas registrando la salida del Vehiculo, valida la zona y placa, ejecuta /start y vuelve a intentarlo")

######################################################### 
#*Ubicar vehiculo|ubicar|ubv {placa}* - Ubicar Vehículo\n"
@bot.message_handler(regexp=r"(^)ubicar vehiculo|ubicar|ubv placa ([a-zA-Z0-9_ ]*)")
def on_get_zone(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"(^)ubicar vehiculo|ubicar|ubv placa ([a-zA-Z0-9_ ]*)",message.text,re.IGNORECASE)
    
    try:        
        placa_vehiculo=(parts.group(2)).upper()
        obtenerPlaca = logic.get_placa(placa_vehiculo)

        if not obtenerPlaca:
            bot.reply_to(message, f"🚨 El vehículo con placa {placa_vehiculo} no se encuentra registrado")
        else:
            zona = logic.get_zona(placa_vehiculo)
            disponibilidad = logic.get_disponibilidad_zona(zona)
            if disponibilidad == True:
                text = f"🚨El vehiculo con placa {placa_vehiculo} ya NO se encuentra ocupando zona del parqueadero\n\n"
            else:
                text = f"🚖La zona en que se encuentra ubicado el vehiculo con placa {placa_vehiculo} es:\n\n"+zona                
            bot.reply_to(message, text, parse_mode="Markdown")                
    except:
        bot.reply_to(message, f"💩 Tuve problemas buscando el Vehiculo, ejecuta /start y vuelve a intentarlo")

#########################################################
#Indica Fecha y hora del último parqueo en caso de que el auto no se encuentre en la universidad
@bot.message_handler(regexp=r"(^)Fecha y hora último parqueo|ultimo parqueo|ulfh placa ([a-zA-Z0-9_ ]*)($)")
def on_reg_ultTiquete(message):
    bot.send_chat_action(message.chat.id, 'typing')

    parts = re.match(r"(^)Fecha y hora último parqueo|ultimo parqueo|ulfh placa ([a-zA-Z0-9_ ]*)($)", message.text, re.IGNORECASE)

    #Ejemplo: ulfh placa UES071
    text = ""
    
    try:
        placa = parts.group(2).upper()
        idUsuario = message.from_user.id
        
        ultParqueo = logic.get_fecha_ultimoParqueo (idUsuario,placa)
        
        if  ultParqueo:              

            if ultParqueo.fecha_salida is None: 
                text = f"🚨 El vehículo aún se encuentra en una zona de parqueo, consulta la opción ubv"

            else:
                text = f"🚗 Vehículo con placa {placa} última fecha de ingreso {ultParqueo.fecha_ingreso} y fecha de salida {ultParqueo.fecha_salida}."
                
        else:
            text = f"🚨 No se encuentra registros del vehículo con placa {placa}"
            
        bot.reply_to(message, text, parse_mode="Markdown")
    except:
        bot.reply_to(message, f"💩 Tuve problemas consultando la información, ejecuta /start valida tus datos y vuelve a intentarlo")

######################################################### 
#Ingresar administradores
@bot.message_handler(regexp=r"(^)insertar admin|ia ([a-zA-Z0-9_ ]*)")
def on_insert_admin(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"(^)insertar admin|ia ([a-zA-Z0-9_ ]*)",message.text,re.IGNORECASE)

    try:
        if logic.check_admin(message.from_user.id):

            id_user=parts.group(2)
            resultado = logic.insert_administrador(id_user)

            if resultado:
                bot.reply_to(message, f"🚨 Nuevo Administrador registrado correctamente.")
            else:            
                text = "El administrador no fue registrado. Ya Existe.\n\n"
                bot.reply_to(message, text, parse_mode="Markdown")
        else:
            text = f"🥺 Esta funcionalidad sólo está disponible para administradores"
            bot.reply_to(message, text, parse_mode="Markdown")        
    except:
        bot.reply_to(message, f"💩 Tuve problemas insertando el nuevo administrador.")

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