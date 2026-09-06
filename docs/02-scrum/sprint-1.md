\## Equipo Scrum



| Rol | Integrante |

|---|---|

| Product Owner | William |

| Scrum Master | Rony |

| Developer | Harry  |

| Developer | Rony   |

| Developer | Lida   |

| Developer | William |



\# SmartSafe

\## Sprint 1 - Fundación técnica



\## 1. Información general



\*\*Sprint:\*\* 1  

\*\*Nombre:\*\* Fundación técnica  

\*\*Duración:\*\* 1 semana  

\*\*Estado:\*\* Planificado  



\## 2. Objetivo del Sprint



Construir la base técnica y de calidad de SmartSafe, dejando disponible una primera versión ejecutable con frontend, backend, base de datos, autenticación, documentación de la API, pruebas automatizadas e integración continua.



Al finalizar el Sprint, el equipo deberá disponer de una infraestructura mínima sobre la cual puedan desarrollarse posteriormente SmartReport y SmartSOS.



\---



\## 3. Sprint Goal



> Disponer de una versión base ejecutable de SmartSafe que permita autenticar usuarios y que cuente con una arquitectura inicial, persistencia de datos, API documentada, pruebas automatizadas y pipeline de integración continua.



\---



\## 4. Historias de usuario incluidas



\### US-01 - Iniciar sesión



Como usuario quiero iniciar sesión para acceder a las funcionalidades correspondientes a mi rol.



\*\*Prioridad:\*\* Alta



\### US-14 - Implementar pruebas automatizadas



Como equipo de desarrollo queremos ejecutar pruebas automatizadas para detectar errores y regresiones.



\*\*Prioridad:\*\* Alta



\### US-15 - Configurar integración continua



Como equipo de desarrollo queremos ejecutar automáticamente las validaciones del proyecto para evitar integrar código defectuoso.



\*\*Prioridad:\*\* Alta



\---



\# 5. Tareas técnicas



\## TECH-01 - Configurar backend FastAPI



Configurar el proyecto backend utilizando FastAPI y establecer la estructura modular inicial.



\## TECH-02 - Configurar frontend React + TypeScript



Inicializar la aplicación frontend utilizando React y TypeScript.



\## TECH-03 - Configurar PostgreSQL



Configurar PostgreSQL como sistema de gestión de base de datos.



\## TECH-04 - Configurar Docker Compose



Permitir la ejecución reproducible de los componentes principales mediante Docker Compose.



\## TECH-05 - Diseñar modelo inicial de datos



Definir las entidades iniciales:



\- User

\- EventType

\- EventRecord



\## TECH-06 - Configurar Swagger / OpenAPI



Documentar automáticamente los endpoints REST mediante OpenAPI.



\## TECH-07 - Configurar estructura de pruebas



Configurar pytest, pytest-cov, Vitest y las carpetas necesarias para pruebas automatizadas.



\---



\# 6. Sprint Backlog



| ID | Elemento | Tipo | Prioridad |

|---|---|---|---|

| US-01 | Iniciar sesión | Historia | Alta |

| US-14 | Implementar pruebas automatizadas | Historia | Alta |

| US-15 | Configurar integración continua | Historia | Alta |

| TECH-01 | Configurar backend FastAPI | Técnica | Alta |

| TECH-02 | Configurar frontend React + TypeScript | Técnica | Alta |

| TECH-03 | Configurar PostgreSQL | Técnica | Alta |

| TECH-04 | Configurar Docker Compose | Técnica | Alta |

| TECH-05 | Diseñar modelo inicial de datos | Técnica | Alta |

| TECH-06 | Configurar Swagger / OpenAPI | Técnica | Alta |

| TECH-07 | Configurar estructura de pruebas | Técnica | Alta |



\---



\# 7. Entregables esperados



Al finalizar el Sprint deberán existir:



\- repositorio GitHub estructurado;

\- frontend React funcionando;

\- backend FastAPI funcionando;

\- PostgreSQL disponible;

\- modelo inicial de datos;

\- autenticación básica;

\- roles CITIZEN y OPERATOR;

\- documentación Swagger accesible;

\- infraestructura de pruebas;

\- primeras pruebas automatizadas;

\- GitHub Actions configurado;

\- Docker Compose funcional.



\---



\# 8. Definition of Done



Un elemento será considerado terminado cuando:



\- cumple sus criterios de aceptación;

\- el código está implementado;

\- utiliza nombres reveladores;

\- posee pruebas cuando corresponde;

\- las pruebas automatizadas son exitosas;

\- la API está documentada cuando corresponde;

\- existe Pull Request;

\- se realizó Code Review;

\- GitHub Actions finalizó correctamente;

\- la documentación fue actualizada.



\---



\# 9. Estrategia de trabajo



Cada elemento seguirá el flujo:



Product Backlog

→ Ready

→ In Progress

→ Code Review

→ Testing

→ Done



Para cada funcionalidad se utilizará:



Issue

→ Branch

→ Commits

→ Pull Request

→ Tests

→ Code Review

→ Merge



\---



\# 10. Estrategia de ramas



Rama de integración:



develop



Ramas de trabajo sugeridas:



feature/backend-foundation

feature/frontend-foundation

feature/authentication

feature/database-foundation

test/testing-foundation

chore/docker-compose

chore/github-actions



Las ramas deberán crearse desde develop.



\---



\# 11. Riesgos iniciales



| Riesgo | Acción |

|---|---|

| Integración tardía entre frontend y backend | Definir API desde el inicio |

| Diferencias en entornos de desarrollo | Utilizar Docker |

| Cambios incompatibles en base de datos | Documentar el modelo previamente |

| Código defectuoso integrado | Pull Requests + GitHub Actions |

| Cobertura insuficiente | Implementar pruebas desde el primer Sprint |

| Sobrecarga de funcionalidades | Mantener estrictamente el alcance MVP |



\---



\# 12. Sprint Review



Esta sección será completada al finalizar el Sprint.



\## Incremento entregado



Pendiente.



\## Funcionalidades demostradas



Pendiente.



\## Elementos no terminados



Pendiente.



\## Observaciones



Pendiente.



\---



\# 13. Sprint Retrospective



Esta sección será completada al finalizar el Sprint.



\### ¿Qué funcionó bien?



Pendiente.



\### ¿Qué dificultades encontramos?



Pendiente.



\### ¿Qué debemos mejorar?



Pendiente.



\### Acción de mejora para el próximo Sprint



Pendiente.

