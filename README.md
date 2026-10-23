# organizador-descargas

Script de Python que ordena los archivos de una carpeta (por defecto `~/Descargas`) en subcarpetas según su tipo: imágenes, documentos, código, comprimidos, audio, video, etc.

Pensado para esa carpeta de Descargas que siempre termina hecha un desastre.

## Lo importante: corre en modo prueba primero

Por defecto **no mueve nada**: te muestra qué haría. Recién cuando le pasás `--aplicar` mueve de verdad. Así nunca reordenás mal una carpeta sin querer.

## Requisitos

Solo Python 3. No usa librerías externas (`pathlib` viene con Python).

## Uso

```bash
python3 organizador.py                      # prueba sobre ~/Descargas
python3 organizador.py --aplicar            # mueve de verdad
python3 organizador.py ~/otra/carpeta       # otra carpeta, en prueba
python3 organizador.py ~/otra -a            # otra carpeta, aplicando
```

| Opción | Qué hace |
|--------|----------|
| `carpeta` | Carpeta a ordenar (default: `~/Descargas`) |
| `-a`, `--aplicar` | Mover de verdad (sin esto, solo muestra qué haría) |

## Qué tiene en cuenta

- **No pisa archivos:** si ya existe uno con el mismo nombre en el destino, agrega un número (`foto.jpg` → `foto_1.jpg`).
- **No toca carpetas ni archivos ocultos:** solo mueve archivos sueltos.
- **Extensiones desconocidas** van a una carpeta `Otros`.

Las categorías se configuran en el diccionario `CATEGORIAS` arriba del script: agregá o cambiá extensiones a gusto.

## Roadmap

- [x] v1: ordenar por tipo, con modo prueba y sin pisar archivos
- [ ] v2: ordenar por fecha (subcarpetas por año/mes)
- [ ] v3: deshacer la última corrida
