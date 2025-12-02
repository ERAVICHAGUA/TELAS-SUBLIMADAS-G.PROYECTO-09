# backend/modules/email_service.py
"""
Servicio de notificaciones por email para alertas de calidad.
Compatible con Gmail y otros proveedores SMTP.
"""

import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List

# Cargar variables de entorno
load_dotenv()

# Configuración SMTP
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")
DEFAULT_TO_EMAIL = os.getenv("ALERT_EMAIL", "jose.lescano868@gmail.com")


class EmailService:
    """Servicio para envío de notificaciones por correo electrónico"""
    
    @staticmethod
    def enviar_alerta_defectos(
        porcentaje: float,
        total_inspecciones: int,
        total_rechazados: int,
        recomendacion: str,
        to_emails: List[str] = None
    ) -> bool:
        """
        Envía una alerta por email cuando se supera el umbral de defectos.
        
        Args:
            porcentaje: Porcentaje de defectos detectado
            total_inspecciones: Total de inspecciones analizadas
            total_rechazados: Cantidad de piezas rechazadas
            recomendacion: Mensaje de recomendación automática
            to_emails: Lista de destinatarios (opcional)
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        
        if to_emails is None:
            to_emails = [DEFAULT_TO_EMAIL]
        
        try:
            # Crear mensaje HTML
            subject = f"⚠️ ALERTA: {porcentaje}% de defectos detectados"
            body_html = EmailService._crear_template_alerta(
                porcentaje, 
                total_inspecciones, 
                total_rechazados,
                recomendacion
            )
            
            # Enviar email
            EmailService._enviar_email(
                to_emails=to_emails,
                subject=subject,
                body_html=body_html
            )
            
            print(f"✅ Alerta enviada correctamente a: {', '.join(to_emails)}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar alerta por email: {e}")
            return False
    
    
    @staticmethod
    def _crear_template_alerta(
        porcentaje: float, 
        total: int, 
        rechazados: int,
        recomendacion: str
    ) -> str:
        """
        Crea el template HTML para el email de alerta.
        
        Args:
            porcentaje: Porcentaje de defectos
            total: Total de inspecciones
            rechazados: Cantidad rechazada
            recomendacion: Mensaje de recomendación
            
        Returns:
            HTML del email formateado
        """
        
        # Determinar nivel de criticidad
        if porcentaje > 20:
            color = "#d32f2f"  # Rojo
            nivel = "CRÍTICO"
        elif porcentaje > 10:
            color = "#f57c00"  # Naranja
            nivel = "URGENTE"
        else:
            color = "#fbc02d"  # Amarillo
            nivel = "ATENCIÓN"
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ 
                    background-color: {color}; 
                    color: white; 
                    padding: 20px; 
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{ 
                    background-color: #f9f9f9; 
                    padding: 30px; 
                    border: 1px solid #ddd;
                    border-radius: 0 0 5px 5px;
                }}
                .stats {{ 
                    background-color: white; 
                    padding: 20px; 
                    margin: 20px 0;
                    border-left: 4px solid {color};
                    border-radius: 3px;
                }}
                .stat-item {{ 
                    display: flex; 
                    justify-content: space-between; 
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .stat-label {{ font-weight: bold; color: #555; }}
                .stat-value {{ color: {color}; font-weight: bold; font-size: 1.2em; }}
                .recommendation {{ 
                    background-color: #fff3cd; 
                    padding: 15px; 
                    margin: 20px 0;
                    border-left: 4px solid #ffc107;
                    border-radius: 3px;
                }}
                .footer {{ 
                    text-align: center; 
                    color: #777; 
                    margin-top: 30px; 
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ ALERTA DE CALIDAD - NIVEL {nivel}</h1>
                </div>
                
                <div class="content">
                    <p>Se ha detectado un porcentaje elevado de defectos en el sistema de control de calidad.</p>
                    
                    <div class="stats">
                        <h3 style="margin-top: 0; color: {color};">📊 Estadísticas del Sistema</h3>
                        
                        <div class="stat-item">
                            <span class="stat-label">Porcentaje de defectos:</span>
                            <span class="stat-value">{porcentaje}%</span>
                        </div>
                        
                        <div class="stat-item">
                            <span class="stat-label">Total de inspecciones:</span>
                            <span class="stat-value">{total}</span>
                        </div>
                        
                        <div class="stat-item">
                            <span class="stat-label">Piezas rechazadas:</span>
                            <span class="stat-value">{rechazados}</span>
                        </div>
                        
                        <div class="stat-item" style="border-bottom: none;">
                            <span class="stat-label">Piezas aprobadas:</span>
                            <span class="stat-value">{total - rechazados}</span>
                        </div>
                    </div>
                    
                    <div class="recommendation">
                        <h3 style="margin-top: 0;">💡 Recomendación Automática</h3>
                        <p style="margin-bottom: 0;">{recomendacion}</p>
                    </div>
                    
                    <p style="margin-top: 20px;">
                        <strong>Fecha y hora del análisis:</strong> {fecha_actual}
                    </p>
                    
                    <p style="color: #777; font-size: 0.9em; margin-top: 20px;">
                        Esta es una notificación automática del Sistema de Control de Calidad Láser.
                        Por favor, tome las acciones correctivas necesarias lo antes posible.
                    </p>
                </div>
                
                <div class="footer">
                    <p>Sistema de Control de Calidad - TELAS SUBLIMADAS</p>
                    <p>Este es un mensaje automático, por favor no responder.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    
    @staticmethod
    def _enviar_email(to_emails: List[str], subject: str, body_html: str) -> None:
        """
        Envía un email usando SMTP.
        
        Args:
            to_emails: Lista de destinatarios
            subject: Asunto del email
            body_html: Contenido HTML del email
            
        Raises:
            Exception: Si hay un error al enviar el email
        """
        
        # Validar configuración
        if not all([SMTP_USER, SMTP_PASS, FROM_EMAIL]):
            raise ValueError(
                "Faltan credenciales SMTP. Verifica las variables de entorno: "
                "SMTP_USER, SMTP_PASS, FROM_EMAIL"
            )
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # Adjuntar HTML
        html_part = MIMEText(body_html, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Enviar
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    
    
    @staticmethod
    def test_conexion() -> bool:
        """
        Prueba la conexión SMTP para verificar credenciales.
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                print("✅ Conexión SMTP exitosa")
                return True
        except Exception as e:
            print(f"❌ Error en conexión SMTP: {e}")
            return False