# 🎓 Campus Online | EduCore MVP
## 📝 Documentación Técnica Maestra: Arquitectura de Plataforma, Seguridad y Gestión de Cobranzas

⚙️ Este repositorio centraliza la planeación estratégica y técnica del núcleo de la plataforma **Campus Online**.

🛡️ Como responsables del **Equipo 2 (Platform Team)**, hemos diseñado la infraestructura lógica y física que garantiza una operación segura, escalable y automatizada.

💳 Integramos los servicios críticos de identidad federada y finanzas digitales para el Proyecto Integrador CSU.

---

## 📋 Índice de Contenidos

* 📖 [1. Descripción General del Módulo de Autenticación](#1-descripción-general-del-módulo-de-autenticación)
* 📂 [2. Estructura del Proyecto y Capas Arquitectónicas](#2-estructura-del-proyecto-y-capas-arquitectónicas)
* 🔄 [3. Flujo de Autenticación e Integración (Google OAuth 2.0)](#3-flujo-de-autenticación-e-integración-google-oauth-20)
* 🔐 [4. Control de Acceso Basado en Roles (RBAC)](#4-control-de-acceso-basado-en-roles-rbac)
* 🔌 [5. Contrato API y Acuerdos de Integración Inter-Equipos](#5-contrato-api-y-acuerdos-de-integración-inter-equipos)
* 📊 [6. Evolución del Modelo de Datos (Base de Datos)](#6-evolución-del-modelo-de-datos-base-de-datos)
* 🚀 [7. Estrategia de Despliegue e Infraestructura Cloud (Microsoft Azure)](#7-estrategia-de-despliegue-e-infraestructura-cloud-microsoft-azure)
* 🔒 [8. Políticas de Hardening de Red y Seguridad del Motor](#8-políticas-de-hardening-de-red-y-seguridad-del-motor)
* 💾 [9. Adjuntos: Scripts SQL del Repositorio](#9-adjuntos-scripts-sql-del-repositorio)

---

## 📖 1. Descripción General del Módulo de Autenticación

🔒 Este módulo implementa la autenticación centralizada de usuarios mediante **Google OAuth 2.0** y el control de acceso basado en roles (**RBAC**) para la plataforma Campus Online.

🛡️ Actúa como la capa de seguridad crítica que intercepta y protege todas las rutas del sistema, delimitando los niveles de autorización tanto en el frontend como en el backend.

### 🛠️ Stack Tecnológico Utilizado

* 🟢 **Node.js + Express:** Servidor web de infraestructura principal y entorno HTTP.
* 🔵 **Passport.js:** Motor middleware para la gestión de estrategias de identidad federada.
* 🟡 **express-session:** Control y gestión segura de sesiones basado en cookies firmadas.
* 🔴 **Google OAuth 2.0:** Proveedor de identidad externo para la federación de cuentas.

---

## 📂 2. Estructura del Proyecto y Capas Arquitectónicas

🏗️ El módulo de backend está organizado en tres capas de abstracción lógica para garantizar la mantenibilidad y la separación estricta de responsabilidades:

* 📄 **`src/config/passport.js`** ( Capan de Autenticación )
  * ⚙️ *Responsabilidad:* Definición de la estrategia de Google OAuth, aprovisionamiento automático de cuentas nuevas y serialización/deserialización de sesiones.

* 📄 **`src/config/database.js`** ( Capa de Datos )
  * ⚙️ *Responsabilidad:* Capa de abstracción de datos. En desarrollo inicial opera en memoria y se reemplaza con PostgreSQL 16 para producción.

* 📄 **`src/middleware/rbac.js`** ( Capa de Autorización )
  * ⚙️ *Responsabilidad:* Interceptores perimetrales `estaAutenticado` y `soloRoles` encargados de bloquear accesos no autorizados.

* 📄 **`src/routes/auth.js`** ( Capa de Rutas )
  * ⚙️ *Responsabilidad:* Declaración de endpoints públicos y protegidos de identidad (`/auth/google`, `/auth/callback`, `/auth/me`, `/auth/logout`).

* 📄 **`src/routes/protected.js`** ( Capa de Rutas )
  * ⚙️ *Responsabilidad:* Rutas restringidas para los roles académicos con las políticas de control RBAC acopladas.

* 📄 **`src/index.js`** ( Capa de Servidor )
  * ⚙️ *Responsabilidad:* Punto de entrada del servicio, montaje de middlewares globales y arranque formal del servidor HTTP.

### 🔄 Migración de Consultas de la DB Simulada

⚙️ Al sustituir la base de datos simulada en memoria dentro de `src/config/database.js` por el pool real de PostgreSQL, se realiza un mapeo directo de funciones:

* 🔍 **`buscarPorOauthId(id)`** → `SELECT * FROM users WHERE oauth_id = $1;`
* 🔍 **`buscarPorEmail(email)`** → `SELECT * FROM users WHERE email = $1;`
* 🔍 **`buscarPorId(id)`** → `SELECT * FROM users WHERE id = $1;`
* 📥 **`crearUsuario(datos)`** → `INSERT INTO users (...) VALUES (...) RETURNING *;`

> 📐 **Nota de Arquitectura:** Debido al aislamiento completo de la capa de datos, el resto de los componentes del backend (Passport, enrutadores y validadores RBAC) permanecen desacoplados y no requieren modificaciones al migrar al motor físico de base de datos.

---

## 🔄 3. Flujo de Autenticación e Integración (Google OAuth 2.0)

⚙️ El proceso de intercambio seguro de tokens y verificación remota se realiza en 7 fases consecutivas:

1. 🌐 **Inicio de Sesión:** El cliente realiza una petición a `/auth/google`. El servidor Express delega el control y redirige al usuario a los portales oficiales de consentimiento de Google.
2. 📑 **Autorización:** Google despliega la interfaz gráfica solicitando aprobación explícita al usuario para compartir su perfil público y su correo electrónico verificado.
3. 🔁 **Callback:** Una vez autorizado, Google devuelve un código temporal firmado hacia el endpoint receptor del backend `/auth/google/callback`.
4. 🗝️ **Verificación:** Passport intercepta dicho código y realiza una negociación interna (back-to-back) con las APIs de Google para descargar de forma segura los datos reales del perfil del usuario.
5. 🗄️ **Búsqueda en DB:** El sistema realiza un escaneo secuencial en el esquema de datos: busca coincidencias por `oauth_id`; si no existen, valida por `email` para vinculación de cuentas, y si la cuenta es nueva, efectúa un registro automático.
6. 🍪 **Sesión:** El identificador del usuario se almacena en el estado de la sesión (`req.session.userId`), despachando una cookie firmada y cifrada al navegador del cliente.
7. 🔀 **Redirección Dinámica:** El enrutador analiza el rol del usuario y lo despacha de inmediato hacia su sección correspondiente (`superadmin` → `/admin/dashboard` u `alumno` → `/alumno/portal`).

---

## 🔐 4. Control de Acceso Basado en Roles (RBAC)

🛠️ El MVP restringe el acceso de forma perimetral aislando las secciones de gestión administrativa de las transacciones financieras estudiantiles:

* 👤 **Rol `superadmin`**
  * 🟢 *Rutas Permitidas:* `/admin/dashboard`, `/admin/alumnos`, `/auth/me`, `/info`
  * 🔴 *Rutas Bloqueadas:* `/alumno/portal`, `/alumno/pagos`

* 👤 **Rol `alumno`**
  * 🟢 *Rutas Permitidas:* `/alumno/portal`, `/alumno/pagos`, `/auth/me`, `/info`
  * 🔴 *Rutas Bloqueadas:* `/admin/dashboard`, `/admin/alumnos`

### 🛡️ Implementación del Middleware de Protección

⚙️ Para blindar las rutas operacionales, los interceptores se inyectan como parámetros intermedios en Express:

```javascript
const { estaAutenticado, soloRoles } = require('../middleware/rbac');

// Acceso general para cualquier cuenta activa con sesión iniciada
router.get('/info', estaAutenticado, handler);

// Privilegios administrativos exclusivos
router.get('/admin/dashboard', soloRoles('superadmin'), handler);

// Privilegios financieros estudiantiles exclusivos
router.get('/alumno/portal', soloRoles('alumno'), handler);
```

### ⚠️ Respuestas de Excepción Perimetral

🛡️ Cuando una sesión activa intenta forzar el acceso a una ruta fuera de su alcance operativo, el middleware interrumpe la petición e inyecta un código de estado **HTTP 403 Forbidden** con el siguiente formato JSON tipificado:

```json
{
  "error": "Acceso denegado",
  "mensaje": "Esta sección es solo para: superadmin",
  "tu_rol": "alumno"
}
```

---

## 🔌 5. Contrato API y Acuerdos de Integración Inter-Equipos

### 🌐 Endpoints Expuestos por el Platform Team

⚙️ Las siguientes rutas están abiertas para consumo directo de los componentes de interacción frontend y facturación backend:

* 🛠️ **MÉTODO GET** | 🔗 **Ruta:** `/auth/google`
  * 🔑 *Acceso:* Público
  * 🎯 *Propósito:* Dispara la negociación inicial y redirección formal con Google.

* 🛠️ **MÉTODO GET** | 🔗 **Ruta:** `/auth/google/callback`
  * 🔑 *Acceso:* Público
  * 🎯 *Propósito:* Punto de retorno para el procesamiento seguro del token de Google.

* 🛠️ **MÉTODO GET** | 🔗 **Ruta:** `/auth/me`
  * 🔑 *Acceso:* Autenticado
  * 🎯 *Propósito:* Devuelve el perfil completo del usuario firmado y su rol. **Crítico para el frontend.**

* 🛠️ **MÉTODO GET** | 🔗 **Ruta:** `/auth/logout`
  * 🔑 *Acceso:* Autenticado
  * 🎯 *Propósito:* Destruye la sesión en el servidor y limpia las cookies locales del cliente.

### 📄 Esquema de Respuesta Cerrado para `/auth/me`

💻 Este payload JSON constituye el contrato central acordado con el **Experience Team (Equipo 1)** para el gobierno de vistas locales:

```json
{
  "id": 3,
  "email": "usuario@gmail.com",
  "nombre": "KEVIN ALEXIS",
  "rol": "alumno",
  "institution_id": 1
}
```

### 🤝 Matriz de Dependencias Técnicas entre Equipos

* 📦 **5.3.1 Lo que Nuestro Equipo Entrega**
  * 📄 El endpoint operativo de estado de identidad `/auth/me` con datos de pertenencia (`institution_id`).
  * ⚙️ El middleware funcional de control perimetral reutilizable `soloRoles()`.
  * 🏷️ Los strings maestros estandarizados de asignación de roles: `'superadmin'` y `'alumno'`.
  * 🔀 Redirección automática según rol directamente desde el servidor post-login.

* 👥 **5.3.2 Lo que se Requiere del Equipo 1 (Experience Team)**
  * 🔗 Definición de las URLs absolutas de aterrizaje en el frontend para cada rol tras la autenticación exitosa.
  * 🛠️ Implementación de los guardianes de ruta en el cliente consumiendo el payload estructurado de `/auth/me`.
  * 🎨 Especificación de UI (si la pantalla de acceso usará solo Google o soporte híbrido para contraseñas locales).

* 💳 **5.3.3 Lo que se Requiere del Equipo 3 (Revenue & Integrations Team)**
  * 📊 Mapeo de los atributos mínimos de usuario requeridos para la creación de clientes en Stripe (e.g., `email`, `id`).
  * 🔗 Listado de rutas financieras sensibles donde se deba inyectar el tag protector `soloRoles('alumno')`.
  * 🔒 Especificación de seguridad para los webhooks de Stripe (uso de firmas criptográficas públicas o validación de sesión).

---

## 📊 6. Evolución del Modelo de Datos (Base de Datos)

⚙️ El diseño del almacenamiento de datos implementa un esquema **Multi-Tenant** sobre PostgreSQL 16 para aislar la información de las instituciones mediante segmentación lógica.

### 📐 Esquema Conceptual de Relaciones Relacionales

🏗️ Las restricciones lógicas y dependencias del sistema se configuran según las siguientes reglas de negocio:

* 🏢 **Aislamiento Multi-Tenant:** Toda institución educativa opera como la raíz del ecosistema de datos, ramificando de manera estricta sus usuarios y ofertas curriculares (`institutions 1:N users` e `institutions 1:N courses_or_subjects`).
* 👤 **Especialización Condicional de Cuentas:** Un registro base en `users` se extiende de forma exclusiva a las tablas de perfil detallado `students` o `teachers` mediante llaves foráneas unívocas. El diseño lógico prohíbe explícitamente que una misma cuenta actúe simultáneamente como docente y alumno.
* 📝 **Control Académico Integrado:** Las inscripciones vinculan filas cruzadas entre estudiantes y materias, forzando restricciones de unicidad compuestas para evitar duplicidades de asignación de carga académica (`uq_student_course_enrollment`).

### 🕒 Historial de Revisiones del Esquema DDL

* 🟢 **6.2.1 Versión 1: Arquitectura Base MVP (`school_platform-v1.sql`)**
  * 💾 En la primera propuesta física, los identificadores se definieron con el estándar robusto `UUID` para simplificar migraciones distribuidas. La gestión contable de deudas escolares se diseñó mediante una tabla central denominada `payments`, encargada de definir los conceptos globales de cobro emitidos por la dirección y vinculada a los saldos a través de la tabla `payment_students`.

* 🔵 **6.2.2 Versión 2: Refactor Semántico de Finanzas (Final) (`school_platform-v2_final.sql`)**
  * 🧮 Durante la fase de integración en el backend, se detectó una fuerte ambigüedad conceptual en la tabla `payments`. La entidad representaba deudas asignadas o cargos emitidos por la escuela (ej. "Inscripción 2026 $1000"), pero su nombre daba a entender que guardaba registros de transacciones bancarias o dinero ya ingresado, induciendo a errores de programación.
  * 🛠️ **Modificación Principal:** Se renombró la tabla de `payments` a `charges` para reflejar con precisión su naturaleza de cargo o deuda institucional.
  * 🔄 **Propagación Síncrona:** Todas las restricciones relacionales, llaves primarias y reglas de control numérico fueron actualizadas (`payments_pkey` → `charges_pkey`, `payments_amount_check` → `charges_amount_check`, `payments_status_check` → `charges_status_check`).
  * 🎓 **Excepción Académica:** Por directrices y especificaciones funcionales del proyecto, la entidad relacional intermedia mantuvo el nombre estricto de `payment_students`, manteniendo su clave foránea `payment_id` apuntando directamente hacia la refactorizada tabla de `charges`.

⚙️ Esta corrección semántica elimina ambigüedades en las operaciones matemáticas del backend y actualiza las consultas relacionales de la siguiente manera:

* ❌ **Sintaxis V1 (Obsoleta):** `SELECT * FROM school_platform.payments;`
* ✅ **Sintaxis V2 (Vigente):** `SELECT * FROM school_platform.charges;`

---

## 🚀 7. Estrategia de Despliegue e Infraestructura Cloud (Microsoft Azure)

🌍 El entorno de producción fue aprovisionado e implementado de extremo a extremo (E2E) en la infraestructura global de nube de **Microsoft Azure**.

### 🖥️ Perfil Técnico de la Instancia de Cómputo

* 💳 **Suscripción de Control:** Azure for Students.
* 🆔 **Identificador de Máquina Virtual:** `csu-final-project-1`.
* 🌍 **Zona de Disponibilidad:** Europe / Switzerland North.
* 💿 **Sistema Operativo Base:** Ubuntu Server 24.04 LTS (Arquitectura Gen2 x64).
* ⚙️ **Dimensionamiento de Hardware:** Nivel Standard `B2ats v2` (2 vCPUs de cómputo y 1 GiB de memoria RAM dedicada).
* 🌐 **IP Pública Asignada de Producción:** `20.208.29.234`.

### 🛠️ Pipeline de Aprovisionamiento y Restauración de Datos

1. 🔌 **Conexión e Inicialización:** Acceso mediante terminal SSH segura hacia el host y actualización de los repositorios del sistema operativo mediante comandos `sudo apt update`.
2. 💾 **Despliegue del Motor:** Instalación de los paquetes base de PostgreSQL versión 16 y utilidades accesorias de control relacional:
   ```bash
   sudo apt install postgresql-16 postgresql-client-16 postgresql-contrib -y
   ```
3. 🌍 **Ajuste de Locales (Soporte Regional):** Para mitigar fallos de codificación, truncamiento de texto o formatos de fecha erróneos al importar el dump relacional de desarrollo, se configuró el soporte de locales de español:
   ```bash
   sudo locale-gen es_ES.UTF-8
   sudo update-locale
   sudo systemctl restart postgresql
   ```
4. 📤 **Transferencia Segura del Dump:** El archivo maestro de persistencia con los datos dummy requeridos para pruebas (`school_platform_vm.sql`) fue copiado al servidor mediante el protocolo seguro `scp` hacia el directorio temporal de la instancia:
   ```bash
   scp school_platform_vm.sql csu-team@20.208.29.234:/tmp/
   ```
5. 📥 **Restauración del Esquema:** Execution del archivo DDL/DML invocando al superusuario del sistema para instanciar las bases de datos, catálogos, restricciones e índices del proyecto:
   ```bash
   sudo -u postgres psql -f /tmp/school_platform_vm.sql
   ```

---

## 🔒 8. Políticas de Hardening de Red y Seguridad del Motor

⚙️ Para garantizar un entorno seguro alineado con los estándares de producción, se implementaron controles estrictos de seguridad de red y base de datos:

### 👥 Creación de Cuentas Operativas Segregadas

🔒 Se deshabilitó el inicio de sesión remoto directo utilizando el rol de administración por defecto `postgres`. En su lugar, se crearon tres credenciales independientes aplicando el principio de menor privilegio para aislar las responsabilidades del sistema:

```sql
CREATE USER db_readonly WITH PASSWORD 'Readonly_csu_1234$';
CREATE USER db_insert WITH PASSWORD 'Insert_020526^';
CREATE USER db_writer WITH PASSWORD 'Writer_1236&';
```

* 🔍 **`db_readonly`:** Otorgamiento exclusivo del privilegio `SELECT` sobre la totalidad de las entidades de datos. Diseñado para procesos analíticos de extracción de reportes y lecturas del frontend escolar.
* 📥 **`db_insert`:** Cuenta registrada únicamente con permisos de inyección `INSERT`. Reservada para la persistencia masiva de eventos del sistema y trazas de auditoría en la tabla `login_logs`.
* ⚙️ **`db_writer`:** Cuenta operativa principal provista de facultades CRUD completas (`SELECT`, `INSERT`, `UPDATE`, `DELETE`). Es el perfil que utiliza el backend de Express para coordinar la persistencia de datos.

### 🧱 Blindaje Host-Based a Nivel de Red (`pg_hba.conf`)

🛡️ Para forzar el uso de algoritmos de cifrado modernos y rechazar credenciales no seguras en los túneles remotos, se editó la directiva de escucha en `postgresql.conf` en el puerto `5432` y se inyectaron las siguientes políticas estrictas de autenticación mediante contraseñas usando el algoritmo `scram-sha-256` en el archivo `pg_hba.conf`:

```text
# Control perimetral de acceso remoto seguro - Campus Online
host    school_platform    db_readonly     0.0.0.0/0    scram-sha-256
host    school_platform    db_insert       0.0.0.0/0    scram-sha-256
host    school_platform    db_writer       0.0.0.0/0    scram-sha-256
```

### 🧱 Reglas de Cortafuegos de Infraestructura

🛡️ Para permitir las peticiones remotas de los equipos externos, se abrieron de forma segura las conexiones del puerto de la base de datos a nivel del kernel del servidor y se aprovisionaron las correspondientes Listas de Control de Acceso (ACL) en el grupo de seguridad de red de Azure:
```bash
sudo ufw allow 5432/tcp
```

### 🔍 Unidades de Validación de Acceso para Desarrolladores

💻 Los equipos de integración pueden validar sus credenciales y realizar pruebas de conexión remotas apuntando a la IP pública del servidor mediante el comando oficial de PostgreSQL:
```bash
psql -h 20.208.29.234 -p 5432 -U db_readonly -d school_platform
```

---

## 💾 9. Adjuntos: Scripts SQL del Repositorio

### Archivo 1: `school_platform-v1.sql`
*💾 Guarda este bloque en un archivo independiente llamado `school_platform-v1.sql` dentro de tu carpeta de base de datos.*

```sql
BEGIN;

CREATE SCHEMA IF NOT EXISTS school_platform;
SET search_path TO school_platform;

CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    logo_url TEXT,
    primary_color VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL,
    role_id UUID NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    name VARCHAR(150) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'blocked')),
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_users_institution
        FOREIGN KEY (institution_id)
        REFERENCES institutions(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_users_role
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    student_code VARCHAR(50) NOT NULL UNIQUE,
    course_level VARCHAR(50),
    enrollment_status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (enrollment_status IN ('active', 'inactive', 'suspended', 'graduated')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_students_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    employee_code VARCHAR(50) NOT NULL UNIQUE,
    specialty VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_teachers_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE courses_or_subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL,
    teacher_id UUID,
    name VARCHAR(120) NOT NULL,
    code VARCHAR(30) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_courses_institution
        FOREIGN KEY (institution_id)
        REFERENCES institutions(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_courses_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES teachers(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT uq_course_code_per_institution
        UNIQUE (institution_id, code)
);

CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL,
    course_subject_id UUID NOT NULL,
    enrolled_at DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'dropped', 'completed')),

    CONSTRAINT fk_enrollments_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_enrollments_course
        FOREIGN KEY (course_subject_id)
        REFERENCES courses_or_subjects(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_student_course_enrollment
        UNIQUE (student_id, course_subject_id)
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL,
    concept VARCHAR(150) NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'MXN',
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'partial', 'paid', 'overdue', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_payments_institution
        FOREIGN KEY (institution_id)
        REFERENCES institutions(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE payment_students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id UUID NOT NULL,
    student_id UUID NOT NULL,
    assigned_amount NUMERIC(12,2) NOT NULL CHECK (assigned_amount >= 0),
    paid_amount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (paid_amount >= 0),
    paid_at TIMESTAMPTZ,
    payment_method VARCHAR(30),
    external_reference VARCHAR(120),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'partial', 'paid', 'failed', 'cancelled')),

    CONSTRAINT fk_payment_students_payment
        FOREIGN KEY (payment_id)
        REFERENCES payments(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_payment_students_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_payment_student
        UNIQUE (payment_id, student_id),

    CONSTRAINT chk_paid_not_exceed_assigned
        CHECK (paid_amount <= assigned_amount)
);

CREATE TABLE login_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    login_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN NOT NULL,

    CONSTRAINT fk_login_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX idx_users_institution_id ON users(institution_id);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_teachers_user_id ON teachers(user_id);
CREATE INDEX idx_courses_institution_id ON courses_or_subjects(institution_id);
CREATE INDEX idx_courses_teacher_id ON courses_or_subjects(teacher_id);
CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX idx_enrollments_course_subject_id ON enrollments(course_subject_id);
CREATE INDEX idx_payments_institution_id ON payments(institution_id);
CREATE INDEX idx_payments_due_date ON payments(due_date);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payment_students_payment_id ON payment_students(payment_id);
CREATE INDEX idx_payment_students_student_id ON payment_students(student_id);
CREATE INDEX idx_payment_students_status ON payment_students(status);
CREATE INDEX idx_login_logs_user_id ON login_logs(user_id);
CREATE INDEX idx_login_logs_login_at ON login_logs(login_at);

COMMIT;
```

### Archivo 2: `school_platform-v2_final.sql`
*💾 Guarda este bloque en un archivo independiente llamado `school_platform-v2_final.sql` dentro de tu carpeta de base de datos.*

```sql
BEGIN;

CREATE SCHEMA IF NOT EXISTS school_platform;
SET search_path TO school_platform, public;

CREATE TABLE school_platform.institutions (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    name character varying(150) NOT NULL,
    logo_url text,
    primary_color character varying(20),
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT institutions_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);

CREATE TABLE school_platform.roles (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    name character varying(50) NOT NULL UNIQUE,
    description text
);

CREATE TABLE school_platform.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    institution_id uuid NOT NULL,
    role_id uuid NOT NULL,
    username character varying(50) NOT NULL UNIQUE,
    email character varying(255) NOT NULL UNIQUE,
    password_hash text NOT NULL,
    name character varying(150) NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    last_login_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT users_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'blocked'::character varying])::text[]))),
    CONSTRAINT fk_users_institution FOREIGN KEY (institution_id) REFERENCES school_platform.institutions(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES school_platform.roles(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE school_platform.students (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL UNIQUE,
    student_code character varying(50) NOT NULL UNIQUE,
    course_level character varying(50),
    enrollment_status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT students_enrollment_status_check CHECK (((enrollment_status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'suspended'::character varying, 'graduated'::character varying])::text[]))),
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES school_platform.users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE school_platform.teachers (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL UNIQUE,
    employee_code character varying(50) NOT NULL UNIQUE,
    specialty character varying(100),
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT teachers_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[]))),
    CONSTRAINT fk_teachers_user FOREIGN KEY (user_id) REFERENCES school_platform.users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE school_platform.courses_or_subjects (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    institution_id uuid NOT NULL,
    teacher_id uuid,
    name character varying(120) NOT NULL,
    code character varying(30) NOT NULL,
    description text,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT courses_or_subjects_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[]))),
    CONSTRAINT fk_courses_institution FOREIGN KEY (institution_id) REFERENCES school_platform.institutions(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_courses_teacher FOREIGN KEY (teacher_id) REFERENCES school_platform.teachers(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT uq_course_code_per_institution UNIQUE (institution_id, code)
);

CREATE TABLE school_platform.enrollments (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    student_id uuid NOT NULL,
    course_subject_id uuid NOT NULL,
    enrolled_at date DEFAULT CURRENT_DATE NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    CONSTRAINT enrollments_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'dropped'::character varying, 'completed'::character varying])::text[]))),
    CONSTRAINT fk_enrollments_course FOREIGN KEY (course_subject_id) REFERENCES school_platform.courses_or_subjects(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id) REFERENCES school_platform.students(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_student_course_enrollment UNIQUE (student_id, course_subject_id)
);

CREATE TABLE school_platform.charges (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    institution_id uuid NOT NULL,
    concept character varying(150) NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character(3) DEFAULT 'MXN'::bpchar NOT NULL,
    due_date date NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT charges_amount_check CHECK ((amount >= (0)::numeric)),
    CONSTRAINT charges_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'partial'::character varying, 'paid'::character varying, 'overdue'::character varying, 'cancelled'::character varying])::text[]))),
    CONSTRAINT fk_payments_institution FOREIGN KEY (institution_id) REFERENCES school_platform.institutions(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE school_platform.payment_students (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    payment_id uuid NOT NULL,
    student_id uuid NOT NULL,
    assigned_amount numeric(12,2) NOT NULL,
    paid_amount numeric(12,2) DEFAULT 0 NOT NULL,
    paid_at timestamp with time zone,
    payment_method character varying(30),
    external_reference character varying(120),
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    CONSTRAINT chk_paid_not_exceed_assigned CHECK ((paid_amount <= assigned_amount)),
    CONSTRAINT payment_students_assigned_amount_check CHECK ((assigned_amount >= (0)::numeric)),
    CONSTRAINT payment_students_paid_amount_check CHECK ((paid_amount >= (0)::numeric)),
    CONSTRAINT payment_students_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'partial'::character varying, 'paid'::character varying, 'failed'::character varying, 'cancelled'::character varying])::text[]))),
    CONSTRAINT fk_payment_students_payment FOREIGN KEY (payment_id) REFERENCES school_platform.charges(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_payment_students_student FOREIGN KEY (student_id) REFERENCES school_platform.students(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_payment_student UNIQUE (payment_id, student_id)
);

CREATE TABLE school_platform.login_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL,
    login_at timestamp with time zone DEFAULT now() NOT NULL,
    ip_address inet,
    user_agent text,
    success boolean NOT NULL,
    CONSTRAINT fk_login_logs_user FOREIGN KEY (user_id) REFERENCES school_platform.users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX idx_charges_due_date ON school_platform.charges USING btree (due_date);
CREATE INDEX idx_charges_institution_id ON school_platform.charges USING btree (institution_id);
CREATE INDEX idx_charges_status ON school_platform.charges USING btree (status);
CREATE INDEX idx_courses_institution_id ON school_platform.courses_or_subjects USING btree (institution_id);
CREATE INDEX idx_courses_teacher_id ON school_platform.courses_or_subjects USING btree (teacher_id);
CREATE INDEX idx_enrollments_course_subject_id ON school_platform.enrollments USING btree (course_subject_id);
CREATE INDEX idx_enrollments_student_id ON school_platform.enrollments USING btree (student_id);
CREATE INDEX idx_login_logs_login_at ON school_platform.login_logs USING btree (login_at);
CREATE INDEX idx_login_logs_user_id ON school_platform.login_logs USING btree (user_id);
CREATE INDEX idx_payment_students_payment_id ON school_platform.payment_students USING btree (payment_id);
CREATE INDEX idx_payment_students_status ON school_platform.payment_students USING btree (status);
CREATE INDEX idx_payment_students_student_id ON school_platform.payment_students USING btree (student_id);
CREATE INDEX idx_students_user_id ON school_platform.students USING btree (user_id);
CREATE INDEX idx_teachers_user_id ON school_platform.teachers USING btree (user_id);
CREATE INDEX idx_users_institution_id ON school_platform.users USING btree (institution_id);
CREATE INDEX idx_users_role_id ON school_platform.users USING btree (role_id);

INSERT INTO school_platform.roles (name, description) VALUES  
('superadmin', 'Acceso total de control global'),
('admin', 'Administrador de nivel institucional'),
('student', 'Perfil de alumno regular'),
('teacher', 'Perfil de docente o profesor académico')
ON CONFLICT (name) DO NOTHING;

INSERT INTO school_platform.institutions (id, name, logo_url, primary_color, status) VALUES  
('72cb3a32-a4d9-4848-994e-da9e2ae35d5f', 'Instituto Tecnológico Demo', '[https://logo.com/demo.png](https://logo.com/demo.png)', '#2563EB', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.users (id, institution_id, role_id, username, email, password_hash, name, status) VALUES  
('09d22dcb-cce4-466c-aad4-8645b09f02bc', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', (SELECT id FROM school_platform.roles WHERE name='admin'), 'admin1', 'admin1@demo.com', 'hash_admin', 'Administrador Uno', 'active'),
('4a352805-391e-4249-a871-168c602c84a1', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', (SELECT id FROM school_platform.roles WHERE name='teacher'), 'teacher1', 'teacher1@demo.com', 'hash_teacher', 'Profesor Juan', 'active'),
('0be55dd8-9f16-42f8-8287-f95408492e12', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', (SELECT id FROM school_platform.roles WHERE name='student'), 'student1', 'student1@demo.com', 'hash_student', 'Alumno Uno', 'active'),
('6760fbae-5ac4-42bb-a9c6-bf39754857aa', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', (SELECT id FROM school_platform.roles WHERE name='student'), 'student2', 'student2@demo.com', 'hash_student', 'Alumno Dos', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.students (id, user_id, student_code, course_level, enrollment_status) VALUES  
('9eaf5515-c9da-44fc-9fe3-e197a283c5c8', '0be55dd8-9f16-42f8-8287-f95408492e12', 'STU001', 'Primero', 'active'),
('5ec07ce0-e022-461d-a562-4611317b7ad9', '6760fbae-5ac4-42bb-a9c6-bf39754857aa', 'STU002', 'Primero', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.teachers (id, user_id, employee_code, specialty, status) VALUES  
('ffa8dcc4-c1d1-4e72-a792-0ae46b378f28', '4a352805-391e-4249-a871-168c602c84a1', 'EMP001', 'Matemáticas', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.courses_or_subjects (id, institution_id, teacher_id, name, code, description, status) VALUES  
('afcdd13b-10e4-4493-bbd8-5617991ee46f', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', 'ffa8dcc4-c1d1-4e72-a792-0ae46b378f28', 'Matemáticas Básicas', 'MAT-101', 'Curso introductorio', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.enrollments (id, student_id, course_subject_id, enrolled_at, status) VALUES  
('e4d39652-5e81-40f2-b761-f63bef016d89', '9eaf5515-c9da-44fc-9fe3-e197a283c5c8', 'afcdd13b-10e4-4493-bbd8-5617991ee46f', '2026-04-21', 'active'),
('c08c8b27-5289-4c75-abad-12bdeba74964', '5ec07ce0-e022-461d-a562-4611317b7ad9', 'afcdd13b-10e4-4493-bbd8-5617991ee46f', '2026-04-21', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.charges (id, institution_id, concept, amount, currency, due_date, status) VALUES  
('4e754644-d175-4c23-bcda-5160379fa8dc', '72cb3a32-a4d9-4848-994e-da9e2ae35d5f', 'Inscripción 2026', 1000.00, 'MXN', '2026-05-06', 'pending')
ON CONFLICT DO NOTHING;

INSERT INTO school_platform.payment_students (id, payment_id, student_id, assigned_amount, paid_amount, paid_at, payment_method, status) VALUES  
('0f147643-8e2a-4dd6-89b8-9476e0cbdeac', '4e754644-d175-4c23-bcda-5160379fa8dc', '5ec07ce0-e022-461d-a562-4611317b7ad9', 1000.00, 0.00, NULL, NULL, 'pending'),
('c7e3b48b-11a7-48c6-a7bf-5f53bb52262b', '4e754644-d175-4c23-bcda-5160379fa8dc', '9eaf5515-c9da-44fc-9fe3-e197a283c5c8', 1000.00, 500.00, '2026-04-21 20:11:55', 'card', 'partial')
ON CONFLICT DO NOTHING;

COMMIT;

-- ===========================================================================
-- PROVISIÓN REMOTA DE USUARIOS DE SEGURIDAD INTERNA (HARDENING OPERATIVO)
-- ===========================================================================
CREATE USER db_readonly WITH PASSWORD 'Readonly_csu_1234$';
CREATE USER db_insert WITH PASSWORD 'Insert_020526^';
CREATE USER db_writer WITH PASSWORD 'Writer_1236&';

GRANT CONNECT ON DATABASE school_platform TO db_readonly, db_insert, db_writer;
GRANT USAGE ON SCHEMA school_platform TO db_readonly, db_insert, db_writer;

GRANT SELECT ON ALL TABLES IN SCHEMA school_platform TO db_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA school_platform GRANT SELECT ON TABLES TO db_readonly;

GRANT INSERT ON ALL TABLES IN SCHEMA school_platform TO db_insert;
ALTER DEFAULT PRIVILEGES IN SCHEMA school_platform GRANT INSERT ON TABLES TO db_insert;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA school_platform TO db_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA school_platform GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO db_writer;

ALTER ROLE db_readonly SET search_path TO school_platform, public;
ALTER ROLE db_insert SET search_path TO school_platform, public;
ALTER ROLE db_writer SET search_path TO school_platform, public;
```

---

## 👥 Equipo de Desarrollo

* 🧑‍💻 **Kibsaim Mejia** - *Industrial Chemical Engineer & Data Analyst* | Encargado de Documentación Técnica del Platform Team.
```
