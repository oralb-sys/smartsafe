# SmartSafe
## Descripción General del Proyecto

## 1. Nombre del proyecto

**SmartSafe: Plataforma para participación ciudadana y atención de emergencias urbanas**

## 2. Descripción

SmartSafe es una aplicación orientada al contexto de una Smart City que permitirá a los ciudadanos registrar incidencias urbanas y generar alertas ante situaciones de emergencia.

El sistema estará compuesto por dos módulos principales:

### SmartReport

Módulo orientado al reporte de incidencias urbanas no urgentes.

Categorías iniciales:

- Bache
- Residuos acumulados
- Alumbrado público
- Fuga de agua

### SmartSOS

Módulo orientado a la generación y gestión de alertas de emergencia.

Categorías iniciales:

- Emergencia médica
- Accidente
- Incendio
- Seguridad personal

SmartReport y SmartSOS forman parte de una única plataforma denominada SmartSafe y compartirán autenticación, usuarios, base de datos, mapas, API e infraestructura.

## 3. Problema

En las ciudades ocurren constantemente incidencias relacionadas con infraestructura, servicios públicos y situaciones de emergencia.

La comunicación de estos acontecimientos suele realizarse mediante canales heterogéneos, dificultando:

- el registro estructurado de la información;
- la identificación precisa de la ubicación;
- el seguimiento del estado del incidente;
- la visualización centralizada;
- la interoperabilidad con otros sistemas urbanos.

SmartSafe busca proporcionar una plataforma común para registrar y gestionar estos acontecimientos como eventos urbanos georreferenciados.

## 4. Objetivo general

Diseñar e implementar un prototipo de plataforma Smart City que permita registrar, gestionar, georreferenciar y consultar incidencias urbanas y alertas de emergencia mediante los módulos SmartReport y SmartSOS, ofreciendo además una API REST para su integración con otros sistemas.

## 5. Objetivos específicos

1. Implementar SmartReport para registrar y gestionar incidencias urbanas.
2. Implementar SmartSOS para generar y gestionar alertas de emergencia.
3. Incorporar geolocalización a los eventos registrados.
4. Implementar un centro de control para visualizar y gestionar eventos.
5. Diseñar una API REST para acceder a las funcionalidades principales.
6. Implementar una representación común denominada UrbanEvent.
7. Utilizar GitHub para gestionar código, Issues, ramas, Pull Requests y releases.
8. Implementar pruebas automatizadas con una cobertura superior al 90 %.
9. Automatizar verificaciones mediante GitHub Actions.
10. Gestionar el desarrollo mediante Scrum e historias de usuario.

## 6. Alcance del MVP

El proyecto será desarrollado durante aproximadamente cuatro semanas por un equipo de cuatro integrantes.

### SmartReport

El ciudadano podrá:

- iniciar sesión;
- registrar una incidencia;
- seleccionar una categoría;
- escribir una descripción;
- adjuntar una fotografía;
- registrar una ubicación;
- consultar sus reportes.

El operador podrá:

- consultar reportes;
- visualizar la ubicación del evento;
- actualizar su estado.

Estados iniciales:

- REPORTED
- IN_PROGRESS
- RESOLVED

### SmartSOS

El ciudadano podrá:

- iniciar sesión;
- activar el botón SOS;
- seleccionar el tipo de emergencia;
- registrar su ubicación;
- enviar una alerta;
- consultar sus alertas.

El operador podrá:

- consultar emergencias;
- visualizar la ubicación;
- actualizar el estado.

Estados iniciales:

- ACTIVE
- IN_PROGRESS
- FINISHED

## 7. Fuera del alcance del MVP

No se desarrollarán inicialmente:

- inteligencia artificial;
- clasificación automática de imágenes;
- detección automática de reportes duplicados;
- machine learning;
- microservicios;
- Kafka;
- RabbitMQ;
- seguimiento GPS continuo;
- Guardian Mode;
- notificaciones push avanzadas;
- integración real con Policía;
- integración real con Bomberos;
- integración real con SAMU;
- mapas de calor;
- analítica predictiva.

Estas funcionalidades serán consideradas como posibles mejoras futuras.

## 8. Actores

### Ciudadano

Puede:

- autenticarse;
- registrar reportes;
- consultar sus reportes;
- activar SmartSOS;
- consultar sus alertas.

### Operador

Puede:

- autenticarse;
- consultar reportes;
- consultar emergencias;
- visualizar eventos en el mapa;
- cambiar estados.

## 9. Enfoque de desarrollo

Se utilizará Scrum con cuatro Sprints de aproximadamente una semana.

- Sprint 1: Fundación técnica.
- Sprint 2: SmartReport.
- Sprint 3: SmartSOS.
- Sprint 4: Integración, calidad y entrega.

## 10. Tecnologías previstas

### Frontend
- React
- TypeScript

### Backend
- FastAPI
- Python

### Base de datos
- PostgreSQL

### Mapas
- Leaflet
- OpenStreetMap

### API
- REST
- JSON
- OpenAPI / Swagger

### Pruebas
- pytest
- pytest-cov
- Vitest
- React Testing Library

### Infraestructura
- Docker
- Docker Compose

### Gestión y CI
- Git
- GitHub
- GitHub Actions
