# backend/modules/alert_service.py
"""
Sistema de alertas automáticas para detección de defectos.
Calcula el porcentaje de fallas y dispara notificaciones cuando supera el umbral.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .db import SessionLocal
from .models import Inspeccion, Alert
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de alertas
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "5.0"))  # 5% por defecto
CALCULATION_WINDOW = int(os.getenv("CALCULATION_WINDOW", "100"))  # Últimas 100 inspecciones


class AlertService:
    """Servicio para gestión de alertas automáticas"""
    
    @staticmethod
    def calcular_porcentaje_defectos(limite: int = CALCULATION_WINDOW) -> dict:
        """
        Calcula el porcentaje de defectos en las últimas N inspecciones.
        
        Args:
            limite: Número de inspecciones a analizar (por defecto 100)
            
        Returns:
            dict con estadísticas de calidad
        """
        db = SessionLocal()
        
        try:
            # Obtener las últimas N inspecciones
            inspecciones = (
                db.query(Inspeccion)
                .order_by(Inspeccion.fecha.desc())
                .limit(limite)
                .all()
            )
            
            if not inspecciones:
                return {
                    "total_inspecciones": 0,
                    "total_rechazados": 0,
                    "porcentaje_defectos": 0.0,
                    "supera_umbral": False
                }
            
            # Contar rechazados
            total = len(inspecciones)
            rechazados = sum(1 for i in inspecciones if i.resultado == "RECHAZADO")
            
            # Calcular porcentaje
            porcentaje = (rechazados / total) * 100 if total > 0 else 0.0
            
            return {
                "total_inspecciones": total,
                "total_rechazados": rechazados,
                "total_aprobados": total - rechazados,
                "porcentaje_defectos": round(porcentaje, 2),
                "supera_umbral": porcentaje > ALERT_THRESHOLD,
                "umbral_configurado": ALERT_THRESHOLD
            }
            
        finally:
            db.close()
    
    
    @staticmethod
    def verificar_y_crear_alerta() -> dict:
        """
        Verifica si se debe crear una alerta y la registra si es necesario.
        
        Returns:
            dict con información de la alerta (si se creó) o None
        """
        db = SessionLocal()
        
        try:
            # Calcular estadísticas actuales
            stats = AlertService.calcular_porcentaje_defectos()
            
            if not stats["supera_umbral"]:
                return {
                    "alerta_creada": False,
                    "razon": "No se superó el umbral de defectos",
                    "estadisticas": stats
                }
            
            # Verificar si ya existe una alerta reciente (últimas 24 horas)
            alerta_reciente = (
                db.query(Alert)
                .filter(Alert.fecha >= datetime.now() - timedelta(hours=1))
                .filter(Alert.tipo_alerta == "PORCENTAJE_DEFECTOS")
                .first()
            )
            
            if alerta_reciente:
                return {
                    "alerta_creada": False,
                    "razon": "Ya existe una alerta reciente (última hora)",
                    "alerta_existente": alerta_reciente.id,
                    "estadisticas": stats
                }
            
            # Crear nueva alerta
            recomendacion = AlertService._generar_recomendacion(stats["porcentaje_defectos"])
            
            nueva_alerta = Alert(
                tipo_alerta="PORCENTAJE_DEFECTOS",
                porcentaje_defectos=stats["porcentaje_defectos"],
                total_inspecciones=stats["total_inspecciones"],
                total_rechazados=stats["total_rechazados"],
                umbral_configurado=ALERT_THRESHOLD,
                recomendacion=recomendacion,
                notificacion_enviada=False,  # Se marcará como True después de enviar email
                fecha=datetime.now()
            )
            
            db.add(nueva_alerta)
            db.commit()
            db.refresh(nueva_alerta)
            
            return {
                "alerta_creada": True,
                "alerta_id": nueva_alerta.id,
                "estadisticas": stats,
                "recomendacion": recomendacion
            }
            
        finally:
            db.close()
    
    
    @staticmethod
    def _generar_recomendacion(porcentaje: float) -> str:
        """
        Genera recomendaciones automáticas basadas en el porcentaje de defectos.
        
        Args:
            porcentaje: Porcentaje de defectos detectado
            
        Returns:
            Mensaje de recomendación
        """
        if porcentaje > 20:
            return (
                "CRÍTICO: Se recomienda DETENER PRODUCCIÓN inmediatamente. "
                "Realizar mantenimiento preventivo completo del equipo y "
                "recalibración del sistema láser."
            )
        elif porcentaje > 10:
            return (
                "URGENTE: Se recomienda revisar calibración del sistema láser "
                "y realizar inspección del molde. Verificar parámetros de corte."
            )
        elif porcentaje > 5:
            return (
                "ATENCIÓN: Se recomienda revisar la calibración del equipo y "
                "verificar condiciones de operación (temperatura, humedad, desgaste del molde)."
            )
        else:
            return "Monitorear tendencia. Verificar si es un patrón temporal."
    
    
    @staticmethod
    def obtener_alertas_pendientes() -> list:
        """
        Obtiene todas las alertas que aún no han sido notificadas por email.
        
        Returns:
            Lista de objetos Alert pendientes
        """
        db = SessionLocal()
        
        try:
            return (
                db.query(Alert)
                .filter(Alert.notificacion_enviada == False)
                .order_by(Alert.fecha.desc())
                .all()
            )
        finally:
            db.close()
    
    
    @staticmethod
    def marcar_alerta_como_notificada(alerta_id: int) -> bool:
        """
        Marca una alerta como notificada después de enviar el email.
        
        Args:
            alerta_id: ID de la alerta a marcar
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        db = SessionLocal()
        
        try:
            alerta = db.query(Alert).filter(Alert.id == alerta_id).first()
            
            if not alerta:
                return False
            
            alerta.notificacion_enviada = True
            db.commit()
            
            return True
            
        finally:
            db.close()
    
    
    @staticmethod
    def obtener_historial_alertas(limite: int = 50) -> list:
        """
        Obtiene el historial de alertas registradas.
        
        Args:
            limite: Número máximo de alertas a retornar
            
        Returns:
            Lista con las últimas alertas
        """
        db = SessionLocal()
        
        try:
            alertas = (
                db.query(Alert)
                .order_by(Alert.fecha.desc())
                .limit(limite)
                .all()
            )
            
            return [
                {
                    "id": a.id,
                    "tipo": a.tipo_alerta,
                    "porcentaje_defectos": a.porcentaje_defectos,
                    "total_inspecciones": a.total_inspecciones,
                    "total_rechazados": a.total_rechazados,
                    "recomendacion": a.recomendacion,
                    "notificacion_enviada": a.notificacion_enviada,
                    "fecha": a.fecha.isoformat()
                }
                for a in alertas
            ]
            
        finally:
            db.close()