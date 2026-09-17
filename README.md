# SmartSafe

SmartSafe es una plataforma académica orientada a la gestión de seguridad urbana que integra dos módulos principales:

- **SmartReport:** registro y seguimiento de incidencias urbanas no urgentes.
- **SmartSOS:** registro y atención de alertas de emergencia.

El proyecto fue desarrollado como parte del curso **Tópicos Avanzados de Software** del Doctorado en Ciencias de la Computación.

> **Importante:** SmartSOS es un prototipo académico y no reemplaza servicios oficiales de emergencia.

---

## 1. Objetivo

Construir un sistema web modular que permita registrar incidencias urbanas, adjuntar fotografías, registrar ubicación geográfica, consultar reportes, gestionar estados, activar alertas SOS, registrar ubicación de emergencias, visualizar eventos en mapa y exponer una API REST unificada.

---

## 2. Arquitectura

SmartSafe utiliza una arquitectura de **monolito modular**.

```text
Frontend React + TypeScript
            |
            | HTTP / JSON / JWT
            v
FastAPI REST API
            |
      +-----+------+
      |            |
   Routers       Schemas
      |
   Services
      |
 Repositories
      |
 SQLAlchemy
      |
   MariaDB
```

Capas principales del backend:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
MariaDB
```

Patrones utilizados:

- Repository
- Service Layer

---

## 3. Tecnologías

### Frontend
- React
- TypeScript
- Vite
- React Router
- React Leaflet
- Leaflet
- OpenStreetMap

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- PyMySQL
- Pydantic
- python-dotenv
- JWT
- Argon2
- Alembic

### Base de datos
- MariaDB 11.4

### Infraestructura y calidad
- Docker
- Docker Compose
- pytest
- pytest-cov
- GitHub Actions
- Git / GitHub

---

## 4. Módulos

### SmartReport

Tipos implementados:

- `POTHOLE`
- `WASTE`
- `STREET_LIGHT`
- `WATER_LEAK`

Flujo:

```text
REPORTED -> IN_PROGRESS -> RESOLVED
```

### SmartSOS

Categorías disponibles en la interfaz:

- Emergencia médica
- Accidente
- Incendio
- Seguridad personal

Flujo:

```text
ACTIVE -> IN_PROGRESS -> FINISHED
```

Actualmente las emergencias se almacenan en backend mediante el tipo genérico `SOS` del módulo `SMART_SOS`.

---

## 5. Roles

### CITIZEN
Puede iniciar sesión, registrar incidencias, adjuntar fotografías, registrar ubicación, consultar sus reportes, activar SmartSOS y registrar la ubicación de la emergencia.

### OPERATOR
Puede consultar emergencias, gestionar estados, visualizar eventos en mapa y consultar UrbanEvents mediante API.

---

## 6. Historias implementadas

| US | Funcionalidad | Estado |
|---|---|---|
| US-01 | Autenticación de usuarios | Completada |
| US-02 | Registrar incidencia | Completada |
| US-03 | Adjuntar fotografía | Completada |
| US-04 | Registrar ubicación del evento | Completada |
| US-05 | Consultar mis reportes | Completada |
| US-06 | Gestionar estado del reporte | Completada |
| US-07 | Activar SOS | Completada |
| US-08 | Seleccionar tipo de emergencia | Completada |
| US-09 | Registrar ubicación SOS | Completada |
| US-10 | Consultar emergencias | Completada |
| US-11 | Gestionar estado de emergencia | Completada |
| US-12 | Visualizar eventos en mapa | Completada |
| US-13 | Consultar UrbanEvents mediante API | Completada |

---

## 7. API REST

Base local:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Health

```http
GET /health
```

### Authentication

```http
POST /api/v1/auth/login
```

### SmartReport

```http
POST /api/v1/reports
GET  /api/v1/reports
GET  /api/v1/reports/{report_id}
POST /api/v1/reports/{report_id}/photo
PUT  /api/v1/reports/{report_id}
```

### SmartSOS

```http
POST /api/v1/emergencies
PUT  /api/v1/emergencies/{emergency_id}/location
GET  /api/v1/emergencies
GET  /api/v1/emergencies/{emergency_id}
PUT  /api/v1/emergencies/{emergency_id}
```

### UrbanEvents

```http
GET /api/v1/events
```

Filtros:

```http
GET /api/v1/events?source=SMART_REPORT
GET /api/v1/events?source=SMART_SOS
GET /api/v1/events?type=POTHOLE
GET /api/v1/events?type=SOS
GET /api/v1/events?status=ACTIVE
GET /api/v1/events?source=SMART_REPORT&type=POTHOLE&status=REPORTED
```

---

## 8. Ejemplo de UrbanEvent

```json
{
  "id": "uuid",
  "source": "SMART_REPORT",
  "type": "POTHOLE",
  "status": "REPORTED",
  "description": "Bache en la vía",
  "latitude": -13.5204,
  "longitude": -71.9751,
  "photo_url": null,
  "created_at": "2026-09-16T20:00:00"
}
```

---

## 9. Variables de entorno

Crear `.env` a partir de `.env.example`.

```env
MARIADB_DATABASE=smartsafe
MARIADB_USER=smartsafe
MARIADB_PASSWORD=change_me
MARIADB_ROOT_PASSWORD=change_me_root

JWT_SECRET_KEY=change_me_with_a_secure_value
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

No incluir secretos reales en el repositorio.

---

## 10. Ejecución con Docker

Desde la raíz:

```powershell
docker compose up --build -d
docker compose ps
```

Para detener:

```powershell
docker compose down
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## 11. Frontend

```powershell
cd frontend
npm install
npm run dev
```

Build:

```powershell
npm run build
```

Vite utiliza normalmente `http://localhost:5173` o `http://localhost:5174`.

---

## 12. Backend local

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 13. Pruebas

```powershell
cd backend
python -m pytest --cov=app --cov-report=term-missing
```

Resultado validado al cierre de US-13:

```text
103 passed
Total coverage: 91.39%
```

Criterio mínimo:

```text
Coverage >= 90%
```

---

## 14. Credenciales demo

### Ciudadano

```text
Email: citizen@smartsafe.demo
Password: SmartSafeTest123!
Role: CITIZEN
```

### Operador

```text
Email: operator@smartsafe.demo
Password: SmartSafeTest123!
Role: OPERATOR
```

Uso exclusivo académico/demo.

---

## 15. Seguridad

El proyecto implementa:

- autenticación JWT;
- hash de contraseñas con Argon2;
- autorización por roles;
- validación con Pydantic;
- restricciones de transición de estados;
- separación de secretos mediante variables de entorno.

---

## 16. Fotografías

Las fotografías SmartReport se almacenan localmente en:

```text
backend/uploads/reports/
```

FastAPI las expone mediante:

```text
/uploads
```

Formatos admitidos:

- JPEG
- PNG
- WebP
- HEIC
- HEIF

Tamaño máximo: **5 MB**.

---

## 17. Mapa de eventos

El operador dispone de una vista unificada con:

- SmartReport;
- SmartSOS;
- marcadores diferenciados;
- selección de eventos;
- información básica;
- ajuste automático de la vista.

Tecnologías:

- Leaflet
- React Leaflet
- OpenStreetMap

---

## 18. Estrategia Git

```text
main
develop
feature/*
```

Flujo:

```text
feature/* -> Pull Request -> develop
```

Convención de commits:

```text
feat(...)
fix(...)
test(...)
docs(...)
refactor(...)
```

---

## 19. CI

GitHub Actions valida:

- MariaDB;
- Python 3.12;
- instalación de dependencias;
- tests;
- cobertura mínima.

---

## 20. Limitaciones

El MVP no incluye:

- IA/ML;
- detección automática de duplicados;
- cálculo avanzado de prioridad;
- mensajería asíncrona;
- seguimiento GPS continuo;
- integración con centrales oficiales de emergencia;
- notificaciones push;
- Guardian Mode;
- aplicación móvil nativa.

Además, la categoría específica seleccionada en SmartSOS todavía no se persiste como tipo diferenciado en backend; el evento se registra como `SOS`.

---

## 21. Trabajo futuro

- persistir categorías específicas SmartSOS;
- notificaciones;
- asignación de operadores;
- trazabilidad completa de estados;
- panel de métricas;
- clustering;
- prioridades configurables;
- detección de duplicados;
- integración con servicios oficiales;
- aplicación móvil;
- analítica histórica;
- procesamiento geoespacial.

---

## 22. Estado del proyecto

```text
US-01 ... US-13 → completadas
Backend tests   → 103 passed
Coverage        → 91.39%
Frontend build  → validado
Docker          → operativo
SmartReport     → operativo
SmartSOS        → operativo
UrbanEvents API → operativo
Mapa unificado  → operativo
```

---

## 23. Contexto académico

Proyecto desarrollado para el curso **Tópicos Avanzados de Software** del **Doctorado en Ciencias de la Computación**.

El proyecto aplica conceptos de arquitectura de software, APIs REST, persistencia, seguridad, contenedores, pruebas automatizadas, integración continua y desarrollo iterativo basado en historias de usuario.
