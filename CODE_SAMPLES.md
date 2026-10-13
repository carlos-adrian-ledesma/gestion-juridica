# Code samples for technical review

Los ejemplos publicados aquí **pertenecen a la aplicación DEMO independiente**, no al Full Source privado. Su función es permitir una revisión real de código, no fingir que la DEMO reproduce toda la complejidad comercial.

### 1. Control de persistencia efímera — `app/store.py`

[`DemoStore.reset()`](app/store.py) crea `sqlite3.connect(':memory:')`, activa `PRAGMA foreign_keys=ON`, define las tablas y genera registros de muestra. Permite restablecer el escenario de evaluación y evita enlazar la base del producto profesional.

**Revisar:** manejo del ciclo de vida de la conexión, relaciones y garantía de aislamiento.

### 2. SQL seguro y restricciones referenciales

[`DemoStore.add_case` / `DemoStore.delete_client`](app/store.py): consultar la validación de ID de cliente, referencias existentes y consultas parametrizadas. Los tests comprueban que una cadena tipo SQL injection se almacena como dato literal, sin ejecutar instrucciones inyectadas.

**Revisar:** integridad referencial real vs. validaciones superficiales solo en UI.

### 3. Montos financieros sin sumar monedas heterogéneas

[`money_to_cents`, `money_text` y `DemoStore.balances`](app/store.py): conversión explícita a centavos enteros, validación de límites y reporte de balances por código de divisa.

**Revisar:** precisión, operaciones aritméticas, separación de unidades y ausencia de tipo de cambio implícito.

### 4. Pruebas de regresión

[`tests/test_demo.py`](tests/test_demo.py) contiene **16 pruebas** ejecutables con `unittest`: altas/ediciones/bajas, restricciones de FK, conteos iniciales, datos anónimos, restablecimiento, importes y fechas, SQL parametrizado y separación monetaria.

**Ejecutar:**

```bash
python -m unittest discover -s tests -v
```

### 5. UI de escritorio

[`demo.py`](demo.py) muestra construcción de navegación Tkinter/ttk, controles de formularios y separación entre vistas y capa de almacenamiento. La DEMO muestra un editor reducido y advertencias al abandonar cambios.

**Aspectos sujetos a revisión futura:** la presentación de estados y la cobertura automatizada de GUI/Windows no están completas; no se afirma una arquitectura por capas estricta ni estándares de accesibilidad certificados.

### Producto completo

El programa privado tiene módulos de documentos, PDF, agenda, expedientes, respaldos y configuración; su diseño se presenta con capturas públicas sanitizadas. Ningún fragmento privado es necesario para ejecutar los ejemplos de este repositorio. Contactar al titular para una revisión privada autorizada durante una entrevista.
