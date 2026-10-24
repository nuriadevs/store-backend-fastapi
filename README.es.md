# Evoltronic Store (Backend)

📘 Disponible también en [Inglés](./README.md)

Esta aplicación fue desarrollada con FastAPI. Es el backend de una tienda online de productos electrónicos y ofrece operaciones CRUD, autenticación y registro de usuarios, verificación de correo, recuperación de contraseña y gestión de pedidos.

## Entorno 🛠️

- Python 3.13
- [FastAPI](https://fastapi.tiangolo.com/) 0.115.8
- [PostgreSQL](https://www.postgresql.org/) 16.8
- [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.38 + Alembic (migraciones)
- [Pydantic](https://docs.pydantic.dev/) 2.10.6
- Docker 27.3.1
- [Mailpit](https://mailpit.axllent.org/) (pruebas de correo)
- API
- Tests (Pytest)
- CRUD
- Postman o Bruno
- Visual Studio Code

## Características ✨

- **Autenticación de usuarios**: registro, inicio de sesión, refresco de token, verificación de correo y recuperación de contraseña.
- **Gestión de productos**: los administradores pueden añadir, editar y eliminar productos.
- **Gestión de categorías**: los productos se organizan en categorías.
- **Gestión de pedidos**: los clientes pueden hacer pedidos y consultar sus detalles.
- **Perfiles de usuario**: los clientes pueden crear y actualizar su perfil y su dirección.
- **Envío de correos con Mailpit**: correos de registro y confirmación.

## Instalación ⚙️

1.  Clona el repositorio en tu máquina local: `git clone https://github.com/nuriadevs/store-backend-fastapi.git`.
2.  Entra en la carpeta del proyecto con `cd store-backend-fastapi`.
3.  Crea tu propio archivo `.env` con las variables de entorno.
4.  Construye y arranca los contenedores de Docker con `docker-compose up --build`.
5.  Ejecuta las migraciones (esto también crea el usuario administrador):

    `docker exec -it fastapi_app alembic upgrade head`

6.  Abre la documentación interactiva de la API en tu navegador en [http://localhost:8000/docs](http://localhost:8000/docs).
7.  Abre Mailpit para leer los correos que envía la aplicación en [http://localhost:8025](http://localhost:8025/).

> ⚠️ Requisitos previos: [Docker](https://www.docker.com/) y Docker Compose. Python y PostgreSQL solo hacen falta si ejecutas el proyecto fuera de Docker.

## 📡 Endpoints de la API

La autenticación usa OAuth2 con token Bearer. La columna **Acceso** indica quién puede usar cada ruta: `Público` (sin token), `Auth` (cualquier usuario autenticado) o `Admin` (solo administradores).

| Endpoint                   | Método | Ruta                              | Acceso  |
| -------------------------- | ------ | --------------------------------- | ------- |
| **Autenticación**          |        |                                   |         |
| Login                      | POST   | `auth/login`                      | Público |
| Refrescar token            | POST   | `auth/refresh`                    | Público |
| Olvidé mi contraseña       | POST   | `auth/forgot-password`            | Público |
| Restablecer contraseña     | PUT    | `auth/reset-password`             | Público |
| **Usuarios**               |        |                                   |         |
| Registro                   | POST   | `users`                           | Público |
| Verificar cuenta           | POST   | `users/verify`                    | Público |
| Usuario autenticado        | GET    | `users/me`                        | Auth    |
| Mostrar                    | GET    | `users/{user_id}`                 | Admin   |
| Actualizar username        | PUT    | `users/{user_id}`                 | Auth    |
| Eliminar                   | DELETE | `users/{user_id}`                 | Admin   |
| **Perfil de usuario**      |        |                                   |         |
| Crear                      | POST   | `users/profile/create`            | Auth    |
| Mi perfil                  | GET    | `users/profile/me`                | Auth    |
| Actualizar                 | PUT    | `users/profile/update`            | Auth    |
| Actualizar dirección       | PATCH  | `users/profile/{user_id}/address` | Auth    |
| Mostrar                    | GET    | `users/profile/{user_id}`         | Admin   |
| Eliminar (borrado lógico)  | DELETE | `users/profile/{user_id}`         | Admin   |
| **Productos**              |        |                                   |         |
| Listar                     | GET    | `products/products/`              | Público |
| Mostrar                    | GET    | `products/{product_id}`           | Público |
| Crear                      | POST   | `products/create`                 | Admin   |
| Actualizar                 | PUT    | `products/products/{product_id}`  | Admin   |
| Eliminar                   | DELETE | `products/products/{product_id}`  | Admin   |
| **Categorías**             |        |                                   |         |
| Listar                     | GET    | `categories/categories/`          | Auth    |
| Mostrar                    | GET    | `categories/{category_id}`        | Auth    |
| Crear                      | POST   | `categories/create`               | Admin   |
| Actualizar                 | PATCH  | `categories/{category_id}`        | Admin   |
| Eliminar                   | DELETE | `categories/{category_id}`        | Admin   |
| **Pedidos**                |        |                                   |         |
| Crear                      | POST   | `orders/create/`                  | Auth    |
| Mis pedidos                | GET    | `orders/me`                       | Auth    |
| Listar                     | GET    | `orders/orders/`                  | Admin   |
| Mostrar                    | GET    | `orders/{order_id}`               | Auth    |
| Actualizar estado          | PATCH  | `orders/{order_id}`               | Admin   |
| Eliminar (solo pendientes) | DELETE | `orders/{order_id}`               | Admin   |
| Cancelar (borrado lógico)  | PATCH  | `orders/{order_id}/delete`        | Auth    |
| **Público**                |        |                                   |         |
| Índice                     | GET    | `index/`                          | Público |
| Raíz                       | GET    | `/`                               | Público |

## Uso 🚀

### Postman o Bruno

Si quieres explorar y probar la API, importa el archivo `api_docs/evoltronic.json` en Postman o Bruno. También puedes probar todas las rutas desde la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

Inicia sesión con el usuario **admin** que crea la migración.

### Iniciar sesión

La ruta de login usa un formulario (`application/x-www-form-urlencoded`), no JSON:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=Lolo&password=PassHashed_123!"

```

La respuesta contiene `access_token`, `refresh_token`, `expires_in` y `token_type`. Usa el token en las rutas protegidas:

```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer <access_token>"

```

Para obtener un nuevo token de acceso, envía el refresh token en la cabecera `refresh-token` a `POST /auth/refresh`.

### Registrar un nuevo usuario (cliente)

```json
POST /users
{
  "username": "Lolo",
  "email": "lolo@example.com",
  "password": "PassHashed_123!"
}

```

### Crear un nuevo producto (admin)

```json
POST /products/create
{
  "name": "Laptop",
  "description": "Laptop Samsung ultra.",
  "price": 800.50,
  "stock": 10,
  "category_id": 1
}

```

### Crear un nuevo pedido (cliente)

```json
POST /orders/create/
{
  "user_id": 1,
  "products": [
    { "product_id": 1, "quantity": 2 }
  ]
}

```

## Tests 🧪

```bash
docker-compose exec app pytest

```

## Variables de entorno

Crea tu propio archivo `.env` en la raíz del proyecto con las variables de la base de datos, las claves de seguridad y el servidor de correo (Mailpit).

## Demo en Postman :man_astronaut:

<img src="./media/1.png" alt="postman" width="600" />

## Enlaces

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Pydantic](https://docs.pydantic.dev/)
- [Docker](https://www.docker.com/)
- [Mailpit](https://mailpit.axllent.org/)
- [Bruno](https://www.usebruno.com/)
- [Postman](https://www.postman.com/)

## Contacto

Si tienes alguna pregunta, escríbeme un correo.

✉️ [Email](mailto:nuriadevs@gmail.com)

## Resumen

- Ejecuta la migración para probar la aplicación con un usuario administrador.
- No olvides crear tu propio archivo `.env` con las variables.
- La ruta de login espera datos de formulario, no JSON.
- Los correos (verificación y recuperación de contraseña) se pueden leer en Mailpit en `http://localhost:8025`.
- Este proyecto está en construcción... se puede mejorar.

## Gracias 🍀

Muchas gracias por leer este proyecto.
