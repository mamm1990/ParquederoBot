import database.db as db
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

class Tiquete(db.Base):
    __tablename__ = 'tiquete'
 
    id_tiquete = Column('id_tiquete', Integer, primary_key=True, autoincrement=True, nullable=False)
    id_vehiculo = Column('id_vehiculo', Integer, ForeignKey('vehiculo.id_vehiculo', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    id_zona = Column('id_zona', String(60), ForeignKey('zona.id_zona', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    fecha_ingreso = Column('fecha_ingreso', DateTime, server_default=func.now(), nullable=False)
    fecha_salida = Column('fecha_salida', DateTime, nullable=True)
    duracion = Column('duracion', Float, nullable=False)
 
    def __init__(self, id_vehiculo, id_zona, duracion =0):        
        self.id_vehiculo = id_vehiculo
        self.id_zona = id_zona
        self.duracion = duracion
        
 
    def __repr__(self):
        return f"<Tiquete {self.id_tiquete}>"