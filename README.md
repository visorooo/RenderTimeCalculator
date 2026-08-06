# Render Time Calculator

A tiny standalone Windows app for estimating 3D render time. Enter the time per
frame and the number of frames, and it gives you the total render time, the total
in seconds, and the **wall-clock time it finishes if you start now**.

Built at [VISOR](https://github.com/visorooo) for 3D/CGI/VFX production.

## Download

Grab `RenderTimeCalc.exe` from the [Releases](../../releases) page. No installer,
no dependencies — double-click and it runs.

## Use

1. Enter time per frame as **hours / minutes / seconds**.
2. Enter the **number of frames**.
3. Read off:
   - total render time (formatted)
   - total seconds
   - the date and time it finishes if started now

## Run from source

Pure standard library — `tkinter` ships with Python, so there's nothing to install.

```
python render_time_calc.pyw
```

## Build the .exe

```
pip install pyinstaller
pyinstaller --onefile --windowed --name "RenderTimeCalc" --icon render_time_calc.ico render_time_calc.pyw
```

The exe lands in `dist\`. `RenderTimeCalc.spec` is the saved PyInstaller config
if you prefer `pyinstaller RenderTimeCalc.spec`.

## Files

| File | What it is |
|---|---|
| `render_time_calc.pyw` | The whole app — single file, no dependencies |
| `render_time_calc.ico` | App icon, baked into the exe |
| `RenderTimeCalc.spec` | PyInstaller build config |

## License

MIT — see [LICENSE](LICENSE).
