# Esquema de Base de Datos - FotoFlow

## Descripción General
FotoFlow es un sistema de gestión de fotografías profesionales que permite a los fotógrafos organizar sesiones fotográficas y compartir galerías con sus clientes.

## Tablas

### users
Almacena información de los usuarios del sistema (fotógrafos y clientes).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Identificador único del usuario (PK) |
| name | String | Nombre completo del usuario |
| email | String | Correo electrónico (único) |
| password | String | Contraseña encriptada |
| role | String | Rol del usuario ('photographer' o 'client') |

### sessions
Gestiona las sesiones fotográficas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Identificador único de la sesión (PK) |
| photographer_id | Integer | ID del fotógrafo (FK -> users.id) |
| client_id | Integer | ID del cliente (FK -> users.id) |
| date | DateTime | Fecha de la sesión |
| description | String | Descripción de la sesión |
| status | String | Estado de la sesión |

### galleries
Organiza las fotografías en galerías para compartir con clientes.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Identificador único de la galería (PK) |
| session_id | Integer | ID de la sesión asociada (FK -> sessions.id) |
| name | String | Nombre de la galería |
| description | String | Descripción de la galería |
| created_at | DateTime | Fecha de creación |
| status | String | Estado de la galería |

### photos
Almacena la información de las fotografías.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Identificador único de la foto (PK) |
| gallery_id | Integer | ID de la galería (FK -> galleries.id) |
| filename | String | Nombre del archivo |
| path | String | Ruta de almacenamiento |
| uploaded_at | DateTime | Fecha de carga |
| selected | Boolean | Indica si la foto fue seleccionada por el cliente |
| favorite | Boolean | Indica si la foto fue marcada como favorita |

## Relaciones

1. **users - sessions**
   - Un fotógrafo puede tener múltiples sesiones
   - Un cliente puede tener múltiples sesiones
   - Una sesión pertenece a un fotógrafo y un cliente

2. **sessions - galleries**
   - Una sesión puede tener múltiples galerías
   - Una galería pertenece a una sesión

3. **galleries - photos**
   - Una galería contiene múltiples fotos
   - Una foto pertenece a una galería

## Índices

- users(email) - Único
- sessions(photographer_id, client_id)
- galleries(session_id)
- photos(gallery_id)

## Restricciones

1. El email de usuario debe ser único
2. Las contraseñas se almacenan encriptadas
3. El rol de usuario solo puede ser 'photographer' o 'client'
4. Una foto debe pertenecer a una galería
5. Una galería debe pertenecer a una sesión