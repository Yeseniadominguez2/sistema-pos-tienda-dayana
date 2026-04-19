import customtkinter as ctk
from datetime import datetime
from core.config import C
from core.database import ejecutar


class Menu(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self._build()

    def _build(self):
        self._sidebar()
        self._main_content()

    def _sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=C["blanco"], width=240,
                               corner_radius=0, border_color=C["borde"], border_width=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_f = ctk.CTkFrame(sidebar, fg_color="transparent", height=90)
        logo_f.pack(fill="x", pady=(0, 4))
        logo_f.pack_propagate(False)

        ico = ctk.CTkFrame(logo_f, fg_color=C["primario"], corner_radius=14,
                           width=52, height=52)
        ico.place(relx=0.5, rely=0.5, anchor="center")
        ico.pack_propagate(False)
        ctk.CTkLabel(ico, text="🏪", font=("Arial", 24)).pack(expand=True)

        ctk.CTkFrame(sidebar, fg_color=C["borde"], height=1).pack(fill="x")

        info = ctk.CTkFrame(sidebar, fg_color="transparent")
        info.pack(fill="x", padx=18, pady=16)
        ctk.CTkLabel(info, text="TIENDA DAYANA",
                     font=("Arial", 14, "bold"), text_color=C["texto"]).pack(anchor="w")
        ctk.CTkLabel(info, text="Sistema POS v2.0",
                     font=("Arial", 10), text_color=C["texto3"]).pack(anchor="w", pady=(2, 0))

        ahora = datetime.now()
        fecha_f = ctk.CTkFrame(sidebar, fg_color=C["fondo3"], corner_radius=10,
                               border_color=C["borde"], border_width=1)
        fecha_f.pack(fill="x", padx=14, pady=(0, 16))
        ctk.CTkLabel(fecha_f, text=f"📅  {ahora.strftime('%A, %d de %B').capitalize()}",
                     font=("Arial", 10), text_color=C["texto2"]).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(fecha_f, text=f"🕐  {ahora.strftime('%H:%M')} hrs",
                     font=("Arial", 10), text_color=C["texto2"]).pack(anchor="w", padx=12, pady=(0, 8))

        ctk.CTkFrame(sidebar, fg_color=C["borde"], height=1).pack(fill="x", padx=14)

        ctk.CTkLabel(sidebar, text="SISTEMA", font=("Arial", 9, "bold"),
                     text_color=C["texto3"]).pack(anchor="w", padx=18, pady=(14, 6))

        bd_f = ctk.CTkFrame(sidebar, fg_color=C["verde_bg"], corner_radius=8,
                            border_color=C["verde_light"], border_width=1)
        bd_f.pack(fill="x", padx=14, pady=(0, 6))
        row = ctk.CTkFrame(bd_f, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=8)
        dot = ctk.CTkFrame(row, fg_color=C["verde"], corner_radius=4, width=8, height=8)
        dot.pack(side="left", pady=2)
        dot.pack_propagate(False)
        ctk.CTkLabel(row, text="  Base de datos conectada",
                     font=("Arial", 10), text_color=C["verde_t"]).pack(side="left")

        self._quick_stats(sidebar)

        ctk.CTkFrame(sidebar, fg_color="transparent").pack(fill="both", expand=True)
        ctk.CTkFrame(sidebar, fg_color=C["borde"], height=1).pack(fill="x", padx=14)
        ctk.CTkLabel(sidebar, text="© 2025 Tienda Dayana",
                     font=("Arial", 9), text_color=C["texto3"]).pack(pady=10)

    def _quick_stats(self, parent):
        ctk.CTkLabel(parent, text="HOY", font=("Arial", 9, "bold"),
                     text_color=C["texto3"]).pack(anchor="w", padx=18, pady=(14, 6))

        res = ejecutar(
            "SELECT COALESCE(SUM(total),0) as t, COUNT(*) as n FROM ventas WHERE fecha = CURDATE()",
            fetchone=True
        )
        total_hoy  = float(res["t"]) if res else 0.0
        num_ventas = res["n"] if res else 0

        prods_bajos = ejecutar(
            "SELECT COUNT(*) as n FROM productos WHERE stock <= stock_minimo", fetchone=True
        )
        n_bajo = prods_bajos["n"] if prods_bajos else 0

        for ico, lbl, val, color in [
            ("💰", "Ventas",        f"", C["verde"]),
            ("🛒", "Transacciones", str(num_ventas),     C["primario"]),
            ("⚠",  "Alertas stock", str(n_bajo),         C["naranja"] if n_bajo > 0 else C["texto3"]),
        ]:
            f = ctk.CTkFrame(parent, fg_color=C["fondo3"], corner_radius=8,
                             border_color=C["borde"], border_width=1, height=44)
            f.pack(fill="x", padx=14, pady=3)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=ico, font=("Arial", 14)).pack(side="left", padx=(10, 6), pady=10)
            ctk.CTkLabel(f, text=lbl, font=("Arial", 10), text_color=C["texto3"]).pack(side="left")
            ctk.CTkLabel(f, text=val, font=("Arial", 11, "bold"),
                         text_color=color).pack(side="right", padx=12)

    def _main_content(self):
        main = ctk.CTkFrame(self, fg_color=C["fondo"], corner_radius=0)
        main.pack(side="left", fill="both", expand=True)

        hdr = ctk.CTkFrame(main, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(24, 0))
        ctk.CTkLabel(hdr, text="Panel de Control",
                     font=("Arial", 24, "bold"), text_color=C["texto"]).pack(side="left")

        ctk.CTkLabel(main, text="Selecciona el módulo al que deseas acceder",
                     font=("Arial", 12), text_color=C["texto3"]).pack(anchor="w", padx=28, pady=(4, 18))

        grid_wrapper = ctk.CTkFrame(main, fg_color="transparent")
        grid_wrapper.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        self._modulos_grid(grid_wrapper)

    def _modulos_grid(self, parent):
        MODULOS = [
            {"icono": "🛒", "titulo": "Realizar Venta",
             "desc": "Escanear productos y cobrar al cliente",
             "dest": "cu01", "acento": C["primario"], "badge": "Principal"},
            {"icono": "📦", "titulo": "Gestión de Productos",
             "desc": "Agregar, editar o eliminar del catálogo",
             "dest": "productos", "acento": C["morado"], "badge": "Catálogo"},
            {"icono": "🔔", "titulo": "Alertas de Inventario",
             "desc": "Revisar stock bajo y productos por vencer",
             "dest": "cu03", "acento": C["naranja"], "badge": "Inventario"},
            {"icono": "🔍", "titulo": "Consultar Precio",
             "desc": "Buscar precio y existencia por código o nombre",
             "dest": "cu04", "acento": C["cyan"], "badge": "Consulta"},
            {"icono": "💰", "titulo": "Cierre de Caja",
             "desc": "Reporte del día y comparación de efectivo",
             "dest": "cu05", "acento": C["verde"], "badge": "Finanzas"},
        ]

        fila1 = ctk.CTkFrame(parent, fg_color="transparent")
        fila1.pack(fill="x", expand=False, pady=(0, 12))
        fila2 = ctk.CTkFrame(parent, fg_color="transparent")
        fila2.pack(fill="x", expand=False)

        for i, m in enumerate(MODULOS):
            fila = fila1 if i < 3 else fila2
            self._modulo_card(fila, m)

    def _modulo_card(self, parent, m):
        acento = m["acento"]

        outer = ctk.CTkFrame(parent, fg_color=C["blanco"], corner_radius=14,
                             border_color=C["borde"], border_width=1,
                             width=280, height=155)
        outer.pack(side="left", padx=8)
        outer.pack_propagate(False)

        ctk.CTkFrame(outer, fg_color=acento, height=4, corner_radius=0).pack(fill="x")

        inner = ctk.CTkFrame(outer, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=12)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ico_bg = acento + "20"
        ico_f = ctk.CTkFrame(top, fg_color=C["fondo3"], corner_radius=10, width=46, height=46,
                             border_color=C["borde"], border_width=1)
        ico_f.pack(side="left")
        ico_f.pack_propagate(False)
        ctk.CTkLabel(ico_f, text=m["icono"], font=("Arial", 20)).pack(expand=True)

        badge = ctk.CTkFrame(top, fg_color=C["fondo3"], corner_radius=20,
                             border_color=C["borde"], border_width=1)
        badge.pack(side="right")
        ctk.CTkLabel(badge, text=m["badge"], font=("Arial", 9, "bold"),
                     text_color=acento, padx=8, pady=3).pack()

        ctk.CTkLabel(inner, text=m["titulo"], font=("Arial", 13, "bold"),
                     text_color=C["texto"], anchor="w").pack(fill="x")
        ctk.CTkLabel(inner, text=m["desc"], font=("Arial", 10),
                     text_color=C["texto3"], anchor="w", wraplength=240).pack(fill="x", pady=(3, 0))

        flecha_f = ctk.CTkFrame(inner, fg_color="transparent")
        flecha_f.pack(fill="x")
        ctk.CTkLabel(flecha_f, text="→ Abrir módulo",
                     font=("Arial", 10, "bold"), text_color=acento).pack(side="right")

        def _on_enter(e, w=outer):
            w.configure(border_color=acento, border_width=2)

        def _on_leave(e, w=outer):
            w.configure(border_color=C["borde"], border_width=1)

        for widget in self._all_children(outer) + [outer]:
            widget.bind("<Button-1>", lambda e, d=m["dest"]: self.ir(d))
            widget.bind("<Enter>", _on_enter)
            widget.bind("<Leave>", _on_leave)
            widget.configure(cursor="hand2")

    def _all_children(self, widget):
        children = list(widget.winfo_children())
        for child in list(children):
            children.extend(self._all_children(child))
        return children
