# 🚚 Sistema de Autenticación Segura - Cesar Tomas Transport

Proyecto educativo para la clase de **Programación Segura** que implementa un sistema completo de autenticación con **2FA/MFA usando OTP** (Google Authenticator).

## 🎯 Objetivo del Proyecto

Demostrar la implementación de un sistema de autenticación robusto y seguro que incluye:

- ✅ Autenticación segura con credenciales (email/password)
- ✅ **Two-Factor Authentication (2FA)** con códigos OTP
- ✅ Tokens JWT (Access + Refresh tokens)
- ✅ Rate limiting y protección contra fuerza bruta
- ✅ Hashing seguro de contraseñas (Bcrypt)
- ✅ Logging de eventos de seguridad
- ✅ Validación y sanitización de inputs
- ✅ Headers de seguridad HTTP

## 🚀 Inicio Rápido

### 1. Configurar Backend

```bash
cd backend
npm install
# Configurar .env con credenciales de MySQL
npm run dev
```

### 2. Configurar Frontend

```bash
npm install
npm start
```

## 📱 Configurar 2FA con Google Authenticator

1. Descarga **Google Authenticator** en tu móvil
2. Inicia sesión en la aplicación
3. Ve a "Configuración de Seguridad"
4. Escanea el código QR mostrado
5. Ingresa el código de 6 dígitos
6. ¡2FA activado! 🎉

## 📚 Documentación Completa

- **[Backend README](backend/README.md)** - Documentación del API
- **[SECURITY.md](backend/SECURITY.md)** - Documentación de seguridad detallada

## 🔐 Características de Seguridad Implementadas

- Bcrypt password hashing (12 rounds)
- JWT access tokens (15 min) + refresh tokens (7 días)
- 2FA con TOTP (Google Authenticator compatible)
- Rate limiting por IP
- Account locking (5 intentos fallidos)
- SQL injection prevention (prepared statements)
- XSS protection (input sanitization)
- Security headers (Helmet.js)
- CORS restrictivo
- Security event logging

## 🏗️ Tecnologías

**Frontend:**
- Angular 20
- TypeScript
- SASS

**Backend:**
- Node.js + Express
- MySQL
- JWT (jsonwebtoken)
- Bcrypt
- Speakeasy (OTP)
- QRCode
- Helmet.js
- Winston (logging)

## 📖 Recursos Educativos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Backend SECURITY.md](backend/SECURITY.md) - Explicación detallada de cada medida de seguridad

---

**Proyecto educativo** - Programación Segura
