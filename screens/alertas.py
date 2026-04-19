import customtkinter as ctk
from datetime import datetime
from core.config import C
from core.database import ejecutar
from components.widgets import (
    make_titlebar, make_btn, make_btn_outline,
    make_sep, make_card, make_metric
)


class CU03(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self._build()

    def _build(self):
        make_titlebar(self, "Alertas de Inventario", "Bajo stock y productos proximos a vencer", "🔔")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=10)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._sidebar(body)
        self._panel_alertas(body)

    def _sidebar(self, parent):
        sb = make_card(parent, width=230)
        sb.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        sb.pack_propagate(False)

        ctk.CTkLabel(sb, text="Resumen", font=("Arial", 13, "bold"),
                     text_color=C["texto"]).pack(anchor="w", padx=14, pady=(14, 8))

        bajo   = ejecutar("SELECT COUNT(*) as n FROM productos WHERE stock <= stock_minimo", fetchone=True)
        vencer = ejecutar("SELECT COUNT(*) as n FROM productos WHERE fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL 14 DAY) AND fecha_caducidad IS NOT NULL", fetchone=True)
        total  = ejecutar("SELECT COUNT(*) as n FROM productos", fetchone=True)

        n_bajo   = bajo["n"]   if bajo   else 0
        n_vencer = vencer["n"] if vencer else 0
        n_total  = total["n"]  if total  else 0

        for txt, count, bg, fg, borde in [
            ("Todas las alertas", str(n_bajo + n_vencer), C["primario_bg"], C["primario_t"], C["primario"]),
            ("Bajo stock",        str(n_bajo),             C["rojo_bg"],     C["rojo_t"],     C["rojo"]),
            ("Prox. a vencer",    str(n_vencer),           C["naranja_bg"],  C["naranja_t"],  C["naranja"]),
        ]:
            f = ctk.CTkFrame(sb, fg_color=bg, corner_radius=8, height=42,
                             border_color=borde, border_width=1)
            f.pack(fill="x", padx=10, pady=3)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=txt, font=("Arial", 11, "bold"), text_color=fg).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=count, font=("Arial", 13, "bold"), text_color=fg).pack(side="right", padx=10)

        make_sep(sb, 10)

        ctk.CTkLabel(sb, text="Ultima revision", font=("Arial", 10, "bold"),
                     text_color=C["texto3"]).pack(anchor="w", padx=14)
        ctk.CTkLabel(sb, text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                     font=("Arial", 11), text_color=C["texto2"]).pack(anchor="w", padx=14, pady=2)

        make_btn(sb, "🔄  Actualizar", lambda: self.ir("cu03"), C["naranja"], 200, 36).pack(padx=14, pady=8)
        make_btn_outline(sb, "← Menu", lambda: self.ir("menu"), 200, 36).pack(padx=14, pady=(0, 14))

    def _panel_alertas(self, parent):
        cont = ctk.CTkFrame(parent, fg_color="transparent")
        cont.grid(row=0, column=1, sticky="nsew")

        bajo   = ejecutar("SELECT COUNT(*) as n FROM productos WHERE stock <= stock_minimo", fetchone=True)
        vencer = ejecutar("SELECT COUNT(*) as n FROM productos WHERE fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL 14 DAY) AND fecha_caducidad IS NOT NULL", fetchone=True)
        total  = ejecutar("SELECT COUNT(*) as n FROM productos", fetchone=True)
        n_bajo   = bajo["n"]   if bajo   else 0
        n_vencer = vencer["n"] if vencer else 0
        n_total  = total["n"]  if total  else 0

        mrow = ctk.CTkFrame(cont, fg_color="transparent")
        mrow.pack(fill="x", pady=(0, 10))
        make_metric(mrow, "Stock critico",   str(n_bajo),           C["rojo"])
        make_metric(mrow, "Prox. a vencer",  str(n_vencer),         C["naranja"])
        make_metric(mrow, "Total productos", str(n_total),          C["texto"])
        make_metric(mrow, "Stock OK",        str(n_total - n_bajo), C["verde"])

        scroll = ctk.CTkScrollableFrame(cont, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Seccion bajo stock
        if True:
            prods_bajo = ejecutar(
                "SELECT * FROM productos WHERE stock <= stock_minimo ORDER BY stock ASC",
                fetchall=True
            ) or []
            if prods_bajo:
                ctk.CTkLabel(scroll, text="📦  Productos con bajo stock",
                             font=("Arial", 12, "bold"), text_color=C["rojo"]).pack(anchor="w", pady=(8, 4))
                for p in prods_bajo:
                    self._card_alerta(scroll, "bajo_stock", p["nombre"],
                                      f"Stock actual: {p['stock']} pzas — Minimo requerido: {p['stock_minimo']} {'| ⚠ AGOTADO' if p['stock']==0 else ''}")

        # Seccion proximos a vencer
        prods_vencer = ejecutar(
            """SELECT *,
               DATEDIFF(fecha_caducidad, CURDATE()) as dias_restantes
               FROM productos
               WHERE fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL 14 DAY)
               AND fecha_caducidad IS NOT NULL
               ORDER BY fecha_caducidad ASC""",
            fetchall=True
        ) or []
        if prods_vencer:
            ctk.CTkLabel(scroll, text="⏰  Proximos a vencer (menos de 2 semanas)",
                         font=("Arial", 12, "bold"), text_color=C["naranja"]).pack(anchor="w", pady=(16, 4))
            for p in prods_vencer:
                dias = p["dias_restantes"]
                if dias < 0:
                    detalle = f"Producto: {p['nombre']} | VENCIDO hace {abs(dias)} dias — Caducidad: {p['fecha_caducidad']}"
                elif dias == 0:
                    detalle = f"Producto: {p['nombre']} | VENCE HOY — Caducidad: {p['fecha_caducidad']}"
                else:
                    detalle = f"Producto: {p['nombre']} | Vence en {dias} dia(s) — Caducidad: {p['fecha_caducidad']}"
                self._card_alerta(scroll, "vencer", p["nombre"], detalle, dias)

        if not prods_bajo and not prods_vencer:
            ctk.CTkLabel(scroll, text="✓  Sin alertas — Todo en orden",
                         font=("Arial", 14), text_color=C["verde"]).pack(pady=40)

    def _card_alerta(self, parent, tipo, nombre, detalle, dias=None):
        es_critica = tipo == "bajo_stock"

        if not es_critica and dias is not None:
            if dias < 0:
                borde = C["rojo"]; bg_ico = C["rojo_bg"]; fg_ico = C["rojo_t"]; badge = "VENCIDO"
            elif dias <= 3:
                borde = C["rojo"]; bg_ico = C["rojo_bg"]; fg_ico = C["rojo_t"]; badge = "Urgente"
            elif dias <= 7:
                borde = C["naranja"]; bg_ico = C["naranja_bg"]; fg_ico = C["naranja_t"]; badge = "Esta semana"
            else:
                borde = C["amarillo"]; bg_ico = C["amarillo_bg"]; fg_ico = C["amarillo_t"]; badge = "Prox. vencer"
        else:
            borde  = C["rojo"]    if es_critica else C["naranja"]
            bg_ico = C["rojo_bg"] if es_critica else C["naranja_bg"]
            fg_ico = C["rojo_t"]  if es_critica else C["naranja_t"]
            badge  = "Stock bajo" if es_critica else "Prox. vencer"

        f = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=10,
                         border_color=borde, border_width=1, height=68)
        f.pack(fill="x", pady=4)
        f.pack_propagate(False)

        ico = ctk.CTkFrame(f, fg_color=bg_ico, corner_radius=8, width=36, height=36)
        ico.pack(side="left", padx=12, pady=16)
        ico.pack_propagate(False)
        ctk.CTkLabel(ico, text="↓" if es_critica else "⏰",
                     font=("Arial", 14, "bold"), text_color=borde).pack(expand=True)

        info = ctk.CTkFrame(f, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=10)
        ctk.CTkLabel(info, text=nombre, font=("Arial", 13, "bold"),
                     text_color=C["texto"], anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=detalle, font=("Arial", 10),
                     text_color=C["texto3"], anchor="w", wraplength=500).pack(fill="x")

        b = ctk.CTkFrame(f, fg_color=bg_ico, corner_radius=20, border_color=borde, border_width=1)
        b.pack(side="right", padx=12, pady=22)
        ctk.CTkLabel(b, text=badge, font=("Arial", 10, "bold"),
                     text_color=fg_ico, padx=10, pady=3).pack()
