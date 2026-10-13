"""ABOGADO Y ASOCIADOS · DEMO PÚBLICA AUTÓNOMA

Implementación de demostración original: NO reutiliza módulos del Full Source privado.
Sólo Python stdlib (Tkinter + SQLite :memory:). Sin acceso a bases reales.
Copyright © 2026 QuintaDimensión Tecnología. Todos los derechos reservados.
"""
from __future__ import annotations

import datetime as dt
import sys
sys.dont_write_bytecode = True  # no .pyc generado al lanzar la aplicación
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from app.store import (
    DemoStore, CLIENT_CATEGORIES, CASE_STATES, DOC_STATES,
    EVENT_KINDS, MONEY_KINDS, CURRENCIES, money_text,
)

VERSION = '1.0.0-demo.1'
COLOR = {
    'bg':'#101820', 'panel':'#1b2633', 'panel2':'#253343', 'selected':'#163f61',
    'line':'#39495a','gold':'#d9b365', 'txt':'#f3f5f8','sub':'#b4c0cc',
    'ok':'#55c799','warn':'#f1bd67','red':'#ff9d9d','paper':'#f7f7f4',
}
NAV = [
    ('Panel jurídico','Panel jurídico'), ('Clientes','Clientes'),
    ('Casos y expedientes','Casos y expedientes'), ('Documentos','Documentos'),
    ('Agenda','Agenda'), ('Honorarios y finanzas','Honorarios y finanzas'),
    ('Acerca de la demo','Acerca de la demo'),
]


def button(parent, title, cmd, accent=False):
    return ttk.Button(parent, text=title, style='Accent.TButton' if accent else 'TButton', command=cmd)


def label(parent, title, size=10, bold=False, color='txt', **kwargs):
    f = ('Segoe UI Semibold' if bold else 'Segoe UI', size)
    return tk.Label(parent, text=title, font=f, bg=COLOR['bg'], fg=COLOR[color], **kwargs)


class DataDialog(tk.Toplevel):
    """Typed entry form with no disk writes."""
    def __init__(self, parent, title, fields, values=None):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.resizable(True, False)
        self.configure(bg=COLOR['panel'])
        self.result = None
        values = values or {}
        self.vars = {}
        content = tk.Frame(self, bg=COLOR['panel'], padx=24, pady=18)
        content.pack(fill='both', expand=True)
        tk.Label(content,text=title,fg=COLOR['gold'],bg=COLOR['panel'],font=('Segoe UI Semibold',15)).pack(anchor='w',pady=(0,12))
        for key,caption,opts in fields:
            tk.Label(content,text=caption,bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',10)).pack(anchor='w',pady=(8,3))
            default = str(values.get(key,'') or '')
            if isinstance(opts, (tuple,list)):
                if not default: default=str(opts[0]) if opts else ''
                var=tk.StringVar(value=default)
                widget=ttk.Combobox(content,textvariable=var,values=opts,state='readonly',width=53)
            else:
                var=tk.StringVar(value=default)
                widget=ttk.Entry(content,textvariable=var,width=56)
            widget.pack(fill='x')
            self.vars[key]=var
        bar=tk.Frame(content,bg=COLOR['panel']);bar.pack(fill='x',pady=(20,0))
        button(bar,'Cancelar',self.destroy).pack(side='right',padx=(10,0))
        button(bar,'Guardar',self.finish,True).pack(side='right')
        self.bind('<Escape>',lambda _event:self.destroy())
        self.bind('<Return>',lambda _event:self.finish())
        self.grab_set()
        self.geometry('540x'+str(min(790,165+len(fields)*79)))
        self.after_idle(self.focus_first)

    def focus_first(self):
        for widget in self.winfo_children()[0].winfo_children():
            if isinstance(widget,(ttk.Entry,ttk.Combobox)):
                widget.focus_set();break

    def finish(self):
        self.result={key:var.get() for key,var in self.vars.items()}
        self.destroy()


class LegalDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ABOGADO Y ASOCIADOS — Demostración pública | QuintaDimensión Tecnología')
        self.configure(bg=COLOR['bg'])
        self.geometry('1360x820')
        self.minsize(1020,660)
        self.store=DemoStore()
        self.current_page=''
        self.active_document=None
        self.doc_dirty=False
        self.doc_loading=False
        self.doc_title=None
        self.doc_text=None
        self.doc_status=None
        self.doc_case=None
        self.nav_widgets={}
        self._styles()
        self._shell()
        self.show('Panel jurídico')
        self.protocol('WM_DELETE_WINDOW',self.exit_app)

    def _styles(self):
        st=ttk.Style(self)
        st.theme_use('clam')
        st.configure('TFrame',background=COLOR['bg'])
        st.configure('TButton',font=('Segoe UI',10),padding=(13,8),foreground=COLOR['txt'],background=COLOR['panel2'],borderwidth=0)
        st.map('TButton',background=[('active',COLOR['selected'])])
        st.configure('Accent.TButton',font=('Segoe UI Semibold',10),padding=(14,8),foreground='#142131',background=COLOR['gold'],borderwidth=0)
        st.map('Accent.TButton',background=[('active','#f1cf85')])
        st.configure('TEntry',padding=7,fieldbackground=COLOR['panel2'],foreground=COLOR['txt'],insertcolor=COLOR['txt'],bordercolor=COLOR['line'])
        st.configure('TCombobox',padding=6,fieldbackground=COLOR['panel2'],foreground=COLOR['txt'],background=COLOR['panel2'],arrowcolor=COLOR['txt'])
        st.map('TCombobox',fieldbackground=[('readonly',COLOR['panel2'])],foreground=[('readonly',COLOR['txt'])],selectforeground=[('readonly',COLOR['txt'])],selectbackground=[('readonly',COLOR['selected'])])
        st.configure('Treeview',rowheight=34,fieldbackground=COLOR['panel'],background=COLOR['panel'],foreground=COLOR['txt'],borderwidth=0,font=('Segoe UI',10))
        st.map('Treeview',background=[('selected',COLOR['selected'])],foreground=[('selected','#ffffff')])
        st.configure('Treeview.Heading',background=COLOR['panel2'],foreground=COLOR['txt'],relief='flat',font=('Segoe UI Semibold',10),padding=(8,10))
        st.map('Treeview.Heading',background=[('active',COLOR['selected'])])

    def _shell(self):
        self.sidebar=tk.Frame(self,bg=COLOR['panel'],width=266)
        self.sidebar.pack(side='left',fill='y')
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text='QUINTADIMENSIÓN',font=('Segoe UI Semibold',10),bg=COLOR['panel'],fg=COLOR['gold']).pack(anchor='w',padx=20,pady=(28,8))
        tk.Label(self.sidebar,text='ABOGADO Y\nASOCIADOS',justify='left',font=('Segoe UI Semibold',20),bg=COLOR['panel'],fg=COLOR['txt']).pack(anchor='w',padx=20)
        tk.Frame(self.sidebar,height=2,bg=COLOR['gold']).pack(fill='x',padx=20,pady=(15,6))
        tk.Label(self.sidebar,text='GESTIÓN JURÍDICA  ·  DEMO',font=('Segoe UI Semibold',9),bg=COLOR['panel'],fg=COLOR['sub']).pack(anchor='w',padx=20,pady=(0,23))
        for name,_ in NAV:
            tab=tk.Label(self.sidebar,text='   '+name,bg=COLOR['panel'],fg=COLOR['txt'],font=('Segoe UI',11),anchor='w',height=2,cursor='hand2')
            tab.pack(fill='x',padx=10,pady=2)
            tab.bind('<Button-1>',lambda _e,k=name:self.show(k))
            self.nav_widgets[name]=tab
        tk.Frame(self.sidebar,bg=COLOR['panel']).pack(fill='both',expand=True)
        tk.Label(self.sidebar,text='MODO DEMOSTRACIÓN',bg=COLOR['panel'],fg=COLOR['ok'],font=('Segoe UI Semibold',10)).pack(anchor='w',padx=20)
        tk.Label(self.sidebar,text='Sólo datos ficticios · Memoria temporal',bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',9)).pack(anchor='w',padx=20,pady=(3,20))
        self.main=tk.Frame(self,bg=COLOR['bg']);self.main.pack(side='left',fill='both',expand=True)
        head=tk.Frame(self.main,bg=COLOR['panel'],height=66)
        head.pack(fill='x');head.pack_propagate(False)
        self.headtext=tk.Label(head,text='',bg=COLOR['panel'],fg=COLOR['txt'],font=('Segoe UI Semibold',14))
        self.headtext.pack(side='left',padx=24)
        button(head,'Restablecer datos',self.reset_demo).pack(side='right',padx=(0,15),pady=12)
        tk.Label(head,text='DEMO PÚBLICA',bg=COLOR['selected'],fg=COLOR['gold'],font=('Segoe UI Semibold',9),padx=12,pady=5).pack(side='right',padx=12)
        self.page=tk.Frame(self.main,bg=COLOR['bg'])
        self.page.pack(fill='both',expand=True,padx=25,pady=(20,6))
        foot=tk.Frame(self.main,bg=COLOR['bg'],height=31)
        foot.pack(fill='x',padx=24)
        tk.Label(foot,text='© 2026 QuintaDimensión Tecnología  •  Sin conexión a estudios, expedientes ni servidores reales',bg=COLOR['bg'],fg=COLOR['sub'],font=('Segoe UI',9)).pack(anchor='w',pady=(4,0))

    def exit_app(self):
        if not self._check_document(): return
        self.store.close();self.destroy()

    def reset_demo(self):
        if not self._check_document():return
        if not messagebox.askyesno('Restablecer demostración','¿Volver a crear todos los datos ficticios de esta sesión?\n\nSe perderán los cambios de la demo.',parent=self):return
        self.store.reset(); self.current_page=''; self.active_document=None; self.doc_dirty=False
        self.show('Panel jurídico')

    def show(self, name):
        if name != self.current_page and not self._check_document(): return
        if name not in dict(NAV): return
        for item in self.page.winfo_children(): item.destroy()
        self.current_page=name
        self.headtext.configure(text=name)
        for key,widget in self.nav_widgets.items():
            widget.configure(bg=COLOR['selected'] if key==name else COLOR['panel'], fg=COLOR['gold'] if key==name else COLOR['txt'])
        mapping={
            'Panel jurídico':self.dashboard,
            'Clientes':self.client_page,
            'Casos y expedientes':self.case_page,
            'Documentos':self.document_page,
            'Agenda':self.agenda_page,
            'Honorarios y finanzas':self.finance_page,
            'Acerca de la demo':self.about,
        }
        mapping[name]()

    def intro(self,title,description):
        label(self.page,title,22,True).pack(anchor='w',pady=(1,8))
        label(self.page,description,10,color='sub').pack(anchor='w',pady=(0,20))

    def dashboard(self):
        self.intro('Panel de gestión jurídica','Vista de ejemplo con información generada para demostrar la organización administrativa.')
        frame=tk.Frame(self.page,bg=COLOR['bg']);frame.pack(fill='x')
        for col,(caption,val) in enumerate(self.store.counts().items()):
            frame.grid_columnconfigure(col,weight=1)
            card=tk.Frame(frame,bg=COLOR['panel'],padx=15,pady=16)
            card.grid(row=0,column=col,sticky='nsew',padx=(0,11 if col<4 else 0))
            tk.Label(card,text=caption.upper(),bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',9)).pack(anchor='w')
            tk.Label(card,text=str(val),bg=COLOR['panel'],fg=COLOR['gold'],font=('Segoe UI Semibold',28)).pack(anchor='w')
        mid=tk.Frame(self.page,bg=COLOR['bg']);mid.pack(fill='both',expand=True,pady=(22,0))
        left=tk.Frame(mid,bg=COLOR['panel'],padx=18,pady=16);left.pack(side='left',fill='both',expand=True,padx=(0,10))
        right=tk.Frame(mid,bg=COLOR['panel'],padx=18,pady=16,width=315);right.pack(side='right',fill='y');right.pack_propagate(False)
        tk.Label(left,text='AGENDA PRÓXIMA',bg=COLOR['panel'],fg=COLOR['gold'],font=('Segoe UI Semibold',11)).pack(anchor='w',pady=(0,14))
        events=self.store.events()[:5]
        for entry in events:
            line=tk.Frame(left,bg=COLOR['panel2'],padx=12,pady=9);line.pack(fill='x',pady=4)
            tk.Label(line,text=entry['event_date'],bg=COLOR['panel2'],fg=COLOR['gold'],font=('Segoe UI Semibold',10)).pack(side='left',padx=(0,18))
            tk.Label(line,text=entry['title'],bg=COLOR['panel2'],fg=COLOR['txt'],font=('Segoe UI',10)).pack(side='left')
        tk.Label(right,text='RESUMEN POR MONEDA',bg=COLOR['panel'],fg=COLOR['gold'],font=('Segoe UI Semibold',11)).pack(anchor='w',pady=(0,14))
        for row in self.store.balances():
            card=tk.Frame(right,bg=COLOR['panel2'],padx=12,pady=12);card.pack(fill='x',pady=5)
            tk.Label(card,text=row['currency'],bg=COLOR['panel2'],fg=COLOR['sub'],font=('Segoe UI Semibold',10)).pack(anchor='w')
            tk.Label(card,text=money_text(row['balance'],row['currency']),bg=COLOR['panel2'],fg=COLOR['ok'] if row['balance']>=0 else COLOR['red'],font=('Segoe UI Semibold',18)).pack(anchor='w')
        tk.Label(right,text='No se suman ni convierten monedas.',bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',9)).pack(anchor='w',pady=(13,0))

    def table_page(self,title,subtitle,columns,headings,rows,add,edit,remove,search=True):
        self.intro(title,subtitle)
        tools=tk.Frame(self.page,bg=COLOR['bg']);tools.pack(fill='x',pady=(0,14))
        button(tools,'+ Nuevo',add,True).pack(side='left',padx=(0,8))
        button(tools,'Editar selección',edit).pack(side='left',padx=(0,8))
        button(tools,'Eliminar de la demo',remove).pack(side='left')
        filter_var=tk.StringVar()
        if search:
            entry=ttk.Entry(tools,textvariable=filter_var,width=32)
            entry.pack(side='right')
            label(tools,'Buscar:',10,color='sub').pack(side='right',padx=(0,10))
        area=tk.Frame(self.page,bg=COLOR['bg']);area.pack(fill='both',expand=True)
        tree=ttk.Treeview(area,columns=columns,show='headings',selectmode='browse')
        for c,h in zip(columns,headings):
            tree.heading(c,text=h)
            tree.column(c,width=140 if c not in ('title','name','label') else 250,anchor='w',stretch=True)
        scroll=ttk.Scrollbar(area,orient='vertical',command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left',fill='both',expand=True)
        scroll.pack(side='right',fill='y')
        return tree,filter_var

    def _selected(self,tree):
        sel=tree.selection()
        if not sel:
            messagebox.showinfo('Seleccione una fila','Elegí un registro para continuar.',parent=self)
            return None
        return int(sel[0])

    def _form(self,title,fields,values=None):
        dialog=DataDialog(self,title,fields,values)
        self.wait_window(dialog)
        return dialog.result

    def _client_options(self):
        return {f"{r['id']} · {r['name']}":r['id'] for r in self.store.clients()}

    def _case_options(self,allow_empty=True):
        d={f"{r['id']} · {r['ref']} — {r['title']}":r['id'] for r in self.store.cases()}
        if allow_empty: return {'Sin vincular':None,**d}
        return d

    @staticmethod
    def _option_by_id(options,selected):
        return next((k for k,v in options.items() if v == selected),next(iter(options),'Sin vincular'))

    def _handle(self,fn):
        try:
            fn();return True
        except (ValueError,sqlite3.Error) as exc:
            messagebox.showerror('No se pudo guardar',str(exc),parent=self)
            return False

    def _refresh_tree(self,tree,data,make_values):
        for child in tree.get_children():tree.delete(child)
        for row in data:tree.insert('','end',iid=str(row['id']),values=make_values(row))

    def client_page(self):
        t=None
        def refresh(*_): self._refresh_tree(t,self.store.clients(q.get()),lambda r:(r['name'],r['kind'],r['email'],r['phone']))
        fields=[('name','Nombre / Razón social',None),('kind','Tipo',CLIENT_CATEGORIES),('email','Correo ficticio',None),('phone','Teléfono ficticio',None)]
        def form(edit=False):
            row_id=self._selected(t) if edit else None
            if edit and row_id is None:return
            r=self.store.one('SELECT * FROM clients WHERE id=?',(row_id,)) if edit else None
            result=self._form('Editar cliente' if edit else 'Nuevo cliente',fields,dict(r) if r else None)
            if result is None:return
            if self._handle(lambda:(self.store.edit_client(row_id,**result) if edit else self.store.add_client(**result))):refresh()
        def remove():
            row_id=self._selected(t)
            if row_id is None:return
            if messagebox.askyesno('Eliminar cliente de demo','¿Eliminar el cliente seleccionado de esta sesión?',parent=self):
                if self._handle(lambda:self.store.delete_client(row_id)):refresh()
        t,q=self.table_page('Clientes','Administración básica con vínculos a expedientes ficticios.',('name','kind','email','phone'),('Nombre / Razón social','Tipo','Correo','Teléfono'),[],lambda:form(),lambda:form(True),remove)
        q.trace_add('write',refresh);refresh();t.bind('<Double-1>',lambda _e:form(True))

    def case_page(self):
        t=None
        def refresh(*_):self._refresh_tree(t,self.store.cases(q.get()),lambda r:(r['ref'],r['title'],r['client_name'],r['category'],r['status']))
        def form(edit=False):
            row_id=self._selected(t) if edit else None
            if edit and row_id is None:return
            r=self.store.one('SELECT * FROM cases WHERE id=?',(row_id,)) if edit else None
            opts=self._client_options()
            if not opts:messagebox.showinfo('Sin clientes','Creá primero un cliente de demo.',parent=self);return
            fields=[('ref','Referencia',None),('title','Título',None),('client_id','Cliente vinculado',tuple(opts)),('category','Rama / área',None),('status','Estado',CASE_STATES),('notes','Nota breve',None)]
            vals=dict(r) if r else {'ref':'DEMO-','status':'Abierto','category':'Civil'}
            vals['client_id']=self._option_by_id(opts,vals.get('client_id'))
            data=self._form('Editar expediente' if edit else 'Nuevo expediente',fields,vals)
            if data is None:return
            data['client_id']=opts[data['client_id']]
            if self._handle(lambda:(self.store.edit_case(row_id,**data) if edit else self.store.add_case(**data))):refresh()
        def remove():
            row_id=self._selected(t)
            if row_id is None:return
            if messagebox.askyesno('Eliminar expediente','¿Quitar este expediente de la sesión demo? Los documentos/eventos asociados se desvincularán.',parent=self):
                if self._handle(lambda:self.store.delete_case(row_id)):refresh()
        t,q=self.table_page('Casos y expedientes','Seguimiento administrativo ilustrativo; no hay conexión a tribunales.',('ref','title','client','category','status'),('Referencia','Asunto','Cliente','Área','Estado'),[],lambda:form(),lambda:form(True),remove)
        q.trace_add('write',refresh);refresh();t.bind('<Double-1>',lambda _e:form(True))

    def agenda_page(self):
        t=None
        def refresh(*_):self._refresh_tree(t,self.store.events(q.get()),lambda r:(r['event_date'],r['title'],r['case_ref'] or '—',r['kind'],r['details']))
        def form(edit=False):
            row_id=self._selected(t) if edit else None
            if edit and row_id is None:return
            r=self.store.one('SELECT * FROM events WHERE id=?',(row_id,)) if edit else None
            opts=self._case_options()
            vals=dict(r) if r else {'event_date':dt.date.today().isoformat(),'kind':'Recordatorio'}
            vals['case_id']=self._option_by_id(opts,vals.get('case_id'))
            fields=[('event_date','Fecha (AAAA-MM-DD)',None),('title','Título',None),('case_id','Expediente',tuple(opts)),('kind','Tipo',EVENT_KINDS),('details','Descripción breve',None)]
            data=self._form('Editar evento' if edit else 'Nuevo evento',fields,vals)
            if data is None:return
            data['case_id']=opts[data['case_id']]
            if self._handle(lambda:self.store.save_event(row_id,data['event_date'],data['title'],data['case_id'],data['kind'],data['details'])):refresh()
        def remove():
            row_id=self._selected(t)
            if row_id is not None and messagebox.askyesno('Quitar evento','¿Eliminar este evento ficticio?',parent=self):
                if self._handle(lambda:self.store.delete_event(row_id)):refresh()
        t,q=self.table_page('Agenda y vencimientos','Fechas manuales administrativas. No calcula plazos judiciales ni feriados legales.',('date','title','case','kind','details'),('Fecha','Evento','Caso','Tipo','Detalle'),[],lambda:form(),lambda:form(True),remove)
        q.trace_add('write',refresh);refresh();t.bind('<Double-1>',lambda _e:form(True))

    def finance_page(self):
        t=None
        def refresh(*_):
            self._refresh_tree(t,self.store.movements(q.get()),lambda r:(r['txn_date'],r['label'],r['kind'],r['currency'],money_text(r['cents'],r['currency']),r['case_ref'] or '—'))
        def form(edit=False):
            row_id=self._selected(t) if edit else None
            if edit and row_id is None:return
            r=self.store.one('SELECT * FROM movements WHERE id=?',(row_id,)) if edit else None
            opts=self._case_options()
            vals=dict(r) if r else {'txn_date':dt.date.today().isoformat(),'kind':'Ingreso','currency':'ARS','amount':'0.01'}
            vals['case_id']=self._option_by_id(opts,vals.get('case_id'))
            if r:vals['amount']=f"{r['cents']//100}.{r['cents']%100:02d}"
            fields=[('txn_date','Fecha (AAAA-MM-DD)',None),('label','Concepto',None),('kind','Movimiento',MONEY_KINDS),('currency','Moneda',CURRENCIES),('amount','Importe positivo (ej.: 1250.50)',None),('case_id','Expediente',tuple(opts))]
            data=self._form('Editar movimiento' if edit else 'Nuevo movimiento',fields,vals)
            if data is None:return
            data['case_id']=opts[data['case_id']]
            if self._handle(lambda:self.store.save_movement(row_id,data['txn_date'],data['label'],data['kind'],data['currency'],data['amount'],data['case_id'])):refresh()
        def remove():
            row_id=self._selected(t)
            if row_id is not None and messagebox.askyesno('Quitar movimiento','¿Eliminar esta entrada ficticia?',parent=self):
                if self._handle(lambda:self.store.delete_movement(row_id)):refresh()
        t,q=self.table_page('Honorarios y finanzas','Importes en centavos enteros. ARS, USD y EUR se informan por separado.',('date','label','kind','currency','amount','case'),('Fecha','Concepto','Tipo','Moneda','Monto','Caso'),[],lambda:form(),lambda:form(True),remove)
        q.trace_add('write',refresh);refresh();t.bind('<Double-1>',lambda _e:form(True))

    def document_page(self):
        self.intro('Editor de documentos · Demo','Escritura de prueba sin exportación ni guardado en disco. Confirmación antes de descartar cambios.')
        self.active_document=None;self.doc_dirty=False
        tools=tk.Frame(self.page,bg=COLOR['bg']);tools.pack(fill='x',pady=(0,12))
        button(tools,'+ Documento nuevo',self._new_doc).pack(side='left',padx=(0,8))
        button(tools,'Guardar en memoria',self._save_doc,True).pack(side='left',padx=(0,8))
        button(tools,'Eliminar documento',self._remove_doc).pack(side='left')
        self.doc_note=label(tools,'',9,color='warn');self.doc_note.pack(side='right')
        body=tk.Frame(self.page,bg=COLOR['bg']);body.pack(fill='both',expand=True)
        left=tk.Frame(body,bg=COLOR['panel'],width=265,padx=8,pady=10);left.pack(side='left',fill='y',padx=(0,13));left.pack_propagate(False)
        tk.Label(left,text='DOCUMENTOS FICTICIOS',bg=COLOR['panel'],fg=COLOR['gold'],font=('Segoe UI Semibold',10)).pack(anchor='w',padx=7,pady=(2,12))
        self.doc_list=tk.Listbox(left,bg=COLOR['panel2'],fg=COLOR['txt'],selectbackground=COLOR['selected'],selectforeground=COLOR['txt'],borderwidth=0,activestyle='none',font=('Segoe UI',10),highlightthickness=0)
        self.doc_list.pack(fill='both',expand=True,padx=6,pady=(0,7))
        self.doc_list.bind('<<ListboxSelect>>',self._select_doc)
        editor=tk.Frame(body,bg=COLOR['panel'],padx=15,pady=13)
        editor.pack(side='left',fill='both',expand=True)
        tk.Label(editor,text='TÍTULO',bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',9)).pack(anchor='w')
        self.doc_title=tk.StringVar()
        ttk.Entry(editor,textvariable=self.doc_title,font=('Segoe UI',11)).pack(fill='x',pady=(5,12))
        self.doc_title.trace_add('write',lambda *_:self._doc_changed())
        pair=tk.Frame(editor,bg=COLOR['panel']);pair.pack(fill='x',pady=(0,12))
        tk.Label(pair,text='Estado:',bg=COLOR['panel'],fg=COLOR['sub']).pack(side='left',padx=(0,8))
        self.doc_status=tk.StringVar(value='Borrador')
        ttk.Combobox(pair,textvariable=self.doc_status,values=DOC_STATES,state='readonly',width=21).pack(side='left',padx=(0,25))
        tk.Label(pair,text='Caso:',bg=COLOR['panel'],fg=COLOR['sub']).pack(side='left',padx=(0,8))
        self.doc_case=tk.StringVar()
        self.doc_case_options=self._case_options()
        ttk.Combobox(pair,textvariable=self.doc_case,values=tuple(self.doc_case_options),state='readonly',width=33).pack(side='left')
        self.doc_status.trace_add('write',lambda *_:self._doc_changed())
        self.doc_case.trace_add('write',lambda *_:self._doc_changed())
        self.doc_text=tk.Text(editor,wrap='word',font=('Segoe UI',11),bg=COLOR['paper'],fg='#1b2734',insertbackground='#1b2734',undo=True,relief='flat',padx=16,pady=14)
        self.doc_text.pack(fill='both',expand=True)
        self.doc_text.bind('<<Modified>>',self._doc_text_modified)
        self._reload_doc_list()
        self._new_doc(ignore_check=True)

    def _reload_doc_list(self):
        self.doc_index=[r['id'] for r in self.store.documents()]
        self.doc_list.delete(0,'end')
        for r in self.store.documents(): self.doc_list.insert('end',f"{r['title'][:35]}")
        if self.active_document in self.doc_index:
            index=self.doc_index.index(self.active_document)
            self.doc_list.selection_set(index)

    def _doc_text_modified(self,_event=None):
        if self.doc_text is None:return
        if self.doc_text.edit_modified():
            self.doc_text.edit_modified(False)
            self._doc_changed()

    def _doc_changed(self):
        if self.doc_loading or self.current_page!='Documentos':return
        self.doc_dirty=True
        if hasattr(self,'doc_note') and self.doc_note.winfo_exists(): self.doc_note.config(text='• Cambios sin guardar')

    def _check_document(self):
        if self.current_page!='Documentos' or not self.doc_dirty:return True
        answer=messagebox.askyesnocancel('Cambios no guardados','El escrito contiene cambios que sólo existen en esta sesión.\n\n¿Guardarlos en memoria antes de continuar?',parent=self)
        if answer is None:return False
        if answer is True:return self._save_doc()
        self.doc_dirty=False
        return True

    def _new_doc(self,ignore_check=False):
        if not ignore_check and not self._check_document():return
        self._set_doc(None,'','Borrador',None,'')
        self.doc_list.selection_clear(0,'end')

    def _set_doc(self,row_id,title,status,case_id,body):
        self.doc_loading=True
        try:
            self.active_document=row_id
            self.doc_title.set(title)
            self.doc_status.set(status)
            self.doc_case.set(self._option_by_id(self.doc_case_options,case_id))
            self.doc_text.delete('1.0','end')
            self.doc_text.insert('1.0',body)
            self.doc_text.edit_modified(False)
            self.doc_dirty=False
            self.doc_note.config(text='Guardado en memoria' if row_id else 'Nuevo sin guardar')
        finally:self.doc_loading=False

    def _select_doc(self,_event=None):
        selection=self.doc_list.curselection()
        if not selection:return
        new_id=self.doc_index[selection[0]]
        if new_id==self.active_document:return
        if not self._check_document():
            self.doc_list.selection_clear(0,'end')
            if self.active_document in self.doc_index:self.doc_list.selection_set(self.doc_index.index(self.active_document))
            return
        r=self.store.one('SELECT * FROM documents WHERE id=?',(new_id,))
        if r:self._set_doc(r['id'],r['title'],r['status'],r['case_id'],r['body'])

    def _save_doc(self):
        def write():
            body=self.doc_text.get('1.0','end-1c')
            case_id=self.doc_case_options.get(self.doc_case.get())
            self.active_document=self.store.save_document(self.active_document,self.doc_title.get(),case_id,body,self.doc_status.get())
        ok=self._handle(write)
        if ok:
            self.doc_dirty=False;self.doc_note.config(text='Guardado en memoria')
            self._reload_doc_list()
        return ok

    def _remove_doc(self):
        if self.active_document is None:
            self._new_doc();return
        if not messagebox.askyesno('Eliminar documento','¿Quitar este documento ficticio de la sesión demo?',parent=self):return
        if self._handle(lambda:self.store.delete_document(self.active_document)):
            self.doc_dirty=False;self._reload_doc_list();self._new_doc(ignore_check=True)

    def about(self):
        self.intro('Alcance de esta demostración','Edición pública independiente. No es el programa privado V1.0.6 RC1.')
        entries=[
            ('✓ Funciones reales de esta demo','Panel, clientes, expedientes, documentos, agenda, movimientos, edición y búsqueda.'),
            ('✓ Totalmente aislada','SQLite exclusivamente en memoria. No busca la base original ni crea archivos de usuario.'),
            ('✓ Sin paquetes de terceros','Tkinter, SQLite, datetime y decimal de Python. No contiene PyMuPDF ni wheels.'),
            ('! Funciones no incluidas','No incorpora PDF, procesador DOCX, archivo digital, backups, roles, PIN ni firma digital.'),
            ('! Alcance jurídico','Sin cómputo legal de vencimientos, integración con tribunales ni asesoramiento jurídico.'),
            ('! No apto para casos reales','No ingresar información personal, confidencial ni expedientes reales. No usar en producción.'),
            ('Cómo empezar','Agregá registros ficticios, editá un documento y reiniciá los datos desde el botón superior.'),
        ]
        for heading,description in entries:
            card=tk.Frame(self.page,bg=COLOR['panel'],padx=17,pady=12);card.pack(fill='x',pady=5)
            tk.Label(card,text=heading,bg=COLOR['panel'],fg=COLOR['gold'],font=('Segoe UI Semibold',11)).pack(anchor='w')
            tk.Label(card,text=description,bg=COLOR['panel'],fg=COLOR['sub'],font=('Segoe UI',10),wraplength=820,justify='left').pack(anchor='w',pady=(5,0))
        label(self.page,f'Versión {VERSION}  ·  © 2026 QuintaDimensión Tecnología · Todos los derechos reservados',9,color='sub').pack(anchor='w',pady=(15,0))


if __name__=='__main__':
    LegalDemo().mainloop()
