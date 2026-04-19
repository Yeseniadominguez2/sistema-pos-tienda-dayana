import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from core.config import C
from core.database import ejecutar
from core.printer import imprimir_ticket
from components.widgets import (
    make_titlebar, make_btn, make_btn_outline,
    make_btn_rojo, make_sep, make_card, mostrar_ticket
)


class CU01(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self.carrito = []
        self.total = 0.0
        self._build()

    def _build(self):
        make_titlebar(self, "Realizar Venta", "Escanea el codigo de barras o escribe el nombre", "🛒")

        tb = ctk.CTkFrame(self, fg_color=C["blanco"], corner_radius=0,
                          border_color=C["borde"], border_width=1, height=58)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        ctk.CTkLabel(tb, text="🔍", font=("Arial", 18)).pack(side="left", padx=(14, 4), pady=14)
        self.inp = ctk.CTkEntry(
            tb, width=500, height=36, corner_radius=10,
            placeholder_text="Apunta el lector aqui o escribe el nombre...",
            border_color=C["primario"], fg_color=C["fondo3"],
            text_color=C["texto"], placeholder_text_color=C["texto3"],
            font=("Arial", 12), border_width=2
        )
        self.inp.pack(side="left", pady=11)
        self.inp.focus()
        self.inp.bind("<Return>", lambda e: self._agregar())

        make_btn(tb, "+ Agregar", self._agregar, C["primario"], 130, 36).pack(side="left", padx=8, pady=11)
        ctk.CTkLabel(tb, text="El lector escribe automaticamente",
                     font=("Arial", 10), text_color=C["texto3"]).pack(side="left", padx=4)
        make_btn_outline(tb, "<- Menu", lambda: self.ir("menu"), 100, 36).pack(side="right", padx=14, pady=11)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=10)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._tabla_carrito(body)
        self._panel_cobro(body)

    def _tabla_carrito(self, parent):
        izq = make_card(parent)
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        hdr = ctk.CTkFrame(izq, fg_color=C["fondo"], corner_radius=0, height=36)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for txt, w in [("#", 40), ("Producto", 300), ("Precio", 100), ("Cant.", 70), ("Subtotal", 100), ("", 50)]:
            ctk.CTkLabel(hdr, text=txt, font=("Arial", 11, "bold"),
                         text_color=C["texto2"], width=w).pack(side="left", padx=4, pady=8)

        self.tabla_frame = ctk.CTkScrollableFrame(izq, fg_color="transparent")
        self.tabla_frame.pack(fill="both", expand=True, padx=8, pady=6)

        footer = ctk.CTkFrame(izq, fg_color=C["primario_bg"], height=40, corner_radius=0,
                              border_color=C["primario"], border_width=1)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        self.lbl_footer = ctk.CTkLabel(footer, text="0 productos | Total: $0.00",
                                       font=("Arial", 12, "bold"), text_color=C["primario_t"])
        self.lbl_footer.pack(side="right", padx=14, pady=10)

    def _panel_cobro(self, parent):
        der = make_card(parent)
        der.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(der, text="Cobro", font=("Arial", 15, "bold"),
                     text_color=C["texto"]).pack(pady=(16, 2), padx=14, anchor="w")
        make_sep(der)

        self.lbl_total = ctk.CTkLabel(der, text="$0.00",
                                      font=("Arial", 38, "bold"), text_color=C["primario"])
        self.lbl_total.pack(pady=14)
        make_sep(der)

        ctk.CTkLabel(der, text="Monto recibido ($):", font=("Arial", 12),
                     text_color=C["texto2"]).pack(anchor="w", padx=14, pady=(8, 3))
        self.inp_monto = ctk.CTkEntry(
            der, width=240, height=42, corner_radius=10,
            placeholder_text="Ej: 200.00",
            border_color=C["borde"], fg_color=C["fondo3"],
            text_color=C["texto"], placeholder_text_color=C["texto3"],
            font=("Arial", 16)
        )
        self.inp_monto.pack(padx=14, pady=(0, 6))
        make_btn_outline(der, "Calcular cambio", self._cambio, 240, 36).pack(padx=14, pady=(0, 4))

        self.lbl_cambio = ctk.CTkLabel(der, text="Cambio: --",
                                       font=("Arial", 15, "bold"), text_color=C["verde"])
        self.lbl_cambio.pack(pady=6)
        make_sep(der)

        ctk.CTkButton(
            der, text="Confirmar Venta", command=self._confirmar,
            fg_color=C["verde"], hover_color=C["verde_hover"],
            text_color=C["blanco"], font=("Arial", 13, "bold"),
            width=240, height=46, corner_radius=10
        ).pack(padx=14, pady=8)
        make_btn_rojo(der, "Cancelar Venta", self._cancelar, 240, 38).pack(padx=14, pady=(0, 16))

    def _agregar(self):
        busq = self.inp.get().strip()
        if not busq:
            return
        p = ejecutar(
            "SELECT * FROM productos WHERE codigo_barras = %s OR nombre LIKE %s LIMIT 1",
            (busq, f"%{busq}%"), fetchone=True
        )
        if not p:
            messagebox.showerror("No encontrado", f"'{busq}' no esta en la base de datos.")
            self.inp.delete(0, "end"); return
        if p["stock"] == 0:
            messagebox.showerror("Agotado", f"'{p['nombre']}' esta agotado.")
            self.inp.delete(0, "end"); return

        existente = next((i for i in self.carrito if i["id"] == p["id"]), None)
        if existente:
            if existente["cant"] >= p["stock"]:
                messagebox.showwarning("Stock", f"Solo hay {p['stock']} unidades."); return
            existente["cant"] += 1
            existente["sub"] = existente["cant"] * float(p["precio"])
        else:
            self.carrito.append({
                "id": p["id"], "nombre": p["nombre"],
                "precio": float(p["precio"]), "cant": 1, "sub": float(p["precio"])
            })
        self._refresh()
        self.inp.delete(0, "end")
        self.inp.focus()

    def _refresh(self):
        for w in self.tabla_frame.winfo_children():
            w.destroy()
        self.total = 0
        for i, it in enumerate(self.carrito):
            self.total += it["sub"]
            bg = C["blanco"] if i % 2 == 0 else C["fondo3"]
            row = ctk.CTkFrame(self.tabla_frame, fg_color=bg, corner_radius=6, height=40)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            for txt, w in [
                (str(i+1), 40), (it["nombre"][:36], 300),
                (f"${it['precio']:.2f}", 100), (str(it["cant"]), 70),
                (f"${it['sub']:.2f}", 100)
            ]:
                ctk.CTkLabel(row, text=txt, font=("Arial", 12),
                             text_color=C["texto"], width=w).pack(side="left", padx=4, pady=8)
            ctk.CTkButton(
                row, text="x", width=36, height=26, corner_radius=6,
                fg_color=C["rojo_bg"], hover_color=C["rojo_light"],
                text_color=C["rojo_t"], font=("Arial", 11),
                command=lambda idx=i: self._quitar(idx)
            ).pack(side="left", padx=4)

        self.lbl_total.configure(text=f"${self.total:.2f}")
        self.lbl_footer.configure(text=f"{len(self.carrito)} producto(s) | Total: ${self.total:.2f}")
        self.lbl_cambio.configure(text="Cambio: --")

    def _quitar(self, idx):
        self.carrito.pop(idx)
        self._refresh()

    def _cambio(self):
        try:
            monto = float(self.inp_monto.get().replace("$", "").strip())
            if monto < self.total:
                messagebox.showerror("Insuficiente", f"Monto: ${monto:.2f} < Total: ${self.total:.2f}"); return
            self.lbl_cambio.configure(text=f"Cambio: ${monto - self.total:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un numero valido")

    def _confirmar(self):
        if not self.carrito:
            messagebox.showwarning("Vacio", "Agrega productos primero"); return
        try:
            monto = float(self.inp_monto.get().replace("$", "").strip())
        except ValueError:
            messagebox.showerror("Error", "Ingresa el monto recibido"); return
        if monto < self.total:
            messagebox.showerror("Insuficiente", "El monto es menor al total"); return

        cambio = monto - self.total
        ahora = datetime.now()
        venta_id = ejecutar(
            "INSERT INTO ventas (fecha, hora, total, monto_pago, cambio) VALUES (%s,%s,%s,%s,%s)",
            (ahora.date(), ahora.time(), self.total, monto, cambio)
        )
        if venta_id:
            for it in self.carrito:
                ejecutar(
                    "INSERT INTO detalle_ventas (venta_id,producto_id,cantidad,precio_unit,subtotal) VALUES (%s,%s,%s,%s,%s)",
                    (venta_id, it["id"], it["cant"], it["precio"], it["sub"])
                )
                ejecutar("UPDATE productos SET stock = stock - %s WHERE id = %s", (it["cant"], it["id"]))
            mostrar_ticket(self, venta_id, self.carrito, self.total, cambio, monto)
            imprimir_ticket(venta_id, self.carrito, self.total, monto, cambio)
            self.ir("cu02", {"venta_id": venta_id, "carrito": self.carrito,
                             "total": self.total, "cambio": cambio})

    def _cancelar(self):
        if self.carrito and messagebox.askyesno("Cancelar", "Cancelar la venta?"):
            self.carrito = []
            self._refresh()


class CU02(ctk.CTkFrame):
    def __init__(self, parent, ir, datos=None):
        super().__init__(parent, fg_color=C["fondo"], corner_radius=0)
        self.ir = ir
        self.datos = datos or {}
        self._build()

    def _build(self):
        make_titlebar(self, "Venta Registrada", "Guardada en MySQL - Tienda Dayana", "✅")

        ctk.CTkLabel(self, text="Venta registrada exitosamente",
                     font=("Arial", 16, "bold"), text_color=C["verde"]).pack(pady=(20, 4))

        g = ctk.CTkFrame(self, fg_color="transparent")
        g.pack(fill="both", expand=True, padx=24, pady=(10, 10))
        g.columnconfigure((0, 1), weight=1)
        g.rowconfigure(0, weight=1)

        cv = make_card(g)
        cv.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ctk.CTkLabel(cv, text="Datos guardados",
                     font=("Arial", 12, "bold"), text_color=C["texto2"]).pack(anchor="w", padx=14, pady=(12, 4))
        make_sep(cv)

        venta_id = self.datos.get("venta_id", "--")
        total    = self.datos.get("total", 0)
        cambio   = self.datos.get("cambio", 0)
        ahora    = datetime.now()

        for lbl, val in [
            ("ID Venta", f"#{venta_id}"), ("Fecha", ahora.strftime("%d/%m/%Y")),
            ("Hora", ahora.strftime("%H:%M:%S")), ("Total", f"${total:.2f}"),
            ("Cambio", f"${cambio:.2f}"), ("Estado", "Guardada en BD")
        ]:
            f = ctk.CTkFrame(cv, fg_color="transparent")
            f.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(f, text=lbl, font=("Arial", 11),
                         text_color=C["texto3"], width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(f, text=val, font=("Arial", 11, "bold"),
                         text_color=C["verde"] if lbl == "Estado" else C["texto"]).pack(side="left")

        ci = make_card(g)
        ci.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ctk.CTkLabel(ci, text="Stock actualizado",
                     font=("Arial", 12, "bold"), text_color=C["texto2"]).pack(anchor="w", padx=14, pady=(12, 4))
        make_sep(ci)

        scroll = ctk.CTkScrollableFrame(ci, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=6)
        for it in self.datos.get("carrito", []):
            f = ctk.CTkFrame(scroll, fg_color=C["fondo3"], corner_radius=8, height=44)
            f.pack(fill="x", pady=3)
            f.pack_propagate(False)
            ctk.CTkLabel(f, text=it["nombre"], font=("Arial", 12),
                         text_color=C["texto"], anchor="w").pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(f, text=f"-{it['cant']} pza(s)",
                         font=("Arial", 11, "bold"), text_color=C["rojo_t"]).pack(side="right", padx=6)
            ctk.CTkLabel(f, text="OK", font=("Arial", 12),
                         text_color=C["verde"]).pack(side="right", padx=4)

        foot = ctk.CTkFrame(self, fg_color="transparent")
        foot.pack(pady=(0, 16))
        make_btn_outline(foot, "<- Menu", lambda: self.ir("menu"), 180, 40).pack(side="left", padx=8)
        make_btn(foot, "Nueva venta", lambda: self.ir("cu01"), C["primario"], 180, 40).pack(side="left", padx=8)