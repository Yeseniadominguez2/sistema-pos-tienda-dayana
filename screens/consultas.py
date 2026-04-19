import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from core.config import C
from core.database import ejecutar
from components.widgets import (
    make_titlebar, make_btn, make_btn_outline,
    make_sep, make_card, make_metric
)


class CU04(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self._build()

    def _build(self):
        make_titlebar(self, "Consultar Precio", "Escanea o escribe el nombre del producto", "🔍")

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.pack(fill="both", expand=True, padx=60, pady=16)

        cb = make_card(centro)
        cb.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(cb, text="🔍  Buscar producto",
                     font=("Arial", 14, "bold"), text_color=C["cyan_t"]).pack(anchor="w", padx=20, pady=(16, 8))

        fila = ctk.CTkFrame(cb, fg_color="transparent")
        fila.pack(fill="x", padx=20, pady=(0, 16))

        self.inp = ctk.CTkEntry(
            fila, height=42, corner_radius=10, font=("Arial", 13),
            placeholder_text="Código de barras o nombre...",
            border_color=C["cyan"], fg_color=C["fondo3"],
            text_color=C["blanco"], placeholder_text_color=C["texto3"],
            border_width=2
        )
        self.inp.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.inp.bind("<Return>", lambda e: self._buscar())
        make_btn(fila, "Buscar", self._buscar, C["cyan"], 120, 42).pack(side="left", padx=(0, 6))
        make_btn_outline(fila, "Limpiar", self._limpiar, 100, 42).pack(side="left")

        self.res_card = make_card(centro)
        self.res_card.pack(fill="x", pady=(0, 12))
        self.res_frame = ctk.CTkFrame(self.res_card, fg_color="transparent")
        self.res_frame.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(self.res_frame, text="Ingresa un código o nombre para buscar",
                     font=("Arial", 13), text_color=C["texto3"]).pack(pady=16)

        cp = make_card(centro)
        cp.pack(fill="both", expand=True)
        ctk.CTkLabel(cp, text="📦  Todos los productos",
                     font=("Arial", 12, "bold"), text_color=C["texto3"]).pack(anchor="w", padx=20, pady=(12, 4))
        make_sep(cp)

        scroll = ctk.CTkScrollableFrame(cp, fg_color="transparent", height=180)
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        prods = ejecutar(
            "SELECT p.*, c.nombre as cat FROM productos p LEFT JOIN categorias c ON p.categoria_id=c.id ORDER BY p.nombre",
            fetchall=True
        ) or []
        for i, p in enumerate(prods):
            f = ctk.CTkFrame(scroll, fg_color=C["fondo3"] if i % 2 else C["card"],
                             corner_radius=6, height=36)
            f.pack(fill="x", pady=2)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=p["nombre"], font=("Arial", 12),
                         text_color=C["texto"], anchor="w").pack(side="left", padx=10)
            s_color = C["verde"] if p["stock"] > p["stock_minimo"] else C["rojo"]
            ctk.CTkLabel(f, text=f"{p['stock']} pzas",
                         font=("Arial", 11), text_color=s_color).pack(side="right", padx=10)
            ctk.CTkLabel(f, text=f"${float(p['precio']):.2f}",
                         font=("Arial", 12, "bold"), text_color=C["cyan_t"]).pack(side="right", padx=20)

        make_btn_outline(cp, "← Menú principal", lambda: self.ir("menu"), 180, 36).pack(anchor="e", padx=20, pady=10)

    def _buscar(self):
        busq = self.inp.get().strip()
        if not busq: return
        p = ejecutar(
            "SELECT p.*, c.nombre as cat FROM productos p LEFT JOIN categorias c ON p.categoria_id=c.id "
            "WHERE p.codigo_barras=%s OR p.nombre LIKE %s LIMIT 1",
            (busq, f"%{busq}%"), fetchone=True
        )
        for w in self.res_frame.winfo_children():
            w.destroy()

        if p:
            hdr = ctk.CTkFrame(self.res_frame, fg_color="transparent")
            hdr.pack(fill="x", pady=(0, 10))

            ico = ctk.CTkFrame(hdr, fg_color=C["cyan_bg"], corner_radius=10, width=52, height=52)
            ico.pack(side="left", padx=(0, 14))
            ico.pack_propagate(False)
            ctk.CTkLabel(ico, text="📦", font=("Arial", 22)).pack(expand=True)

            info = ctk.CTkFrame(hdr, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(info, text=p["nombre"], font=("Arial", 16, "bold"),
                         text_color=C["blanco"], anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"Código: {p['codigo_barras']} | {p['cat'] or ''}",
                         font=("Arial", 11), text_color=C["texto3"], anchor="w").pack(fill="x")

            disp = p["stock"] > 0
            b = ctk.CTkFrame(hdr, fg_color=C["verde_bg"] if disp else C["rojo_bg"],
                             corner_radius=20, border_color=C["verde"] if disp else C["rojo"], border_width=1)
            b.pack(side="right")
            ctk.CTkLabel(b, text="✓ Disponible" if disp else "✕ Agotado",
                         font=("Arial", 11, "bold"),
                         text_color=C["verde_t"] if disp else C["rojo_t"],
                         padx=10, pady=4).pack()

            mrow = ctk.CTkFrame(self.res_frame, fg_color="transparent")
            mrow.pack(fill="x")
            s_color = C["verde"] if p["stock"] > p["stock_minimo"] else C["rojo"]
            for lbl, val, col in [
                ("Precio",  f"${float(p['precio']):.2f}", C["cyan_t"]),
                ("Stock",   f"{p['stock']} pzas",         s_color),
                ("Caduca",  str(p["fecha_caducidad"] or "—"), C["texto3"])
            ]:
                m = ctk.CTkFrame(mrow, fg_color=C["fondo3"], corner_radius=8,
                                 border_color=C["borde"], border_width=1)
                m.pack(side="left", expand=True, fill="x", padx=5, ipadx=12, ipady=6)
                ctk.CTkLabel(m, text=lbl, font=("Arial", 10), text_color=C["texto3"]).pack()
                ctk.CTkLabel(m, text=val, font=("Arial", 15, "bold"), text_color=col).pack()
        else:
            ctk.CTkLabel(self.res_frame, text=f"❌  '{busq}' no encontrado",
                         font=("Arial", 13), text_color=C["rojo_t"]).pack(pady=10)

    def _limpiar(self):
        self.inp.delete(0, "end")
        for w in self.res_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.res_frame, text="Ingresa un código o nombre para buscar",
                     font=("Arial", 13), text_color=C["texto3"]).pack(pady=16)


class CU05(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        res = ejecutar(
            "SELECT COALESCE(SUM(total),0) as total, COUNT(*) as num FROM ventas WHERE fecha = CURDATE()",
            fetchone=True
        )
        self.total_sistema = float(res["total"]) if res else 0.0
        self.num_ventas    = res["num"] if res else 0
        self._fisico = None
        self._dif    = None
        self._build()

    def _build(self):
        make_titlebar(self, "Cierre de Caja", "Reporte del día y comparación de efectivo", "💰")

        mrow = ctk.CTkFrame(self, fg_color="transparent")
        mrow.pack(fill="x", padx=16, pady=(12, 8))
        promedio = self.total_sistema / self.num_ventas if self.num_ventas > 0 else 0
        make_metric(mrow, "Total sistema",  f"${self.total_sistema:.2f}", C["verde"])
        make_metric(mrow, "Ventas del día", str(self.num_ventas),          C["texto"])
        make_metric(mrow, "Ticket prom.",   f"${promedio:.2f}",            C["primario_t"])
        make_metric(mrow, "Fecha",          datetime.now().strftime("%d/%m/%Y"), C["texto"])

        g = ctk.CTkFrame(self, fg_color="transparent")
        g.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        g.columnconfigure((0, 1), weight=1)
        g.rowconfigure(0, weight=1)

        self._tabla_ventas(g)
        self._panel_caja(g)

    def _tabla_ventas(self, parent):
        ct = make_card(parent)
        ct.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(ct, text="📊  Ventas de hoy",
                     font=("Arial", 12, "bold"), text_color=C["texto3"]).pack(anchor="w", padx=14, pady=(12, 4))
        make_sep(ct)

        hdr = ctk.CTkFrame(ct, fg_color=C["fondo3"], corner_radius=6, height=34)
        hdr.pack(fill="x", padx=10, pady=(0, 4))
        hdr.pack_propagate(False)
        for txt, w in [("ID", 50), ("Hora", 80), ("Total", 100), ("Pagó", 100), ("Cambio", 100)]:
            ctk.CTkLabel(hdr, text=txt, font=("Arial", 11, "bold"),
                         text_color=C["texto3"], width=w).pack(side="left", padx=4, pady=8)

        scroll = ctk.CTkScrollableFrame(ct, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        ventas = ejecutar("SELECT * FROM ventas WHERE fecha = CURDATE() ORDER BY hora DESC", fetchall=True) or []
        for i, v in enumerate(ventas):
            bg = C["card"] if i % 2 == 0 else C["fondo3"]
            row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6, height=36)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            hora_str = str(v["hora"])[:5] if v["hora"] else "—"
            for txt, w in [
                (f"#{v['id']}", 50), (hora_str, 80),
                (f"${float(v['total']):.2f}", 100),
                (f"${float(v['monto_pago'] or 0):.2f}", 100),
                (f"${float(v['cambio'] or 0):.2f}", 100)
            ]:
                ctk.CTkLabel(row, text=txt, font=("Arial", 11),
                             text_color=C["texto"], width=w).pack(side="left", padx=4, pady=8)

        tot = ctk.CTkFrame(ct, fg_color=C["verde_bg"], corner_radius=6, height=36,
                           border_color=C["verde"], border_width=1)
        tot.pack(fill="x", padx=10, pady=(0, 10))
        tot.pack_propagate(False)
        ctk.CTkLabel(tot, text="TOTAL DEL DÍA",
                     font=("Arial", 11, "bold"), text_color=C["verde_t"]).pack(side="left", padx=14)
        ctk.CTkLabel(tot, text=f"${self.total_sistema:.2f}",
                     font=("Arial", 14, "bold"), text_color=C["verde"]).pack(side="right", padx=14)

    def _panel_caja(self, parent):
        cc = make_card(parent)
        cc.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(cc, text="💰  Comparar efectivo",
                     font=("Arial", 12, "bold"), text_color=C["texto3"]).pack(anchor="w", padx=14, pady=(12, 4))
        make_sep(cc)

        f1 = ctk.CTkFrame(cc, fg_color="transparent")
        f1.pack(fill="x", padx=14, pady=4)
        ctk.CTkLabel(f1, text="Sistema registró:", font=("Arial", 12), text_color=C["texto3"]).pack(side="left")
        ctk.CTkLabel(f1, text=f"${self.total_sistema:.2f}",
                     font=("Arial", 13, "bold"), text_color=C["verde"]).pack(side="right")

        ctk.CTkLabel(cc, text="Dinero contado en caja ($):",
                     font=("Arial", 12), text_color=C["texto2"]).pack(anchor="w", padx=14, pady=(14, 4))

        finp = ctk.CTkFrame(cc, fg_color="transparent")
        finp.pack(fill="x", padx=14)
        self.inp_monto = ctk.CTkEntry(
            finp, height=40, corner_radius=10, font=("Arial", 14),
            placeholder_text="Ej: 980.00",
            border_color=C["borde"], fg_color=C["fondo3"],
            text_color=C["blanco"], placeholder_text_color=C["texto3"]
        )
        self.inp_monto.pack(side="left", fill="x", expand=True, padx=(0, 8))
        make_btn(finp, "Calcular", self._calcular, C["verde"], 110, 40).pack(side="left")

        self.dif_frame = ctk.CTkFrame(cc, fg_color="transparent")
        self.dif_frame.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(self.dif_frame, text="Ingresa el monto y presiona Calcular",
                     font=("Arial", 12), text_color=C["texto3"]).pack(pady=10)

        make_sep(cc)
        make_btn(cc, "✓  Confirmar cierre", self._confirmar, C["verde"], 230, 42).pack(padx=14, pady=6)
        make_btn_outline(cc, "← Menú principal", lambda: self.ir("menu"), 230, 38).pack(padx=14, pady=(0, 14))

    def _calcular(self):
        try:
            fisico = float(self.inp_monto.get().replace("$", "").replace(",", "").strip())
            dif = fisico - self.total_sistema
            for w in self.dif_frame.winfo_children():
                w.destroy()

            pos   = dif >= 0
            bg    = C["verde_bg"] if pos else C["rojo_bg"]
            fg    = C["verde_t"]  if pos else C["rojo_t"]
            borde = C["verde"]    if pos else C["rojo"]
            txt_dif = f"+${dif:.2f} (Sobrante)" if pos else f"-${abs(dif):.2f} (Faltante)"

            box = ctk.CTkFrame(self.dif_frame, fg_color=bg, corner_radius=10,
                               border_color=borde, border_width=2)
            box.pack(fill="x", pady=4)
            ctk.CTkLabel(box, text="Diferencia calculada",
                         font=("Arial", 11), text_color=fg).pack(pady=(10, 2))
            ctk.CTkLabel(box, text=txt_dif,
                         font=("Arial", 18, "bold"), text_color=borde).pack(pady=(0, 10))

            self._fisico = fisico
            self._dif    = dif
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido")

    def _confirmar(self):
        if self._fisico is None:
            messagebox.showwarning("Aviso", "Primero calcula la diferencia"); return
        if messagebox.askyesno("Confirmar cierre",
                               f"¿Confirmar el cierre de caja?\nTotal del día: ${self.total_sistema:.2f}"):
            ejecutar(
                "INSERT INTO cierre_caja (fecha, total_sistema, monto_fisico, diferencia, num_ventas) VALUES (%s,%s,%s,%s,%s)",
                (datetime.now().date(), self.total_sistema, self._fisico, self._dif, self.num_ventas)
            )
            ejecutar("DELETE FROM detalle_ventas WHERE venta_id IN (SELECT id FROM ventas WHERE fecha = CURDATE())")
            ejecutar("DELETE FROM ventas WHERE fecha = CURDATE()")
            messagebox.showinfo("✓ Cierre exitoso",
                                "Cierre guardado correctamente.\nVentas del día archivadas.\nEl sistema está listo para mañana.")
            self.ir("menu")