"""Memoria de demostración. No carga, importa, restaura ni lee datos del producto privado.

Sólo SQLite :memory:; todos los datos creados por el operador se pierden al cerrar.
Licencia reservada: QuintaDimensión Tecnología © 2026.
"""
from __future__ import annotations

import datetime as dt
import re
import sqlite3
from decimal import Decimal, InvalidOperation

DATABASE_URI = ':memory:'
CLIENT_CATEGORIES = ('Persona', 'Empresa', 'Organización')
CASE_STATES = ('Abierto', 'En seguimiento', 'Cerrado')
DOC_STATES = ('Borrador', 'En revisión', 'Finalizado (demo)')
EVENT_KINDS = ('Reunión', 'Recordatorio', 'Vencimiento administrativo', 'Otro')
MONEY_KINDS = ('Ingreso', 'Egreso')
CURRENCIES = ('ARS', 'USD', 'EUR')


def valid_date(value: str) -> str:
    value = str(value).strip()
    try:
        parsed = dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError('Fecha inválida: use AAAA-MM-DD.') from None
    if parsed.isoformat() != value:
        raise ValueError('Fecha inválida: use AAAA-MM-DD.')
    return value


def money_to_cents(value: str) -> int:
    txt = str(value).strip().replace(',', '.')
    if not re.fullmatch(r'\d{1,9}(?:\.\d{1,2})?', txt):
        raise ValueError('Importe inválido. Use un positivo con máximo 2 decimales.')
    try:
        dec = Decimal(txt)
    except InvalidOperation:
        raise ValueError('Importe inválido.') from None
    if not (Decimal('0') < dec <= Decimal('999999999.99')):
        raise ValueError('El importe debe ser positivo y estar dentro del límite de la demo.')
    return int(dec * 100)


def money_text(cents: int, currency: str = '') -> str:
    amount = abs(int(cents))
    major, minor = divmod(amount, 100)
    thousands = f'{major:,}'.replace(',', '.')
    return f'{currency} {"−" if cents < 0 else ""}{thousands},{minor:02d}'.strip()


class DemoStore:
    """Data layer with explicit SQL, FKs, and no persistence by design."""

    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None
        self.reset()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def reset(self) -> None:
        self.close()
        self.connection = sqlite3.connect(DATABASE_URI)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.executescript('''
            CREATE TABLE clients (
                id INTEGER PRIMARY KEY, name TEXT NOT NULL, kind TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT '', phone TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE cases (
                id INTEGER PRIMARY KEY, ref TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
                client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
                category TEXT NOT NULL, status TEXT NOT NULL, notes TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY, title TEXT NOT NULL,
                case_id INTEGER REFERENCES cases(id) ON DELETE SET NULL,
                body TEXT NOT NULL DEFAULT '', status TEXT NOT NULL
            );
            CREATE TABLE events (
                id INTEGER PRIMARY KEY, event_date TEXT NOT NULL, title TEXT NOT NULL,
                case_id INTEGER REFERENCES cases(id) ON DELETE SET NULL,
                kind TEXT NOT NULL, details TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE movements (
                id INTEGER PRIMARY KEY, txn_date TEXT NOT NULL, label TEXT NOT NULL,
                kind TEXT NOT NULL, currency TEXT NOT NULL,
                cents INTEGER NOT NULL CHECK (cents > 0),
                case_id INTEGER REFERENCES cases(id) ON DELETE SET NULL
            );
            CREATE INDEX idx_cases_client ON cases(client_id);
            CREATE INDEX idx_events_date ON events(event_date);
            CREATE INDEX idx_movements_date ON movements(txn_date);
        ''')
        self.seed()

    def seed(self) -> None:
        assert self.connection is not None
        today = dt.date.today()
        clients = [
            ('Cliente A', 'Persona', 'cliente-a@example.invalid', '000-0001'),
            ('Cliente B', 'Persona', 'cliente-b@example.invalid', '000-0002'),
            ('Entidad C', 'Empresa', 'entidad-c@example.invalid', '000-0003'),
            ('Entidad D', 'Organización', 'entidad-d@example.invalid', '000-0004'),
            ('Cliente E', 'Persona', 'cliente-e@example.invalid', '000-0005'),
            ('Entidad F', 'Empresa', 'entidad-f@example.invalid', '000-0006'),
        ]
        cases = [
            ('DEMO-001', 'Consulta contractual de muestra', 1, 'Civil', 'Abierto', 'Sin valor legal'),
            ('DEMO-002', 'Revisión de convenio ficticio', 2, 'Comercial', 'En seguimiento', ''),
            ('DEMO-003', 'Expediente societario inventado', 3, 'Societario', 'Abierto', ''),
            ('DEMO-004', 'Solicitud administrativa de ejemplo', 4, 'Administrativo', 'Cerrado', ''),
            ('DEMO-005', 'Asunto familiar simulado', 5, 'Familia', 'En seguimiento', ''),
            ('DEMO-006', 'Gestión de cobro ilustrativa', 6, 'Comercial', 'Abierto', ''),
            ('DEMO-007', 'Consulta de documentación', 1, 'Civil', 'Cerrado', ''),
            ('DEMO-008', 'Revisión preventiva interna', 3, 'Comercial', 'Abierto', ''),
        ]
        documents = [
            ('Borrador de entrevista inicial', 1, 'Documento de demostración.\n\nEste contenido es completamente ficticio.\nNo constituye un escrito ni asesoramiento jurídico.', 'Borrador'),
            ('Resumen de documentación recibida', 2, 'Listado simulado de documentos para revisión administrativa.', 'En revisión'),
            ('Modelo de nota interna', 3, 'Nota de ejemplo: validar los datos antes de toda presentación real.', 'Borrador'),
            ('Minuta de reunión ficticia', 5, 'Se comentaron alternativas de manera hipotética.', 'Finalizado (demo)'),
            ('Lista de tareas del asunto', 6, '1. Verificar datos ficticios\n2. Organizar documentación\n3. Revisar agenda', 'Borrador'),
            ('Memorando demostrativo', None, 'Vista de funciones básicas de un editor local en modo temporal.', 'En revisión'),
        ]
        events = [
            ((today + dt.timedelta(days=1)).isoformat(), 'Reunión de prueba', 1, 'Reunión', 'Agenda ficticia'),
            ((today + dt.timedelta(days=3)).isoformat(), 'Revisión de borrador', 2, 'Recordatorio', ''),
            ((today + dt.timedelta(days=5)).isoformat(), 'Fecha administrativa ilustrativa', 3, 'Vencimiento administrativo', 'No es plazo judicial calculado'),
            ((today + dt.timedelta(days=9)).isoformat(), 'Llamada de seguimiento', 6, 'Recordatorio', ''),
            ((today + dt.timedelta(days=12)).isoformat(), 'Control de documentos', 5, 'Otro', ''),
        ]
        movs = [
            (today.isoformat(), 'Anticipo simulado', 'Ingreso', 'ARS', 12500000, 1),
            (today.isoformat(), 'Gasto ilustrativo', 'Egreso', 'ARS', 2500000, 2),
            (today.isoformat(), 'Honorario ficticio exterior', 'Ingreso', 'USD', 27500, 3),
            (today.isoformat(), 'Suscripción de muestra', 'Egreso', 'USD', 3800, None),
            (today.isoformat(), 'Servicio demostrativo', 'Ingreso', 'EUR', 9500, 6),
            (today.isoformat(), 'Insumo de prueba', 'Egreso', 'ARS', 135000, None),
        ]
        with self.connection:
            self.connection.executemany('INSERT INTO clients(name,kind,email,phone) VALUES(?,?,?,?)', clients)
            self.connection.executemany('INSERT INTO cases(ref,title,client_id,category,status,notes) VALUES(?,?,?,?,?,?)', cases)
            self.connection.executemany('INSERT INTO documents(title,case_id,body,status) VALUES(?,?,?,?)', documents)
            self.connection.executemany('INSERT INTO events(event_date,title,case_id,kind,details) VALUES(?,?,?,?,?)', events)
            self.connection.executemany('INSERT INTO movements(txn_date,label,kind,currency,cents,case_id) VALUES(?,?,?,?,?,?)', movs)

    def all(self, query: str, params=()) -> list[sqlite3.Row]:
        assert self.connection is not None
        return list(self.connection.execute(query, params))

    def one(self, query: str, params=()) -> sqlite3.Row | None:
        assert self.connection is not None
        return self.connection.execute(query, params).fetchone()

    def execute(self, query: str, params=()) -> int:
        assert self.connection is not None
        with self.connection:
            cursor = self.connection.execute(query, params)
            return int(cursor.lastrowid)

    def clients(self, filter_text=''):
        return self.all('SELECT * FROM clients WHERE lower(name) LIKE ? ORDER BY name', (f'%{filter_text.lower()}%',))

    def cases(self, filter_text=''):
        return self.all('''SELECT cases.*, clients.name AS client_name FROM cases
            JOIN clients ON clients.id=cases.client_id
            WHERE lower(cases.ref || ' ' || cases.title || ' ' || clients.name) LIKE ?
            ORDER BY cases.id DESC''', (f'%{filter_text.lower()}%',))

    def documents(self):
        return self.all('''SELECT documents.*, cases.ref AS case_ref FROM documents
            LEFT JOIN cases ON cases.id=documents.case_id ORDER BY documents.id DESC''')

    def events(self, filter_text=''):
        return self.all('''SELECT events.*, cases.ref AS case_ref FROM events
            LEFT JOIN cases ON cases.id=events.case_id
            WHERE lower(events.title || ' ' || events.event_date) LIKE ? ORDER BY event_date, events.id''',
            (f'%{filter_text.lower()}%',))

    def movements(self, filter_text=''):
        return self.all('''SELECT movements.*, cases.ref AS case_ref FROM movements
            LEFT JOIN cases ON cases.id=movements.case_id
            WHERE lower(movements.label || ' ' || movements.currency || ' ' || movements.txn_date) LIKE ?
            ORDER BY txn_date DESC, movements.id DESC''', (f'%{filter_text.lower()}%',))

    def counts(self) -> dict[str, int]:
        return {key: int(self.one(f'SELECT count(*) AS total FROM {table}')['total']) for key, table in (
            ('clientes','clients'),('expedientes','cases'),('documentos','documents'),
            ('agenda','events'),('movimientos','movements'))}

    def balances(self):
        return self.all('''SELECT currency,
        SUM(CASE WHEN kind='Ingreso' THEN cents ELSE -cents END) AS balance,
        SUM(CASE WHEN kind='Ingreso' THEN cents ELSE 0 END) AS income,
        SUM(CASE WHEN kind='Egreso' THEN cents ELSE 0 END) AS expense
        FROM movements GROUP BY currency ORDER BY currency''')

    def add_client(self, name, kind, email, phone):
        if not name.strip(): raise ValueError('El nombre es obligatorio.')
        if kind not in CLIENT_CATEGORIES: raise ValueError('Categoría no válida.')
        return self.execute('INSERT INTO clients(name,kind,email,phone) VALUES (?,?,?,?)', (name.strip(),kind,email.strip(),phone.strip()))

    def edit_client(self, row_id, name, kind, email, phone):
        if not name.strip(): raise ValueError('El nombre es obligatorio.')
        if kind not in CLIENT_CATEGORIES: raise ValueError('Categoría no válida.')
        self.execute('UPDATE clients SET name=?,kind=?,email=?,phone=? WHERE id=?', (name.strip(),kind,email.strip(),phone.strip(),row_id))

    def delete_client(self, row_id):
        try:
            self.execute('DELETE FROM clients WHERE id=?', (row_id,))
        except sqlite3.IntegrityError:
            raise ValueError('Cliente vinculado a un expediente: elimine o reasigne el asunto primero.') from None

    def add_case(self, ref, title, client_id, category, status, notes):
        if not ref.strip() or not title.strip(): raise ValueError('Referencia y título son obligatorios.')
        if status not in CASE_STATES: raise ValueError('Estado no válido.')
        try:
            return self.execute('''INSERT INTO cases(ref,title,client_id,category,status,notes) VALUES(?,?,?,?,?,?)''',
                (ref.strip(),title.strip(),int(client_id),category.strip(),status,notes.strip()))
        except sqlite3.IntegrityError:
            raise ValueError('Referencia repetida o cliente inexistente.') from None

    def edit_case(self, row_id, ref, title, client_id, category, status, notes):
        if not ref.strip() or not title.strip(): raise ValueError('Referencia y título son obligatorios.')
        if status not in CASE_STATES: raise ValueError('Estado no válido.')
        try:
            self.execute('''UPDATE cases SET ref=?,title=?,client_id=?,category=?,status=?,notes=? WHERE id=?''',
                (ref.strip(),title.strip(),int(client_id),category.strip(),status,notes.strip(),row_id))
        except sqlite3.IntegrityError:
            raise ValueError('Referencia repetida o cliente inexistente.') from None

    def delete_case(self, row_id):
        self.execute('DELETE FROM cases WHERE id=?', (row_id,))

    def save_document(self, row_id, title, case_id, body, status):
        if not title.strip(): raise ValueError('El documento debe tener título.')
        if status not in DOC_STATES: raise ValueError('Estado inválido.')
        if row_id is None:
            return self.execute('INSERT INTO documents(title,case_id,body,status) VALUES (?,?,?,?)',
                (title.strip(),case_id,body,status))
        self.execute('UPDATE documents SET title=?,case_id=?,body=?,status=? WHERE id=?',
            (title.strip(),case_id,body,status,int(row_id)))
        return int(row_id)

    def delete_document(self, row_id):
        self.execute('DELETE FROM documents WHERE id=?', (int(row_id),))

    def save_event(self, row_id, date_value, title, case_id, kind, details):
        valid_date(date_value)
        if not title.strip(): raise ValueError('El evento debe tener título.')
        if kind not in EVENT_KINDS: raise ValueError('Tipo de evento inválido.')
        params=(date_value,title.strip(),case_id,kind,details.strip())
        if row_id is None:
            return self.execute('INSERT INTO events(event_date,title,case_id,kind,details) VALUES(?,?,?,?,?)', params)
        self.execute('UPDATE events SET event_date=?,title=?,case_id=?,kind=?,details=? WHERE id=?', params + (row_id,))
        return row_id

    def delete_event(self, row_id):
        self.execute('DELETE FROM events WHERE id=?', (row_id,))

    def save_movement(self, row_id, date_value, label, kind, currency, amount, case_id):
        valid_date(date_value)
        if not label.strip(): raise ValueError('Concepto obligatorio.')
        if kind not in MONEY_KINDS or currency not in CURRENCIES:
            raise ValueError('Moneda o tipo inválido.')
        cents = money_to_cents(amount)
        params = (date_value,label.strip(),kind,currency,cents,case_id)
        if row_id is None:
            return self.execute('INSERT INTO movements(txn_date,label,kind,currency,cents,case_id) VALUES(?,?,?,?,?,?)', params)
        self.execute('UPDATE movements SET txn_date=?,label=?,kind=?,currency=?,cents=?,case_id=? WHERE id=?', params + (row_id,))
        return row_id

    def delete_movement(self, row_id):
        self.execute('DELETE FROM movements WHERE id=?', (row_id,))
