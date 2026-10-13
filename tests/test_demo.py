"""Automated isolated regression checks; no user data or network access."""
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.store import DemoStore, valid_date, money_to_cents, money_text


class DemoTests(unittest.TestCase):
    def setUp(self):self.s=DemoStore()
    def tearDown(self):self.s.close()

    def test_seed_counts(self):
        self.assertEqual(self.s.counts(),{'clientes':6,'expedientes':8,'documentos':6,'agenda':5,'movimientos':6})

    def test_seed_clients_are_anonymous(self):
        labels=[row['name'] for row in self.s.clients()]
        self.assertEqual(sorted(labels), sorted(['Cliente A','Cliente B','Entidad C','Entidad D','Cliente E','Entidad F']))
        self.assertTrue(all('example.invalid' in r['email'] for r in self.s.clients()))

    def test_database_is_in_memory(self):
        db_list=self.s.all('PRAGMA database_list')
        self.assertEqual(db_list[0]['file'],'')

    def test_reset_erases_session_additions(self):
        self.s.add_client('Demo Temporal','Persona','', '')
        self.assertEqual(self.s.counts()['clientes'],7)
        self.s.reset()
        self.assertEqual(self.s.counts()['clientes'],6)

    def test_clients_crud_search(self):
        rid=self.s.add_client('Cliente Test','Persona','a@example.invalid','000-000')
        self.assertTrue(any(r['id']==rid for r in self.s.clients('test')))
        self.s.edit_client(rid,'Cliente Actualizado','Empresa','','')
        self.assertEqual(self.s.one('SELECT kind FROM clients WHERE id=?',(rid,))['kind'],'Empresa')
        self.s.delete_client(rid)
        self.assertIsNone(self.s.one('SELECT * FROM clients WHERE id=?',(rid,)))

    def test_client_fk_delete_is_restricted(self):
        with self.assertRaisesRegex(ValueError,'vinculado'):
            self.s.delete_client(1)

    def test_cases_crud_and_joins(self):
        rid=self.s.add_case('DEMO-100','Consulta simulada',1,'Civil','Abierto','')
        self.assertEqual(self.s.one('SELECT ref FROM cases WHERE id=?',(rid,))['ref'],'DEMO-100')
        self.s.edit_case(rid,'DEMO-100','Actualizado',2,'Comercial','Cerrado','sin caso real')
        self.assertEqual(next(r for r in self.s.cases('DEMO-100') if r['id']==rid)['client_name'],'Cliente B')
        self.s.delete_case(rid)
        self.assertIsNone(self.s.one('SELECT * FROM cases WHERE id=?',(rid,)))

    def test_cases_unique_ref(self):
        with self.assertRaises(ValueError):
            self.s.add_case('DEMO-001','Repetido',1,'Civil','Abierto','')

    def test_sql_strings_are_not_executed(self):
        malicious="'; DROP TABLE clients; --"
        cid=self.s.add_client(malicious,'Persona','','')
        self.assertEqual(self.s.one('SELECT name FROM clients WHERE id=?',(cid,))['name'],malicious)
        self.assertEqual(self.s.counts()['clientes'],7)

    def test_document_create_edit_delete(self):
        rid=self.s.save_document(None,'Escrito ficticio',1,'Texto no jurídico','Borrador')
        self.s.save_document(rid,'Escrito corregido',2,'Nueva redacción','En revisión')
        row=self.s.one('SELECT * FROM documents WHERE id=?',(rid,))
        self.assertEqual((row['title'],row['body'],row['status']),('Escrito corregido','Nueva redacción','En revisión'))
        self.s.delete_document(rid)
        self.assertIsNone(self.s.one('SELECT * FROM documents WHERE id=?',(rid,)))

    def test_linked_document_case_removed_sets_null(self):
        case_id=self.s.add_case('DEMO-101','Baja',1,'Civil','Abierto','')
        doc_id=self.s.save_document(None,'Prueba',case_id,'text','Borrador')
        self.s.delete_case(case_id)
        self.assertIsNone(self.s.one('SELECT case_id FROM documents WHERE id=?',(doc_id,))['case_id'])

    def test_date_validation_and_events(self):
        with self.assertRaises(ValueError):valid_date('2026-02-30')
        with self.assertRaises(ValueError):valid_date('07/10/2026')
        rid=self.s.save_event(None,'2026-10-14','Evento ficticio',1,'Reunión','Nota')
        self.assertEqual(self.s.one('SELECT title FROM events WHERE id=?',(rid,))['title'],'Evento ficticio')
        self.s.delete_event(rid)

    def test_currency_not_combined(self):
        rows={r['currency']:r['balance'] for r in self.s.balances()}
        self.assertEqual(rows,{'ARS':9865000,'EUR':9500,'USD':23700})
        self.assertEqual(money_text(9865000,'ARS'),'ARS 98.650,00')

    def test_money_exact_precision(self):
        self.assertEqual(money_to_cents('0.01'),1)
        self.assertEqual(money_to_cents('1250,50'),125050)
        for s in ['-1','0','1.234','1e3','123.456','abc']:
            with self.subTest(s=s),self.assertRaises(ValueError):money_to_cents(s)

    def test_add_update_remove_finance(self):
        mid=self.s.save_movement(None,'2026-10-13','Ingreso ficticio','Ingreso','ARS','10.01',1)
        self.assertEqual(self.s.one('SELECT cents FROM movements WHERE id=?',(mid,))['cents'],1001)
        self.s.save_movement(mid,'2026-10-13','Egreso ficticio','Egreso','USD','1.03',None)
        self.assertEqual(self.s.one('SELECT currency FROM movements WHERE id=?',(mid,))['currency'],'USD')
        self.s.delete_movement(mid)

    def test_foreign_keys_enabled(self):
        self.assertEqual(self.s.one('PRAGMA foreign_keys')[0],1)
        with self.assertRaises(ValueError):self.s.add_case('DEMO-109','test',99999,'Civil','Abierto','')


if __name__=='__main__':unittest.main(verbosity=2)
