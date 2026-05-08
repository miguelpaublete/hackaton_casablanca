# 🚀 Manual de Instalación — KDD PMO Copilot
### Para personas sin conocimientos técnicos previos

---

## 📋 Índice

1. [¿Qué necesito instalar?](#1-qué-necesito-instalar)
2. [Instalar Git](#2-instalar-git)
3. [Instalar Python](#3-instalar-python)
4. [Descargar el repositorio](#4-descargar-el-repositorio)
5. [Configurar el fichero .env](#5-configurar-el-fichero-env)
6. [Instalar las dependencias del proyecto](#6-instalar-las-dependencias-del-proyecto)
7. [Arrancar la aplicación](#7-arrancar-la-aplicación)
8. [Usar la interfaz](#8-usar-la-interfaz)
9. [Solución de problemas frecuentes](#9-solución-de-problemas-frecuentes)

---

## 1. ¿Qué necesito instalar?

Antes de empezar, necesitas tener en tu ordenador estas dos herramientas gratuitas:

| Herramienta | Para qué sirve | ¿Lo tengo? |
|---|---|---|
| **Git** | Descargar el repositorio de GitHub | Abre una terminal y escribe `git --version` |
| **Python 3.11+** | Ejecutar el código del proyecto | Abre una terminal y escribe `python --version` |

> 💡 **¿Cómo abro una terminal?**
> En Windows: pulsa `Windows + R`, escribe `cmd` y pulsa Enter.

---

## 2. Instalar Git

1. Ve a 👉 **https://git-scm.com/download/win**
2. Descarga el instalador (el botón grande que dice "Click here to download")
3. Ejecuta el instalador y pulsa **Next** en todo (los valores por defecto están bien)
4. Cuando termine, **cierra y vuelve a abrir** tu terminal
5. Verifica que funciona escribiendo:
   ```
   git --version
   ```
   Deberías ver algo como `git version 2.44.0`

---

## 3. Instalar Python

1. Ve a 👉 **https://www.python.org/downloads/**
2. Descarga la versión más reciente (**Python 3.12** o superior)
3. Ejecuta el instalador
4. ⚠️ **MUY IMPORTANTE**: En la primera pantalla del instalador, marca la casilla que dice **"Add Python to PATH"** (está abajo del todo)
5. Pulsa **Install Now**
6. Cuando termine, **cierra y vuelve a abrir** tu terminal
7. Verifica que funciona:
   ```
   python --version
   ```
   Deberías ver algo como `Python 3.12.3`

> ⚠️ Si ves `Python 2.7.x` en lugar de `3.x`, usa el comando `python3` en lugar de `python` en todos los pasos siguientes.

---

## 4. Descargar el repositorio

Abre una terminal y ejecuta estos comandos **uno a uno**:

```bash
# 1. Ve a una carpeta donde quieras guardar el proyecto
#    (por ejemplo, tus Documentos)
cd C:\Users\TU_USUARIO\Documents

# 2. Descarga el repositorio
git clone https://github.com/alejandromontalban-sketch/spec-driven.git

# 3. Entra en la carpeta del proyecto
cd spec-driven
```

> 💡 Cambia `TU_USUARIO` por tu nombre de usuario de Windows.
> Lo puedes ver abriendo el Explorador de archivos → la carpeta de usuario en `C:\Users\`

Si te pide usuario y contraseña de GitHub, usa tus credenciales de GitHub.

---

## 5. Configurar el fichero .env

El proyecto necesita un fichero `.env` con las credenciales (tokens, correos, etc.).
Este fichero **no está en el repositorio** por seguridad — hay que crearlo manualmente.

### Paso a paso:

1. Dentro de la carpeta del proyecto, ve a la subcarpeta `agent`:
   ```
   cd agent
   ```

2. Crea el fichero `.env`. En Windows puedes hacerlo así:
   ```
   copy NUL .env
   ```

3. Abre el fichero con el Bloc de notas:
   ```
   notepad .env
   ```

4. Pega el siguiente contenido y rellena los valores (te los tiene que pasar Alejandro):

```ini
# ── Email (Mailjet) ──────────────────────────────────
MAILJET_API_KEY=pon_aqui_la_api_key_de_mailjet
MAILJET_API_SECRET=pon_aqui_el_secret_de_mailjet
SENDER_EMAIL=pon_aqui_el_email_remitente
PMO_EMAIL=tu_correo@bbva.com

# ── GitHub ────────────────────────────────────────────
GITHUB_TOKEN=pon_aqui_tu_token_de_github
GITHUB_REPO=alejandromontalban-sketch/spec-driven

# ── Proxy corporativo BBVA (si estás en la red BBVA) ──
# HTTP_PROXY=http://proxy.bbva.com:8080

# ── Streamlit ─────────────────────────────────────────
STREAMLIT_PORT=8501
```

5. Guarda el fichero (`Ctrl + S`) y cierra el Bloc de notas.

> 💡 **¿Cómo obtengo mi GitHub Token?**
> 1. Entra en https://github.com → tu foto de perfil → Settings
> 2. Baja hasta "Developer settings" (abajo a la izquierda)
> 3. Personal access tokens → Tokens (classic) → Generate new token
> 4. Dale un nombre, marca los permisos `repo` y pulsa "Generate token"
> 5. **Cópialo ahora** — solo se muestra una vez

---

## 6. Instalar las dependencias del proyecto

Asegúrate de estar en la carpeta `agent` del proyecto y ejecuta:

```bash
# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

Esto puede tardar **1-2 minutos**. Verás cómo se descargan paquetes. Es normal.

Si ves algún error de permisos, prueba con:
```bash
pip install -r requirements.txt --user
```

---

## 7. Arrancar la aplicación

Asegúrate de estar en la carpeta `agent` y ejecuta:

```bash
streamlit run app.py
```

Deberías ver en la terminal algo como:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

El navegador **se abrirá solo** con la interfaz. Si no se abre, escribe manualmente en tu navegador:
```
http://localhost:8501
```

> 💡 **Para parar la aplicación**: vuelve a la terminal y pulsa `Ctrl + C`

---

## 8. Usar la interfaz

Una vez abierta la aplicación:

1. **Selecciona el proyecto** en el desplegable de la izquierda (ej. "Deco algo", "carbon-markets")
2. **Selecciona el acta** que quieres procesar
3. Pulsa **"⚡ Generar Specs"** — la IA leerá el acta y generará los artefactos KDD
4. **Revisa** los artefactos generados (ADR, DOM, WRK-TASK) en la parte derecha
5. **Edita** si algo no está bien
6. Pulsa **"✅ Validar y Commitear Specs"** — los ficheros se guardarán en el repositorio

---

## 9. Solución de problemas frecuentes

### ❌ "python no se reconoce como un comando"
→ Python no está instalado o no se añadió al PATH.
Vuelve al **paso 3** y asegúrate de marcar "**Add Python to PATH**" durante la instalación.

### ❌ "git no se reconoce como un comando"
→ Git no está instalado. Vuelve al **paso 2**.
Recuerda **cerrar y abrir** la terminal después de instalar.

### ❌ "No module named 'streamlit'" u otro módulo
→ Las dependencias no están instaladas. Vuelve al **paso 6** y ejecuta:
```bash
pip install -r requirements.txt
```

### ❌ "La página localhost ha rechazado la conexión"
→ La aplicación no está arrancada. Vuelve al **paso 7** y ejecuta:
```bash
streamlit run app.py
```
Deja la terminal **abierta** mientras usas la app.

### ❌ Error de proxy / conexión en red BBVA
→ Descomenta la línea del proxy en el `.env`:
```ini
HTTP_PROXY=http://proxy.bbva.com:8080
```
Pregunta a Alejandro cuál es el proxy correcto de BBVA.

### ❌ "Invalid credentials" o error de GitHub
→ Tu `GITHUB_TOKEN` en el `.env` ha caducado o está mal copiado.
Genera uno nuevo siguiendo las instrucciones del **paso 5**.

---

## 📞 ¿Sigues con problemas?

Escríbele a **Alejandro** con:
1. Una captura de pantalla del error
2. En qué paso estás
3. Qué sistema operativo tienes (Windows 10, Windows 11...)

---

*Manual KDD PMO Copilot — Versión 1.0 — Mayo 2026*

