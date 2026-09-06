# SmartSafe
## Product Backlog

## 1. Objetivo

Este Product Backlog contiene las historias de usuario iniciales necesarias para construir el MVP de SmartSafe.

Cada historia deberá posteriormente asociarse a:

- un GitHub Issue;
- un Sprint;
- una rama;
- uno o más Pull Requests;
- pruebas automatizadas;
- evidencia de ejecución.

---

# 2. Product Backlog

| ID | Historia de usuario | Prioridad | Sprint |
|---|---|---|---|
| US-01 | Como usuario quiero iniciar sesión para acceder a SmartSafe. | Alta | Sprint 1 |
| US-02 | Como ciudadano quiero registrar una incidencia urbana para informar un problema. | Alta | Sprint 2 |
| US-03 | Como ciudadano quiero adjuntar una fotografía para aportar evidencia. | Alta | Sprint 2 |
| US-04 | Como ciudadano quiero registrar la ubicación del evento para indicar dónde ocurrió. | Alta | Sprint 2 |
| US-05 | Como ciudadano quiero consultar mis reportes para conocer su estado. | Alta | Sprint 2 |
| US-06 | Como operador quiero actualizar el estado de un reporte para registrar su atención. | Alta | Sprint 2 |
| US-07 | Como ciudadano quiero activar un botón SOS para generar una alerta de emergencia. | Alta | Sprint 3 |
| US-08 | Como ciudadano quiero seleccionar el tipo de emergencia para informar qué está ocurriendo. | Alta | Sprint 3 |
| US-09 | Como ciudadano quiero registrar mi ubicación junto con la alerta SOS. | Alta | Sprint 3 |
| US-10 | Como operador quiero consultar las emergencias recibidas para gestionar su atención. | Alta | Sprint 3 |
| US-11 | Como operador quiero actualizar el estado de una emergencia para registrar su atención. | Alta | Sprint 3 |
| US-12 | Como operador quiero visualizar reportes y emergencias en un mapa común. | Media | Sprint 4 |
| US-13 | Como sistema externo quiero consultar los eventos mediante API REST para integrar SmartSafe. | Alta | Sprint 4 |
| US-14 | Como equipo quiero ejecutar pruebas automatizadas para verificar la calidad del software. | Alta | Todos |
| US-15 | Como equipo quiero ejecutar automáticamente validaciones en GitHub para detectar errores antes de integrar código. | Alta | Sprint 1 |

---

# 3. Historias de usuario detalladas

## US-01. Iniciar sesión

**Como** usuario  
**quiero** iniciar sesión  
**para** acceder a las funcionalidades correspondientes a mi rol.

### Criterios de aceptación

- El usuario debe proporcionar correo y contraseña.
- Las credenciales válidas deberán permitir acceder al sistema.
- Credenciales inválidas deberán ser rechazadas.
- El sistema deberá identificar el rol CITIZEN u OPERATOR.

### API relacionada

POST /api/v1/auth/login

### Sprint

Sprint 1

---

## US-02. Registrar incidencia

**Como** ciudadano  
**quiero** registrar una incidencia urbana  
**para** informar un problema que requiere atención.

### Criterios de aceptación

- El ciudadano debe estar autenticado.
- Debe seleccionar una categoría válida.
- Debe proporcionar una descripción.
- Debe registrar una ubicación.
- El sistema debe crear el reporte con estado REPORTED.
- La API debe responder 201 Created.

### API relacionada

POST /api/v1/reports

### Sprint

Sprint 2

---

## US-03. Adjuntar fotografía

**Como** ciudadano  
**quiero** adjuntar una fotografía  
**para** proporcionar evidencia del problema reportado.

### Criterios de aceptación

- El formulario debe permitir seleccionar una imagen.
- La referencia de la imagen deberá asociarse al reporte.
- Los formatos permitidos deberán validarse.

### Sprint

Sprint 2

---

## US-04. Registrar ubicación

**Como** ciudadano  
**quiero** registrar la ubicación de una incidencia  
**para** indicar dónde ocurrió.

### Criterios de aceptación

- El sistema debe solicitar permiso de ubicación.
- Debe registrar latitud y longitud.
- Debe permitir visualizar la ubicación en un mapa.

### Sprint

Sprint 2

---

## US-05. Consultar mis reportes

**Como** ciudadano  
**quiero** consultar mis reportes  
**para** conocer su estado.

### Criterios de aceptación

- Solo deberán visualizarse los reportes del usuario autenticado.
- Se mostrará categoría, fecha y estado.
- Se podrá visualizar el detalle.

### API relacionada

GET /api/v1/reports

### Sprint

Sprint 2

---

## US-06. Gestionar estado del reporte

**Como** operador  
**quiero** cambiar el estado de un reporte  
**para** registrar su proceso de atención.

### Estados permitidos

REPORTED -> IN_PROGRESS -> RESOLVED

### Criterios de aceptación

- Solo OPERATOR puede actualizar estados.
- No deben permitirse transiciones inválidas.
- La actualización deberá persistirse.

### API relacionada

PUT /api/v1/reports/{id}

### Sprint

Sprint 2

---

## US-07. Activar botón SOS

**Como** ciudadano  
**quiero** activar un botón SOS  
**para** generar una alerta de emergencia.

### Criterios de aceptación

- El botón SOS debe estar claramente visible.
- El ciudadano deberá seleccionar un tipo de emergencia.
- La alerta deberá crearse con estado ACTIVE.

### API relacionada

POST /api/v1/emergencies

### Sprint

Sprint 3

---

## US-08. Seleccionar tipo de emergencia

**Como** ciudadano  
**quiero** indicar el tipo de emergencia  
**para** proporcionar información sobre la situación.

### Tipos iniciales

- Emergencia médica
- Accidente
- Incendio
- Seguridad personal

### Sprint

Sprint 3

---

## US-09. Registrar ubicación SOS

**Como** ciudadano  
**quiero** enviar mi ubicación junto con la alerta  
**para** indicar dónde ocurre la emergencia.

### Criterios de aceptación

- La aplicación debe solicitar ubicación.
- La alerta debe guardar latitud y longitud.
- El operador podrá visualizarla en un mapa.

### Sprint

Sprint 3

---

## US-10. Consultar emergencias

**Como** operador  
**quiero** visualizar las emergencias registradas  
**para** gestionar su atención.

### API relacionada

GET /api/v1/emergencies

### Sprint

Sprint 3

---

## US-11. Gestionar emergencia

**Como** operador  
**quiero** modificar el estado de una emergencia  
**para** registrar su proceso de atención.

### Estados

ACTIVE -> IN_PROGRESS -> FINISHED

### API relacionada

PUT /api/v1/emergencies/{id}

### Sprint

Sprint 3

---

## US-12. Visualizar eventos en mapa

**Como** operador  
**quiero** visualizar reportes y emergencias en un mismo mapa  
**para** supervisar los eventos urbanos.

### Criterios de aceptación

- El mapa deberá mostrar eventos SmartReport.
- El mapa deberá mostrar eventos SmartSOS.
- Los dos tipos deberán poder distinguirse visualmente.

### Sprint

Sprint 4

---

## US-13. Consultar UrbanEvents mediante API

**Como** sistema externo  
**quiero** consultar los eventos urbanos mediante una API REST  
**para** integrar SmartSafe con otros sistemas Smart City.

### API

GET /api/v1/events

### Criterios de aceptación

- Debe devolver SmartReport y SmartSOS.
- Debe devolver JSON.
- Debe permitir filtros básicos.

### Sprint

Sprint 4

---

## US-14. Pruebas automatizadas

**Como** equipo de desarrollo  
**quiero** ejecutar pruebas automatizadas  
**para** detectar regresiones y errores.

### Criterios de aceptación

- Las funcionalidades críticas deberán poseer pruebas.
- La cobertura objetivo será superior al 90 %.
- Las pruebas deberán poder ejecutarse localmente y en CI.

---

## US-15. Integración continua

**Como** equipo  
**quiero** ejecutar automáticamente las validaciones del proyecto  
**para** evitar integrar código defectuoso.

### Criterios de aceptación

GitHub Actions deberá ejecutar al menos:

- instalación de dependencias;
- lint;
- pruebas;
- cobertura;
- build.

### Sprint

Sprint 1

---

# 4. Definition of Done

Una historia solamente podrá pasar a Done cuando:

- cumple todos los criterios de aceptación;
- el código está implementado;
- utiliza nombres reveladores;
- posee las pruebas correspondientes;
- las pruebas son exitosas;
- la cobertura cumple los límites acordados;
- la API está documentada cuando corresponde;
- existe Pull Request;
- el Pull Request fue revisado;
- GitHub Actions fue exitoso;
- la documentación fue actualizada.
