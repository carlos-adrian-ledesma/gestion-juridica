[TESTING.md](https://github.com/user-attachments/files/33391072/TESTING.md)
# Testing & Verification · Pruebas reproducibles

**Edición evaluada:** aplicación DEMO autónoma (`1.0.0-demo.1`, contenido del presente portafolio). El código de la aplicación privada no forma parte de estas pruebas.

## Evidencia local del paquete

| Verificación | Resultado | Alcance |
|---|---|---|
| `python -m unittest discover -s tests -v` | **16 PASS / 0 FAIL** | Lógica y persistencia temporal en Linux |
| `python -m compileall -q demo.py app tests` | **PASS** | Sintaxis Python disponible |
| Captura de 3 pantallas DEMO | **HECHO** | Tkinter/Xvfb, no Windows |
| 8 capturas premium | **HECHO** | GUI real con datos sintéticos, sin validar módulos end-to-end |
| Doble clic `INICIAR_DEMO.bat` en Windows | **NO PROBADO** | Requiere Windows real |
| Escalado Windows y antivirus | **NO PROBADO** | Requiere evaluación manual |
| GitHub Actions · compilación + tests | **4/4 entornos PASS** (13/10/2026) | Python 3.11 y 3.12 en `windows-latest` y `ubuntu-latest` · [ejecución](https://github.com/carlos-adrian-ledesma/gestion-juridica/actions/runs/38412555905) |
| GitHub Release `v1.0.0-demo.1` | **POR PUBLICAR** | Requiere crear el tag y la Release desde GitHub; no hay ejecutable Windows |

**Pruebas incluidas:** conteos y reinicio de fixtures, datos anónimos, aislamiento en memoria, creación/edición/borrado de clientes y casos, restricciones FK, SQL injection como dato, documentos, fechas, importes, multicurrency, validación de formato y estado de eliminaciones.

```bash
python -m unittest discover -s tests -v
python -m compileall -q demo.py app tests
```

## Evidencia de integración continua (13 de octubre de 2026)

El workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) se ejecutó en GitHub Actions. La ejecución [38412555905](https://github.com/carlos-adrian-ledesma/gestion-juridica/actions/runs/38412555905) finalizó con resultado **success** en todos los jobs:

| Sistema de CI | Python | Compilación de código | Pruebas unitarias |
|---|---|---|---|
| `ubuntu-latest` | 3.11 | PASS | PASS |
| `ubuntu-latest` | 3.12 | PASS | PASS |
| `windows-latest` | 3.11 | PASS | PASS |
| `windows-latest` | 3.12 | PASS | PASS |

La configuración ejecuta `python -m compileall -q demo.py app tests` y `python -m unittest discover -s tests -v`. Es evidencia de **compatibilidad de sintaxis y reglas probadas** en esos entornos, no una ejecución automatizada de la GUI. En particular, no prueba que `INICIAR_DEMO.bat` se haya abierto mediante doble clic, ni el escalado de Windows, ni su aptitud para datos reales.



## Manual Windows checklist

1. Instalar Python 3.11 o 3.12 con Tkinter y launcher `py`; abrir terminal como usuario sin administrador.
2. Extraer/copiar el repositorio y ejecutar `INICIAR_DEMO.bat`.
3. Confirmar contadores iniciales (clientes 6, casos 8, documentos 6, eventos 5, movimientos 6).
4. Crear cliente `Cliente X`, editarlo, filtrar y borrar; intentar borrar Cliente A referenciado y comprobar bloqueo.
5. Crear caso `DEMO-099`, asociarlo y actualizar estado.
6. Crear documento temporal y probar diálogo Guardar / Descartar / Cancelar al salir del módulo.
7. Añadir movimiento de USD 12,30 y verificar que el balance ARS/EUR no varía.
8. Restablecer datos; reiniciar app; verificar que los cambios no persisten.
9. Verificar navegación a 1366×768 y 1920×1080, escalado 100/125/150 %.
10. Confirmar que no hay escrituras a bases privadas, archivos de expedientes, backup ni accesos de red.

**Criterio de aceptación:** documentar plataforma, Python, resultado por paso y screenshots reales antes de publicar un binario Windows o prometer uso final por clientes.
