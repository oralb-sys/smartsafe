SmartSafe

Diseño de API REST

1. Base URL

/api/v1

2. Autenticación

Login

POST /api/v1/auth/login

Permite autenticar a un usuario mediante correo electrónico y contraseña.

Request

{
  "email": "usuario@smartsafe.demo",
  "password": "password"
}

Response exitosa

200 OK

Ejemplo:

{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "role": "CITIZEN"
}

El campo role puede tomar los valores:

CITIZEN

OPERATOR

El access_token es un JWT firmado que incluye el identificador del usuario, su rol y una fecha de expiración.

Credenciales inválidas

401 Unauthorized

Ejemplo:

{
  "detail": "Credenciales invalidas"
}

Validación de datos

Si el correo no tiene un formato válido, la API responde:

422 Unprocessable Entity

Seguridad de contraseñas

Las contraseñas no se almacenan en texto plano. SmartSafe utiliza Argon2 para generar y verificar los hashes almacenados en el campo password_hash.

3. SmartReport

Crear reporte

POST /api/v1/reports

Permite registrar una incidencia urbana no urgente asociada al usuario autenticado.

Requiere autenticación mediante Bearer JWT.

Request

{
  "category": "POTHOLE",
  "description": "Bache profundo en una vía principal",
  "latitude": -13.5204,
  "longitude": -71.9751,
  "photo_url": null
}

Categorías permitidas

POTHOLE

WASTE

STREET_LIGHT

WATER_LEAK

Las categorías corresponden al catálogo de tipos de incidencia de SmartReport.

El reporte se crea con:

status = REPORTED

Response exitosa

201 Created

Ejemplo:

{
  "id": "uuid",
  "category": "POTHOLE",
  "description": "Bache profundo en una vía principal",
  "latitude": -13.520400,
  "longitude": -71.975100,
  "photo_url": null,
  "status": "REPORTED",
  "created_at": "2026-09-12T20:00:00"
}

Errores posibles

Usuario no autenticado

401 Unauthorized

Se produce cuando no se proporciona un token JWT válido.

Categoría no disponible

400 Bad Request

Se produce cuando la categoría solicitada no se encuentra disponible en el catálogo de SmartReport.

Datos inválidos

422 Unprocessable Entity

Se produce cuando los datos de entrada no cumplen las validaciones definidas.

Entre otros casos:

categoría no válida;

latitud menor que -90 o mayor que 90;

longitud menor que -180 o mayor que 180;

longitud de descripción superior al límite permitido;

longitud de photo_url superior al límite permitido.

Listar reportes

GET /api/v1/reports

Respuesta:

200 OK

El usuario CITIZEN verá únicamente sus propios reportes.

El usuario OPERATOR podrá consultar todos los reportes.

Este endpoint forma parte del contrato previsto para el MVP y todavía no se encuentra implementado.

Obtener reporte

GET /api/v1/reports/{id}

Respuestas previstas:

200 OK
404 Not Found

Este endpoint todavía no se encuentra implementado.

Actualizar reporte

PUT /api/v1/reports/{id}

Respuesta prevista:

200 OK

Este endpoint todavía no se encuentra implementado.

Eliminar reporte

DELETE /api/v1/reports/{id}

Respuesta prevista:

204 No Content

Este endpoint todavía no se encuentra implementado.

4. SmartSOS

Crear emergencia

POST /api/v1/emergencies

Respuesta prevista:

201 Created

La emergencia deberá crearse con:

status = ACTIVE

Este endpoint todavía no se encuentra implementado.

Listar emergencias

GET /api/v1/emergencies

Respuesta prevista:

200 OK

Este endpoint todavía no se encuentra implementado.

Obtener emergencia

GET /api/v1/emergencies/{id}

Respuestas previstas:

200 OK
404 Not Found

Este endpoint todavía no se encuentra implementado.

Actualizar emergencia

PUT /api/v1/emergencies/{id}

Respuesta prevista:

200 OK

Este endpoint todavía no se encuentra implementado.

Eliminar emergencia

DELETE /api/v1/emergencies/{id}

Respuesta prevista:

204 No Content

Este endpoint todavía no se encuentra implementado.

5. UrbanEvent

Consultar eventos integrados

GET /api/v1/events

Filtros opcionales previstos:

source

type

status

Ejemplo:

GET /api/v1/events?source=SMART_SOS&status=ACTIVE

Respuesta prevista:

200 OK

Este endpoint todavía no se encuentra implementado.

6. Códigos HTTP

Código

Uso

200

Consulta, autenticación o actualización exitosa

201

Creación exitosa

204

Eliminación exitosa

400

Solicitud incorrecta

401

No autenticado o credenciales inválidas

403

Sin autorización

404

Recurso inexistente

409

Conflicto

422

Datos inválidos

500

Error interno

No debe utilizarse 200 OK para representar errores.

7. Formato de errores

Formato común previsto para los endpoints de dominio:

{
  "error": {
    "code": "EVENT_NOT_FOUND",
    "message": "El evento solicitado no existe."
  }
}

Los endpoints implementados actualmente utilizan el formato estándar de error HTTP de FastAPI en determinados casos.

Ejemplo:

{
  "detail": "Credenciales invalidas"
}

La estrategia de errores se uniformizará progresivamente conforme se implementen los demás endpoints del MVP.

8. Documentación OpenAPI

FastAPI publica automáticamente la documentación interactiva y el esquema OpenAPI de SmartSafe.

8.1. Interfaces disponibles

Con el backend ejecutándose localmente en el puerto 8000:

Recurso

URL

Propósito

Swagger UI

http://127.0.0.1:8000/docs

Explorar y probar los endpoints mediante una interfaz interactiva

ReDoc

http://127.0.0.1:8000/redoc

Consultar la documentación de referencia de la API

Esquema OpenAPI

http://127.0.0.1:8000/openapi.json

Obtener la especificación de la API en formato JSON

8.2. Configuración actual

La aplicación declara el título SmartSafe API, la versión 0.1.0 y una descripción de los módulos SmartReport y SmartSOS.

Asimismo, incluye la advertencia de que SmartSOS es un prototipo académico y no reemplaza los servicios oficiales de emergencia.

Actualmente se encuentran implementados y documentados los siguientes endpoints:

GET /health
POST /api/v1/auth/login
POST /api/v1/reports

El endpoint /health permite verificar que el servicio se encuentra disponible.

El endpoint /api/v1/auth/login permite autenticar usuarios, validar credenciales, identificar los roles CITIZEN y OPERATOR y emitir un token JWT de acceso.

El endpoint /api/v1/reports permite registrar incidencias urbanas no urgentes asociadas al usuario autenticado, incluyendo categoría, descripción, ubicación y fotografía opcional.

Los nuevos reportes se crean con el estado inicial:

REPORTED

8.3. Estado de implementación

Actualmente se encuentran implementadas las siguientes operaciones:

verificación del estado del backend mediante GET /health;

autenticación de usuarios mediante POST /api/v1/auth/login;

registro de incidencias SmartReport mediante POST /api/v1/reports.

Las demás rutas de SmartReport, SmartSOS y UrbanEvent descritas en este documento constituyen el contrato de API previsto para el MVP y se incorporarán progresivamente conforme sean implementadas.

Por tanto, únicamente los endpoints señalados explícitamente como implementados deben considerarse actualmente disponibles en la API.

8.4. Criterios para nuevos endpoints

Cada endpoint que se implemente deberá documentar, según corresponda:

propósito y descripción de la operación;

parámetros de ruta y consulta;

cuerpo de solicitud y esquema de respuesta;

códigos HTTP de éxito y error;

ejemplos representativos;

requisitos de autenticación y autorización.

La documentación deberá mantenerse sincronizada con el comportamiento real de la API.