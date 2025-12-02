# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from modules.db import Base, engine

from modules import models

# Importamos la lógica de análisis
from modules.analisis import analizar_molde, cargar_contorno_ideal

# Importamos CRUD para guardar y listar registros
from modules.crud import guardar_inspeccion, listar_inspecciones

# NUEVO: Importar servicios de alertas y email
from modules.alert_service import AlertService
from modules.email_service import EmailService

# ---------------------------------------------------------
# CONFIG FASTAPI
# ---------------------------------------------------------

app = FastAPI(
    title="Sistema de Control de Calidad Láser (Simulación)",
    description="Backend de FastAPI modular para detección de rebaba, registro de inspecciones y sistema de alertas."
)

# Configurar CORS (si tienes frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# EVENTO DE INICIO: CARGA DE PLANTILLA IDEAL
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():
    """Carga la plantilla ideal y crea la base de datos si no existe."""
    
    # Crear tablas de SQLite
    Base.metadata.create_all(bind=engine)
    print("✔ Base de datos lista. Tablas creadas.")
    
    # Cargar plantilla ideal
    if not cargar_contorno_ideal():
        print("⚠ ADVERTENCIA: No se cargó la plantilla ideal. El análisis no funcionará.")
    
    # NUEVO: Probar conexión SMTP
    print("\n🔧 Probando configuración de email...")
    EmailService.test_conexion()


# ---------------------------------------------------------
# ENDPOINT PRINCIPAL: INSPECCIÓN DE MOLDE (CON ALERTAS)
# ---------------------------------------------------------

@app.post("/api/inspeccionar")
async def inspeccionar_calidad(file: UploadFile = File(...)):
    """
    Recibe la imagen y devuelve si está APROBADA o RECHAZADA.
    Además guarda el resultado en SQLite y verifica si debe crear una alerta.
    """
    try:
        # Leer bytes de la imagen
        imagen_bytes = await file.read()

        # Ejecutar análisis
        resultado = analizar_molde(imagen_bytes)

        # Validación de errores
        if resultado.get("status") == "ERROR":
            raise HTTPException(status_code=400, detail=resultado["mensaje"])

        # Guardar resultado en SQLite
        guardar_inspeccion(
            resultado=resultado["status"],
            max_distancia=resultado["max_distancia"],
            puntos_defectuosos=resultado["puntos_defectuosos"],
        )

        # NUEVO: Verificar si se debe crear una alerta automática
        alerta_info = AlertService.verificar_y_crear_alerta()
        
        # Si se creó una alerta, intentar enviar notificación por email
        if alerta_info.get("alerta_creada"):
            stats = alerta_info["estadisticas"]
            email_enviado = EmailService.enviar_alerta_defectos(
                porcentaje=stats["porcentaje_defectos"],
                total_inspecciones=stats["total_inspecciones"],
                total_rechazados=stats["total_rechazados"],
                recomendacion=alerta_info["recomendacion"]
            )
            
            # Marcar alerta como notificada si el email se envió correctamente
            if email_enviado:
                AlertService.marcar_alerta_como_notificada(alerta_info["alerta_id"])
        
        # Agregar información de alerta a la respuesta
        resultado["alerta_info"] = alerta_info

        return JSONResponse(content=resultado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# ENDPOINT: LISTAR TODAS LAS INSPECCIONES
# ---------------------------------------------------------

@app.get("/api/registros")
def obtener_registros():
    """
    Lista todas las inspecciones guardadas en SQLite.
    """
    registros = listar_inspecciones()

    respuesta = []
    for r in registros:
        respuesta.append({
            "id": r.id,
            "resultado": r.resultado,
            "max_distancia": r.max_distancia,
            "puntos_defectuosos": json.loads(r.puntos_defectuosos),
            "fecha": r.fecha.isoformat()
        })

    return {"inspecciones": respuesta}


# ---------------------------------------------------------
# NUEVOS ENDPOINTS: SISTEMA DE ALERTAS
# ---------------------------------------------------------

@app.get("/api/alertas/estadisticas")
def obtener_estadisticas():
    """
    Obtiene estadísticas actuales de calidad y porcentaje de defectos.
    """
    try:
        stats = AlertService.calcular_porcentaje_defectos()
        return JSONResponse(content=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alertas/historial")
def obtener_historial_alertas(limite: int = 50):
    """
    Obtiene el historial de alertas registradas.
    
    Args:
        limite: Número máximo de alertas a retornar (por defecto 50)
    """
    try:
        historial = AlertService.obtener_historial_alertas(limite=limite)
        return JSONResponse(content={"alertas": historial})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/alertas/verificar")
def verificar_alertas_manual():
    """
    Verifica manualmente si se debe crear una alerta (útil para pruebas).
    """
    try:
        alerta_info = AlertService.verificar_y_crear_alerta()
        
        # Si se creó una alerta, enviar notificación
        if alerta_info.get("alerta_creada"):
            stats = alerta_info["estadisticas"]
            email_enviado = EmailService.enviar_alerta_defectos(
                porcentaje=stats["porcentaje_defectos"],
                total_inspecciones=stats["total_inspecciones"],
                total_rechazados=stats["total_rechazados"],
                recomendacion=alerta_info["recomendacion"]
            )
            
            if email_enviado:
                AlertService.marcar_alerta_como_notificada(alerta_info["alerta_id"])
        
        return JSONResponse(content=alerta_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/alertas/test-email")
def probar_email():
    """
    Envía un email de prueba para verificar la configuración SMTP.
    """
    try:
        exito = EmailService.enviar_alerta_defectos(
            porcentaje=15.5,
            total_inspecciones=100,
            total_rechazados=15,
            recomendacion="Esta es una prueba del sistema de alertas."
        )
        
        if exito:
            return JSONResponse(content={
                "success": True,
                "mensaje": "Email de prueba enviado correctamente"
            })
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "mensaje": "Error al enviar email de prueba"
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/")
def health_check():
    """Endpoint para verificar que el servidor está funcionando."""
    return {
        "status": "online",
        "servicio": "Sistema de Control de Calidad Láser",
        "version": "2.0"
    }


# ---------------------------------------------------------
# EJECUCIÓN MANUAL (opcional)
# ---------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)