# Autenticación

## **Visión General**

La autenticación es un componente fundamental de la aplicación **FotoFlow**, que garantiza que solo los usuarios autorizados puedan acceder y gestionar los recursos del sistema. Este módulo maneja el proceso de inicio de sesión, la generación y validación de tokens de acceso, y la asignación de roles que determinan los permisos de cada usuario dentro de la plataforma.

## **Flujo de Autenticación**

1. **Inicio de Sesión:**
   - El usuario (Administrador, Fotógrafo o Cliente) envía una solicitud de inicio de sesión proporcionando sus credenciales (nombre de usuario y contraseña) al endpoint `/token`.
   
2. **Generación de Token:**
   - El sistema valida las credenciales del usuario.
   - Si las credenciales son correctas, el sistema genera un **Token JWT** (JSON Web Token) que contiene información sobre el usuario y sus roles.
   
3. **Uso del Token:**
   - El cliente (aplicación frontend) almacena el token, usualmente en el almacenamiento local del navegador.
   - Para acceder a recursos protegidos, el cliente incluye este token en el encabezado de autorización de sus solicitudes (`Authorization: Bearer <token>`).
   
4. **Validación del Token:**
   - El servidor verifica la validez del token en cada solicitud protegida.
   - Si el token es válido y no ha expirado, el servidor procesa la solicitud.
   - Si el token es inválido o ha expirado, el servidor responde con un error de autenticación.

## **Endpoints de Autenticación**

### **POST `/token`**

- **Descripción:** Autentica al usuario y proporciona un token de acceso.
- **Roles que Usan:** Administrador, Fotógrafo, Cliente
- **Request:**
  - **Headers:**
    - `Content-Type: application/json`
  - **Body:**
    ```json
    {
      "username": "usuario_ejemplo",
      "password": "contraseña_segura"
    }
    ```
- **Response:**
  - **Éxito (200 OK):**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
      "token_type": "bearer",
      "expires_in": 3600
    }
    ```
  - **Error (401 Unauthorized):**
    ```json
    {
      "detail": "Credenciales inválidas."
    }
    ```

## **Gestión de Tokens**

- **Formato del Token:** JWT (JSON Web Token)
- **Contenido del Token:**
  - **Header:** Información sobre el algoritmo de cifrado.
  - **Payload:** Datos del usuario, incluyendo su ID, nombre de usuario y roles.
  - **Signature:** Firma criptográfica que asegura la integridad del token.
  
- **Expiración del Token:** Los tokens tienen una duración limitada (por ejemplo, 1 hora) tras la cual deben ser renovados mediante un nuevo inicio de sesión.

- **Renovación del Token:** Actualmente, la renovación se realiza solicitando un nuevo token a través del endpoint `/token` con las credenciales del usuario.

## **Roles y Permisos**

### **Administrador**

- **Descripción:** Tiene acceso completo a todos los recursos y funcionalidades de la aplicación.
- **Permisos:**
  - Gestionar usuarios (crear, actualizar, eliminar).
  - Gestionar sesiones fotográficas y galerías.
  - Asignar galerías a clientes.
  - Acceder y gestionar favoritos y comentarios de todos los usuarios.

### **Fotógrafo**

- **Descripción:** Puede gestionar sus propias sesiones, galerías y fotografías, y asignarlas a sus clientes.
- **Permisos:**
  - Crear, actualizar y eliminar sesiones fotográficas.
  - Crear y gestionar galerías.
  - Asignar galerías a clientes específicos.
  - Acceder y gestionar favoritos y comentarios dentro de sus propias galerías asignadas.

### **Cliente**

- **Descripción:** Puede acceder únicamente a las galerías que le han sido asignadas y gestionar sus propias selecciones.
- **Permisos:**
  - Ver galería asignada y las fotografías dentro de ella.
  - Marcar y desmarcar fotografías como favoritas.
  - Añadir comentarios a las fotografías seleccionadas.
  - Ver una lista consolidada de sus fotografías favoritas.

## **Consideraciones de Seguridad**

- **Almacenamiento Seguro del Token:**
  - Es recomendable almacenar el token en `httpOnly` cookies para protegerlo contra ataques de Cross-Site Scripting (XSS).
  - Alternativamente, si se almacena en el almacenamiento local, se deben implementar medidas adicionales para protegerlo.

- **Protección Contra CSRF:**
  - Implementar tokens CSRF si los tokens se almacenan en cookies.
  
- **Cifrado de Contraseñas:**
  - Las contraseñas de los usuarios deben almacenarse de manera segura utilizando algoritmos de hashing robustos, como bcrypt.

- **Validación y Revocación de Tokens:**
  - Implementar mecanismos para revocar tokens en caso de sospecha de compromiso.
  - Monitorear y registrar accesos para detectar actividades inusuales.

- **HTTPS:**
  - Todas las comunicaciones deben realizarse sobre HTTPS para asegurar la transmisión segura de datos.

## **Ejemplo de Flujo de Autenticación**

1. **Inicio de Sesión:**
   - Un **Cliente** abre la aplicación y navega a la página de inicio de sesión.
   - Ingresa su nombre de usuario y contraseña y envía el formulario.
   
2. **Solicitud al Endpoint `/token`:**
   - La aplicación envía una solicitud POST al endpoint `/token` con las credenciales del cliente.
   
3. **Generación y Respuesta del Token:**
   - El servidor valida las credenciales.
   - Si son correctas, genera un JWT que incluye los roles del cliente y devuelve el token en la respuesta.
   
4. **Almacenamiento del Token:**
   - La aplicación almacena el token de manera segura.
   
5. **Acceso a Recursos Protegidos:**
   - El cliente navega a "Mis Galerías" y la aplicación envía una solicitud GET a `/galleries/` incluyendo el token en el encabezado de autorización.
   
6. **Validación del Token:**
   - El servidor verifica la validez del token y, si es válido, devuelve la lista de galerías asignadas al cliente.
   
7. **Renovación del Token:**
   - Si el cliente intenta acceder a recursos después de que el token ha expirado, debe iniciar sesión nuevamente para obtener un nuevo token.

## **Integración con Otras Módulos**

La autenticación está estrechamente integrada con la gestión de usuarios y permisos. Cada solicitud a los endpoints protegidos utiliza el token para determinar qué recursos y acciones están disponibles para el usuario autenticado, garantizando así una separación adecuada de responsabilidades y el cumplimiento de las políticas de seguridad establecidas.