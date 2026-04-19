import customtkinter as ctk
from datetime import datetime
from core.config import C


def make_titlebar(parent, titulo, subtitulo="", icono="🏪"):
    bar = ctk.CTkFrame(parent, fg_color=C["blanco"], height=60, corner_radius=0,
                       border_color=C["borde"], border_width=1)
    bar.pack(fill="x")
    bar.pack_propagate(False)

    izq = ctk.CTkFrame(bar, fg_color="transparent")
    izq.pack(side="left", padx=18, pady=8)

    ico_f = ctk.CTkFrame(izq, fg_color=C["primario_bg"], corner_radius=10, width=40, height=40)
    ico_f.pack(side="left", padx=(0, 12))
    ico_f.pack_propagate(False)
    ctk.CTkLabel(ico_f, text=icono, font=("Arial", 18)).pack(expand=True)

    txt_f = ctk.CTkFrame(izq, fg_color="transparent")
    txt_f.pack(side="left")
    ctk.CTkLabel(txt_f, text=titulo, text_color=C["texto"],
                 font=("Arial", 15, "bold")).pack(anchor="w")
    if subtitulo:
        ctk.CTkLabel(txt_f, text=subtitulo, text_color=C["texto3"],
                     font=("Arial", 10)).pack(anchor="w")

    der = ctk.CTkFrame(bar, fg_color=C["fondo3"], corner_radius=10,
                       border_color=C["borde"], border_width=1)
    der.pack(side="right", padx=18, pady=14)
    ahora = datetime.now()
    ctk.CTkLabel(der,
                 text=f"  📅 {ahora.strftime('%d/%m/%Y')}   🕐 {ahora.strftime('%H:%M')}  ",
                 text_color=C["texto2"], font=("Arial", 11)).pack(padx=6, pady=5)


def make_btn(parent, texto, cmd, color, w=160, h=40):
    return ctk.CTkButton(
        parent, text=texto, command=cmd,
        fg_color=color, hover_color=C["primario_hover"],
        text_color=C["blanco"],
        font=("Arial", 12, "bold"),
        width=w, height=h, corner_radius=10
    )


def make_btn_outline(parent, texto, cmd, w=140, h=40):
    return ctk.CTkButton(
        parent, text=texto, command=cmd,
        fg_color=C["blanco"], hover_color=C["fondo3"],
        text_color=C["texto2"],
        border_color=C["borde"], border_width=1,
        font=("Arial", 12), width=w, height=h, corner_radius=10
    )


def make_btn_rojo(parent, texto, cmd, w=140, h=40):
    return ctk.CTkButton(
        parent, text=texto, command=cmd,
        fg_color=C["rojo_bg"], hover_color=C["rojo_light"],
        text_color=C["rojo_t"],
        border_color=C["rojo_light"], border_width=1,
        font=("Arial", 12), width=w, height=h, corner_radius=10
    )


def make_sep(parent, pady=6):
    ctk.CTkFrame(parent, fg_color=C["borde"], height=1).pack(fill="x", pady=pady)


def make_card(parent, **kw):
    return ctk.CTkFrame(
        parent, fg_color=C["card"], corner_radius=14,
        border_color=C["borde"], border_width=1, **kw
    )


def make_metric(parent, label, valor, color):
    f = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12,
                     border_color=C["borde"], border_width=1)
    f.pack(side="left", expand=True, fill="x", padx=5, ipadx=10, ipady=10)
    ctk.CTkLabel(f, text=label, font=("Arial", 11), text_color=C["texto3"]).pack()
    ctk.CTkLabel(f, text=valor, font=("Arial", 20, "bold"), text_color=color).pack()


def make_campo(parent, label, placeholder="", show=""):
    ctk.CTkLabel(parent, text=label, font=("Arial", 11, "bold"),
                 text_color=C["texto2"]).pack(anchor="w", padx=16)
    e = ctk.CTkEntry(
        parent, height=38, corner_radius=8,
        font=("Arial", 12), placeholder_text=placeholder, show=show,
        border_color=C["borde"], fg_color=C["fondo3"],
        text_color=C["texto"], placeholder_text_color=C["texto3"]
    )
    e.pack(fill="x", padx=16, pady=(3, 10))
    return e


def _linea(parent, char="-"):
    ctk.CTkLabel(parent, text=f"{char} " * 28,
                 font=("Courier", 9), text_color=C["borde"]).pack(pady=4)


def mostrar_ticket(parent, venta_id, carrito, total, cambio, monto):
    win = ctk.CTkToplevel(parent)
    win.title("Ticket de Venta")
    win.geometry("400x620")
    win.resizable(False, False)
    win.configure(fg_color=C["blanco"])
    win.grab_set()

    ahora = datetime.now()

    hdr = ctk.CTkFrame(win, fg_color=C["primario"], corner_radius=0)
    hdr.pack(fill="x")
    ctk.CTkLabel(hdr, text="🏪 TIENDA DAYANA",
                 font=("Courier", 16, "bold"), text_color=C["blanco"]).pack(pady=(16, 2))
    ctk.CTkLabel(hdr, text="Zacatepec, Morelos",
                 font=("Courier", 11), text_color="#BFDBFE").pack(pady=(0, 16))

    _linea(win)

    info = ctk.CTkFrame(win, fg_color="transparent")
    info.pack(fill="x", padx=22)
    for lbl, val in [("Ticket #:", f"{venta_id:05d}"), ("Fecha:", ahora.strftime("%d/%m/%Y")), ("Hora:", ahora.strftime("%H:%M:%S"))]:
        row = ctk.CTkFrame(info, fg_color="transparent")
        row.pack(fill="x", pady=1)
        ctk.CTkLabel(row, text=lbl, font=("Courier", 11), text_color=C["texto3"], width=90, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=val, font=("Courier", 11, "bold"), text_color=C["texto"]).pack(side="left")

    _linea(win)

    enc = ctk.CTkFrame(win, fg_color="transparent")
    enc.pack(fill="x", padx=22)
    ctk.CTkLabel(enc, text="PRODUCTO", font=("Courier", 9, "bold"), text_color=C["texto3"], anchor="w").pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(enc, text="CANT", font=("Courier", 9, "bold"), text_color=C["texto3"], width=40, anchor="center").pack(side="left")
    ctk.CTkLabel(enc, text="SUBTOTAL", font=("Courier", 9, "bold"), text_color=C["texto3"], width=80, anchor="e").pack(side="left")

    scroll = ctk.CTkScrollableFrame(win, fg_color="transparent", height=150)
    scroll.pack(fill="x", padx=22)
    for it in carrito:
        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x", pady=1)
        nombre = it["nombre"][:22] + "…" if len(it["nombre"]) > 22 else it["nombre"]
        ctk.CTkLabel(row, text=nombre, font=("Courier", 10), text_color=C["texto"], anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(row, text=str(it["cant"]), font=("Courier", 10), text_color=C["texto2"], width=40, anchor="center").pack(side="left")
        ctk.CTkLabel(row, text=f"", font=("Courier", 10), text_color=C["texto"], width=80, anchor="e").pack(side="left")

    _linea(win, char="=")

    tots = ctk.CTkFrame(win, fg_color="transparent")
    tots.pack(fill="x", padx=22)
    for lbl, val, bold, color in [
        ("Subtotal:", f"", False, C["texto"]),
        ("Pagó:", f"", False, C["texto"]),
        ("CAMBIO:", f"", True, C["verde"]),
        ("TOTAL:", f"", True, C["primario"]),
    ]:
        row = ctk.CTkFrame(tots, fg_color="transparent")
        row.pack(fill="x", pady=2)
        fs = ("Courier", 13, "bold") if bold else ("Courier", 11)
        ctk.CTkLabel(row, text=lbl, font=fs, text_color=color, anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(row, text=val, font=fs, text_color=color, anchor="e").pack(side="right")

    _linea(win)

    ctk.CTkLabel(win, text="¡Gracias por su compra!",
                 font=("Courier", 12, "bold"), text_color=C["primario"]).pack(pady=(4, 2))
    ctk.CTkLabel(win, text="Tienda Dayana — Zacatepec",
                 font=("Courier", 10), text_color=C["texto3"]).pack(pady=(0, 10))

    ctk.CTkButton(win, text="✕  Cerrar ticket", command=win.destroy,
                  fg_color=C["primario"], hover_color=C["primario_hover"],
                  text_color=C["blanco"], font=("Arial", 12, "bold"),
                  width=200, height=38, corner_radius=10).pack(pady=(0, 16))
