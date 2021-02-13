import database.db as db
from datetime import datetime
from sqlalchemy import extract

#########################################################
def get_about_this(VERSION):
    response = (
    f"Parqueadero UAM Bot (pyTelegramBot) v{VERSION}"
    "\n\n"
    "Desarrollado por:"
    "\n\n"
    "Marco Montoya <marcoa.montoyam@autonoma.edu.co>"
    "\n\n"
    "Jose Omar Cardona <joseo.cardonag@autonoma.edu.co>"
    "\n\n"
    "Cristian Ruiz <cristian.ruizvm@autonoma.edu.co>"
    "\n\n"
    "Alejandra Peralta <alejandra.peraltad@autonoma.edu.co>"
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
    )
    return response

#########################################################