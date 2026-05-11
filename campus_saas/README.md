# Campus Online | EduCore MVP 🎓

## Documentación Técnica: Arquitectura de Plataforma, Seguridad y Gestión de Cobranzas

---

### 📖 1. Resumen Ejecutivo de Plataforma

Este repositorio centraliza la planeación estratégica y técnica del núcleo de la plataforma **Campus Online**.  
Como responsables del **Equipo 2 (Platform Team)**, hemos diseñado la infraestructura lógica que garantiza una operación segura, escalable y automatizada, integrando servicios críticos de identidad y finanzas.

---

### 👨‍💻 2. Alcance del Equipo de Plataforma (Equipo 2)

Nuestra gestión se centra en la definición de los pilares que sostienen el ecosistema digital:

- **Arquitectura de Identidad:** Diseño del flujo de autenticación federada con Google OAuth 2.0.
- **Gobierno de Datos:** Creación del modelo relacional (Diagrama E-R) para la persistencia de información académica y financiera.
- **Seguridad y Control:** Definición de la matriz de roles y permisos (RBAC).
- **Estandarización de API:** Documentación de contratos de servicio para la integración de los equipos de Frontend y Revenue.

---

### 📂 3. Inventario de Documentación Técnica

La propuesta técnica se detalla en los siguientes archivos (ubicados en la carpeta raíz del proyecto):

#### 🛡️ Seguridad y Autenticación

- `campus-online-auth-documentacion.docx`: Manual detallado sobre la implementación de Passport.js, el flujo de OAuth 2.0 y la lógica de seguridad RBAC.
- `Endpoints.pdf`: Catálogo completo de rutas de API, incluyendo métodos, parámetros de acceso y descripción de funciones.

#### 📊 Base de Datos y Estructura

- `diagrama-E-R.pdf`: Representación visual de la base de datos, detallando entidades como Institutions, Users y Payments.
- `Mockup CSU Campus Online.pdf`: Prototipo visual del panel administrativo para la gestión de usuarios y reportes.

#### 💳 Integraciones Financieras

- `PASARELA DE PAGOS STRIPE.pdf`: Documentación del flujo de cobranza digital, desde la creación de sesiones de checkout hasta la conciliación vía webhooks.

---

### 🔐 4. Matriz de Roles (RBAC)

Se ha definido una estructura de permisos estricta para proteger la integridad de los datos institucionales:

| Rol         | Facultades Principales                           | Acceso Crítico            |
|-------------|--------------------------------------------------|---------------------------|
| SuperAdmin  | Gestión de instituciones y auditoría de pagos.   | `/admin/dashboard`        |
| Alumno      | Consulta de portal personal y ejecución de pagos.| `/alumno/portal`          |

> Todos los endpoints sensibles requieren validación de sesión activa mediante el middleware de seguridad diseñado.

---

### 🔌 5. Contrato de Integración (API Me)

Para facilitar el trabajo del Equipo de Experiencia (Frontend), se ha definido el siguiente contrato de respuesta JSON para la identificación del usuario:

```json
{
  "id": 3,
  "nombre": "KEVIN ALEXIS",
  "email": "usuario@gmail.com",
  "rol": "alumno",
  "institution_id": 1
}
```

###🚀 6. Roadmap de Implementación Sugerido
Basado en la documentación entregada, los pasos para la construcción del MVP son:

Configuración de credenciales en Google Cloud Console.
Implementación de la capa de datos en PostgreSQL siguiendo el modelo E-R.
Despliegue de los middlewares de autenticación y protección de rutas.
Activación de webhooks de Stripe para la conciliación en tiempo real.
###👥 Equipo de Desarrollo
Kibsaim Mejia
Industrial Chemical Engineer & Data Analyst
Encargado de Documentación Técnica del Platform Team
