import customtkinter as ctk

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "23090928",
    "database": "tienda_dayana1"
}

C = {
    "fondo": "#F1F5F9",
    "fondo2": "#FFFFFF",
    "fondo3": "#F8FAFC",
    "card": "#FFFFFF",
    "card2": "#F1F5F9",
    "borde": "#E2E8F0",
    "borde2": "#CBD5E1",
    "blanco": "#FFFFFF",
    "texto": "#0F172A",
    "texto2": "#475569",
    "texto3": "#94A3B8",
    "gris_claro": "#F8FAFC",
    "primario": "#2563EB",
    "primario_hover": "#1D4ED8",
    "primario_bg": "#EFF6FF",
    "primario_t": "#1E40AF",
    "verde": "#16A34A",
    "verde_hover": "#15803D",
    "verde_bg": "#F0FDF4",
    "verde_t": "#166534",
    "verde_light": "#DCFCE7",
    "rojo": "#DC2626",
    "rojo_hover": "#B91C1C",
    "rojo_bg": "#FEF2F2",
    "rojo_t": "#991B1B",
    "rojo_light": "#FEE2E2",
    "morado": "#7C3AED",
    "morado_hover": "#6D28D9",
    "morado_bg": "#F5F3FF",
    "morado_t": "#4C1D95",
    "naranja": "#D97706",
    "naranja_hover": "#B45309",
    "naranja_bg": "#FFFBEB",
    "naranja_t": "#92400E",
    "cyan": "#0891B2",
    "cyan_hover": "#0E7490",
    "cyan_bg": "#ECFEFF",
    "cyan_t": "#164E63",
    "amarillo": "#CA8A04",
    "amarillo_bg": "#FEFCE8",
    "amarillo_t": "#713F12",
}

def init_theme():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
