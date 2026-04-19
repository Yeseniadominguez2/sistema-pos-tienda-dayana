-- ══════════════════════════════════════════════
-- Sistema POS - Punto de Venta
-- ══════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS tienda_dayana1;

USE tienda_dayana1;

-- ══════════════════════════════════════════════
-- TABLA 1: categorias
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS categorias (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);
Select * from categorias;
select * from productos;
select * from ventas;
select * from detalle_vents;
select * from cierre_caja;
-- ══════════════════════════════════════════════
-- TABLA 2: productos
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS productos (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras    VARCHAR(50)    UNIQUE NOT NULL,
    nombre           VARCHAR(150)   NOT NULL,
    precio           DECIMAL(10,2)  NOT NULL,
    stock            INT            DEFAULT 0,
    stock_minimo     INT            DEFAULT 5,
    categoria_id     INT,
    fecha_caducidad  DATE,
    creado_en        TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ══════════════════════════════════════════════
-- TABLA 3: ventas
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS ventas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    fecha       DATE          NOT NULL,
    hora        TIME          NOT NULL,
    total       DECIMAL(10,2) NOT NULL,
    monto_pago  DECIMAL(10,2),
    cambio      DECIMAL(10,2),
    estado      VARCHAR(20)   DEFAULT 'completada',
    creado_en   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ══════════════════════════════════════════════
-- TABLA 4: detalle_ventas  ← TABLA INTERMEDIA
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    venta_id     INT           NOT NULL,
    producto_id  INT           NOT NULL,
    cantidad     INT           NOT NULL,
    precio_unit  DECIMAL(10,2) NOT NULL,
    subtotal     DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id)
        REFERENCES ventas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ══════════════════════════════════════════════
-- TABLA 5: cierre_caja
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS cierre_caja (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    fecha           DATE          NOT NULL,
    total_sistema   DECIMAL(10,2) NOT NULL,
    monto_fisico    DECIMAL(10,2) NOT NULL,
    diferencia      DECIMAL(10,2) NOT NULL,
    num_ventas      INT           DEFAULT 0,
    creado_en       TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ══════════════════════════════════════════════
-- DATOS INICIALES: categorias
-- ══════════════════════════════════════════════
INSERT INTO categorias (nombre, descripcion) VALUES
('Lacteos',           'Leche, yogurt, queso, crema'),
('Panaderia',         'Pan, pasteles, galletas'),
('Bebidas',           'Refrescos, agua, jugos'),
('Abarrotes',         'Aceite, azucar, arroz, frijol'),
('Limpieza',          'Jabon, detergente, cloro'),
('Frutas y verduras', 'Productos frescos');

-- ══════════════════════════════════════════════
-- DATOS INICIALES: productos
-- ══════════════════════════════════════════════
INSERT INTO productos (codigo_barras, nombre, precio, stock, stock_minimo, categoria_id, fecha_caducidad) VALUES
('7501234567890', 'Leche entera 1L',       22.50, 24, 10, 1, '2026-04-20'),
('7509999001234', 'Pan Bimbo blanco',       38.00, 15,  8, 2, '2026-03-18'),
('7501111222333', 'Refresco cola 600ml',    18.00, 30, 12, 3, '2026-12-31'),
('7502222333444', 'Aceite vegetal 1L',      45.00,  2, 10, 4, '2026-06-01'),
('7503333444555', 'Azucar 1kg',             28.00,  1,  8, 4, '2027-01-01'),
('7504444555666', 'Jabon lavanderia',       42.00,  0,  5, 5, '2027-01-01'),
('7505555666777', 'Yogurt fresa 1kg',       35.00,  8,  6, 1, '2026-03-16'),
('7506666777888', 'Arroz 1kg',              25.00, 20, 10, 4, '2027-01-01'),
('7507777888999', 'Frijol negro 1kg',       32.00, 18,  8, 4, '2027-06-01'),
('7508888999000', 'Agua purificada 1.5L',   12.00, 40, 15, 3, '2027-01-01'),
('7509111222333', 'Crema acida 500g',       28.00,  5,  6, 1, '2026-03-17'),
('7500111222333', 'Detergente polvo 1kg',   55.00, 10,  5, 5, '2027-01-01');

-- Verificar creación
SELECT '✓ Base de datos tienda_dayana creada correctamente' AS resultado;
SELECT CONCAT('✓ ', COUNT(*), ' productos insertados')     AS productos  FROM productos;
SELECT CONCAT('✓ ', COUNT(*), ' categorias creadas')       AS categorias FROM categorias;

select * from productos;