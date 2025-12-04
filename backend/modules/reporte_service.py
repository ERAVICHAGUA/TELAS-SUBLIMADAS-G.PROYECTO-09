from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Inspeccion, ReporteSemanal

class ReporteService:

    @staticmethod
    def generar_reporte_semanal():
        """
        Genera automáticamente el reporte semanal de calidad.
        """
        db = SessionLocal()
        try:
            # Obtener semana actual (lunes–domingo)
            hoy = date.today()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)

            # Verificar si ya se generó reporte para esa semana
            reporte_existente = (
                db.query(ReporteSemanal)
                .filter(ReporteSemanal.fecha_inicio == inicio_semana)
                .first()
            )

            if reporte_existente:
                return {"mensaje": "Reporte semanal ya existe", "generado": False}

            # Obtener inspecciones dentro de la semana
            inspecciones = (
                db.query(Inspeccion)
                .filter(Inspeccion.fecha >= datetime.combine(inicio_semana, datetime.min.time()))
                .filter(Inspeccion.fecha <= datetime.combine(fin_semana, datetime.max.time()))
                .all()
            )

            total = len(inspecciones)
            rechazados = sum(1 for i in inspecciones if i.resultado == "RECHAZADO")
            aprobados = total - rechazados
            porcentaje = (rechazados / total) * 100 if total > 0 else 0

            # Tendencia vs semana anterior
            semana_anterior = inicio_semana - timedelta(days=7)
            fin_sem_anterior = semana_anterior + timedelta(days=6)

            inspecciones_previas = (
                db.query(Inspeccion)
                .filter(Inspeccion.fecha >= datetime.combine(semana_anterior, datetime.min.time()))
                .filter(Inspeccion.fecha <= datetime.combine(fin_sem_anterior, datetime.max.time()))
                .all()
            )

            rechazados_prev = sum(1 for i in inspecciones_previas if i.resultado == "RECHAZADO")
            total_prev = len(inspecciones_previas)
            porc_prev = (rechazados_prev / total_prev) * 100 if total_prev > 0 else 0

            tendencia = porcentaje - porc_prev

            # Guardar reporte
            reporte = ReporteSemanal(
                fecha_inicio=inicio_semana,
                fecha_fin=fin_semana,
                total_inspecciones=total,
                total_rechazados=rechazados,
                total_aprobados=aprobados,
                porcentaje_defectos=round(porcentaje, 2),
                tendencia=round(tendencia, 2)
            )

            db.add(reporte)
            db.commit()

            return {"mensaje": "Reporte semanal generado", "generado": True}

        finally:
            db.close()
