import customtkinter as ctk
from tkinter import messagebox
from core.config import C
from core.database import ejecutar
from components.widgets import (
    make_titlebar, make_btn, make_btn_outline,
    make_btn_rojo, make_sep, make_card, make_campo
)


class GestionProductos(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self.producto_sel_id = None
        self._build()

    def _build(self):
        make_titlebar(self, "Gestion de Productos", "Agrega, edita o elimina productos")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=10)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._panel_lista(body)
        self._panel_form(body)

    def _panel_lista(self, parent):
        izq = make_card(parent)
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tb = ctk.CTkFrame(izq, fg_color="transparent")
        tb.pack(fill="x", padx=12, pady=(12, 6))

        self.inp_buscar = ctk.CTkEntry(
            tb, height=36, corner_radius=8,
            placeholder_text="  Buscar producto por nombre o codigo...",
            border_color=C["borde"], fg_color=C["fondo3"],
            text_color=C["blanco"], placeholder_text_color=C["texto3"],
            font=("Arial", 12)
        )
        self.inp_buscar.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.inp_buscar.bind("<KeyRelease>", lambda e: self._cargar_lista())
        make_btn_outline(tb, "Limpiar", self._limpiar_busqueda, 100, 36).pack(side="left")

        hdr = ctk.CTkFrame(izq, fg_color=C["fondo"], corner_radius=6, height=34)
        hdr.pack(fill="x", padx=12, pady=(0, 4))
        hdr.pack_propagate(False)
        for txt, w in [("Codigo", 140), ("Nombre", 220), ("Precio", 80), ("Stock", 70), ("Categoria", 110)]:
            ctk.CTkLabel(hdr, text=txt, font=("Arial", 10, "bold"),
                         text_color=C["texto3"], width=w).pack(side="left", padx=4, pady=8)

        self.lista_frame = ctk.CTkScrollableFrame(izq, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self._cargar_lista()

    def _panel_form(self, parent):
        der = make_card(parent)
        der.grid(row=0, column=1, sticky="nsew")

        tab_bar = ctk.CTkFrame(der, fg_color=C["fondo3"], corner_radius=10, height=44)
        tab_bar.pack(fill="x", padx=14, pady=(14, 0))
        tab_bar.pack_propagate(False)

        self.btn_tab_agregar = ctk.CTkButton(
            tab_bar, text="  Agregar",
            command=lambda: self._tab("agregar"),
            fg_color=C["primario"], text_color=C["blanco"],
            font=("Arial", 12, "bold"), height=36, corner_radius=8, width=145
        )
        self.btn_tab_agregar.pack(side="left", padx=4, pady=4)

        self.btn_tab_editar = ctk.CTkButton(
            tab_bar, text="✏️  Editar",
            command=lambda: self._tab("editar"),
            fg_color="transparent", text_color=C["texto3"],
            font=("Arial", 12), height=36, corner_radius=8, width=130,
            hover_color=C["borde"]
        )
        self.btn_tab_editar.pack(side="left", padx=4, pady=4)

        make_sep(der)

        self.form_scroll = ctk.CTkScrollableFrame(der, fg_color="transparent")
        self.form_scroll.pack(fill="both", expand=True, padx=4)

        self.action_frame = ctk.CTkFrame(der, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=14, pady=(0, 6))

        make_btn_outline(der, "Menu principal", lambda: self.ir("menu"), 210, 36).pack(padx=14, pady=(0, 14))
        self._tab("agregar")

    def _cargar_lista(self):
        for w in self.lista_frame.winfo_children():
            w.destroy()

        busq = self.inp_buscar.get().strip()
        if busq:
            prods = ejecutar(
                "SELECT p.*, c.nombre as cat FROM productos p LEFT JOIN categorias c ON p.categoria_id=c.id "
                "WHERE p.nombre LIKE %s OR p.codigo_barras LIKE %s ORDER BY p.nombre",
                (f"%{busq}%", f"%{busq}%"), fetchall=True
            ) or []
        else:
            prods = ejecutar(
                "SELECT p.*, c.nombre as cat FROM productos p LEFT JOIN categorias c ON p.categoria_id=c.id ORDER BY p.nombre",
                fetchall=True
            ) or []

        if not prods:
            ctk.CTkLabel(self.lista_frame, text="Sin productos registrados",
                         font=("Arial", 13), text_color=C["texto3"]).pack(pady=30)
            return

        for i, p in enumerate(prods):
            bg = C["card"] if i % 2 == 0 else C["fondo3"]
            row = ctk.CTkFrame(self.lista_frame, fg_color=bg, corner_radius=6, height=40)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            s_col = C["verde"] if p["stock"] > p["stock_minimo"] else C["rojo"]
            for txt, w in [
                (p["codigo_barras"][:14], 140), (p["nombre"][:28], 220),
                (f"${float(p['precio']):.2f}", 80), (str(p["stock"]), 70),
                ((p["cat"] or "—")[:14], 110)
            ]:
                color = s_col if txt == str(p["stock"]) else C["texto"]
                ctk.CTkLabel(row, text=txt, font=("Arial", 11), text_color=color,
                             width=w, anchor="w").pack(side="left", padx=4, pady=8)

            row.bind("<Button-1>", lambda e, prod=p: self._seleccionar(prod))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, prod=p: self._seleccionar(prod))

    def _seleccionar(self, prod):
        self.producto_sel_id = prod["id"]
        self._tab("editar")
        self._form_editar(prod)

    def _tab(self, modo):
        self.btn_tab_agregar.configure(
            fg_color=C["primario"] if modo == "agregar" else "transparent",
            text_color=C["blanco"] if modo == "agregar" else C["texto3"]
        )
        self.btn_tab_editar.configure(
            fg_color=C["morado"] if modo == "editar" else "transparent",
            text_color=C["blanco"] if modo == "editar" else C["texto3"]
        )
        if modo == "agregar":
            self._form_agregar()
        elif modo == "editar" and not self.producto_sel_id:
            for w in self.form_scroll.winfo_children():
                w.destroy()
            for w in self.action_frame.winfo_children():
                w.destroy()
            ctk.CTkLabel(self.form_scroll,
                         text="Selecciona un producto\nde la lista",
                         font=("Arial", 13), text_color=C["texto3"],
                         justify="center").pack(pady=40)

    def _get_cats(self):
        cats = ejecutar("SELECT * FROM categorias ORDER BY nombre", fetchall=True) or []
        return cats, {c["nombre"]: c["id"] for c in cats}, [c["nombre"] for c in cats]

    def _form_agregar(self):
        for w in self.form_scroll.winfo_children():
            w.destroy()
        for w in self.action_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.form_scroll, text="Nuevo Producto",
                     font=("Arial", 14, "bold"), text_color=C["primario_t"]).pack(anchor="w", padx=16, pady=(10, 4))

        self.e_codigo    = make_campo(self.form_scroll, "Codigo de barras *", "Escanea o escribe")
        self.e_nombre    = make_campo(self.form_scroll, "Nombre *", "Ej: Leche entera 1L")
        self.e_precio    = make_campo(self.form_scroll, "Precio ($) *", "Ej: 22.50")
        self.e_stock     = make_campo(self.form_scroll, "Stock inicial *", "Ej: 24")
        self.e_stk_min   = make_campo(self.form_scroll, "Stock mínimo", "Ej: 10")
        self.e_caducidad = make_campo(self.form_scroll, "Caducidad (YYYY-MM-DD)", "Ej: 2026-12-31")

        _, self.cat_map, cat_nombres = self._get_cats()
        ctk.CTkLabel(self.form_scroll, text="Categoria *",
                     font=("Arial", 11, "bold"), text_color=C["texto2"]).pack(anchor="w", padx=16)
        self.combo_cat = ctk.CTkComboBox(
            self.form_scroll, values=cat_nombres, height=38,
            font=("Arial", 12), border_color=C["borde"],
            fg_color=C["fondo3"], text_color="#000000",
            button_color=C["borde"], dropdown_fg_color=C["card"],
            dropdown_text_color="#000000"
        )
        self.combo_cat.pack(fill="x", padx=16, pady=(3, 10))
        if cat_nombres:
            self.combo_cat.set(cat_nombres[0])

        make_btn(self.action_frame, "  Agregar producto", self._agregar, C["primario"], 210, 40).pack(side="left", padx=(0, 6))
        make_btn_outline(self.action_frame, "Limpiar", self._limpiar_form, 100, 40).pack(side="left")

    def _form_editar(self, prod):
        for w in self.form_scroll.winfo_children():
            w.destroy()
        for w in self.action_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(self.form_scroll, text="Editar Producto",
                     font=("Arial", 14, "bold"), text_color=C["morado_t"]).pack(anchor="w", padx=16, pady=(10, 2))
        ctk.CTkLabel(self.form_scroll, text=prod["nombre"],
                     font=("Arial", 11), text_color=C["texto3"]).pack(anchor="w", padx=16, pady=(0, 8))

        self.e_codigo    = make_campo(self.form_scroll, "Codigo de barras *")
        self.e_nombre    = make_campo(self.form_scroll, "Nombre *")
        self.e_precio    = make_campo(self.form_scroll, "Precio ($) *")
        self.e_stock     = make_campo(self.form_scroll, "Stock *")
        self.e_stk_min   = make_campo(self.form_scroll, "Stock minimo")
        self.e_caducidad = make_campo(self.form_scroll, "Caducidad (YYYY-MM-DD)")

        _, self.cat_map, cat_nombres = self._get_cats()
        ctk.CTkLabel(self.form_scroll, text="Categoria",
                     font=("Arial", 11, "bold"), text_color=C["texto2"]).pack(anchor="w", padx=16)
        self.combo_cat = ctk.CTkComboBox(
            self.form_scroll, values=cat_nombres, height=38,
            font=("Arial", 12), border_color=C["borde"],
            fg_color=C["fondo3"], text_color="#000000",
            button_color=C["borde"], dropdown_fg_color=C["card"],
            dropdown_text_color="#000000"
        )
        self.combo_cat.pack(fill="x", padx=16, pady=(3, 10))

        self.e_codigo.insert(0, prod["codigo_barras"])
        self.e_nombre.insert(0, prod["nombre"])
        self.e_precio.insert(0, str(float(prod["precio"])))
        self.e_stock.insert(0, str(prod["stock"]))
        self.e_stk_min.insert(0, str(prod["stock_minimo"]))
        if prod["fecha_caducidad"]:
            self.e_caducidad.insert(0, str(prod["fecha_caducidad"]))
        cat_actual = ejecutar("SELECT nombre FROM categorias WHERE id = %s", (prod["categoria_id"],), fetchone=True)
        if cat_actual and cat_actual["nombre"] in cat_nombres:
            self.combo_cat.set(cat_actual["nombre"])

        make_btn(self.action_frame, "  Guardar", self._guardar_edicion, C["morado"], 150, 40).pack(side="left", padx=(0, 6))
        make_btn_rojo(self.action_frame, "  Eliminar", self._eliminar, 120, 40).pack(side="left")

    def _validar(self):
        codigo  = self.e_codigo.get().strip()
        nombre  = self.e_nombre.get().strip()
        precio  = self.e_precio.get().strip()
        stock   = self.e_stock.get().strip()
        stk_min = self.e_stk_min.get().strip()

        if not codigo:
            messagebox.showwarning("Requerido", "El codigo de barras es obligatorio"); return None
        if not nombre:
            messagebox.showwarning("Requerido", "El nombre es obligatorio"); return None
        try:
            precio_f = float(precio)
            if precio_f <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Invalido", "Ingresa un precio valido mayor a 0"); return None
        try:
            stock_i = int(stock)
        except ValueError:
            messagebox.showwarning("Invalido", "El stock debe ser un numero entero"); return None

        stk_min_i = int(stk_min) if stk_min.isdigit() else 5
        cat_id    = self.cat_map.get(self.combo_cat.get())
        caducidad = self.e_caducidad.get().strip() or None
        return {"codigo": codigo, "nombre": nombre, "precio": precio_f, "stock": stock_i,
                "stk_min": stk_min_i, "cat_id": cat_id, "caducidad": caducidad}

    def _agregar(self):
        d = self._validar()
        if not d: return
        existe = ejecutar("SELECT id FROM productos WHERE codigo_barras = %s", (d["codigo"],), fetchone=True)
        if existe:
            messagebox.showerror("Duplicado", f"El codigo '{d['codigo']}' ya existe."); return
        pid = ejecutar(
            "INSERT INTO productos (codigo_barras, nombre, precio, stock, stock_minimo, categoria_id, fecha_caducidad) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (d["codigo"], d["nombre"], d["precio"], d["stock"], d["stk_min"], d["cat_id"], d["caducidad"])
        )
        if pid:
            messagebox.showinfo("Agregado", f"'{d['nombre']}' guardado. ID: #{pid}")
            self._limpiar_form()
            self._cargar_lista()

    def _guardar_edicion(self):
        d = self._validar()
        if not d or not self.producto_sel_id: return
        ejecutar(
            "UPDATE productos SET codigo_barras=%s,nombre=%s,precio=%s,stock=%s,stock_minimo=%s,categoria_id=%s,fecha_caducidad=%s WHERE id=%s",
            (d["codigo"], d["nombre"], d["precio"], d["stock"], d["stk_min"], d["cat_id"], d["caducidad"], self.producto_sel_id)
        )
        messagebox.showinfo("Guardado", f"'{d['nombre']}' actualizado correctamente")
        self._cargar_lista()

    def _eliminar(self):
        if not self.producto_sel_id: return
        p = ejecutar("SELECT nombre FROM productos WHERE id = %s", (self.producto_sel_id,), fetchone=True)
        nombre = p["nombre"] if p else "este producto"
        if messagebox.askyesno("Eliminar", f"Eliminar '{nombre}'?\nEsta accion no se puede deshacer."):
            ejecutar("DELETE FROM productos WHERE id = %s", (self.producto_sel_id,))
            messagebox.showinfo("Eliminado", f"'{nombre}' eliminado")
            self.producto_sel_id = None
            self._tab("agregar")
            self._cargar_lista()

    def _limpiar_form(self):
        for e in [self.e_codigo, self.e_nombre, self.e_precio, self.e_stock, self.e_stk_min, self.e_caducidad]:
            e.delete(0, "end")

    def _limpiar_busqueda(self):
        self.inp_buscar.delete(0, "end")
        self._cargar_lista()