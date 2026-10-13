# Software Engineering Case Study — Legal Desktop Management

**Owner:** QuintaDimensión Tecnología · **Work:** design, desktop development, persistence, local document workflows, security/QA stabilization and public portfolio separation.

## Contexto / Problem

Un software local de gestión jurídica reúne dominios con distintos riesgos: escritos editables, expedientes vinculados, vencimientos que deben revisarse profesionalmente, finanzas multimoneda, archivos PDF y recuperación. La ingeniería exige distinguir **capacidades de interfaz**, **reglas verificadas** y **habilitación para utilizar datos reales**.

## Diseño de producto completo (privado)

El código V1.0.6 RC1 suministrado para el trabajo interno contiene páginas Tkinter/ttk, almacenamiento SQLite, editor de escritos, área PDF, gestión de clientes/casos, agenda, finanzas y utilidades de respaldo. Las ocho capturas de este repositorio fueron obtenidas del programa ejecutado con datos sintéticos. La edición privada sigue siendo una *release candidate* pendiente de aceptación Windows, endurecimiento y revisión de dependencias/redistribución.

## Problema de publicación

Publicar el ZIP profesional o copiar todas sus dependencias a GitHub expondría implementación propietaria y podría confundir a los visitantes sobre el estado de distribución del motor PDF. En su lugar se preparó una **DEMO nueva y separada**, con persistencia solo en memoria y operaciones explícitamente limitadas.

## Solución técnica que sí está disponible públicamente

1. `demo.py` ofrece seis áreas funcionales de evaluación y navegación sin servidor.
2. `app/store.py` encapsula el esquema SQLite temporal y las reglas de consistencia.
3. Los movimientos monetarios se representan como **centavos enteros**, con balances por moneda.
4. Los registros de partida usan identificadores genéricos (Cliente A, Entidad C, etc.) y dominios de ejemplo.
5. `tests/test_demo.py` permite comprobar 16 comportamientos con la biblioteca estándar.
6. README, guía técnica, matrices y galería separan estrictamente producto privado de muestra ejecutable.

## Verificación observable

- `16/16` pruebas unitarias ejecutadas en Linux al preparar este paquete.
- Capturas visuales generadas desde la aplicación real en entorno gráfico virtual.
- No se distribuyen databases reales, credenciales, wheels ni binarios del producto completo.
- **Sin prueba de aceptación física Windows** al momento de empaquetar este portafolio.

## Decisiones y trade-offs

- Demo en memoria → muy fácil de restablecer y auditar; no persiste información.
- Toolkit estándar → evita dependencias comerciales en el paquete público; requiere Python/Tkinter instalado.
- Portfolio de código mínimo → prueba habilidades acotadas; no reemplaza acceso al sistema completo para una auditoría profunda.
- Muestras del producto completo → permiten demostrar alcance de diseño sin prometer funciones que la DEMO no contiene.

## Pendientes antes de venta u operación jurídica

Aceptar en Windows, revisar licencias del motor PDF, validar recuperación ante fallos, proteger respaldos, revisar roles/permisos, precisión financiera y límites jurisdiccionales. **No se certifica aptitud para expedientes reales.**

[Full scope](PORTFOLIO_SCOPE.md) · [Test report](TESTING.md) · [Decisiones de arquitectura](docs/DECISIONS.md)
