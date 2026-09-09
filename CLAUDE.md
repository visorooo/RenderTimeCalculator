# RenderTimeCalculator

A single-window Windows app that turns time-per-frame × frame count into a total
render time and the wall-clock time it finishes. Public on
`visorooo/RenderTimeCalculator`, MIT. The README is the user documentation.

## Shape of the code

`render_time_calc.pyw` is the entire app — standard library only, `tkinter` plus
`datetime`, no dependencies to install. The `.pyw` extension is intentional: it
launches without a console window on Windows.

Four things in it:

- `resource_path(name)` — resolves the icon both from source and from inside a
  PyInstaller one-file bundle (`sys._MEIPASS`). Any new bundled asset must go
  through it or it will work in source and break in the exe.
- `parse_float(value, default)` — tolerant field parsing; empty and malformed
  inputs fall back rather than raising.
- `format_hms(total_seconds)` — the formatted duration string.
- `class App` — the UI.

## Running and building

```bash
python render_time_calc.pyw
```

```bash
pyinstaller RenderTimeCalc.spec
```

The `.spec` is the saved config and is preferred over retyping the flags; it
carries `--onefile --windowed` and the icon. Output lands in `dist/`.

## Release

`dist/` and `build/` are gitignored. `RenderTimeCalc.exe` (~11.6 MB) ships as a
GitHub Release asset, currently `v1.0.0`, with the local copy kept in the untracked
`dist/` for re-upload. Never commit the binary.

Keeping this dependency-free is the point — it is why the exe is 11 MB rather than
EXRtoPNG's 34 MB and why it starts instantly. Reach for the standard library before
adding a package.
