#importa la libreria porque copié la carpeta en la misma que contine el archivo pero hay que cambiarlo
import database.db as db
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Administrador(db.Base):
    __tablename__ = 'administrador'
 
    id_administrador = Column('id_administrador', Integer, primary_key=True, nullable=False)

    #el tipo de dato se puede revisar aqui https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.DateTime
    fecha_crea = Column('fecha_crea', DateTime, server_default=func.now(), nullable=True)
 
    def __init__(self, id_administrador):
        self.id_administrador = id_administrador
 
    def __repr__(self):
        return f"<Administrador {self.id_administrador}>"