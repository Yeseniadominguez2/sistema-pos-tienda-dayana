# Sistema POS — Tienda Dayana

Sistema de punto de venta desarrollado en Python + CustomTkinter con base de datos MySQL.

**Estudiante:** Karla Yesenia Dominguez Calderon  
**No. Control:** 23090928  
**Asignatura:** Ingenieria de Software  
**Docente:** Claudia Gabriela Bustillos Gaytan  

---

## Estructura del proyecto
---

---

## Modulos del sistema

### Modulo 1 — Gestion de Productos (`screens/productos.py`)
CRUD completo del catalogo de productos. Permite agregar, editar, eliminar y buscar productos con validacion de campos y estado visual del stock.

**Requerimientos:** RF-13 al RF-18

### Modulo 2 — Realizar Venta (`screens/ventas.py`)
Punto de venta principal. Escaneo de productos, carrito de compra, calculo de total y cambio, registro en MySQL e impresion automatica del ticket.

**Requerimientos:** RF-01 al RF-06

### Modulo 3 — Alertas de Inventario (`screens/alertas.py`)
Muestra productos con stock bajo y productos proximos a vencer en los siguientes 14 dias con indicadores visuales por nivel de urgencia.

**Requerimientos:** RF-07 al RF-08

### Modulo 4 — Consultar Precio (`screens/consultas.py`)
Busqueda rapida de precios y disponibilidad por codigo de barras o nombre sin necesidad de iniciar una venta.

**Requerimientos:** RF-09 al RF-10

### Modulo 5 — Cierre de Caja (`screens/consultas.py`)
Reporte diario de ventas, comparacion de efectivo sistema vs fisico, calculo de diferencia y archivado automatico de ventas.

**Requerimientos:** RF-11 al RF-12

---

## Fragmentos de codigo principales

### `_agregar()` — screens/ventas.py
Recibe el codigo del lector USB, busca el producto en MySQL y lo agrega al carrito verificando stock disponible.

```python
def _agregar(self):
    p = ejecutar(
        "SELECT * FROM productos WHERE codigo_barras = %s OR nombre LIKE %s LIMIT 1",
        (busq, f"%{busq}%"), fetchone=True)
    if p and p["stock"] > 0:
        self.carrito.append({...})
        self._refresh()
```

### `_confirmar()` — screens/ventas.py
Inserta la venta en MySQL, guarda el detalle de productos y descuenta el stock automaticamente.

```python
def _confirmar(self):
    venta_id = ejecutar("INSERT INTO ventas (...) VALUES (...)", (...))
    for it in self.carrito:
        ejecutar("INSERT INTO detalle_ventas (...) VALUES (...)", (...))
        ejecutar("UPDATE productos SET stock = stock - %s WHERE id = %s",
                 (it["cant"], it["id"]))
```

### `_agregar()` — screens/productos.py
Valida los campos del formulario y registra un nuevo producto en la base de datos.

```python
def _agregar(self):
    d = self._validar()
    if not d: return
    pid = ejecutar(
        "INSERT INTO productos (...) VALUES (%s,%s,%s,%s,%s,%s,%s)", (...))
```

### `ejecutar()` — core/database.py
Funcion central que maneja todas las consultas SQL del sistema.

```python
def ejecutar(sql, params=None, fetchall=False, fetchone=False):
    conn = conectar()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    if fetchall: return cur.fetchall()
    if fetchone: return cur.fetchone()
    conn.commit()
    return cur.lastrowid
```

---

## Base de datos

### Tablas principales
| Tabla | Descripcion |
|-------|-------------|
| productos | Catalogo de productos con stock y caducidad |
| categorias | Categorias de productos |
| ventas | Cabecera de cada venta realizada |
| detalle_ventas | Productos individuales de cada venta |
| cierre_caja | Registros de cierre diario |

### Relaciones
- `productos.categoria_id` → `categorias.id`
- `detalle_ventas.venta_id` → `ventas.id`
- `detalle_ventas.producto_id` → `productos.id`

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
- **CustomTkinter** — Interfaz grafica moderna
- **MySQL** — Base de datos
- **mysql-connector-python** — Conexion a BD
- **Git + GitHub** — Control de versiones


