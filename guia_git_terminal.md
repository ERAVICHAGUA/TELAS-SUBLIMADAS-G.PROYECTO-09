# Guía Rápida de Git + Terminal

## Comandos de Git

### Ver ramas
- `git branch` — Mostrar ramas locales
- `git branch -a` — Mostrar ramas locales + remotas
- `git branch -av` — Ramas con su último commit

### Actualizar repositorio
- `git fetch origin` — Trae cambios del remoto sin aplicarlos
- `git pull origin main` — Trae y aplica cambios en main

### Cambiar y crear ramas
- `git switch main` — Cambiar a main
- `git switch -c nueva origin/nueva` — Crear rama local desde remota
- `git checkout rama` — Cambiar (método antiguo)

### Fusionar (merge)
- `git merge rama` — Fusiona esa rama en la actual

### Subir cambios
- `git push origin main` — Subir cambios a GitHub

### Historial de commits
- `git log` — Ver historial completo
- `git log --oneline` — Versión compacta
- `git log origin/main -n 5` — Últimos 5 commits del remoto
- `git for-each-ref --format="%(refname:short) | %(authorname) | %(authordate:short) | %(subject)" refs/heads refs/remotes/origin` — Último commit de todas las ramas

### Estado del repositorio
- `git status` — Muestra cambios pendientes
- `git remote -v` — Ver URL del repo remoto

---

## Terminal / Python

### Entornos virtuales
- `python -m venv v venv` — Crear un entorno virtual
- `./venv/Scripts/activate` — Activar venv
- `deactivate` — Desactivar venv

### Instalar dependencias
- `pip install -r requirements.txt` — Instalar librerías del proyecto

### Backend
- `uvicorn main:app --reload` — Correr backend en FastAPI
- `python app.py` — Ejecutar backend simple

### Frontend Streamlit
- `streamlit run app.py` — Correr interfaz Streamlit

### Navegación de carpetas
- `cd carpeta` — Entrar a una carpeta
- `cd ..` — Subir una carpeta
- `pwd` — Mostrar ruta actual
- `dir` — Listar archivos

---

**Guía lista para copiar y usar cuando la necesites.**
