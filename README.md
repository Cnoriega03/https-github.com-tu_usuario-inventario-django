# Sistema Web de Inventario Django listo para produccion

Aplicacion Django para gestionar inventario con autenticacion, usuarios administrados desde el panel admin, permisos por roles, PostgreSQL en produccion, WhiteNoise para archivos estaticos y Gunicorn como servidor WSGI.

## Caracteristicas

- Login con usuario y contrasena.
- Sin registro publico de usuarios.
- Usuarios creados solo desde `/admin/` por un administrador.
- Usuarios normales sin acceso al panel admin.
- Gestion de categorias, productos, entradas y salidas de inventario.
- Actualizacion automatica de stock al registrar movimientos.
- Alertas de stock minimo.
- Preparado para Render, Railway o VPS.
- Configuracion por variables de entorno.
- PostgreSQL en produccion mediante `DATABASE_URL`.
- SQLite opcional solo para desarrollo local cuando no existe `DATABASE_URL`.

## Estructura principal

- `inventario_empresa/`: configuracion Django del proyecto.
- `inventario/`: modelos, vistas, formularios, URLs, admin y comando de permisos.
- `templates/`: vistas HTML con Bootstrap.
- `static/`: estilos propios.
- `requirements.txt`: dependencias de produccion.
- `Procfile`: comando de arranque para plataformas cloud.
- `runtime.txt`: version sugerida de Python.
- `.env.example`: ejemplo de variables de entorno.

## Variables de entorno

Copia `.env.example` como `.env` para desarrollo local o configura estas variables en el hosting:

```env
SECRET_KEY=change-this-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://your-domain.com
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
```

Notas:

- `SECRET_KEY`: usa una clave larga y privada.
- `DEBUG`: en produccion debe ser `False`.
- `ALLOWED_HOSTS`: dominios permitidos, separados por coma, sin `https://`.
- `CSRF_TRUSTED_ORIGINS`: origenes confiables, separados por coma, con `https://`.
- `DATABASE_URL`: URL de PostgreSQL entregada por Render, Railway o tu VPS.

## Ejecutar en desarrollo local

```powershell
cd "C:\Users\carlo\Documents\Codex\2026-06-24\quiero-crear-un-sistema-web-de\outputs\django-inventario"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py configurar_permisos
python manage.py createsuperuser
python manage.py runserver
```

Luego abre:

- Sistema: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Roles y permisos

El proyecto incluye el comando:

```powershell
python manage.py configurar_permisos
```

Crea dos grupos:

- `Administrador`: puede entrar al panel admin, crear usuarios y gestionar todo.
- `Usuario Inventario`: no puede entrar al panel admin; solo usa las pantallas del inventario.

Asignar un usuario existente como administrador:

```powershell
python manage.py configurar_permisos --admin-user nombre_usuario
```

Asignar un usuario existente como usuario normal:

```powershell
python manage.py configurar_permisos --inventory-user nombre_usuario
```

Para que un usuario normal no entre al admin, debe tener `is_staff=False` y `is_superuser=False`.

## Preparar GitHub

1. Entra a la carpeta del proyecto:

   ```powershell
   cd "C:\Users\carlo\Documents\Codex\2026-06-24\quiero-crear-un-sistema-web-de\outputs\django-inventario"
   ```

2. Inicializa Git:

   ```powershell
   git init
   git add .
   git commit -m "Proyecto Django inventario listo para produccion"
   ```

3. Crea un repositorio en GitHub.

4. Conecta el repositorio local con GitHub:

   ```powershell
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

No subas `.env`, `.venv`, `db.sqlite3` ni `staticfiles/`; ya estan excluidos en `.gitignore`.

## Deploy en Render

1. Sube el proyecto a GitHub.
2. En Render, crea un `PostgreSQL Database`.
3. Copia la `External Database URL` o `Internal Database URL`.
4. Crea un `Web Service` conectado al repositorio de GitHub.
5. Configura:

   - Runtime: Python
   - Build Command:

     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```

   - Start Command:

     ```bash
     gunicorn inventario_empresa.wsgi:application --log-file -
     ```

6. Agrega variables de entorno:

   ```env
   SECRET_KEY=tu-clave-secreta
   DEBUG=False
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=tu-app.onrender.com
   CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
   ```

7. Despliega el servicio.

8. Ejecuta migraciones desde la consola/shell de Render:

   ```bash
   python manage.py migrate
   python manage.py configurar_permisos
   python manage.py createsuperuser
   ```

9. Abre la URL publica de Render:

   ```text
   https://tu-app.onrender.com/
   ```

## Deploy en Railway

1. Sube el proyecto a GitHub.
2. En Railway, crea un nuevo proyecto desde GitHub.
3. Agrega un servicio PostgreSQL.
4. Configura las variables:

   ```env
   SECRET_KEY=tu-clave-secreta
   DEBUG=False
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ALLOWED_HOSTS=tu-app.up.railway.app
   CSRF_TRUSTED_ORIGINS=https://tu-app.up.railway.app
   ```

5. Usa como comando de inicio:

   ```bash
   gunicorn inventario_empresa.wsgi:application --log-file -
   ```

6. Si Railway permite comando de build, usa:

   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

7. Ejecuta migraciones en la terminal de Railway:

   ```bash
   python manage.py migrate
   python manage.py configurar_permisos
   python manage.py createsuperuser
   ```

8. Accede a la URL publica generada por Railway.

## Deploy en un VPS

1. Instala dependencias del sistema:

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip postgresql nginx git
   ```

2. Clona el repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

3. Crea entorno virtual e instala dependencias:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Crea una base PostgreSQL y usuario.

5. Crea un archivo `.env` con las variables reales:

   ```env
   SECRET_KEY=tu-clave-secreta
   DEBUG=False
   DATABASE_URL=postgresql://usuario:password@localhost:5432/inventario
   ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
   CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
   ```

6. Ejecuta:

   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py configurar_permisos
   python manage.py createsuperuser
   ```

7. Prueba Gunicorn:

   ```bash
   gunicorn inventario_empresa.wsgi:application --bind 0.0.0.0:8000
   ```

8. Configura Gunicorn como servicio `systemd` y Nginx como proxy inverso hacia `127.0.0.1:8000`.

9. Configura HTTPS con Certbot:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
   ```

## Comandos utiles de produccion

Migraciones:

```bash
python manage.py migrate
```

Recolectar estaticos:

```bash
python manage.py collectstatic --noinput
```

Crear grupos de permisos:

```bash
python manage.py configurar_permisos
```

Crear superusuario:

```bash
python manage.py createsuperuser
```

Arrancar servidor de produccion:

```bash
gunicorn inventario_empresa.wsgi:application --log-file -
```

## Seguridad importante

- No publiques `.env`.
- No uses `DEBUG=True` en produccion.
- Usa PostgreSQL para produccion, no SQLite.
- Cambia la contraseÃ±a temporal del administrador si creaste una localmente.
- Solo usuarios con `is_staff=True` pueden entrar al panel admin.
- Los usuarios normales deben estar en el grupo `Usuario Inventario` y tener `is_staff=False`.
