A continuación, se presenta una tabla que incluye únicamente los endpoints necesarios para gestionar los Casos de Uso CU01, CU02 y CU07, junto con sus métodos, descripciones y los roles que los utilizan.

| **Método** | **Endpoint**              | **Descripción**                                                                                       | **Roles que Usan**                      |
|------------|---------------------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------|
| **Autenticación**                                                                                                                               |
| POST       | `/token`                  | **Login**: Autentica al usuario y proporciona un token de acceso.                                     | Administrador, Fotógrafo, Cliente       |
| **Galerías**                                                                                                                                    |
| GET        | `/galleries/`             | **Ver Galerías Asignadas (CU01)**: Lista todas las galerías asignadas al cliente autenticado.        | Cliente                                 |
| GET        | `/galleries/{id}/photos`  | **Ver Fotografías de una Galería (CU01)**: Obtiene las fotografías de una galería específica asignada.| Cliente                                 |
| POST       | `/galleries/`             | **Crear Galería (CU07)**: Crea una nueva galería de fotografías.                                     | Administrador, Fotógrafo                |
| POST       | `/galleries/{id}/assign`  | **Asignar Galería a Cliente (CU07)**: Asigna una galería específica a un cliente determinado.        | Administrador, Fotógrafo                |
| **Selección de Fotografías**                                                                                                                     |
| POST       | `/photos/{id}/favorite`   | **Marcar como Favorito (CU02)**: Marca una fotografía específica como favorita para selección de álbum.| Cliente                                 |
| DELETE     | `/photos/{id}/favorite`   | **Deseleccionar Favorito (CU02)**: Remueve la marca de favorito de una fotografía específica.         | Cliente                                 |
| GET        | `/users/me/favorites`     | **Obtener Favoritos del Usuario (CU02)**: Lista todas las fotografías marcadas como favoritas por el usuario.| Cliente                           |
| **Comentarios**                                                                                                                                 |
| POST       | `/photos/{id}/comments`   | **Añadir Comentario (CU02)**: Añade un comentario a una fotografía específica seleccionada.           | Cliente                                 |

### **Descripción de Endpoints Incluidos**

#### **Autenticación**
- **POST `/token`**: Permite a los usuarios autenticarse en el sistema y obtener un token de acceso necesario para interactuar con otros endpoints.

#### **Galerías**
- **GET `/galleries/`** (*CU01*): Permite a los clientes ver todas las galerías que les han sido asignadas.
- **GET `/galleries/{id}/photos`** (*CU01*): Permite a los clientes visualizar las fotografías contenidas en una galería específica.
- **POST `/galleries/`** (*CU07*): Permite a fotógrafos y administradores crear nuevas galerías para organizar las fotografías.
- **POST `/galleries/{id}/assign`** (*CU07*): Permite a fotógrafos y administradores asignar una galería existente a un cliente específico.

#### **Selección de Fotografías**
- **POST `/photos/{id}/favorite`** (*CU02*): Permite a los clientes marcar fotografías como favoritas para su inclusión en un álbum.
- **DELETE `/photos/{id}/favorite`** (*CU02*): Permite a los clientes desmarcar fotografías previamente marcadas como favoritas.
- **GET `/users/me/favorites`** (*CU02*): Permite a los clientes obtener una lista de todas las fotografías que han marcado como favoritas.

#### **Comentarios**
- **POST `/photos/{id}/comments`** (*CU02*): Permite a los clientes añadir comentarios a fotografías específicas seleccionadas para su álbum.

### **Roles y Acceso**

- **Administrador**:
  - **Acceso Completo**: Puede utilizar todos los endpoints incluidos, permitiendo gestionar galerías, asignarlas a clientes y acceder a la información de favoritos y comentarios.

- **Fotógrafo**:
  - **Crear y Asignar Galerías**: Puede crear nuevas galerías y asignarlas a clientes mediante los endpoints `/galleries/` y `/galleries/{id}/assign`.
  - **Acceso Administrativo**: Similar al administrador en lo que respecta a la gestión de galerías.

- **Cliente**:
  - **Ver y Seleccionar Galerías y Fotografías (CU01 & CU02)**: Puede visualizar sus galerías asignadas, ver las fotografías dentro de ellas, marcar y desmarcar favoritas, y añadir comentarios a las fotografías seleccionadas.

