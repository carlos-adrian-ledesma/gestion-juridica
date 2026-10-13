# Publicación en GitHub · checklist operativo

## Repositorio sugerido

Nombre: `gestion-juridica`  
Descripción: `Legal desktop software | Python/Tkinter + SQLite | isolated runnable demo, tested code and full-product UI portfolio`  
Visibilidad: **Public** · Rama: `main` · Topics: `python`, `tkinter`, `sqlite`, `desktop-app`, `legaltech`, `software-engineering`, `portfolio`, `unit-testing`, `windows`, `local-first`.

**No incluir el ZIP FULL SOURCE privado ni su instalador.** Este paquete contiene exclusivamente los archivos de este repositorio público.

## Preparación inicial

1. Crear en la cuenta GitHub un repositorio **vacío** llamado `gestion-juridica`, marcado `Public`. **No** marcar creación automática de README, `.gitignore` o licencia, ya que este paquete trae esos archivos.
2. Extraer el archivo ZIP de entrega y abrir una terminal **en la carpeta que contiene `README.md`, `demo.py` y `.github`**.
3. Ejecutar:

```bash
git init
git branch -M main
git add .
git status --short
git commit -m "Publish isolated legal desktop demo and engineering portfolio"
git remote add origin https://github.com/carlos-adrian-ledesma/gestion-juridica.git
git push -u origin main
```

Si el repositorio ya existe o tiene un commit, **NO usar `git push --force`**: primero revisar y reconciliar su historia.

## Revisiones antes de `git add .`

- Confirmar que solo están los archivos del paquete público: **código DEMO, tests, documentación y 11 imágenes**.
- Verificar que no aparecen `.db`, `.sqlite`, `.env`, `.venv`, `wheelhouse`, logs, respaldos, programas privados o instaladores premium.
- Abrir cada imagen publicada y comprobar que no muestra nombres reales, DNI/CUIT ni información confidencial.
- En el repositorio público, abrir README y comprobar que sus enlaces relativos y sus imágenes renderizan.
- Mirar Actions: ejecutar/confirmar resultados del workflow antes de poner un badge PASS.
- Describir que la DEMO no incluye funciones premium PDF y no está validada para casos reales.

## Perfil profesional

- Agregar `gestion-juridica` al apartado **Pinned** de GitHub para aparecer en el perfil.
- Ajustar `About` con la descripción sugerida, Topics y website (si existe una URL propia verificada).
- Issues: habilitar para reportar problemas de DEMO sin datos privados; no publicar vulnerabilidades sensibles.
- Wiki y Projects: opcionales, no son necesarios si el README y `docs/` están actualizados.
- Releases: **opcional** después de verificar Windows. No adjuntar instaladores premium ni DLLs/wheels no licenciados. Preferir código fuente empaquetado por GitHub hasta confirmar derechos.

## Nota

El package ZIP en sí **no reemplaza** a un repositorio navegable. Se publica su **contenido descomprimido**, para que cada archivo e imagen aparezcan de forma normal en GitHub.
