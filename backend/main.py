# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
from modules.db import Base, engine

from modules import models

# Importamos la lógica de análisis
from modules.analisis import analizar_molde, cargar_contorno_ideal

# Importamos CRUD para guardar y listar registros
from modules.crud import guardar_inspeccion, listar_inspecciones

# ---------------------------------------------------------
# CONFIG FASTAPI
# ---------------------------------------------------------

app = FastAPI(
    title="Sistema de Control de Calidad Láser (Simulación)",
    description="Backend de FastAPI modular para detección de rebaba y registro de inspecciones."
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


# ---------------------------------------------------------
# ENDPOINT PRINCIPAL: INSPECCIÓN DE MOLDE
# ---------------------------------------------------------

@app.post("/api/inspeccionar")
async def inspeccionar_calidad(file: UploadFile = File(...)):
    """
    Recibe la imagen y devuelve si está APROBADA o RECHAZADA.
    Además guarda el resultado en SQLite.
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
# EJECUCIÓN MANUAL (opcional)
# ---------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
