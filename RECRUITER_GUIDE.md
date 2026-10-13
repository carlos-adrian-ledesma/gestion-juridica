# Recruiter & Hiring Manager Guide · Guía para reclutadores

## Evaluación en 5 minutos

1. Leer [README](README.md): alcance real del producto y capturas del software completo.
2. Abrir [documentación de arquitectura](ARCHITECTURE.md) y su diagrama de responsabilidades.
3. Inspeccionar código de la **DEMO independiente** en [`app/store.py`](app/store.py) y [`demo.py`](demo.py).
4. Revisar [`tests/test_demo.py`](tests/test_demo.py) y ejecutar la suite sin instalar paquetes externos.
5. Comprobar [decisiones de ingeniería](docs/DECISIONS.md), [límites](PORTFOLIO_SCOPE.md) y [seguridad](SECURITY.md).

## Competencias observables

| Competencia | Evidencia localizable |
|---|---|
| Python desktop | `demo.py`, componentes y navegación Tkinter |
| Diseño de datos | `app/store.py`, esquema relacional, llaves foráneas |
| Reglas de negocio | `money_to_cents`, control de referencias y estados |
| Ingeniería defensiva | Consultas parametrizadas y validaciones explícitas |
| QA / regresión | `tests/test_demo.py` (16 casos unitarios) |
| Arquitectura local-first | SQLite en memoria para demo; explicación del producto privado |
| Documentación | Estudios de caso, arquitectura, decisiones, alcance, pruebas, avisos de terceros |
| Gestión de versiones | Etiquetado de DEMO vs Full Source privado y roadmap delimitado |

## Lo que muestra el producto privado

La galería `docs/screenshots/full-product/` exhibe ocho pantallas auténticas de la versión profesional V1.0.6 RC1: Dashboard, Clientes, Casos, Editor, PDF, Agenda, Finanzas y Respaldo. **No** implica que esas funciones estén disponibles en esta DEMO reducida ni que la versión privada haya sido homologada para expedientes reales.

## Conversación técnica sugerida

- ¿Por qué la demo usa `:memory:` en lugar de distribuir una base de ejemplo en disco?
- ¿Cómo se controlan las referencias cuando un cliente tiene casos vinculados?
- ¿Por qué los montos de la demo se representan en centavos enteros?
- ¿Qué diferencias hay entre una vista de PDF y una verificación criptográfica de firma?
- ¿Qué controles hacen falta para convertir un software local de gestión legal en un producto operativo y distribuible?

## Contacto / portfolio

Autor: Carlos Adrián Ledesma (QuintaDimensión Tecnología). Consultar el [perfil de GitHub](https://github.com/carlos-adrian-ledesma) para otros proyectos. La revisión del Full Source privado queda sujeta a autorización expresa; **no forma parte del acceso público**.

---

**English summary:** This repo is an engineering portfolio with a fully inspectable, runnable *isolated sample app*, 16 tested domain/data rules, and clearly labeled captures of the separate full desktop product. Review the [English overview](docs/README_EN.md), [case study](TECHNICAL_CASE_STUDY.md) and [architecture](ARCHITECTURE.md). The public demo is **not** the proprietary product and is not approved for real client/case data.
