# SmartSafe
## Especificación de Requisitos del MVP

## 1. Propósito

Este documento define los requisitos mínimos necesarios para desarrollar el MVP de SmartSafe durante un periodo aproximado de cuatro semanas.

El alcance ha sido deliberadamente reducido para priorizar un flujo funcional completo, pruebas automatizadas, integración mediante API REST y calidad de software.

---

# 2. Requisitos funcionales de SmartReport

## RF-SR-01. Registrar incidencia

El ciudadano deberá poder registrar una incidencia urbana proporcionando:

- categoría;
- descripción;
- fotografía;
- ubicación.

El sistema deberá registrar automáticamente:

- identificador;
- usuario;
- fecha y hora;
- estado inicial.

## RF-SR-02. Seleccionar categoría

El ciudadano deberá poder seleccionar una de las siguientes categorías:

- Bache
- Residuos acumulados
- Alumbrado público
- Fuga de agua

## RF-SR-03. Consultar reportes

El ciudadano deberá poder consultar los reportes que haya registrado y visualizar su estado actual.

## RF-SR-04. Gestionar estado

El operador deberá poder modificar el estado de un reporte.

Estados permitidos:

- REPORTED
- IN_PROGRESS
- RESOLVED

## RF-SR-05. Visualizar reportes en mapa

El operador deberá poder visualizar la ubicación de los reportes sobre un mapa.

---

# 3. Requisitos funcionales de SmartSOS

## RF-SS-01. Activar alerta SOS

El ciudadano deberá poder generar una alerta mediante un botón SOS.

## RF-SS-02. Seleccionar tipo de emergencia

El ciudadano deberá seleccionar una de las siguientes categorías:

- Emergencia médica
- Accidente
- Incendio
- Seguridad personal

## RF-SS-03. Registrar ubicación

El sistema deberá obtener la ubicación disponible del dispositivo al generar la alerta.

## RF-SS-04. Visualizar alerta

El operador deberá poder consultar las alertas registradas incluyendo:

- tipo;
- usuario;
- ubicación;
- fecha y hora;
- estado.

## RF-SS-05. Gestionar estado

El operador deberá poder modificar el estado de una emergencia.

Estados permitidos:

- ACTIVE
- IN_PROGRESS
- FINISHED

---

# 4. Requisitos comunes

## RF-COM-01. Autenticación

El sistema deberá permitir autenticación para ciudadanos y operadores.

## RF-COM-02. Roles

El sistema deberá diferenciar como mínimo:

- CITIZEN
- OPERATOR

## RF-COM-03. UrbanEvent

SmartReport y SmartSOS deberán poder representar sus registros mediante un contrato común denominado UrbanEvent.

## RF-COM-04. API REST

SmartSafe deberá proporcionar una API REST para crear, consultar, actualizar y eliminar recursos.

## RF-COM-05. Centro de control

El operador deberá disponer de un centro de control para consultar reportes y emergencias.

## RF-COM-06. Mapa integrado

El sistema deberá permitir visualizar eventos SmartReport y SmartSOS en un mismo mapa.

---

# 5. Requisitos no funcionales

## RNF-01. Usabilidad

Las principales funcionalidades deberán ser comprensibles para un usuario no técnico.

## RNF-02. Seguridad

Las contraseñas no deberán almacenarse en texto plano.

Las funcionalidades protegidas deberán requerir autenticación y autorización.

## RNF-03. Interoperabilidad

La API deberá utilizar HTTP/HTTPS, REST y JSON.

## RNF-04. Mantenibilidad

El código deberá organizarse por módulos y capas, utilizando nombres reveladores y responsabilidades claramente definidas.

## RNF-05. Pruebas

El sistema deberá contar con pruebas automatizadas.

El objetivo del proyecto será alcanzar una cobertura superior al 90 %.

## RNF-06. Integración continua

Los Pull Requests deberán ejecutar automáticamente pruebas y validaciones mediante GitHub Actions.

## RNF-07. Documentación

La API deberá documentarse mediante OpenAPI / Swagger.

La documentación técnica deberá mantenerse dentro del repositorio GitHub.

## RNF-08. Portabilidad

El proyecto deberá poder ejecutarse mediante Docker y Docker Compose.

## RNF-09. Rendimiento

Las operaciones principales deberán ofrecer tiempos de respuesta adecuados para el MVP.

La optimización solo se realizará cuando una medición indique que un requisito de rendimiento no se cumple.

---

# 6. Reglas de negocio

## RN-01

Todo reporte SmartReport será creado inicialmente con estado:

REPORTED

## RN-02

Toda alerta SmartSOS será creada inicialmente con estado:

ACTIVE

## RN-03

Un ciudadano solamente podrá consultar sus propios reportes y alertas.

## RN-04

Solo un operador podrá gestionar estados de eventos.

## RN-05

SmartReport solo admitirá las categorías definidas para SmartReport.

## RN-06

SmartSOS solo admitirá las categorías definidas para SmartSOS.

## RN-07

Las transiciones de estado deberán respetar el flujo definido.

SmartReport:

REPORTED -> IN_PROGRESS -> RESOLVED

SmartSOS:

ACTIVE -> IN_PROGRESS -> FINISHED

## RN-08

SmartSOS deberá mostrar la advertencia:

"SmartSOS es un prototipo académico y no reemplaza los servicios oficiales de emergencia."

---

# 7. Restricciones

- Duración aproximada: cuatro semanas.
- Equipo: cuatro integrantes.
- No se implementarán microservicios en el MVP.
- No se utilizará IA en la primera versión.
- Se utilizará GitHub para todo el control de versiones.
- La API REST es obligatoria.
- La documentación Swagger es obligatoria.
- Las pruebas automatizadas son obligatorias.
