#!/usr/bin/env python3
"""
Script para descargar los datasets faltantes del análisis "Mejor Lugar para Vivir"
y colocarlos automáticamente en las carpetas temáticas correctas.

REQUISITOS:
    pip install kaggle

CONFIGURACIÓN:
    1. Ve a https://www.kaggle.com/settings/account
    2. Sección "API" → clic en "Create New Token"
    3. Se descargará un archivo kaggle.json
    4. Colócalo en:
       - Mac/Linux: ~/.kaggle/kaggle.json
       - Windows:   C:\\Users\\<usuario>\\.kaggle\\kaggle.json
    5. Ejecuta este script desde cualquier terminal:
       python download_datasets.py

El script descarga y organiza todo automáticamente.
"""

import os
import sys
import zipfile
import shutil
import json

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE DESTINO
# ─────────────────────────────────────────────

# Detectar automáticamente la carpeta del proyecto (donde está este script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = SCRIPT_DIR
TEMP = os.path.join(BASE, "_temp_downloads")

# Mapeo: dataset Kaggle → carpeta destino
DATASETS = [
    # ── PRIORIDAD ALTA ──────────────────────────────────────────────────────────
    {
        "kaggle_id":   "arsalanrehman/world-crime-index-2023",
        "destino":     "PRINCIPAL/06_seguridad_y_criminalidad/world-crime-index-2023",
        "descripcion": "World Crime Index 2023 (Numbeo)",
        "prioridad":   "🔴 ALTA"
    },
    {
        "kaggle_id":   "sudalairajkumar/daily-temperature-of-major-cities",
        "destino":     "PRINCIPAL/09_clima_y_desastres/daily-temperature-major-cities",
        "descripcion": "Temperatura diaria de ciudades principales",
        "prioridad":   "🔴 ALTA"
    },
    {
        "kaggle_id":   "adityaramachandran27/world-air-quality-index-by-city-and-coordinates",
        "destino":     "PRINCIPAL/05_medioambiente_y_sostenibilidad/world-air-quality-index",
        "descripcion": "World Air Quality Index por ciudad (AQI, PM2.5, NO2, CO)",
        "prioridad":   "🔴 ALTA"
    },
    {
        "kaggle_id":   "tr1gg3rtrash/global-disaster-risk-index-time-series-dataset",
        "destino":     "PRINCIPAL/09_clima_y_desastres/global-disaster-risk-index",
        "descripcion": "Índice Global de Riesgo de Desastres Naturales",
        "prioridad":   "🔴 ALTA"
    },
    # ── PRIORIDAD MEDIA ─────────────────────────────────────────────────────────
    {
        "kaggle_id":   "jainaru/world-happiness-report-2024-yearly-updated",
        "destino":     "PRINCIPAL/01_calidad_de_vida_y_bienestar/world-happiness-2024",
        "descripcion": "World Happiness Report 2024 (reemplaza datos hasta 2019)",
        "prioridad":   "🟡 MEDIA"
    },
    {
        "kaggle_id":   "yajuvendrasinh/press-freedom-index-2014-to-2023",
        "destino":     "PRINCIPAL/07_gobernanza_y_libertades/press-freedom-index",
        "descripcion": "Press Freedom Index 2014–2023 (RSF)",
        "prioridad":   "🟡 MEDIA"
    },
    {
        "kaggle_id":   "joebeachcapital/henley-passport-index-dataset",
        "destino":     "PRINCIPAL/08_migracion_y_movilidad/henley-passport-index",
        "descripcion": "Henley Passport Index (movilidad internacional por pasaporte)",
        "prioridad":   "🟡 MEDIA"
    },
    {
        "kaggle_id":   "justin2028/freedom-in-the-world-2013-2022",
        "destino":     "PRINCIPAL/07_gobernanza_y_libertades/freedom-in-the-world",
        "descripcion": "Freedom in the World Rankings 2013–2022 (Freedom House)",
        "prioridad":   "🟡 MEDIA"
    },
]


# ─────────────────────────────────────────────
#  FUNCIONES
# ─────────────────────────────────────────────

def check_kaggle():
    """Verifica que Kaggle esté instalado y con credenciales."""
    try:
        import kaggle  # noqa: F401
    except ImportError:
        print("❌  El paquete 'kaggle' no está instalado.")
        print("    Ejecuta: pip install kaggle")
        sys.exit(1)

    cred_paths = [
        os.path.expanduser("~/.kaggle/kaggle.json"),
        os.path.join(os.environ.get("USERPROFILE", ""), ".kaggle", "kaggle.json"),
    ]
    creds_found = any(os.path.exists(p) for p in cred_paths)
    if not creds_found:
        print("❌  No se encontró kaggle.json con tus credenciales.")
        print("    Ve a https://www.kaggle.com/settings/account → API → 'Create New Token'")
        print("    y guarda el archivo en ~/.kaggle/kaggle.json")
        sys.exit(1)

    print("✅  Kaggle API configurada correctamente.\n")


def download_and_place(dataset: dict):
    """Descarga un dataset de Kaggle y lo mueve a la carpeta destino."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    kaggle_id   = dataset["kaggle_id"]
    destino_rel = dataset["destino"]
    descripcion = dataset["descripcion"]
    prioridad   = dataset["prioridad"]

    destino_abs = os.path.join(BASE, destino_rel)
    temp_dir    = os.path.join(TEMP, kaggle_id.replace("/", "__"))

    print(f"{prioridad}  {descripcion}")
    print(f"     Kaggle: {kaggle_id}")
    print(f"     Destino: {destino_rel}")

    # Si ya existe y tiene contenido, saltar
    if os.path.exists(destino_abs) and os.listdir(destino_abs):
        print("     ⏭️   Ya descargado, se omite.\n")
        return

    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(destino_abs, exist_ok=True)

    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(
            kaggle_id,
            path=temp_dir,
            unzip=True,
            quiet=False,
        )

        # Mover todos los archivos descargados al destino final
        for fname in os.listdir(temp_dir):
            src = os.path.join(temp_dir, fname)
            dst = os.path.join(destino_abs, fname)
            shutil.move(src, dst)

        print(f"     ✅  Descargado y colocado en: {destino_rel}\n")

    except Exception as e:
        print(f"     ❌  Error al descargar: {e}\n")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def create_climate_folder():
    """Crea la carpeta de clima/desastres si no existe."""
    folder = os.path.join(BASE, "PRINCIPAL/09_clima_y_desastres")
    os.makedirs(folder, exist_ok=True)


def cleanup():
    """Elimina la carpeta temporal."""
    if os.path.exists(TEMP):
        shutil.rmtree(TEMP)


def print_summary():
    """Imprime un árbol de la estructura final."""
    print("\n" + "=" * 55)
    print("📁  ESTRUCTURA FINAL — PRINCIPAL/")
    print("=" * 55)
    principal = os.path.join(BASE, "PRINCIPAL")
    if os.path.exists(principal):
        for folder in sorted(os.listdir(principal)):
            folder_path = os.path.join(principal, folder)
            if os.path.isdir(folder_path):
                datasets = [d for d in os.listdir(folder_path)
                            if os.path.isdir(os.path.join(folder_path, d))]
                print(f"  📂 {folder}  ({len(datasets)} datasets)")
                for ds in sorted(datasets):
                    print(f"       └── {ds}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  DESCARGA DE DATASETS — Mejor Lugar para Vivir")
    print("=" * 55)
    print(f"  Directorio base: {BASE}\n")

    check_kaggle()
    create_climate_folder()
    os.makedirs(TEMP, exist_ok=True)

    for ds in DATASETS:
        download_and_place(ds)

    cleanup()
    print_summary()
    print("\n✅  ¡Todos los datasets han sido descargados y organizados!")


if __name__ == "__main__":
    main()
