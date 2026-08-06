"""
Render Time Calculator
-----------------------
A tiny standalone desktop app for estimating 3D render time.

Enter the time per frame (hours / minutes / seconds) and the number of frames,
and get the total render time, total seconds, and the wall-clock time it'll
finish if you start now.

No external dependencies (pure standard library / tkinter).

To build a single Windows .exe (run on a Windows machine with Python installed):
    pip install pyinstaller
    pyinstaller --onefile --windowed --name "RenderTimeCalc" render_time_calc.pyw

The .exe lands in the "dist" folder.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


def resource_path(name):
    """Path to a bundled resource, works for plain script and PyInstaller exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

# --- Dark theme palette ---------------------------------------------------
BG        = "#1e1e1e"   # window background
BORDER    = "#3a3a3d"   # entry border (idle)
TEXT      = "#eaeaea"   # primary text
MUTED     = "#8c8c90"   # secondary labels
ACCENT    = "#4a9eff"   # highlight (total + focused border)
ENTRY_BG  = "#333336"   # entry background


def parse_float(value, default=0.0):
    try:
        return float(str(value).strip().replace(",", "."))
    except (ValueError, AttributeError):
        return default


def format_hms(total_seconds):
    total_seconds = int(round(total_seconds))
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    parts = []
    if h > 0:
        parts.append(f"{h}h")
    if m > 0 or h > 0:
        parts.append(f"{m}m")
    parts.append(f"{s}s")
    return " ".join(parts)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Render Time Calculator")
        root.minsize(320, 360)
        root.configure(bg=BG, padx=22, pady=20)
        root.columnconfigure(0, weight=1)
        self._set_icon()

        self._build_styles()

        # ---- Section 1: time per frame ----
        ttk.Label(root, text="TIME PER FRAME", style="Head.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )

        tf = tk.Frame(root, bg=BG)
        tf.grid(row=1, column=0, sticky="ew")
        for c in range(3):
            tf.columnconfigure(c, weight=1, uniform="units")
        self.h = self._unit_entry(tf, 0, "hours", "0", pad=(0, 5))
        self.m = self._unit_entry(tf, 1, "min", "0", pad=(5, 5))
        self.s = self._unit_entry(tf, 2, "sec", "0", pad=(5, 0))

        ttk.Separator(root, orient="horizontal").grid(
            row=2, column=0, sticky="ew", pady=16
        )

        # ---- Section 2: number of frames ----
        ttk.Label(root, text="NUMBER OF FRAMES", style="Head.TLabel").grid(
            row=3, column=0, sticky="w", pady=(0, 6)
        )
        self.frames = self._entry(root, font=("Segoe UI", 12))
        self.frames.grid(row=4, column=0, sticky="ew", ipady=5)
        self.frames.insert(0, "0")

        ttk.Separator(root, orient="horizontal").grid(
            row=5, column=0, sticky="ew", pady=16
        )

        # ---- Outputs ----
        out = tk.Frame(root, bg=BG)
        out.grid(row=6, column=0, sticky="ew")
        out.columnconfigure(1, weight=1)

        self.hms_var = tk.StringVar(value="—")
        self.secs_var = tk.StringVar(value="—")
        self.eta_var = tk.StringVar(value="—")

        self._out_row(out, 0, "Total render time", self.hms_var, accent=True)
        self._out_row(out, 1, "Total seconds", self.secs_var)
        self._out_row(out, 2, "Done at (if started now)", self.eta_var)

        for entry in (self.h, self.m, self.s, self.frames):
            entry.bind("<KeyRelease>", lambda _e: self.calculate())

        self.calculate()

    # -- icon --
    def _set_icon(self):
        # Tell Windows this is its own app so the taskbar uses our icon,
        # not the default Python one.
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "gabe.rendertimecalc"
            )
        except Exception:
            pass
        # Title-bar + taskbar icon.
        try:
            self.root.iconbitmap(resource_path("render_time_calc.ico"))
        except Exception:
            pass

    # -- styling --
    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Head.TLabel", background=BG, foreground=MUTED,
                        font=("Segoe UI", 9, "bold"))
        style.configure("Unit.TLabel", background=BG, foreground=MUTED,
                        font=("Segoe UI", 8))
        style.configure("Out.TLabel", background=BG, foreground=MUTED,
                        font=("Segoe UI", 10))
        style.configure("Val.TLabel", background=BG, foreground=TEXT,
                        font=("Segoe UI", 11))
        style.configure("ValBig.TLabel", background=BG, foreground=ACCENT,
                        font=("Segoe UI", 18, "bold"))
        style.configure("TSeparator", background=BORDER)

    def _entry(self, parent, font):
        # Classic tk.Entry -> flat corners, no ttk border artifacts.
        # width=1 keeps it from forcing a minimum; grid sticky="ew" stretches it.
        return tk.Entry(
            parent, width=1, font=font, justify="center",
            bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT,
            disabledbackground=ENTRY_BG,
        )

    def _unit_entry(self, parent, col, label, default, pad):
        box = tk.Frame(parent, bg=BG)
        box.grid(row=0, column=col, sticky="ew", padx=pad)
        e = self._entry(box, font=("Segoe UI", 12))
        e.pack(fill="x", ipady=5)
        e.insert(0, default)
        ttk.Label(box, text=label, style="Unit.TLabel").pack(anchor="w", pady=(3, 0))
        return e

    def _out_row(self, parent, r, label, var, accent=False):
        ttk.Label(parent, text=label, style="Out.TLabel").grid(
            row=r, column=0, sticky="w", pady=5
        )
        style = "ValBig.TLabel" if accent else "Val.TLabel"
        ttk.Label(parent, textvariable=var, style=style).grid(
            row=r, column=1, sticky="e", pady=5, padx=(24, 0)
        )

    def calculate(self):
        per_frame = (parse_float(self.h.get()) * 3600
                     + parse_float(self.m.get()) * 60
                     + parse_float(self.s.get()))
        frames = parse_float(self.frames.get())
        total = per_frame * frames

        if total > 0:
            self.hms_var.set(format_hms(total))
            self.secs_var.set(f"{int(round(total)):,} s")
            done = datetime.now() + timedelta(seconds=total)
            day_diff = (done.date() - datetime.now().date()).days
            label = done.strftime("%H:%M")
            if day_diff == 1:
                label += " (+1 day)"
            elif day_diff > 1:
                label += f" (+{day_diff} days)"
            self.eta_var.set(label)
        else:
            self.hms_var.set("—")
            self.secs_var.set("—")
            self.eta_var.set("—")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
