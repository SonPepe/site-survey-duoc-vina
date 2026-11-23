# Explicación del código

La herramienta es **un solo archivo HTML** (`index.html`) con HTML, CSS y JavaScript sin librerías externas. Funciona abriéndolo en el navegador o desde GitHub Pages.

Como `index.html` lleva incrustados el plano (PNG en base64) y la grilla de muros, que juntos ocupan unos 150 KB de texto ilegible, el código fuente legible está separado en `src/`:

```
src/
├── template.html            ← todo el código (HTML + CSS + JS), sin los datos base64
├── build.py                 ← arma index.html reemplazando __PLAN__ y __GRID__
└── assets/
    ├── plano_planta_tipo.png  ← plano de la planta tipo, 2200 × 1240 px (30 px = 1 m)
    └── muros_grid.b64         ← grilla de muros: 367 × 207 celdas de 0,2 m, 1 byte por celda
```

Para regenerar la página después de editar el código:

```bash
python3 src/build.py
```

## 1. Estructura de la página

| Bloque | Qué contiene |
|---|---|
| `<header>` | Título, selector de **piso** (3, 4, 5), botones *Cargar diseño sugerido* y *Vaciar plano* |
| `.kpis` | 5 indicadores: % de área ≥ umbral, señal mínima, % con roaming, % con SINR ≥ 25 dB y número de APs |
| `.mapcol` | Barra de herramientas (Mover / Añadir / Quitar, banda, vista), `<canvas id="map">`, lectura del punto y leyenda |
| `aside.panel` | AP seleccionado (nombre, canal y potencia por radio), cobertura por sala, ajustes, modelo de propagación, guardar/compartir y "Cómo calcula" |

El CSS usa variables (`--bg`, `--accent`, etc.) con tema claro y oscuro, y se reacomoda en una columna bajo 1100 px de ancho, para que funcione en el teléfono.

## 2. Datos del edificio

```js
const PX=30, PW=2200, PH=1240;     // 30 px = 1 m → planta de 73,3 × 41,3 m
const GC=0.2, GW=367, GH=207;      // grilla de muros: celdas de 0,2 m
const HC=0.5;                      // grilla de cálculo: celdas de 0,5 m
```

- **`grid`**: la grilla de muros decodificada desde base64. Cada byte es un material: 0 = aire, 1 = muro exterior, 2 = núcleo de ascensores, 3 = columna, 4 = tabique metalcon, 5 = vidrio de sala, 6 = baranda de vidrio.
- **`MATS`**: nombre, atenuación en 2,4 y 5 GHz y color de cada material. Las atenuaciones se pueden editar desde el panel.
- **`INTERIOR`**, **`VOIDS`** y **`ROOMS`**: rectángulos en metros del contorno útil, de los vacíos (atrio, escaleras, ascensores) y de cada sala.
- **`cellRoom`**: clasifica cada celda de 0,5 m como fuera del edificio (−3), vacío (−2) o el índice de la sala (o pasillo). Con esto se sacan el área útil y la tabla por sala.
- **`GAIN`** y **`FS1M`**: ganancia de antena del AirEngine 5761-11 (3 / 2 dBi) y pérdida en espacio libre a 1 m (47,0 / 40,2 dB).
- **`CH24`** y **`CH5`**: canales disponibles; en 5 GHz dependen del ancho (20, 40 u 80 MHz), y los DFS (52–144) van marcados.

## 3. Estado

```js
let S = {...DEF_SETTINGS};   // banda, vista, umbral, ancho, n, ruido, alturas, pérdidas…
let APS = [];                // APs del piso visible
const DESIGNS = {3:…, 4:…, 5:…};  // diseño de cada piso
```

Cada AP es un objeto `{id, name, x, y, on5, on24, p5, p24, ch5, ch24, cnt, sig}`:

- `x`, `y` están en metros.
- `cnt` es el conteo de muros (caché).
- `sig` es la señal calculada por banda (caché).

`presetAps()` crea los 21 APs del diseño sugerido y renombra las salas según el piso (AP 311 → AP 411 → AP 511). Además deja encendida la radio de 2,4 GHz solo en 6 de ellos.

## 4. Cálculo de la señal

### `trace(ap)`: muros cruzados

Por cada celda de 0,5 m recorre la recta desde el AP con el algoritmo **DDA** (Amanatides–Woo) sobre la grilla de muros de 0,2 m. Cada vez que el rayo entra a un material distinto del anterior, suma 1 al contador de ese material.

El resultado se guarda en `ap.cnt` (6 contadores por celda). Solo se recalcula cuando el AP se mueve.

### `signal(ap, band)`: modelo de propagación

```js
d = max(1, √(dx² + dy² + (alturaAP − alturaUsuario)²));
señal = (Ptx + GAIN) − FS1M − 10·n·log10(d) − Σ (muros_i × pérdida_i);
```

Usa el modelo log-distancia con pérdida por muro (multi-wall). Guarda el resultado en `ap.sig[band]` para no repetir el cálculo al cambiar de vista.

### `aggregate()`: combinar los APs

Para cada celda calcula:

- `best`: la mejor señal y `bi`, qué AP la entrega (el AP que atiende).
- `cntThr`: cuántos APs superan el umbral (solape para roaming).
- `sinr`: `best − 10·log10(ruido + Σ señales de los APs en el mismo canal)`. El ruido se escala con el ancho de canal (+3 dB por cada duplicación). En 5 GHz se consideran mismo canal los que coinciden; en 2,4 GHz los que están a menos de 5 canales.

### `stats()`: indicadores y tabla

Recorre las celdas útiles (sin vacíos y, si se elige, sin el baño) y calcula los porcentajes de los KPIs y el promedio, mínimo, % sobre umbral y AP principal de cada sala. El indicador de cobertura sale como "Cumple" (≥ 99 %), "Casi" (≥ 95 %) o "No cumple".

## 5. Dibujo

`draw()` pinta en el `<canvas>` en este orden:

1. El plano (PNG).
2. El mapa de calor, generado en un canvas chico de 147 × 83 píxeles (una celda = un píxel) por `heatImage()` y escalado con suavizado. Se recorta para no pintar fuera del edificio ni en los vacíos.
3. El plano de nuevo en modo *multiply* al 35 %, para que los muros se vean sobre el color.
4. Opcional: la capa de muros detectados, con el color de cada material.
5. La sala resaltada, si se tocó una fila de la tabla.
6. Los APs: círculo numerado y etiqueta con el canal, o "apagado".

Hay 4 vistas: **Señal** (escala de −88 a −40 dBm), **SINR** (0 a 42 dB), **Solape** (0, 1, 2, 3, 4+ APs) y **AP que atiende** (un color por AP, con el ángulo dorado para que los vecinos se distingan).

`resize()` ajusta el canvas al ancho disponible y a la densidad de píxeles de la pantalla.

## 6. Interacción

| Acción | Código |
|---|---|
| Arrastrar un AP | `pointerdown` / `pointermove` / `pointerup`. Recalcula en cada `requestAnimationFrame` |
| Añadir AP | En modo *Añadir*, un toque crea un AP con `mkAp()` y le asigna canal con `autoChFor()` (el canal cuyo AP más cercano esté más lejos) |
| Quitar AP | En modo *Quitar*, tocando el AP, o con la tecla `Supr` |
| Mover fino | Flechas: 0,1 m; con Shift: 1 m |
| Lectura del punto | `probe()` muestra posición, sala, señal, AP, canal, SINR y número de APs |
| Editar AP | Formulario: nombre, radio encendida, canal y potencia por banda (`fillForm()`) |

## 7. Asignación automática de canales

`autoChannels(band)`:

1. Arma una matriz **W** con la interferencia entre cada par de APs: la señal del AP *b* en la posición del AP *a*, en mW.
2. Ordena los APs del que más interferencia recibe al que menos.
3. A cada AP le asigna el canal que minimiza la suma de W con los APs que ya tienen ese canal. Repite 3 pasadas para refinar.
4. **Rota la lista de canales según el piso** (`rot = (piso − 3) · canales / 3`). Así el piso 4 parte en otro canal que el 3, y los APs que quedan uno encima del otro no comparten canal.

La opción "Evitar DFS" quita los canales 52–144 antes de asignar.

## 8. Guardar y compartir

- `save()` guarda en `localStorage` (clave `ss-pisos-345-v1`) los ajustes y los APs de los tres pisos. `load()` los recupera al abrir la página.
- *Copiar JSON*: exporta el piso visible con sus ajustes. *Importar JSON*: lo carga con `applyImport()`.
- *Copiar tabla de APs*: copia una tabla separada por tabulaciones con los APs de **los tres pisos** (piso, nombre, x, y, canales y potencias), lista para pegar en Excel.

## 9. Arranque

Al abrir la página:

1. Si hay un diseño guardado, se carga.
2. Si no, se genera el diseño sugerido en los pisos 3, 4 y 5 con sus canales asignados.
3. Se muestra el piso 3 y un `ResizeObserver` redibuja cuando cambia el tamaño de la ventana.
