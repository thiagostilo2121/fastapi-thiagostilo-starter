# 🚀 FastAPI Starter Template (Enterprise Edition)

Un **boilerplate de nivel de producción** para construir APIs robustas en Python. Diseñado con separación estricta de responsabilidades (Clean Architecture en Capas), seguridad por defecto y sin código espagueti.

Creado por **[Thiago Stilo](https://github.com/thiagostilo)**, basado en la arquitectura y patrones extraídos de los desarrollos en producción de la startup **[Pedilo](https://github.com/thiagostilo2121/pedilo-api)**.

---

## 🧠 Filosofía de Diseño

Este boilerplate nace de la necesidad de estructurar APIs backend que puedan crecer orgánicamente sin convertirse en monolitos inmanejables. La filosofía principal se resume en los siguientes pilares:

1. **El HTTP es un detalle:** Tu lógica de negocio no debe saber que está respondiendo a una petición web. Los `services/` no devuelven códigos HTTP 404 ni 400. Lanzan **Excepciones de Dominio** genéricas que la capa superior (FastAPI) captura y traduce de manera inteligente a respuestas HTTP estándar.
2. **Definiciones Únicas (DRY en Datos):** Gracias a **SQLModel**, se elimina la duplicación histórica entre los Modelos de ORM (SQLAlchemy) y la Validación (Pydantic). Emites una sola clase y sirve para interactuar con la Base de Datos y validar la entrada del usuario.
3. **Escalabilidad Horizontal por Capas:** Las dependencias están claramente definidas. Si mañana decides extraer un servicio, su lógica, validaciones y modelos están aislados y son completamente acoplables a cualquier framework o tecnología asíncrona (como RabbitMQ, WebSockets o Celery).
4. **Respeto a los Datos Históricos (Soft Deletes):** En un sistema empresarial real, los datos rara vez se eliminan. Cuentan la historia del producto. Por eso, las entidades modelo vienen preparadas por defecto para el borrado lógico (`is_active: bool = True`).
5. **Autenticación "Zero-Trust":** Usamos `Depends(get_current_user)` inyectado como barrera arquitectónica. Es matemáticamente imposible que un dev "olvide" proteger una ruta o asigne datos a un usuario equivocado.

---

## 🏗️ Arquitectura Técnica Detallada

El flujo de información respeta una versión ágil de la arquitectura *Layered Architecture* y de *Puertos y Adaptadores*, fluyendo exclusivamente desde el exterior *(HTTP)* hacia el interior *(Base de Datos)*.

```bash
app/
├── api/             # Capa de Presentación (Controladores HTTPS)
│   ├── deps.py      # Inyección de Dependencias (Current User, Sesión DB)
│   ├── router.py    # Agrupador central
│   └── routes/      # Endpoints (FastAPI). Gestionan el I/O HTTP y delegación a "services/".
├── core/            # Núcleo Global del Sistema
│   ├── config.py    # Singleton (Pydantic Settings) que auto-valida Variables de Entorno.
│   ├── database.py  # Conexión con Motor Transaccional (Driver Engine de DB).
│   ├── exceptions.py# Jerarquía global de Errores de Negocio.
│   ├── error_handlers.py # Captura global en FastAPI (Mapeo de Errores a Códigos 4XX/5XX HTTP).
│   ├── rate_limit.py# Prevención de Spamming vía SlowAPI.
│   └── security.py  # Hashing Argon2 y Firma y Verificación de JSON Web Tokens (JWT).
├── models/          # Data Access Layer / Entidades de Base De Datos
│   └── user.py      # Tablas SQLModel. Traducidas a Esquemas relacionales automáticos.
├── schemas/         # Data Transfer Objects (DTOs)
│   └── user.py      # Pydantic schemas (Ej: UserCreate, UserResponse). La frontera rígida I/O.
└── services/        # Domain Logic Layer (Lógica de Negocio Pura)
    └── user_service.py # Validaciones comerciales (Ej: Mail duplicado) y sentencias CRUD.
```

### 🔒 Seguridad Incluida "Out of the Box"
- **Autenticación Stateless (JWT):** Sistema altamente escalable, sin bloqueos de lectura base de datos en interacciones API, gracias a la criptografía.
- **Hashing Resiliente (Argon2):** El estándar más moderno para el hashing asimétrico, resistente a la fuerza bruta computacional usando GPUs, memoria, y ASICs.
- **Protección de Tráfico (Rate Limiting):** A través de `SlowAPI`, los endpoints que puedan ser blanco de ataques DDoS o escalada de fuerza bruta (como el login y el registro) están pre-protegidos nativamente.

---

## 🧑‍💻 Cómo empezar (Quickstart)

### 1. Clonar el repositorio
*(Nota: Renombra la carpeta meta al nombre de tu proyecto definitivo)*
```bash
git clone https://github.com/thiagostilo/tu-repo-boilerplate.git mi-startup-backend
cd mi-startup-backend
```

### 2. Configura las variables de entorno
```bash
cp .env.example .env
```
Abre `.env` y genera una **clave secreta invulnerable** en tu terminal (Linux/Mac) con `openssl rand -hex 32` para poblar el parámetro `SECRET_KEY`.

### 3. Entorno e Instalación
El framework asume el uso de **Python 3.10** o superior por las características avanzadas de tipado como `int | str`.
```bash
python -m venv .venv

# Activa el entorno
# En Linux/Mac:
source .venv/bin/activate
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Empaqueta e Instala todo
pip install -r requirements.txt
```

### 4. Inicializa el Servidor (Auto-Migración)
Al arrancar, SQLModel interceptará la capa *lifespan* temporal y creará automáticamente el pool de Base de datos `dev.db` usando el controlador de *SQLite*. Al ser escalable, al moverte de entorno puedes poner una URL de *PostgreSQL* en `.env` y el código de persistencia continuará intacto.
```bash
make dev
```
Tu Servidor API en vivo, con autogeneración viva del esquema OAS3 y Swagger, te espera en: **http://localhost:8000/docs** 🎉

---

## 🛡️ Herramientas Formateo y Mantenimiento (Makefile)

Para conservar la pulcritud absoluta en el código base, asegúrate de utilizar el makefile *antes* de proponer cada iteración al sistema control de versiones y a *Main*.

```bash
# Formatea y alinea los espaciados, imports y sintaxis general de PEP8 usando (Ruff).
make format

# Revisa de raíz el tipado inferido, los huecos de seguridad, y estandariza (MyPy, Bandit, Ruff linter).
make lint

# ¡El combo completo! Ejecuta el chequeo holístico.
make check
```

---

## 📜 Licencia y Créditos
Diseñado, planificado y automatizado por **Thiago Stilo**.
Este Boilerplate es libre de uso general (Código Abierto), y fue liberado para apoyar el rápido prototipado del ecosistema dev mundial. Úsalo como cohete para propulsar tu próximo Unicornio.
