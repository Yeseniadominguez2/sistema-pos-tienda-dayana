# Sistema POS — Tienda Dayana

Sistema de punto de venta desarrollado en Python + CustomTkinter con base de datos MySQL.

**Estudiante:** Karla Yesenia Dominguez Calderon  
**No. Control:** 23090928  
**Asignatura:** Ingenieria de Software  
**Docente:** Claudia Gabriela Bustillos Gaytan  

---

## Estructura del proyecto
---

## Modulo evaluado: Gestion de Productos

### ¿Que hace?
Permite administrar completamente el catalogo de productos: agregar, editar, eliminar y buscar productos conectandose directamente a MySQL.

### Requerimientos que cubre
| ID | Requerimiento |
|----|--------------|
| RF-7 | Agregar nuevo producto con todos sus datos |
| RF-8 | Editar informacion de producto existente |
| RF-9 | Eliminar producto con confirmacion previa |
| RF-11| Busqueda en tiempo real por nombre o codigo |
| RF-12 | Stock en rojo si es bajo, verde si esta OK |

---

## Fragmentos de codigo explicados

### 1. `screens/productos.py` — Funcion `_agregar()`
Registra un nuevo producto en MySQL. Primero valida los campos, luego verifica que el codigo no este duplicado y finalmente ejecuta el INSERT.

```python
def _agregar(self):
    # 1. Valida los campos del formulario
    d = self._validar()
    if not d: return

    # 2. Verifica que el codigo no exista ya en la BD
    existe = ejecutar(
        "SELECT id FROM productos WHERE codigo_barras = %s",
        (d["codigo"],), fetchone=True)
    if existe:
        messagebox.showerror("Duplicado", "El codigo ya existe.")
        return

    # 3. Inserta el nuevo producto en MySQL
    pid = ejecutar(
        "INSERT INTO productos (codigo_barras, nombre, precio, "
        "stock, stock_minimo, categoria_id, fecha_caducidad) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (d["codigo"], d["nombre"], d["precio"],
         d["stock"], d["stk_min"], d["cat_id"], d["caducidad"]))
    if pid:
        messagebox.showinfo("Agregado", f"Producto guardado ID: #{pid}")
```

---

### 2. `screens/productos.py` — Funcion `_validar()`
Verifica que los datos del formulario sean correctos antes de enviarlos a la BD. Retorna `None` si algo falla o un diccionario con los datos limpios si todo esta bien.

```python
def _validar(self):
    codigo = self.e_codigo.get().strip()
    nombre = self.e_nombre.get().strip()
    precio = self.e_precio.get().strip()
    stock  = self.e_stock.get().strip()

    if not codigo:
        messagebox.showwarning("Requerido", "El codigo es obligatorio")
        return None
    try:
        precio_f = float(precio)
        if precio_f <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("Invalido", "Precio debe ser mayor a 0")
        return None

    return {"codigo": codigo, "nombre": nombre,
            "precio": precio_f, "stock": int(stock), ...}
```

---

### 3. `screens/productos.py` — Funcion `_eliminar()`
Elimina un producto con confirmacion previa. Si el usuario acepta, ejecuta el DELETE y recarga la lista automaticamente.

```python
def _eliminar(self):
    if not self.producto_sel_id: return

    p = ejecutar("SELECT nombre FROM productos WHERE id = %s",
                 (self.producto_sel_id,), fetchone=True)
    nombre = p["nombre"] if p else "este producto"

    if messagebox.askyesno("Eliminar",
        f"Eliminar '{nombre}'? Esta accion no se puede deshacer."):
        ejecutar("DELETE FROM productos WHERE id = %s",
                 (self.producto_sel_id,))
        messagebox.showinfo("Eliminado", f"'{nombre}' eliminado")
        self.producto_sel_id = None
        self._cargar_lista()  # Refresca la lista
```

---

### 4. `core/database.py` — Funcion `ejecutar()`
Funcion central que maneja todas las consultas SQL. Evita repetir codigo de conexion en cada pantalla.

```python
def ejecutar(sql, params=None, fetchall=False, fetchone=False):
    conn = conectar()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)  # Retorna filas como dicts
        cur.execute(sql, params or ())

        if fetchall: return cur.fetchall()  # Lista de registros
        if fetchone: return cur.fetchone()  # Un solo registro

        conn.commit()         # Guarda cambios INSERT/UPDATE/DELETE
        return cur.lastrowid  # Retorna ID del nuevo registro
    except Error as e:
        messagebox.showerror("Error SQL", str(e))
        return None
    finally:
        conn.close()  # Siempre cierra la conexion
```

---

## Base de datos

### Tabla: `productos`
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INT PK AUTO | Identificador unico |
| codigo_barras | VARCHAR(50) | Codigo unico (solo numeros) |
| nombre | VARCHAR(100) | Nombre del producto |
| precio | DECIMAL(10,2) | Precio de venta |
| stock | INT | Cantidad actual |
| stock_minimo | INT | Minimo antes de alerta |
| categoria_id | INT FK | Referencia a categorias.id |
| fecha_caducidad | DATE | Fecha de vencimiento |

### Tabla: `categorias`
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INT PK AUTO | Identificador unico |
| nombre | VARCHAR(100) | Nombre de la categoria |

---

## Como ejecutar

```bash
pip install customtkinter mysql-connector-python
cd sistema-pos-tienda-dayana
python main.py
```

---

## Tecnologias
- **Python 3.14**
- **CustomTkinter** — Interfaz grafica
- **MySQL** — Base de datos
- **mysql-connector-python** — Conexion a BD