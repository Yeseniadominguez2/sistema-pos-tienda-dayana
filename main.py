import customtkinter as ctk
import traceback
from core.config import init_theme
from screens.menu      import Menu
from screens.ventas    import CU01, CU02
from screens.alertas   import CU03
from screens.consultas import CU04, CU05
from screens.productos import GestionProductos

class SistemaPOS(ctk.CTk):
    PANTALLAS = {
        "menu":      Menu,
        "cu01":      CU01,
        "cu02":      CU02,
        "cu03":      CU03,
        "cu04":      CU04,
        "cu05":      CU05,
        "productos": GestionProductos,
    }

    def __init__(self):
        super().__init__()
        self.title("Sistema POS — Tienda Dayana")
        self.geometry("1280x800")
        self.minsize(1024, 680)
        from core.config import C
        self.configure(fg_color=C["fondo"])
        self.pantalla_actual = None
        self.ir("menu")

    def ir(self, nombre, datos=None):
        try:
            if self.pantalla_actual:
                self.pantalla_actual.destroy()
            cls = self.PANTALLAS.get(nombre)
            if cls:
                self.pantalla_actual = cls(self, self.ir, datos)
                self.pantalla_actual.pack(fill="both", expand=True)
        except Exception as e:
            traceback.print_exc()
            from tkinter import messagebox
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    init_theme()
    app = SistemaPOS()
    app.mainloop()
