import database.db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    __tablename__ = 'vehiculo'
 
    id_vehiculo = Column('id_vehiculo', String(60), primary_key=True, nullable=False)
    id_usuario = Column('id_usuario', String(60), nullable=False)
    tipo_vehiculo = Column('tipo_vehiculo', String(100), nullable=False)
    placa = Column('placa', String(10), nullable=False)
    estado_vehiculo = Column('estado_vehiculo', String(30), nullable=False)
    fecha_crea = Column('fecha_crea', DateTime, server_default=func.now(), nullable=True)
 
    def __init__(self, id_vehiculo, id_usuario, tipo_vehiculo, placa, estado_vehiculo):
        self.id_vehiculo = id_vehiculo
        self.id_usuario = id_usuario
        self.tipo_vehiculo = tipo_vehiculo
        self.placa = placa
        self.estado_vehiculo = id_usuario
 
    def __repr__(self):
        return f"<Vehiculo {self.id_vehiculo}>"