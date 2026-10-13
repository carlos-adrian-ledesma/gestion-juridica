# Arquitectura de la DEMO pública

```text
INICIAR_DEMO.bat
       │  Python 3.10+
       ▼
    demo.py                 Ventana principal, vistas Tkinter y formularios
       │
       ▼
    app/store.py            Consultas parametrizadas y reglas de demo
       │
       ▼
    SQLite :memory:         Base transitoria aislada (jamás persistida)
```

**Separación de código:** la DEMO fue implementada como aplicación autónoma nueva. No importa `programa/app/*` ni distribuye módulos del Full Source privado V1.0.6 RC1. No incluye el `wheelhouse`, ejecutables, binarios PDF ni archivos del trabajo original.

**Contratos:** operaciones CRUD y validación de estado, moneda y fecha en `DemoStore`; `PRAGMA foreign_keys=ON`; SQL con parámetros; borrado de clientes referenciados restringido, borrado de casos desvincula documentos, agenda y movimientos. Unidades monetarias enteras para la capa pública. Navegación/presentación en `demo.py`.

**Seguridad de demostración:** solo se crea una base en RAM; no se utiliza `Documents`, `%APPDATA%`, `%LOCALAPPDATA%` ni variables de la app privada, y no se hacen llamadas HTTP. No hay información de clientes, expedientes ni claves reales.

**Alcance real:** no hay persistencia, sesiones multiusuario, roles, cifrado de bases, firma digital, cálculos legales ni auditoría certificada. No se equipara este prototipo a un sistema jurídicamente validado.
