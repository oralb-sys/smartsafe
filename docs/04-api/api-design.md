# SmartSafe

## Diseño de API REST

## 1\. Base URL

```text
/api/v1
```

\---

## 2\. Autenticación

### Login

```http
POST /api/v1/auth/login
```

#### Request

```json
{
  "email": "usuario@smartsafe.demo",
  "password": "password"
}
```

#### Response

```text
200 OK
```

Ejemplo:

```json
{
  "access\_token": "...",
  "token\_type": "bearer"
}
```

Errores posibles:

* 401 Unauthorized

\---

## 3\. SmartReport

### Crear reporte

```http
POST /api/v1/reports
```

Respuesta:

* 201 Created

### Listar reportes

```http
GET /api/v1/reports
```

Respuesta:

* 200 OK

El usuario CITIZEN verá únicamente sus propios reportes.

El usuario OPERATOR podrá consultar todos los reportes.

### Obtener reporte

```http
GET /api/v1/reports/{id}
```

Respuestas:

* 200 OK
* 404 Not Found

### Actualizar reporte

```http
PUT /api/v1/reports/{id}
```

Respuesta:

* 200 OK

### Eliminar reporte

```http
DELETE /api/v1/reports/{id}
```

Respuesta:

* 204 No Content

\---

## 4\. SmartSOS

### Crear emergencia

```http
POST /api/v1/emergencies
```

Respuesta:

* 201 Created

La emergencia deberá crearse con:

```text
status = ACTIVE
```

### Listar emergencias

```http
GET /api/v1/emergencies
```

Respuesta:

* 200 OK

### Obtener emergencia

```http
GET /api/v1/emergencies/{id}
```

Respuestas:

* 200 OK
* 404 Not Found

### Actualizar emergencia

```http
PUT /api/v1/emergencies/{id}
```

Respuesta:

* 200 OK

### Eliminar emergencia

```http
DELETE /api/v1/emergencies/{id}
```

Respuesta:

* 204 No Content

\---

## 5\. UrbanEvent

### Consultar eventos integrados

```http
GET /api/v1/events
```

Filtros opcionales:

* source
* type
* status

Ejemplo:

```text
GET /api/v1/events?source=SMART\_SOS\&status=ACTIVE
```

Respuesta:

* 200 OK

\---

## 6\. Códigos HTTP

|Código|Uso|
|-|-|
|200|Consulta o actualización exitosa|
|201|Creación exitosa|
|204|Eliminación exitosa|
|400|Solicitud incorrecta|
|401|No autenticado|
|403|Sin autorización|
|404|Recurso inexistente|
|409|Conflicto|
|422|Datos inválidos|
|500|Error interno|

No debe utilizarse 200 OK para representar errores.

\---

## 7\. Formato de errores

Formato común:

```json
{
  "error": {
    "code": "EVENT\_NOT\_FOUND",
    "message": "El evento solicitado no existe."
  }
}
```

\---

## 8. Documentación OpenAPI

FastAPI publica automáticamente la documentación interactiva y el esquema OpenAPI de SmartSafe.

### 8.1. Interfaces disponibles

Con el backend ejecutándose localmente en el puerto 8000, se puede acceder a:

| Recurso         | URL                                  | Propósito                                                          |
| --------------- | ------------------------------------ | ------------------------------------------------------------------ |
| Swagger UI      | `http://127.0.0.1:8000/docs`         | Explorar y probar los endpoints mediante una interfaz interactiva. |
| ReDoc           | `http://127.0.0.1:8000/redoc`        | Consultar la documentación de referencia de la API.                |
| Esquema OpenAPI | `http://127.0.0.1:8000/openapi.json` | Obtener la especificación de la API en formato JSON.               |

### 8.2. Configuración actual

La aplicación declara el título **SmartSafe API**, la versión `0.1.0` y una descripción de los módulos SmartReport y SmartSOS. Asimismo, incluye la advertencia de que SmartSOS es un prototipo académico y no reemplaza los servicios oficiales de emergencia.

Actualmente, el endpoint implementado y documentado es:

```http
GET /health
```

Este endpoint permite verificar que el servicio se encuentra disponible y responde con:

```json
{
  "status": "ok",
  "service": "SmartSafe API"
}
```

La operación se encuentra agrupada bajo la etiqueta **Health** y especifica su resumen, descripción, código HTTP 200 y ejemplo de respuesta.

### 8.3. Estado de implementación

Las rutas de autenticación, SmartReport, SmartSOS y UrbanEvent descritas en las secciones anteriores constituyen el contrato de API previsto para el MVP. Se incorporarán progresivamente al esquema OpenAPI conforme sean implementadas en los siguientes Sprints.

Por tanto, la documentación generada actualmente no debe interpretarse como evidencia de que dichos endpoints ya están disponibles.

### 8.4. Criterios para nuevos endpoints

Cada endpoint que se implemente deberá documentar, según corresponda:

* propósito y descripción de la operación;
* parámetros de ruta y consulta;
* cuerpo de solicitud y esquema de respuesta;
* códigos HTTP de éxito y error;
* ejemplos representativos;
* requisitos de autenticación y autorización.

La documentación deberá mantenerse sincronizada con el comportamiento real de la API.


