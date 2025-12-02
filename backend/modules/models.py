
# backend/modules/models.py
<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
=======
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
>>>>>>> f1fc54e (Añadido sistema de alertas, SMTP y análisis)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    # Código legible para el supervisor: LT-0001, LT-2025-01, etc.
    codigo_lote = Column(String(30), unique=True, index=True)
    inspector = Column(String(100))                  # Quién inspeccionó
    estado = Column(String(20), default="EN PROCESO")  # EN PROCESO / COMPLETO / OBSERVADO
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    # Relación 1:N → un lote tiene muchas inspecciones
    inspecciones = relationship("Inspeccion", back_populates="lote")


class Inspeccion(Base):
    __tablename__ = "inspecciones"

    id = Column(Integer, primary_key=True, index=True)
    resultado = Column(String(20))             # APROBADO / RECHAZADO
    max_distancia = Column(Float)              # Distancia máxima detectada
    puntos_defectuosos = Column(String)        # JSON string

  # ejemplos: "Corte incompleto", "Sobrecalentamiento", "Excluido", etc.
    categoria = Column(String(50), index=True, default="Excluido")

    fecha = Column(DateTime(timezone=True), default=func.now())

<<<<<<< HEAD
      # 🔗 Relación con Lote (opcional: una inspección puede o no pertenecer a un lote)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=True)
    lote = relationship("Lote", back_populates="inspecciones")
=======

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
>>>>>>> f1fc54e (Añadido sistema de alertas, SMTP y análisis)
