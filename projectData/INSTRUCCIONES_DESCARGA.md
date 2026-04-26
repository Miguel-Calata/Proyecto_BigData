# Cómo descargar los datasets faltantes

El script `download_datasets.py` descarga y organiza automáticamente los **8 datasets de alta/media prioridad** identificados en el análisis de brechas.

---

## Pasos

### 1. Obtener credenciales de Kaggle (gratis)

1. Ve a [https://www.kaggle.com](https://www.kaggle.com) y crea una cuenta si no tienes una
2. Una vez con sesión: **Settings → API → "Create New Token"**
3. Se descargará un archivo `kaggle.json`
4. Colócalo en:
   - **Mac / Linux:** `~/.kaggle/kaggle.json`
   - **Windows:** `C:\Users\<tu_usuario>\.kaggle\kaggle.json`

### 2. Instalar el paquete de Kaggle

```bash
pip install kaggle
```

### 3. Ejecutar el script

Desde terminal, navega hasta esta carpeta y ejecuta:

```bash
python download_datasets.py
```

El script descarga todo, descomprime los archivos y los coloca automáticamente en las carpetas temáticas correctas.

---

## Qué se descarga y dónde queda

| Prioridad | Dataset | Carpeta destino |
|-----------|---------|----------------|
| 🔴 Alta | World Crime Index 2023 | `PRINCIPAL/06_seguridad_y_criminalidad/` |
| 🔴 Alta | Daily Temperature of Major Cities | `PRINCIPAL/09_clima_y_desastres/` |
| 🔴 Alta | World Air Quality Index by City | `PRINCIPAL/05_medioambiente_y_sostenibilidad/` |
| 🔴 Alta | Global Disaster Risk Index | `PRINCIPAL/09_clima_y_desastres/` |
| 🟡 Media | World Happiness Report 2024 | `PRINCIPAL/01_calidad_de_vida_y_bienestar/` |
| 🟡 Media | Press Freedom Index 2014–2023 | `PRINCIPAL/07_gobernanza_y_libertades/` |
| 🟡 Media | Henley Passport Index | `PRINCIPAL/08_migracion_y_movilidad/` |
| 🟡 Media | Freedom in the World 2013–2022 | `PRINCIPAL/07_gobernanza_y_libertades/` |

---

## Si el script falla para algún dataset

Descárgalo manualmente desde Kaggle y colócalo en la carpeta indicada arriba:

- [World Crime Index 2023](https://www.kaggle.com/datasets/arsalanrehman/world-crime-index-2023)
- [Daily Temperature of Major Cities](https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities)
- [World Air Quality Index by City](https://www.kaggle.com/datasets/adityaramachandran27/world-air-quality-index-by-city-and-coordinates)
- [Global Disaster Risk Index](https://www.kaggle.com/datasets/tr1gg3rtrash/global-disaster-risk-index-time-series-dataset)
- [World Happiness Report 2024](https://www.kaggle.com/datasets/jainaru/world-happiness-report-2024-yearly-updated)
- [Press Freedom Index 2014–2023](https://www.kaggle.com/datasets/yajuvendrasinh/press-freedom-index-2014-to-2023)
- [Henley Passport Index](https://www.kaggle.com/datasets/joebeachcapital/henley-passport-index-dataset)
- [Freedom in the World 2013–2022](https://www.kaggle.com/datasets/justin2028/freedom-in-the-world-2013-2022)
