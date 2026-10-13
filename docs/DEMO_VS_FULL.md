# Matriz de alcance — DEMO ejecutable vs. producto privado

| Área | DEMO pública ejecutable | Edición completa V1.0.6 RC1 (capturas y código inspeccionado) |
|---|---|---|
| Dashboard | Métricas de fixtures y saldos por moneda | Panel del estudio con métricas, próximos eventos y actividad |
| Clientes | CRUD simple, búsqueda, FK | Fichas más amplias, contacto, historial y referencias |
| Casos/expedientes | CRUD básico y asociación de cliente | Campos jurisdiccionales, etapas, roles y seguimiento |
| Documentos | Editor limitado, guardado temporal y aviso por cambios | Editor jurídico, versiones y opciones exportación |
| PDF | **No incluido** | Vista PDF, zoom, búsqueda, opciones de resaltado/subrayado/comentario; requiere motor PDF privado |
| Agenda | Eventos administrativos manuales | Eventos y vencimientos; **no cómputo judicial certificado** |
| Finanzas | Ingresos/egresos y monedas separadas, solo en memoria | Honorarios, gastos, estados y registros vinculados |
| Backup/restore | **No incluido** | Página y herramientas; operación con datos reales **no validada** |
| Auditoría / papelera / pruebas | No incluidas | Pestañas en aplicación privada |
| Roles y cifrado | No incluidos | No afirmar RBAC ni cifrado integral sin pruebas |
| Almacenamiento | Solo SQLite `:memory:` | SQLite y archivos locales fuera del repositorio |
| Uso con expedientes reales | **Prohibido en la DEMO** | **Pendiente de aceptación técnica/legal** |

**Evidencia:** estructura del código fuente privado suministrado y capturas reales obtenidas con fixtures; no se deduce certificación, garantía legal o funcionalidad end-to-end por una pantalla visible.
