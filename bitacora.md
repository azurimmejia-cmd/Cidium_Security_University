🛡️ Bitácora de Registro: Ruta de Arranque (Linux y Git)
Estudiante: Azurim (@azurimmejia-cmd)

Fecha de ejecución: 22 de marzo, 2026

Duración estimada: 1.5 horas 

Sistema Operativo: Windows 11 (usando MINGW64 / Git Bash)

1. Resumen de Ejecución (Paso a Paso)
Paso 1 (Ubicación): Ejecuté pwd y ls -lah. Confirmé mi directorio en /c/Users/yo y visualicé archivos ocultos de configuración.

Paso 2 (Clonación): Usé git clone para descargar mi repositorio de análisis de ventas de panadería a mi máquina local.

Paso 3 (Navegación): Usé cd para entrar a la carpeta del proyecto.

Paso 4 (Ramas): Creé la rama semana2-arranque con git checkout -b para trabajar de forma segura.

Paso 5 (Creación): Generé el archivo hello.txt usando el comando touch.

Paso 6 (Edición): Entré a nano hello.txt y registré mi usuario y mi color favorito (Azul).

Paso 7 (Registro): Ejecuté git status para revisar los archivos. Preparé el archivo con git add y guardé el cambio local con git commit.

Paso 8 (Sincronización): Realicé el git push para subir la rama y los cambios a la nube de GitHub.

2. Incidentes y Aprendizajes Técnicos
Interrupción de Flujo (^C): Se generó un comando nulo mediante Ctrl + C. Aprendí que en Bash esto sirve para limpiar la línea actual o abortar procesos sin dañar el sistema.

Advertencia de Saltos de Línea (CRLF): Git avisó sobre el reemplazo de LF por CRLF. Identifiqué que es una gestión automática de Git para que archivos creados en Windows sean compatibles con Linux.

Seguridad e Higiene Digital:Se generó un Personal Access Token (classic) con permisos de repo. Además, se cuenta con MFA (Autenticación Multifactor) activado en GitHub para proteger la cuenta.

3. Evidencia de Historial Final (git log)

2cd727f (HEAD -> semana2-arranque, origin/semana2-arranque) docs: Se agrega username y color favorito en hello.txt
9c12db4 (origin/main, origin/HEAD, main) análisis de ventas de panadería


