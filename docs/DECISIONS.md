# Engineering Decisions (ADRs)

### ADR-001: Separación pública/privada
**Estado:** adoptado. **Contexto:** se necesita un portafolio accesible sin revelar la aplicación comercial íntegra. **Decisión:** escribir una demo autónoma con contratos limitados, documentar el producto completo con capturas sintéticas. **Consecuencia:** el repositorio es ejecutable pero no cubre todas las funciones de producción.

### ADR-002: SQLite exclusivamente en RAM en la DEMO
**Estado:** adoptado. **Decisión:** conexión `:memory:` recreada al iniciar/restablecer. **Consecuencia:** no quedan bases de datos de prueba en disco y no se abre la DB privada; no es una solución de almacenamiento confidencial ni persistente.

### ADR-003: Centavos enteros, monedas segregadas
**Estado:** adoptado para la DEMO. **Decisión:** validar y convertir valores decimales de entrada a unidades menores enteras; agrupar balances por código ISO. **Consecuencia:** evita error de flotantes de entrada y sumas ARS/USD/EUR; conversión monetaria no implementada.

### ADR-004: Mostrar claramente lo no validado
**Estado:** adoptado. **Decisión:** no anunciar cómputo de plazos jurisdiccionales, firma electrónica/digital verificada ni Windows universal. **Consecuencia:** los reclutadores pueden distinguir evidencia de backlog.

### ADR-005: CI simple y reproducible
**Estado:** workflow incluido; **no ejecutado en GitHub aún**. **Decisión:** correr unittest y compileall en Python multiplataforma mediante GitHub Actions tras publicación. **Consecuencia:** CI no sustituye pruebas gráficas manuales o aceptación en Windows.
