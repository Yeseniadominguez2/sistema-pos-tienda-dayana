import tempfile
import os
import subprocess
from datetime import datetime

TIENDA = {
    "nombre":    "TIENDA DAYANA",
    "direccion": "Acamilpa, Morelos",
}

MESES = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril",
    5:"mayo", 6:"junio", 7:"julio", 8:"agosto",
    9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
}

DIAS = {
    "Monday":"lunes", "Tuesday":"martes", "Wednesday":"miercoles",
    "Thursday":"jueves", "Friday":"viernes", "Saturday":"sabado", "Sunday":"domingo"
}


def _fecha_es(dt):
    dia_semana = DIAS.get(dt.strftime("%A"), dt.strftime("%A"))
    mes = MESES.get(dt.month, "")
    return f"{dia_semana} {dt.day} de {mes} de {dt.year}"


def _hora_es(dt):
    h = dt.hour
    sufijo = "a.m." if h < 12 else "p.m."
    h12 = h if h <= 12 else h - 12
    if h12 == 0: h12 = 12
    return f"{h12:02d}:{dt.strftime('%M')} {sufijo}"


def generar_ticket_txt(venta_id, carrito, total, monto, cambio):
    ahora = datetime.now()
    ancho = 44
    linea  = "-" * ancho
    dlinea = "=" * ancho

    def centrar(texto):
        return texto.center(ancho)

    def fila(izq, der):
        espacios = ancho - len(izq) - len(der)
        return izq + " " * max(espacios, 1) + der

    lineas = [
        "",
        centrar(TIENDA["nombre"]),
        centrar(TIENDA["direccion"]),
    
        linea,
        fila("Ticket #:", f"{venta_id:05d}"),
        fila("Fecha:", _fecha_es(ahora)),
        fila("Hora:", _hora_es(ahora)),
        linea,
        f"{'PRODUCTO':<18} {'CANT':>4} {'P.UNIT':>7} {'TOTAL':>7}",
        linea,
    ]

    for it in carrito:
        nombre = it["nombre"][:18]
        cant   = str(it["cant"])
        precio = f"${it['precio']:.2f}"
        sub    = f"${it['sub']:.2f}"
        lineas.append(f"{nombre:<18} {cant:>4} {precio:>7} {sub:>7}")

    lineas += [
        dlinea,
        fila("Subtotal:",        f"${total:.2f}"),
        fila("Monto recibido:",  f"${monto:.2f}"),
        fila("Cambio:",          f"${cambio:.2f}"),
        dlinea,
        fila("TOTAL A PAGAR:",   f"${total:.2f}"),
        dlinea,
        "",
        centrar("*** GRACIAS POR SU COMPRA ***"),
        centrar("Vuelva pronto :)"),
        centrar("Tienda Dayana - Acamilpa"),
        "",
        "",
    ]

    return "\n".join(lineas)


def imprimir_ticket(venta_id, carrito, total, monto, cambio):
    texto = generar_ticket_txt(venta_id, carrito, total, monto, cambio)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False,
        encoding="utf-8", prefix="ticket_"
    )
    tmp.write(texto)
    tmp.close()

    try:
        subprocess.Popen(
            ["notepad.exe", "/p", tmp.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        os.startfile(tmp.name)

    return tmp.name
