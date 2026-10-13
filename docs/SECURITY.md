# Security and Privacy / Seguridad y privacidad

## Demo isolation

- `DemoStore` creates a new SQLite database using `:memory:` and **never writes it to disk**.
- No code in this distribution imports or opens the private `gestión_juridica.db`, installation directories, credentials, backups, clients or attached PDFs.
- No third-party dependencies, telemetry, web requests, analytics, cloud services, installers, scheduled tasks, or external processes are required to run the Python app.
- The `.bat` merely invokes a local Python interpreter from the extracted folder; read it before execution if needed.
- Test clients, cases, dates, documents and amounts are synthetic and visibly labeled as examples.

## Important limitations

Data typed into this demo remains in **process memory until the app exits**. It is not a confidential data vault: OS swap, crash dumps, screen captures, or physical access could expose entered text. Do not enter private information or treat the app as fit for professional case work. It contains no authentication, encryption, production audit trail, or legal guarantee.

A sandbox is a design property of this small independent project, **not** a security assessment of the separate full product. No Windows release acceptance was performed here. Avoid accepting files from strangers as if they were authenticated ZIPs.

## GitHub publication controls

Inspect commits and all contents before publishing. Never add `.db`, `.sqlite*`, `Logs`, `Respaldos`, credentials, zip files of the private application, `wheelhouse`, real case files, or user data. This demo has no need for any such resources.
