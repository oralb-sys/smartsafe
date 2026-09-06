# SmartSafe
## Arquitectura del sistema

## 1. Objetivo

Definir la arquitectura técnica del MVP de SmartSafe, procurando simplicidad, mantenibilidad, testabilidad e interoperabilidad.

SmartSafe será implementado como una aplicación modular con frontend y backend separados, comunicados mediante una API REST.

---

## 2. Arquitectura general

La arquitectura propuesta es:

Frontend
↓
REST API
↓
Router / Controller
↓
Service Layer
↓
Repository Layer
↓
MariaDB

Representación conceptual:

```text
┌─────────────────────────────┐
│          FRONTEND           │
│      React + TypeScript     │
└──────────────┬──────────────┘
               │
               │ HTTP / JSON
               ▼
┌─────────────────────────────┐
│          REST API           │
│           FastAPI           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        ROUTER LAYER         │
│ Endpoints / Validaciones    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        SERVICE LAYER        │
│     Reglas de negocio       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      REPOSITORY LAYER       │
│      Acceso a datos         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         MariaDB          │
└─────────────────────────────┘
```

---

## 3. Módulos principales

El backend se organizará inicialmente en:

```text
app/
├── auth/
├── users/
├── smartreport/
├── smartsos/
├── events/
└── shared/
```

### auth

Responsable de:
- autenticación;
- JWT;
- validación de credenciales;
- autorización.

### users

Responsable de:
- usuarios;
- roles;
- consulta de información básica.

### smartreport

Responsable de:
- registro de incidencias;
- consulta de reportes;
- actualización de estado;
- validaciones de SmartReport.

### smartsos

Responsable de:
- creación de alertas SOS;
- consulta de emergencias;
- actualización de estado;
- validaciones de SmartSOS.

### events

Responsable de:
- representación UrbanEvent;
- integración de eventos SmartReport y SmartSOS;
- filtros comunes.

### shared

Responsable de:
- utilidades;
- excepciones;
- configuración;
- componentes reutilizables.

---

## 4. Frontend

El frontend utilizará React + TypeScript.

Estructura prevista:

```text
src/
├── auth/
├── smartreport/
├── smartsos/
├── control-center/
├── shared/
└── services/
```

La comunicación con el backend se realizará exclusivamente mediante la API REST.

---

## 5. Centro de control

El operador dispondrá de una interfaz que permitirá:
- consultar reportes;
- consultar emergencias;
- visualizar eventos sobre un mapa;
- modificar estados;
- consultar detalles.

---

## 6. Integración

SmartSafe expondrá un endpoint común:

```text
GET /api/v1/events
```

que devolverá una representación común denominada UrbanEvent.

El objetivo es permitir futuras integraciones con otros sistemas Smart City.

---

## 7. Decisiones arquitectónicas

### DA-01

No se utilizarán microservicios durante el MVP.

Justificación: el proyecto será desarrollado en cuatro semanas por un equipo de cuatro integrantes y la separación en microservicios introduciría complejidad operativa innecesaria.

### DA-02

Se utilizará arquitectura por capas.

Justificación: permite separar presentación, lógica de negocio y persistencia, facilitando pruebas y mantenimiento.

### DA-03

SmartReport y SmartSOS serán módulos del mismo backend.

Justificación: comparten usuarios, autenticación, base de datos e infraestructura.

### DA-04

La integración externa se realizará mediante API REST.

Justificación: proporciona interoperabilidad sencilla y responde directamente a los requisitos académicos del proyecto.
