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
| Release/CI GitHub | **PENDIENTE** | Empieza después de publicar el repo |

**Pruebas incluidas:** conteos y reinicio de fixtures, datos anónimos, aislamiento en memoria, creación/edición/borrado de clientes y casos, restricciones FK, SQL injection como dato, documentos, fechas, importes, multicurrency, validación de formato y estado de eliminaciones.

```bash
python -m unittest discover -s tests -v
python -m compileall -q demo.py app tests
```

El workflow `.github/workflows/ci.yml` está configurado para **ejecutarse en el futuro** en GitHub Actions (`ubuntu-latest`, `windows-latest`, Python 3.11/3.12); su mera presencia no significa que ya se hayan obtenido resultados.

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
