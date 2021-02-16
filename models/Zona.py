#importa la libreria porque copié la carpeta en la misma que contine el archivo pero hay que cambiarlo
import database.db as db
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

class Zona(db.Base):
    __tablename__ = 'zona'
 
    id_zona = Column('id_zona', String(5), primary_key=True, nullable=False)
    disponible = Column('disponible', Boolean, nullable=False)
    fecha_crea = Column('fecha_crea', DateTime, server_default=func.now(), nullable=True)
 
    def __init__(self, id_zona, disponible):
        self.id_zona = id_zona
        self.disponible = disponible 
    def __repr__(self):
        return f"<Zona {self.id_zona}>"