import tkinter as tk
from tkinter import font as tkfont
import math
from temperature import is_overheating

# ─── Constantes ───────────────────────────────────────────────
UMBRAL = 80          # °C
TEMP_MAX_DISPLAY = 120  # tope visual del termómetro

BG        = "#1a1a2e"
PANEL     = "#16213e"
ACCENT    = "#e94560"
OK_COLOR  = "#00b894"
WARN_COLOR= "#fdcb6e"
HOT_COLOR = "#e94560"
TEXT      = "#eaeaea"
TUBE_BG   = "#2d3436"


# ─── Lógica de dibujo ─────────────────────────────────────────
def _clamp(value, lo, hi):
    return max(lo, min(hi, value))


def draw_thermometer(canvas, temp):
    """Dibuja un termómetro vertical animado."""
    canvas.delete("all")

    W = int(canvas["width"])
    H = int(canvas["height"])

    cx     = W // 2
    tube_x1, tube_x2 = cx - 14, cx + 14
    tube_top    = 30
    tube_bottom = H - 60
    bulb_r      = 22
    bulb_cy     = tube_bottom + bulb_r + 4

    # Fondo del canvas
    canvas.create_rectangle(0, 0, W, H, fill=BG, outline="")

    # --- Tubo exterior (sombra) ---
    canvas.create_rounded_rect = _rounded_rect.__get__(canvas)
    _rounded_rect(canvas, tube_x1-2, tube_top-2, tube_x2+2, tube_bottom+2,
                  radius=14, fill="#111", outline="")

    # --- Tubo interior (vacío) ---
    _rounded_rect(canvas, tube_x1, tube_top, tube_x2, tube_bottom,
                  radius=12, fill=TUBE_BG, outline="")

    # --- Mercurio (nivel) ---
    pct    = _clamp(temp / TEMP_MAX_DISPLAY, 0, 1)
    hg_top = tube_bottom - pct * (tube_bottom - tube_top)

    if temp <= UMBRAL * 0.75:
        hg_color = OK_COLOR
    elif temp <= UMBRAL:
        hg_color = WARN_COLOR
    else:
        hg_color = HOT_COLOR

    _rounded_rect(canvas, tube_x1+4, hg_top, tube_x2-4, tube_bottom,
                  radius=8, fill=hg_color, outline="")

    # --- Bulbo ---
    canvas.create_oval(cx-bulb_r, bulb_cy-bulb_r,
                       cx+bulb_r, bulb_cy+bulb_r,
                       fill=hg_color, outline="#111", width=2)

    # --- Marcas de temperatura ---
    for t in range(0, TEMP_MAX_DISPLAY+1, 20):
        pct_t = t / TEMP_MAX_DISPLAY
        y = tube_bottom - pct_t * (tube_bottom - tube_top)
        canvas.create_line(tube_x2, y, tube_x2+10, y, fill=TEXT, width=1)
        canvas.create_text(tube_x2+24, y, text=f"{t}°", fill=TEXT,
                           font=("Consolas", 8), anchor="w")

    # Línea de umbral
    y_umbral = tube_bottom - (UMBRAL/TEMP_MAX_DISPLAY)*(tube_bottom-tube_top)
    canvas.create_line(tube_x1-6, y_umbral, tube_x2+6, y_umbral,
                       fill=ACCENT, width=2, dash=(4, 3))
    canvas.create_text(tube_x1-8, y_umbral, text="⚠ MÁX",
                       fill=ACCENT, font=("Consolas", 7, "bold"), anchor="e")


def _rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kw):
    """Dibuja rectángulo con esquinas redondeadas en un canvas."""
    pts = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


# ─── Lógica de la GUI ─────────────────────────────────────────
class HornoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 Monitor de Temperatura – Horno Industrial")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()
        self._update_display(25)   # temperatura inicial de ejemplo

    # ── Construcción de widgets ──────────────────────────────
    def _build_ui(self):
        # Título
        tk.Label(self, text="HORNO INDUSTRIAL", bg=BG, fg=ACCENT,
                 font=("Consolas", 16, "bold")).pack(pady=(18, 0))
        tk.Label(self, text="Sistema de control de temperatura",
                 bg=BG, fg=TEXT, font=("Consolas", 9)).pack(pady=(2, 12))

        # Contenedor central
        center = tk.Frame(self, bg=BG)
        center.pack(padx=24)

        # Canvas termómetro
        self.canvas = tk.Canvas(center, width=140, height=320,
                                bg=BG, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=(0, 20))

        # Panel derecho
        right = tk.Frame(center, bg=BG)
        right.grid(row=0, column=1, sticky="n")

        # Lectura grande
        tk.Label(right, text="TEMPERATURA ACTUAL",
                 bg=BG, fg=TEXT, font=("Consolas", 8)).pack(anchor="w")
        self.lbl_temp = tk.Label(right, text="--°C", bg=BG, fg=TEXT,
                                  font=("Consolas", 42, "bold"))
        self.lbl_temp.pack(anchor="w")

        # Estado
        self.lbl_estado = tk.Label(right, text="", bg=BG,
                                    font=("Consolas", 13, "bold"))
        self.lbl_estado.pack(anchor="w", pady=(4, 16))

        # Separador
        tk.Frame(right, bg="#444", height=1, width=240).pack(fill="x", pady=8)

        # Umbral info
        tk.Label(right, text=f"Umbral máximo: {UMBRAL} °C",
                 bg=BG, fg=WARN_COLOR, font=("Consolas", 9)).pack(anchor="w")

        # Separador
        tk.Frame(right, bg="#444", height=1, width=240).pack(fill="x", pady=8)

        # Input
        tk.Label(right, text="Ingresar temperatura (°C):",
                 bg=BG, fg=TEXT, font=("Consolas", 9)).pack(anchor="w", pady=(4,2))

        input_row = tk.Frame(right, bg=BG)
        input_row.pack(anchor="w")

        self.entry = tk.Entry(input_row, width=10, font=("Consolas", 14),
                              bg=PANEL, fg=TEXT, insertbackground=TEXT,
                              relief="flat", bd=6)
        self.entry.pack(side="left", padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._on_check())

        tk.Button(input_row, text="VERIFICAR", command=self._on_check,
                  bg=ACCENT, fg="white", font=("Consolas", 10, "bold"),
                  relief="flat", padx=10, cursor="hand2").pack(side="left")

        # Mensaje de error
        self.lbl_error = tk.Label(right, text="", bg=BG, fg=WARN_COLOR,
                                   font=("Consolas", 9))
        self.lbl_error.pack(anchor="w", pady=(6, 0))

        # Historial
        tk.Frame(right, bg="#444", height=1, width=240).pack(fill="x", pady=8)
        tk.Label(right, text="Historial de lecturas:",
                 bg=BG, fg=TEXT, font=("Consolas", 8)).pack(anchor="w")
        self.txt_historial = tk.Text(right, width=30, height=5,
                                      bg=PANEL, fg=TEXT, font=("Consolas", 8),
                                      relief="flat", state="disabled",
                                      bd=4)
        self.txt_historial.pack(anchor="w", pady=(2, 0))

        # Footer
        tk.Label(self, text="v1.0.0  |  Umbral: 80 °C  |  Python + tkinter",
                 bg=BG, fg="#555", font=("Consolas", 7)).pack(pady=10)

    # ── Callbacks ────────────────────────────────────────────
    def _on_check(self):
        raw = self.entry.get().strip()
        self.lbl_error.config(text="")

        # Validación de entrada
        try:
            temp = float(raw)
        except ValueError:
            self.lbl_error.config(text="⚠ Ingresá un número válido.")
            return

        # Validación de sensor (delegada a temperature.py)
        try:
            alarma = is_overheating(temp)
        except ValueError as e:
            self.lbl_error.config(text=f"⚠ Error de sensor: {e}")
            self._add_historial(temp, error=True)
            return

        self._update_display(temp)
        self._add_historial(temp, alarma=alarma)
        self.entry.delete(0, tk.END)

    def _update_display(self, temp):
        try:
            alarma = is_overheating(temp)
        except ValueError:
            return

        draw_thermometer(self.canvas, temp)
        self.lbl_temp.config(text=f"{temp:.1f}°C")

        if alarma:
            self.lbl_estado.config(text="⚠  ALARMA: TEMPERATURA ALTA", fg=HOT_COLOR)
            self._flash()
        else:
            self.lbl_estado.config(text="✅  TEMPERATURA NORMAL", fg=OK_COLOR)

    def _add_historial(self, temp, alarma=False, error=False):
        linea = f"{temp:.1f}°C"
        if error:
            linea += "  ← ERROR SENSOR"
        elif alarma:
            linea += "  ← ⚠ ALARMA"
        else:
            linea += "  ← OK"
        linea += "\n"

        self.txt_historial.config(state="normal")
        self.txt_historial.insert("1.0", linea)   # más reciente arriba
        self.txt_historial.config(state="disabled")

    def _flash(self, count=0):
        """Parpadeo suave del label de alarma."""
        if count >= 6:
            self.lbl_estado.config(fg=HOT_COLOR)
            return
        color = BG if count % 2 == 0 else HOT_COLOR
        self.lbl_estado.config(fg=color)
        self.after(250, lambda: self._flash(count+1))


# ─── Entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    app = HornoApp()
    app.mainloop()