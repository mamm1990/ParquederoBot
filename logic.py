import database.db as db
import sqlite3
from datetime import datetime
from sqlalchemy import extract
from models.Administrador import Administrador
from models.Vehiculo import Vehiculo
from models.Zona import Zona
from models.Tiquete import Tiquete

#########################################################
def insert_admins():
    #admin1 = Administrador(1528370599)#Marco Montoya
    #admin2 = Administrador(1221493315)#Alejandra Peralta
    #admin3 = Administrador(1551638159)#Jose Omar Cardona
    #admin4 = Administrador(1563918474)#Cristian Ruiz
    administradores = [1528370599,1221493315,1551638159,1563918474]
    for index in administradores:
        admin = None
        admin = db.session.query(Administrador).get(index)

        if admin == None:
            admin = Administrador(index)
            db.session.add(admin)
            db.session.commit()
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
    "*agregar vehiculo|agv placa {placa} , tipo {tipo}* (Tipos Vehículo: 1. Carro, 2. Moto)- Agregar Vehículo\n"
    "*listar vehiculos|lsv* - Listar Vehículos\n"
    "*remover vehiculo|rmv placa {placa}* - Remover Vehiculo\n"
    "*registrar ingreso|ingreso|ring {placa} en la zona {idzona}* - Registrar Ingreso Vehículo\n"
    "*registrar salida|salida|rsal {placa}* - Registrar Salida Vehículo\n"
    "*ubicar vehiculo|ubicar|ubv {placa}* - Ubicar Vehículo\n"
    )
    return response
#########################################################
#Obtener Zona
def get_zona (placa_vehiculo):
    id_ve=db.session.query(Vehiculo).filter_by(placa=placa_vehiculo).get(id_vehiculo)
    
    zona=db.session.query(Tiquete).filter_by(id_vehiculo=id_ve).get(id_zona)

    db.session.commit()

    return zona

#########################################################
#Agregar Vehículo
def add_vehiculo(tipoVehiculo, placa, idUsuario):  
    
    nuevoVehiculo = Vehiculo(idUsuario, tipoVehiculo, placa)

    db.session.add(nuevoVehiculo)

    db.session.commit()

    return True
######################################################### 
# Eliminar Vehículo
def remove_vehiculo(user_id, placaVehiculo):
    vehiculo = db.session.query(Vehiculo).filter(
        Vehiculo.id_usuario == user_id
    ).filter(
        Vehiculo.placa == placaVehiculo
    ).first()

    if not vehiculo:
        db.session.rollback()
        return False   

    db.session.delete(vehiculo)    
    db.session.commit()
    
    return True    

######################################################### 
# Listar Vehículo
def list_vehiculos():
	vehiculo = db.session.query(Vehiculo).all()

	return vehiculo

######################################################### 

def get_fallback_message (text):
    response = f"\U0001F648 No entendí lo que me acabas de decir"  
    return response

#########################################################