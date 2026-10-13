# Security Policy / Seguridad

## Alcance

Este repositorio contiene una **DEMO aislada**, no la aplicación jurídica profesional completa. Los ejemplos son sintéticos. No contiene servicio remoto, telemetría, backup, procesamiento PDF ni ejecutable comercial.

- Se utiliza SQLite `:memory:` en cada sesión.
- Las consultas de la demo usan parámetros en las rutas funcionales previstas y claves foráneas habilitadas.
- No se procesan expedientes, datos personales reales, documentos jurídicos ni credenciales.
- No es un entorno confidencial: swap, dumps y capturas del sistema podrían exponer texto introducido por error.
- No tiene autenticación ni cifrado integral. No representa cumplimiento regulatorio ni autorización jurídica.

**Nunca introducir información real** ni usar para ejercicio profesional.

## Reportar vulnerabilidades

No publicar credenciales, rutas privadas ni técnicas de explotación con datos reales en Issues. Contactar al mantenedor a través de su [perfil GitHub](https://github.com/carlos-adrian-ledesma) y coordinar un canal privado antes de compartir detalles sensibles. Las limitaciones públicas pueden documentarse en Issues sin datos confidenciales.

## Límites del Full Source privado

Los mecanismos del software privado (instalación, respaldos, permisos, licencias del motor PDF y aceptación Windows) requieren evaluaciones independientes. La DEMO y sus tests no los certifican.
