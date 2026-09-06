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

## 8\. Documentación OpenAPI

FastAPI deberá publicar:

```text
/docs
```

y:

```text
/redoc
```

Los endpoints deberán especificar:

* request;
* response;
* parámetros;
* códigos HTTP.

