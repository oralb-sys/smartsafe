# SmartSafe
## Patrones de Diseño

## 1. Objetivo

Documentar los patrones de diseño utilizados en SmartSafe y justificar su aplicación.

Los patrones se emplearán únicamente cuando resuelvan un problema concreto.

---

## 2. Repository Pattern

### Problema

La lógica de negocio no debe depender directamente de PostgreSQL ni de consultas específicas de persistencia.

### Solución

Se utilizará Repository Pattern.

Ejemplos:
- UserRepository
- EventRepository
- EventTypeRepository

Responsabilidades:
- crear;
- buscar;
- actualizar;
- eliminar.

### Beneficio

Permite:
- desacoplar persistencia;
- facilitar pruebas;
- mejorar mantenibilidad.

---

## 3. Service Layer

### Problema

Los endpoints REST no deben contener reglas de negocio complejas.

### Solución

Se implementarán servicios:
- AuthService
- ReportService
- EmergencyService
- UrbanEventService

### Beneficio

Permite mantener separados:
- transporte HTTP;
- reglas de negocio;
- persistencia.

---

## 4. Strategy Pattern

### Evaluación

SmartReport y SmartSOS poseen comportamientos parcialmente diferentes, especialmente en:
- estados iniciales;
- transiciones permitidas;
- tipos válidos.

Se evaluará la utilización de Strategy Pattern si estas diferencias generan lógica condicional repetitiva.

Ejemplo conceptual:

```text
EventStrategy
     │
     ├── SmartReportStrategy
     └── SmartSOSStrategy
```

### Regla

No se implementará el patrón hasta que exista una necesidad real.

Esto evita sobreingeniería.

---

## 5. Arquitectura por capas

La estructura general será:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

Esta organización facilitará:
- pruebas unitarias;
- sustitución de dependencias;
- mantenimiento;
- legibilidad.
