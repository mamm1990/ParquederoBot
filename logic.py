import database.db as db
import sqlite3
from datetime import datetime
from sqlalchemy import extract
from models.Administrador import Administrador
from models.Vehiculo import Vehiculo

#########################################################
def insert_admins():
    Administrador(1528370599)#Marco Montoya
    Administrador(0)#Alejandra Peralta
    Administrador(1551638159)#Jose Omar Cardona
    Administrador(000)#Cristian Ruiz
    return True
#########################################################
def get_about_this(VERSION):
    response = (
    f"Parqueadero UAM Bot (pyTelegramBot) v{VERSION}"
    "\n\n"
    "Desarrollado por:"
    "\n\n"
    "Alejandra Peralta <alejandra.peraltad@autonoma.edu.co>"
    "\n\n"
    "Marco Montoya <marcoa.montoyam@autonoma.edu.co>"
    "\n\n"
    "Jose Omar Cardona <joseo.cardonag@autonoma.edu.co>"
    "\n\n"
    "Cristian Ruiz <cristian.ruizvm@autonoma.edu.co>"
    )
    return response

#########################################################
def get_welcome_message(bot_data):
    response = (
    f"Hola, soy *{bot_data.first_name}* "
    f"también conocido como *{bot_data.username}*.\n\n"
    "¡Estoy aquí para ayudarte en todo lo relacionado con los parqueaderos de la UAM!"
    )
    return response

#########################################################
def get_help_message ():
    response = (
    "Estos son los comandos y órdenes disponibles:\n"
    "\n"
    "*/start* - Inicia la interacción con el bot (obligatorio)\n"
    "*/help* - Muestra este mensaje de ayuda\n"
    "*/about* - Muestra detalles de esta aplicación\n"
    "*agregar zona|agz {idzona}, {disponible}* - Agregar Nueva Zona (sólo admin)\n"
    "*listar zonas|lsz* - Listar Zonas Agregadas (sólo admin)\n"
    "*remover zona|rmz {idzona}* - Remover Zona (sólo admin)\n"
    "*agregar vehiculo|agv {placa} , tipo {tipo}* (Tipos Vehículo: 1. Carro, 2. Moto)- Agregar Vehículo\n"
    "*listar vehiculos|lsv* - Listar Vehículos\n"
    "*remover vehiculo|rmv {placa}* - Remover Vehiculo\n"
    "*registrar ingreso|ingreso|ring {placa} en la zona {idzona}* - Registrar Ingreso Vehículo\n"
    "*registrar salida|salida|rsal {placa}* - Registrar Salida Vehículo\n"
    "*ubicar vehiculo|ubicar|ubv {placa}* - Ubicar Vehículo\n"
    )
    return response

#########################################################
def add_vehiculo(tipoVehiculo, placa, idUsuario):#id_vehiculo, id_usuario, tipo_vehiculo, placa, fecha_crea):

    #vehiculo = db.session.query(Vehiculo)
    #db.session.commit()

    #if vehiculo == None:
     #   vehiculo = Vehiculo(id_vehiculo, id_usuario, tipo_vehiculo, placa, fecha_crea)
      #  db.session.add(vehiculo)
       # db.session.commit()
        #return True

    #return False 
    
    #conn = sqlite3.connect('db.db') 
    #conn.execute("INSERT INTO Vehiculo (id_usuario,tipo_vehiculo,placa,fecha_crea) "
    #            "VALUES (001, '01', 'Carro', 'IPD 153', '18/02/2021')")

    #conn.commit()
    #conn.close()
    #response = placa

    #return response 
    
    
    nuevoVehiculo = Vehiculo(10, idUsuario, tipoVehiculo, placa)
        

    db.session.add(nuevoVehiculo)

    db.session.commit()

    return True



#########################################################
def get_fallback_message (text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"  
    return response

#########################################################