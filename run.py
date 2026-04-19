import sys
import os

# Esto le dice a Python que busque dentro de la carpeta tienda_dayana
ruta = os.path.join(os.path.dirname(__file__), 'tienda_dayana')
sys.path.append(ruta)

if __name__ == "__main__":
    from tienda_dayana.main import SistemaPOS
    app = SistemaPOS()
    app.mainloop()