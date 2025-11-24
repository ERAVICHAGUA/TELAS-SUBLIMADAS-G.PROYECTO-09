from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Inspeccion
import json
from datetime import datetime


def get_db():
    """Crea una sesión nueva por cada operación CRUD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def guardar_inspeccion(resultado: str, max_distancia: float, puntos_defectuosos: list):
    """
    Guarda los datos de inspección en SQLite.
    Esta versión NO recibe 'db' porque crea su propia sesión interna.
    """
    db = SessionLocal()

    try:
        nueva = Inspeccion(
            resultado=resultado,
            max_distancia=max_distancia,
            puntos_defectuosos=json.dumps(puntos_defectuosos),
            fecha=datetime.now()
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        return nueva

    finally:
        db.close()


def listar_inspecciones():
    db = SessionLocal()
    try:
        return db.query(Inspeccion).order_by(Inspeccion.fecha.desc()).all()
    finally:
        db.close()
