# ADR-001: Uso de MariaDB como motor de persistencia

## Estado

**Aceptado**

## Fecha

2026-09-06

## 1. Contexto

SmartSafe es una aplicación modular orientada a una Smart City que integra dos módulos funcionales principales:

- SmartReport, para el registro y gestión de incidencias urbanas.
- SmartSOS, para la generación y gestión de alertas de emergencia.

El MVP será desarrollado en aproximadamente cuatro semanas por un equipo de cuatro integrantes.

La arquitectura definida para el backend es:

```text
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
Base de datos relacional
```

Inicialmente se consideró PostgreSQL como motor de persistencia. Antes de iniciar la implementación del backend se decidió reevaluar esta elección en función del alcance real del MVP, la simplicidad operativa y la experiencia del equipo.

## 2. Decisión

Se utilizará **MariaDB** como sistema de gestión de base de datos relacional para el MVP de SmartSafe.

La integración prevista será:

```text
FastAPI
↓
SQLAlchemy
↓
PyMySQL
↓
MariaDB
```

## 3. Alternativas consideradas

### PostgreSQL

Ventajas:

- Excelente soporte relacional.
- Tipo UUID nativo.
- Amplias capacidades JSON.
- Muy buenas capacidades geoespaciales mediante PostGIS.

Desventajas para el alcance actual:

- Las capacidades avanzadas de PostGIS no son necesarias para el MVP.
- Puede introducir funcionalidades que el proyecto no utilizará durante esta fase.
- Si el equipo posee mayor familiaridad con el ecosistema MySQL/MariaDB, PostgreSQL incrementaría innecesariamente la curva de aprendizaje.

### MariaDB

Ventajas:

- Adecuada para operaciones CRUD.
- Integración sencilla con FastAPI y SQLAlchemy.
- Compatible con Docker.
- Familiar para equipos con experiencia previa en MySQL.
- Suficiente para almacenar usuarios, tipos de eventos, eventos, estados y coordenadas.
- Permite mantener una arquitectura simple durante el MVP.

Limitaciones:

- No posee un tipo UUID equivalente al de PostgreSQL.
- El soporte geoespacial es menos avanzado que PostgreSQL + PostGIS.
- Algunas capacidades avanzadas de JSON y análisis espacial son más limitadas.

Estas limitaciones no afectan los requisitos actuales del MVP.

## 4. Justificación

SmartSafe necesita inicialmente almacenar:

- usuarios;
- roles;
- tipos de eventos;
- registros de eventos;
- descripciones;
- coordenadas geográficas;
- referencias a fotografías;
- estados;
- fechas y horas.

El MVP no requiere inicialmente:

- análisis espacial complejo;
- búsquedas por distancia;
- polígonos geográficos;
- mapas de calor;
- clustering espacial;
- funciones geoespaciales avanzadas.

Por esta razón, MariaDB satisface completamente los requisitos de persistencia definidos para la primera versión.

La decisión también favorece la simplicidad operativa y reduce riesgos asociados a una tecnología que podría resultar menos familiar para el equipo.

## 5. Impacto en el modelo de datos

El modelo conceptual se mantiene:

```text
User
 1
 │
 N
EventRecord
 N
 │
 1
EventType
```

No se modifican las relaciones ni las responsabilidades de las entidades.

### Identificadores

En lugar de utilizar el tipo UUID nativo de PostgreSQL, los identificadores se almacenarán inicialmente como:

```sql
CHAR(36)
```

Esto permite mantener UUID como identificador lógico sin añadir complejidad innecesaria.

Ejemplo:

```text
550e8400-e29b-41d4-a716-446655440000
```

### Coordenadas

Las coordenadas continuarán almacenándose como:

```sql
latitude DECIMAL(9,6)
longitude DECIMAL(9,6)
```

Esto es suficiente para la visualización de eventos mediante Leaflet y OpenStreetMap.

## 6. Impacto en la arquitectura

La arquitectura general no cambia.

Antes:

```text
FastAPI
↓
Service Layer
↓
Repository Layer
↓
PostgreSQL
```

Después:

```text
FastAPI
↓
Service Layer
↓
Repository Layer
↓
MariaDB
```

Los módulos de dominio, servicios, repositorios y endpoints REST no deberán depender directamente de características específicas de MariaDB.

El Repository Pattern ayudará a mantener esta separación.

## 7. Impacto en dependencias

El backend utilizará:

- FastAPI
- SQLAlchemy
- PyMySQL

Posteriormente se evaluará el uso de Alembic para la gestión de migraciones.

La cadena de conexión tendrá una forma similar a:

```text
mysql+pymysql://usuario:password@host:3306/smartsafe
```

Las credenciales reales no deberán almacenarse en el repositorio.

Se utilizarán variables de entorno.

## 8. Impacto en Docker

MariaDB será incorporada posteriormente como servicio dentro de `docker-compose.yml`.

Conceptualmente:

```text
SmartSafe Backend
        ↓
     MariaDB
```

La configuración deberá incluir, mediante variables de entorno:

- nombre de base de datos;
- usuario;
- contraseña;
- contraseña de administrador;
- puerto.

No se incluirán credenciales reales en GitHub.

## 9. Consecuencias positivas

- Menor complejidad para el MVP.
- Fácil ejecución con Docker.
- Buena integración con SQLAlchemy.
- Compatible con el modelo relacional definido.
- Facilita el trabajo si el equipo posee experiencia con MySQL/MariaDB.
- No modifica el diseño de la API REST.
- No modifica las historias de usuario.
- No modifica los módulos SmartReport y SmartSOS.
- No modifica la estrategia de pruebas.

## 10. Consecuencias negativas

- Los UUID deberán representarse mediante `CHAR(36)` o una alternativa equivalente.
- Si SmartSafe evoluciona hacia análisis geoespacial avanzado, podría ser necesario reevaluar la tecnología de persistencia.
- Algunas optimizaciones futuras podrían requerir características específicas del motor.

## 11. Riesgos

### Riesgo 1: dependencia del motor de base de datos

Mitigación:

Utilizar SQLAlchemy y Repository Pattern para evitar que la lógica de negocio dependa directamente de consultas específicas de MariaDB.

### Riesgo 2: manejo incorrecto de credenciales

Mitigación:

Utilizar variables de entorno y mantener `.env` fuera del control de versiones.

### Riesgo 3: necesidad futura de capacidades geoespaciales avanzadas

Mitigación:

Mantener latitud y longitud como datos independientes y reevaluar el motor únicamente si aparecen requisitos reales que lo justifiquen.

## 12. Archivos que deberán actualizarse

Como consecuencia de esta decisión deberán actualizarse posteriormente:

```text
docs/03-architecture/architecture.md
docs/03-architecture/database.md
```

y cualquier otra documentación que mencione PostgreSQL como motor definitivo.

Estas actualizaciones deberán realizarse mediante una rama y Pull Request específicos.

## 13. Criterio de revisión futura

Esta decisión deberá reevaluarse únicamente si aparece un requisito real relacionado con:

- análisis espacial avanzado;
- consultas geográficas complejas;
- necesidades de escalabilidad no cubiertas;
- restricciones de interoperabilidad;
- requerimientos institucionales o de infraestructura.

Mientras ninguno de esos requisitos exista, MariaDB será el motor de persistencia oficial del MVP de SmartSafe.
