import datetime

from sqlalchemy.sql.functions import func
import database.db as db
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

class Zona(db.Base):
    __tablename__ = 'zona'
 
    id_zona = Column('id_zona', String(5), primary_key=True, nullable=False)
    disponible = Column('disponible', Boolean, nullable=False)
    fecha_crea = Column('fecha_crea', datetime, server_default=func.now(), nullable=True)
 
    def __init__(self, id_zona, disponible):
        self.id_zona = id_zona
        self.disponible = disponible 
    def __repr__(self):
        return f"<Zona {self.id_zona}>"