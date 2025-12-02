
# backend/modules/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from .db import Base

class Inspeccion(Base):
    __tablename__ = "inspecciones"

    id = Column(Integer, primary_key=True, index=True)
    resultado = Column(String(20))             # APROBADO / RECHAZADO
    max_distancia = Column(Float)              # Distancia máxima detectada
    puntos_defectuosos = Column(String)        # JSON string
    fecha = Column(DateTime(timezone=True), default=func.now())


class Alert(Base):
    """
    Modelo para registrar alertas cuando se supera el umbral de defectos.
    """
    __tablename__ = "alertas"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_alerta = Column(String(50))                    # PORCENTAJE_DEFECTOS
    porcentaje_defectos = Column(Float)                 # % calculado
    total_inspecciones = Column(Integer)                # Total analizado
    total_rechazados = Column(Integer)                  # Cantidad rechazada
    umbral_configurado = Column(Float)                  # Umbral que se superó
    recomendacion = Column(Text)                        # Mensaje automático
    notificacion_enviada = Column(Boolean, default=False)  # Si ya se envió email
    fecha = Column(DateTime(timezone=True), default=func.now())