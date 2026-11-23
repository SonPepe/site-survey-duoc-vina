"""Arma index.html a partir de la plantilla y los recursos.

Uso (desde la raíz del repo):  python3 src/build.py
"""
import base64
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent

html = (SRC / "template.html").read_text(encoding="utf-8")
plano = base64.b64encode((SRC / "assets" / "plano_planta_tipo.png").read_bytes()).decode()
grid = (SRC / "assets" / "muros_grid.b64").read_text().strip()

html = html.replace("__PLAN__", "data:image/png;base64," + plano, 1)
html = html.replace("__GRID__", grid, 1)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("index.html generado:", len(html), "caracteres")
