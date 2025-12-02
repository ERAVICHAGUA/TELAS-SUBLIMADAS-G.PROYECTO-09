# backend/test_system.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.alert_service import AlertService
from modules.email_service import EmailService
from modules.crud import guardar_inspeccion
from dotenv import load_dotenv

load_dotenv()

def test_1_conexion_smtp():
    print("\n" + "="*60)
    print("🧪 PRUEBA 1: Verificando conexión SMTP")
    print("="*60)
    
    exito = EmailService.test_conexion()
    if exito:
        print("✅ Conexión SMTP exitosa")
    else:
        print("❌ Error en conexión SMTP")
    return exito


def test_2_calcular_porcentaje():
    print("\n" + "="*60)
    print("🧪 PRUEBA 2: Calculando porcentaje de defectos")
    print("="*60)

    stats = AlertService.calcular_porcentaje_defectos()

    print("\n📊 Estadísticas actuales:")
    print(f"   Total inspecciones : {stats['total_inspecciones']}")
    print(f"   Total rechazados   : {stats['total_rechazados']}")
    print(f"   Total aprobados    : {stats['total_aprobados']}")
    print(f"   Porcentaje defectos: {stats['porcentaje_defectos']}%")
    print(f"   Umbral: {stats['umbral_configurado']}%")
    print(f"   ¿Supera?: {'❌ SÍ' if stats['supera_umbral'] else '✅ NO'}")

    return stats


def test_3_crear_datos_prueba():
    print("\n" + "="*60)
    print("🧪 PRUEBA 3: Creando datos de prueba")
    print("="*60)

    print("\n📝 Insertando 10 inspecciones (70% defectos)")

    for i in range(7):
        guardar_inspeccion(
            resultado="RECHAZADO",
            max_distancia=5,
            puntos_defectuosos=[[100, 200]]
        )
        print(f"   ✔ Rechazada {i+1}/7")

    for i in range(3):
        guardar_inspeccion(
            resultado="APROBADO",
            max_distancia=0,
            puntos_defectuosos=[]
        )
        print(f"   ✔ Aprobada {i+1}/3")

    print("\n✅ Datos de prueba creados")


def test_4_verificar_alerta():
    print("\n" + "="*60)
    print("🧪 PRUEBA 4: Verificando creación de alerta")
    print("="*60)

    resultado = AlertService.verificar_y_crear_alerta()

    if resultado["alerta_creada"]:
        print("\n⚠️ ALERTA CREADA")
        print(f"   ID: {resultado['alerta_id']}")
        print(f"   Porcentaje: {resultado['estadisticas']['porcentaje_defectos']}%")
        print(f"   Recomendación: {resultado['recomendacion']}")

        print("\n📧 Enviando email automáticamente...")
        exito = EmailService.enviar_alerta_defectos(
            porcentaje=resultado["estadisticas"]["porcentaje_defectos"],
            total_inspecciones=resultado["estadisticas"]["total_inspecciones"],
            total_rechazados=resultado["estadisticas"]["total_rechazados"],
            recomendacion=resultado["recomendacion"]
        )

        if exito:
            AlertService.marcar_alerta_como_notificada(resultado["alerta_id"])
            print("   ✔ Email enviado y alerta marcada como notificada")
        else:
            print("   ❌ Falló el envío de email")

        return resultado

    else:
        print("\n✅ No se creó alerta")
        print(f"   Razón: {resultado['razon']}")
        return None


def test_5_enviar_email():
    print("\n" + "="*60)
    print("🧪 PRUEBA 5: Enviar email manual")
    print("="*60)

    exito = EmailService.enviar_alerta_defectos(
        porcentaje=70.0,
        total_inspecciones=10,
        total_rechazados=7,
        recomendacion="PRUEBA: Email manual"
    )

    if exito:
        print("✔ Email enviado correctamente")
    else:
        print("❌ Error enviando email")

    return exito


def test_6_historial_alertas():
    print("\n" + "="*60)
    print("🧪 PRUEBA 6: Historial de alertas")
    print("="*60)

    historial = AlertService.obtener_historial_alertas(10)

    if not historial:
        print("\n📭 No existen alertas registradas")
        return

    print(f"\n📋 Últimas {len(historial)} alertas:")
    for a in historial:
        print(f"\n   ID: {a['id']}")
        print(f"   Fecha: {a['fecha']}")
        print(f"   Porcentaje: {a['porcentaje_defectos']}%")
        print(f"   Notificada: {'✔ Sí' if a['notificacion_enviada'] else '❌ No'}")


def menu_principal():
    print("\n" + "="*60)
    print("🧪 SISTEMA DE PRUEBAS - ALERTAS DE CALIDAD")
    print("="*60)
    print("\n1. Probar conexión SMTP")
    print("2. Calcular porcentaje")
    print("3. Crear datos de prueba")
    print("4. Verificar alerta + enviar email + marcar notificada")
    print("5. Enviar email manual")
    print("6. Ver historial")
    print("7. Ejecutar TODO")
    print("0. Salir")

    return input("\n👉 Opción: ").strip()


def ejecutar_todas_pruebas():
    if not test_1_conexion_smtp():
        return

    test_2_calcular_porcentaje()
    test_3_crear_datos_prueba()
    test_2_calcular_porcentaje()

    alerta = test_4_verificar_alerta()

    test_6_historial_alertas()


def main():
    while True:
        opcion = menu_principal()

        if opcion == "1": test_1_conexion_smtp()
        elif opcion == "2": test_2_calcular_porcentaje()
        elif opcion == "3": test_3_crear_datos_prueba()
        elif opcion == "4": test_4_verificar_alerta()
        elif opcion == "5": test_5_enviar_email()
        elif opcion == "6": test_6_historial_alertas()
        elif opcion == "7": ejecutar_todas_pruebas()
        elif opcion == "0":
            print("\n👋 Adiós")
            break

        input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()
