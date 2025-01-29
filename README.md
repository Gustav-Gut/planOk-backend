# BackendPlanOk

![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-blue?logo=django)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.14-blue?logo=django)
![License](https://img.shields.io/badge/License-MIT-green)

**BackendPlanOk** es una API backend para la gestión de proyectos inmobiliarios, desarrollada con **Django** y **Django REST Framework (DRF)**. Utiliza una arquitectura por capas siguiendo el patrón **Model-View-Service (MVS)**, lo que asegura una separación clara de responsabilidades, facilitando el mantenimiento y la escalabilidad del proyecto. Además, está dockerizada para simplificar su despliegue y garantizar la consistencia en diferentes entornos.

## Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
  - [1. Clonar el Repositorio](#1-clonar-el-repositorio)
  - [2. Configurar Variables de Entorno](#2-configurar-variables-de-entorno)
  - [3. Construir y Levantar los Contenedores](#3-construir-y-levantar-los-contenedores)
  - [4. Ejecutar Migraciones y Crear Superusuario](#4-ejecutar-migraciones-y-crear-superusuario)
- [Uso](#uso)
  - [Acceder a la API](#acceder-a-la-api)
  - [Documentación de la API](#documentación-de-la-api)
- [Autenticación](#autenticación)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Notas Adicionales](#notas-adicionales)

## Características

- **CRUD Completo** para la gestión de proyectos, unidades y clientes.
- **Autenticación JWT** para proteger los endpoints.
- **Filtrado y Ordenación** avanzada usando `django-filter` y `OrderingFilter`.
- **Documentación Automática** con Swagger UI mediante `drf-spectacular`.
- **Dockerización** para facilitar el despliegue y garantizar la consistencia de entornos.
- **Arquitectura por Capas (MVS)** con patrón Service para una clara separación de responsabilidades.

## Arquitectura

BackendPlanOk está diseñado siguiendo una **arquitectura por capas** basada en el patrón **Model-View-Service (MVS)**. Esta estructura garantiza que cada componente del sistema tenga una única responsabilidad, lo que facilita el mantenimiento, la prueba y la escalabilidad del proyecto.

### Componentes Principales

1. **Modelos (`models.py`)**

   - Definen la estructura de los datos y las relaciones entre las entidades del dominio.
   - Ejemplos: `Project`, `Unit`, `Customer`.

2. **Serializadores (`serializers.py`)**

   - Transforman los modelos en formatos adecuados para la API (como JSON) y validan los datos de entrada.
   - Ejemplos: `ProjectSerializer`, `UnitSerializer`, `CustomerSerializer`.

3. **Servicios (`services/`)**

   - Contienen la lógica de negocio centralizada.
   - Encapsulan operaciones complejas que pueden ser reutilizadas por múltiples vistas.
   - Ejemplos: `ProjectService`, `UnitService`, `CustomerService`.

4. **Vistas (`views.py`)**

   - Controlan la lógica de manejo de solicitudes HTTP.
   - Utilizan los servicios para ejecutar la lógica de negocio.
   - Implementan `ViewSets` para proporcionar acciones CRUD automáticamente.
   - Integran `DjangoFilterBackend` y `OrderingFilter` para filtrar y ordenar resultados.

5. **URLs (`urls.py`)**

   - Rutean las solicitudes a las vistas correspondientes.
   - Incluyen rutas para la documentación de la API generada por Swagger.

6. **Configuración (`settings.py`)**
   - Configura aplicaciones instaladas, bases de datos, autenticación, y otras opciones del proyecto.
   - Define `drf-spectacular` para la generación de esquemas OpenAPI.

### Patrón Service

El **Patrón Service** se utiliza para separar la lógica de negocio de las vistas. Esto permite que las vistas se mantengan delgadas y enfocadas en manejar las solicitudes y respuestas HTTP, mientras que los servicios se encargan de la lógica de negocio compleja.

**Ventajas del Patrón Service:**

- **Reutilización de Código:** Los servicios pueden ser utilizados por múltiples vistas o incluso por otros servicios.
- **Facilidad de Pruebas:** Es más sencillo probar la lógica de negocio aislada en los servicios.
- **Mantenimiento Simplificado:** Cambios en la lógica de negocio afectan únicamente a los servicios, sin necesidad de modificar las vistas.

## Tecnologías

- **Lenguaje**: Python 3.10
- **Framework**: Django 4.2
- **API Framework**: Django REST Framework 3.14
- **Autenticación**: JSON Web Tokens (JWT) con `djangorestframework-simplejwt`
- **Filtrado y Ordenación**: `django-filter`, `OrderingFilter`
- **Documentación de API**: `drf-spectacular` con Swagger UI
- **Base de Datos**: PostgreSQL (en la nube)
- **Contenedores**: Docker, Docker Compose
- **Servidor WSGI**: Gunicorn
- **CORS**: `django-cors-headers`

## Estructura del Proyecto

backendPlanOk/
├── backendPlanOk/
│ ├── projectBackend/ # Proyecto Django (settings, urls, wsgi, etc.)
│ ├── core/ # App principal de Django (models, views, serializers)
│ ├── services/ # Servicios que contienen la lógica de negocio
│ │ ├── **init**.py
│ │ └── project_service.py
│ ├── manage.py
│ ├── requirements.txt
│ ├── Dockerfile
│ ├── .env
│ ├── .gitignore
│ └── db.sqlite3 # Base de datos local (si se usa para desarrollo)
├── docker-compose.yml # Orquestación de servicios Docker
└── README.md # Este archivo

## Requisitos Previos

- **Docker Desktop** instalado en tu sistema.
  - [Descargar Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
- **Este proyecto cuenta en un servicio de PostgreSQL en la nube, de todas formas si usas DEBUG en el .env podras usar una bd local de sqlite3**
- **Git** para clonar el repositorio.

## Documentacion

http://localhost:8000/api/schema/swagger-ui/

**Dentro del proyecto en GIT va un compartido de Insomnia para que puedan probar los endpoints**

## Autenticación

Todos los endpoints de la API están protegidos mediante **JSON Web Tokens (JWT)** para garantizar la seguridad y autenticación de los usuarios. A continuación, se detalla cómo obtener y utilizar los tokens JWT para acceder a los recursos protegidos.

### Obtención de Tokens JWT

Para acceder a los endpoints protegidos, primero debes obtener un par de tokens JWT (`access` y `refresh`) utilizando tus credenciales de usuario.

#### Solicitud para Obtener Tokens

Realiza una solicitud `POST` al endpoint `/api/token/` con tus credenciales: user: gustav pass: 123456
