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