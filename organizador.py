#!/usr/bin/env python3
"""
Organizador de descargas - v1

Ordena los archivos de una carpeta (por defecto ~/Descargas) en subcarpetas
segun su tipo: imagenes, documentos, codigo, comprimidos, etc.

Por defecto corre en modo PRUEBA (dry-run): te MUESTRA que haria, pero no
mueve nada. Cuando estes conforme, lo corrés con --aplicar para que mueva
de verdad. Asi no reordenás mal una carpeta sin querer.

Uso:
    python3 organizador.py                      # prueba sobre ~/Descargas
    python3 organizador.py --aplicar            # mueve de verdad
    python3 organizador.py ~/otra/carpeta       # otra carpeta, en prueba
    python3 organizador.py ~/otra -a            # otra carpeta, aplicando
"""

import argparse
from pathlib import Path

# Extension (en minuscula) -> carpeta destino.
# Agregá o cambiá lo que quieras.
CATEGORIAS = {
    # Imagenes
    ".jpg": "Imagenes", ".jpeg": "Imagenes", ".png": "Imagenes",
    ".gif": "Imagenes", ".webp": "Imagenes", ".svg": "Imagenes",
    ".bmp": "Imagenes", ".heic": "Imagenes",
    # Documentos
    ".pdf": "Documentos", ".doc": "Documentos", ".docx": "Documentos",
    ".txt": "Documentos", ".odt": "Documentos", ".rtf": "Documentos",
    ".xlsx": "Documentos", ".xls": "Documentos", ".csv": "Documentos",
    ".pptx": "Documentos", ".ppt": "Documentos",
    # Codigo
    ".py": "Codigo", ".js": "Codigo", ".html": "Codigo", ".css": "Codigo",
    ".json": "Codigo", ".sh": "Codigo", ".c": "Codigo", ".cpp": "Codigo",
    ".java": "Codigo", ".sql": "Codigo",
    # Comprimidos
    ".zip": "Comprimidos", ".rar": "Comprimidos", ".tar": "Comprimidos",
    ".gz": "Comprimidos", ".7z": "Comprimidos",
    # Audio y video
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".m4a": "Audio",
    ".mp4": "Video", ".mkv": "Video", ".avi": "Video", ".mov": "Video",
    # Instaladores
    ".deb": "Instaladores", ".appimage": "Instaladores", ".exe": "Instaladores",
}

CARPETA_OTROS = "Otros"   # para extensiones que no esten en la tabla


def parsear_args():
    p = argparse.ArgumentParser(
        description="Ordena los archivos de una carpeta por tipo, en subcarpetas."
    )
    p.add_argument("carpeta", nargs="?", default=str(Path.home() / "Descargas"),
                   help="carpeta a ordenar (default: ~/Descargas)")
    p.add_argument("-a", "--aplicar", action="store_true",
                   help="mover de verdad (sin esto, solo muestra que haria)")
    return p.parse_args()


def carpeta_destino(archivo):
    """Devuelve el NOMBRE de la subcarpeta donde va este archivo."""
    return CATEGORIAS.get(archivo.suffix.lower(), CARPETA_OTROS)


def destino_sin_pisar(carpeta, nombre):
    """
    Si ya existe un archivo con ese nombre en el destino, le agrega un numero
    para no pisarlo: foto.jpg -> foto_1.jpg -> foto_2.jpg ...
    """
    destino = carpeta / nombre
    if not destino.exists():
        return destino
    base, ext = destino.stem, destino.suffix
    n = 1
    while (carpeta / f"{base}_{n}{ext}").exists():
        n += 1
    return carpeta / f"{base}_{n}{ext}"


def main():
    args = parsear_args()
    base = Path(args.carpeta).expanduser()

    if not base.is_dir():
        print(f"No existe la carpeta: {base}")
        return

    # Los nombres de las subcarpetas que creamos: no queremos mover ESAS.
    nuestras_carpetas = set(CATEGORIAS.values()) | {CARPETA_OTROS}

    modo = "APLICANDO (mueve de verdad)" if args.aplicar else "PRUEBA (no mueve nada)"
    print(f"Carpeta: {base}")
    print(f"Modo: {modo}\n")

    movidos = 0
    for archivo in base.iterdir():
        # Solo archivos sueltos. Saltamos carpetas (incluidas las nuestras)
        # y los archivos ocultos (los que empiezan con punto).
        if not archivo.is_file() or archivo.name.startswith("."):
            continue

        nombre_destino = carpeta_destino(archivo)
        carpeta_dest = base / nombre_destino
        destino = destino_sin_pisar(carpeta_dest, archivo.name)

        print(f"  {archivo.name}  ->  {nombre_destino}/{destino.name}")

        if args.aplicar:
            carpeta_dest.mkdir(exist_ok=True)   # crea la subcarpeta si no existe
            archivo.rename(destino)

        movidos += 1

    print()
    if movidos == 0:
        print("No habia archivos sueltos para ordenar.")
    elif args.aplicar:
        print(f"Listo. {movidos} archivo(s) ordenado(s).")
    else:
        print(f"{movidos} archivo(s) se moverian. Corré con --aplicar para hacerlo de verdad.")


if __name__ == "__main__":
    main()
