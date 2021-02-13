import database.db as db
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

class Administrador(db.Base):
    __tablename__ = 'administrador'
 
    id_administrador = Column('id_administrador', Integer, primary_key=True, nullable=False)
    fecha_crea = Column('fecha_crea', DateTime, server_default=func.now(), nullable=True)
 
    def __init__(self, id_administrador):
        self.id_administrador = id_administrador
 
    def __repr__(self):
        return f"<Administrador {self.id_administrador}>"