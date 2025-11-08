# 📋 Instrucciones de Instalación y Configuración

## ✅ Pasos para Iniciar el Proyecto

### Paso 1: Instalar MySQL (si no lo tienes)

1. Descarga MySQL desde: https://dev.mysql.com/downloads/mysql/
2. Instala MySQL siguiendo el wizard
3. Anota el password de root que configures

### Paso 2: Configurar la Base de Datos

Abre MySQL Workbench o terminal MySQL:

```bash
mysql -u root -p
```

**Opción A: Usar root (desarrollo local)**
```sql
-- Solo verificar que puedes conectarte
SELECT 1;
EXIT;
```

**Opción B: Crear usuario específico (recomendado)**
```sql
CREATE USER 'cesar_tomas'@'localhost' IDENTIFIED BY 'tuPassword123!';
GRANT ALL PRIVILEGES ON cesar_tomas_db.* TO 'cesar_tomas'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 3: Configurar el Backend

```bash
# Navegar a la carpeta backend
cd backend

# Instalar dependencias
npm install

# IMPORTANTE: Configurar archivo .env
# El archivo .env ya existe, solo debes editarlo con tus credenciales

# Editar .env con Notepad o tu editor favorito
notepad .env

# Configurar estas líneas en el .env:
# DB_USER=root  (o 'cesar_tomas' si creaste el usuario)
# DB_PASSWORD=tu_password_de_mysql
# DB_NAME=cesar_tomas_db
```

**Ejemplo de .env configurado:**
```env
PORT=3000
NODE_ENV=development

# Base de Datos MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql_aqui
DB_NAME=cesar_tomas_db

# El resto de la configuración ya está lista
```

### Paso 4: Iniciar el Backend

```bash
# Estando en la carpeta backend/
npm run dev
```

**Deberías ver algo como:**
```
═══════════════════════════════════════════════════════════
🚀 SERVIDOR INICIADO CORRECTAMENTE
═══════════════════════════════════════════════════════════
📡 Puerto: 3000
🌍 Entorno: development
🔐 CORS Origin: http://localhost:4200
═══════════════════════════════════════════════════════════
```

✅ Si ves este mensaje, ¡el backend está listo!

### Paso 5: Configurar el Frontend

Abre una **NUEVA terminal** (deja la otra corriendo):

```bash
# Volver a la carpeta raíz del proyecto
cd ..

# Instalar dependencias de Angular (si no se han instalado)
npm install

# Iniciar servidor de desarrollo
npm start
```

Deberías ver:
```
** Angular Live Development Server is listening on localhost:4200 **
```

### Paso 6: Abrir la Aplicación

1. Abre tu navegador
2. Ve a: `http://localhost:4200`
3. Deberías ver la página de login

## 🧪 Probar el Sistema

### 1. Registrar un Usuario

```
Email: test@example.com
Username: testuser
Password: Test123!@#
```

### 2. Iniciar Sesión

Usa las credenciales que acabas de crear.

### 3. Configurar 2FA (Opcional)

1. Descarga **Google Authenticator** en tu móvil:
   - Android: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2
   - iOS: https://apps.apple.com/app/google-authenticator/id388497605

2. En la aplicación web:
   - Ve a "Configuración de Seguridad" o "Settings"
   - Haz clic en "Habilitar 2FA"
   - Se mostrará un código QR

3. En tu móvil:
   - Abre Google Authenticator
   - Toca el botón "+"
   - Selecciona "Escanear código QR"
   - Escanea el código mostrado en la web

4. En la aplicación web:
   - Ingresa el código de 6 dígitos que aparece en tu móvil
   - Haz clic en "Verificar"
   - ¡2FA activado! 🎉

### 4. Probar Login con 2FA

1. Cierra sesión
2. Inicia sesión nuevamente con tu email y password
3. Ahora te pedirá un código OTP
4. Abre Google Authenticator en tu móvil
5. Ingresa el código de 6 dígitos
6. ¡Acceso concedido!

## 🔧 Solución de Problemas

### Error: "Cannot connect to database"

**Solución:**
1. Verificar que MySQL esté corriendo
2. Verificar usuario y password en `backend/.env`
3. Verificar que el usuario tenga permisos:
   ```sql
   GRANT ALL PRIVILEGES ON cesar_tomas_db.* TO 'tu_usuario'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Error: "Port 3000 is already in use"

**Solución:**
1. Matar el proceso en el puerto 3000:
   ```bash
   # Windows
   netstat -ano | findstr :3000
   taskkill /PID <PID_NUMBER> /F
   ```
2. O cambiar el puerto en `backend/.env`:
   ```env
   PORT=3001
   ```

### Error: "CORS policy error" en el navegador

**Solución:**
1. Verificar que el backend esté corriendo
2. Verificar configuración de CORS en `backend/.env`:
   ```env
   CORS_ORIGIN=http://localhost:4200
   ```

### El código OTP no funciona

**Solución:**
1. Verificar que la hora del servidor y del móvil estén sincronizadas
2. Los códigos OTP son sensibles al tiempo
3. Esperar a que se genere un nuevo código (cada 30 segundos)

## 📚 Documentación Adicional

- **[README.md](README.md)** - Documentación principal del proyecto
- **[backend/README.md](backend/README.md)** - Documentación completa del API
- **[backend/SECURITY.md](backend/SECURITY.md)** - Documentación de seguridad detallada

## 🎓 Para tu Clase de Programación Segura

Este proyecto implementa:

### ✅ Conceptos de Seguridad Cubiertos

1. **Password Security**
   - Bcrypt hashing (no texto plano)
   - Salt automático
   - 12 rounds de hashing

2. **Multi-Factor Authentication (MFA/2FA)**
   - TOTP (Time-based One-Time Password)
   - Compatible con Google Authenticator
   - QR code para fácil configuración

3. **Session Management**
   - JWT tokens (stateless)
   - Access + Refresh tokens
   - Token revocation

4. **Protection contra Ataques**
   - SQL Injection (prepared statements)
   - XSS (sanitización)
   - CSRF (SameSite cookies)
   - Brute Force (rate limiting)
   - Timing Attacks (bcrypt constant-time)

5. **Defense in Depth**
   - Múltiples capas de seguridad
   - Account locking
   - Security logging
   - Input validation

6. **Security Best Practices**
   - Principio de mínimo privilegio
   - Fail secure
   - Security by design
   - Complete mediation

### 📊 Características Demostrables

- **Rate Limiting**: Intenta hacer login 6 veces con password incorrecta
- **Account Locking**: Después de 5 intentos, la cuenta se bloquea 15 minutos
- **2FA**: Demuestra autenticación de dos factores funcional
- **Security Logs**: Revisa la tabla `security_logs` en la BD
- **Token Expiration**: Los access tokens expiran en 15 minutos
- **Password Hashing**: Revisa la tabla `users`, las passwords están hasheadas

## 🚀 Próximos Pasos (Opcional)

Si quieres expandir el proyecto:

1. **Agregar roles y permisos**
2. **Implementar recuperación de contraseña por email**
3. **Agregar CAPTCHA**
4. **Implementar OAuth2 (Google, Facebook)**
5. **Agregar biometría (WebAuthn/FIDO2)**
6. **Implementar audit trail completo**
7. **Agregar dashboard de seguridad**

## ✅ Checklist de Verificación

Antes de presentar el proyecto, verifica:

- [ ] Backend corriendo sin errores
- [ ] Frontend conectado al backend
- [ ] Puedes registrar un usuario
- [ ] Puedes hacer login
- [ ] Puedes configurar 2FA
- [ ] El login con 2FA funciona
- [ ] Los logs de seguridad se guardan en la BD
- [ ] Leíste la documentación de seguridad (SECURITY.md)

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del backend en `backend/logs/`
2. Revisa la consola del navegador (F12)
3. Consulta la documentación en `backend/SECURITY.md`

---

**¡Éxito con tu proyecto de Programación Segura!** 🎓🔐
