# Screenshot Provenance / Origen de capturas

## Capturas del producto privado (8 PNG)

Ruta: `docs/screenshots/full-product/`. Tomadas de **ABOGADO Y ASOCIADOS PRIVATE FULL SOURCE V1.0.6 RC1**, durante una sesión Tkinter real en Linux con pantalla virtual Xvfb, resolución de ventana **1540×920**. Se estableció una ruta aislada de datos y se generaron **fixtures**: clientes genéricos, casos demostrativos, documentos neutros, finanzas sintéticas, eventos y un PDF artificial. Ninguna base privada del usuario fue copiada al portafolio.

- La identidad de la aplicación/logo se conserva; los clientes y contrapartes aparecen únicamente como `Cliente A`, `Entidad B`, `Parte demandada` o identificadores análogos.
- No hay nombres propios de clientes ni razón social de empresas. Los campos de DNI/CUIT/teléfono se dejaron vacíos en el dataset final; las direcciones de email del dataset usan `example.invalid`.
- La imagen PDF muestra un documento creado para pruebas; la columna de firma dice **No**. No se ha validado firma digital.
- Son capturas **del producto completo**, no del código DEMO descargable. Que exista un botón no demuestra que haya pasado pruebas de aceptación Windows o que sea lícito distribuir su dependencia.

## Capturas de la DEMO (3 PNG)

Ruta: `screenshots/`. Obtenidas al ejecutar `demo.py` bajo Xvfb con registros anónimos (`Cliente A`, `Entidad C`, `DEMO-*`). Las tres capturas muestran panel, documentos y casos de la aplicación reducida.

## Transparencia

No se inventaron interfaces mediante herramientas de ilustración: se capturaron ventanas Tkinter ejecutadas. No se publica en este repositorio la base temporal de capturas, el script de generación del producto privado, código premium, ruedas de paquetes ni material jurídico real.
