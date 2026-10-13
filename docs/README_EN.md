# ABOGADO Y ASOCIADOS — Engineering Portfolio

**Desktop legal practice management · Public isolated DEMO + Screenshots of Private Full Product**  
**QuintaDimensión Tecnología · Python · Tkinter/ttk · SQLite**

[Volver al README en español](../README.md) · [Architecture](../ARCHITECTURE.md) · [Code samples](../CODE_SAMPLES.md) · [Case study](../TECHNICAL_CASE_STUDY.md) · [Recruiter guide](../RECRUITER_GUIDE.md)

## Important distinction

This repository includes a **runnable, self-contained public demonstration** written separately using Python's standard library, plus **eight genuine screenshots of the private full desktop application (V1.0.6 RC1)**. The full product is **not** part of this repository. Features in the full-product screenshots (notably PDF operations, document export and backup/restore) **are not available in the public demo**.

No real people, companies, clients or case information appear in the screenshots: the data are synthetic, using generic labels such as `Client A` or `Entity B` (displayed as `Cliente A`, `Entidad B` in Spanish UI).

## Explore

- [Runnable source — demo.py](../demo.py) · [In-memory SQLite data layer](../app/store.py)
- [16 unit tests](../tests/test_demo.py) · [Verification report](../TESTING.md)
- [Private full-product screenshot gallery](../README.md#4-galería-de-la-edición-privada--full-product-gallery)
- [Architecture and engineering decisions](../ARCHITECTURE.md) · [ADRs](DECISIONS.md)
- [Full product vs public demo feature comparison](DEMO_VS_FULL.md)
- [Privacy](../PRIVACY.md) · [Security](../SECURITY.md) · [Scope](../PORTFOLIO_SCOPE.md)

## Run the public demo

**Requirements:** Python 3.10+ with Tkinter (not a standalone EXE). No `pip install` or online APIs required.

```bash
python demo.py
python -m unittest discover -s tests -v
```

On Windows, double-click `INICIAR_DEMO.bat` from the extracted repository folder.

- Dashboard, synthetic clients/cases, text documents, administrative events and sample finances are interactive.
- Data are stored in SQLite `:memory:` and reset at process exit.
- No production DB is accessed. Do not input real or sensitive legal case data.
- The separate full product is **not approved for live case management**. Windows launcher acceptance and commercial license reviews are still outstanding.

## What it demonstrates

- Tkinter desktop navigation and lightweight workflow UI.
- SQL parameter binding and foreign-key constraints.
- Domain data validation, CRUD operations and safe error handling in a focused sample.
- Minor-unit integer money representation and currency-separated balances.
- Isolated test data with a deterministic reset workflow.
- Regression testing and explicit product/release scope documentation.

**Verified locally:** 16/16 unit tests on Linux and screenshots from Xvfb GUI sessions. A GitHub Actions workflow for Windows/Linux is included **but has not run in GitHub yet**. No claims of licensed PDF redistribution, digital signature validation, judicial deadline calculation or production security certifications are made.

## Contact and terms

Developer: **Carlos Adrián Ledesma**, QuintaDimensión Tecnología. [GitHub](https://github.com/carlos-adrian-ledesma).

© 2026. All rights reserved. Code is proprietary, visible for portfolio evaluation only. See [LICENSE](../LICENSE).
