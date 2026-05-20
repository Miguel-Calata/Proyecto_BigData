# Proyecto Big Data: Análisis del Mejor Lugar para Vivir

## Descripción General

Proyecto de análisis de datos que combina ingeniería de datos, aprendizaje no supervisado y visualización geoespacial para responder una pregunta práctica: **¿cuál es el mejor país para vivir?**

A partir de ~20 datasets internacionales se construyen 9 índices temáticos por país (208 países), se aplica K-Means para segmentarlos en perfiles de habitabilidad y se generan mapas mundiales interactivos con los resultados.

---

## Estructura del Proyecto

```
Proyecto_BigData/
├── data_external/                                 # Datasets crudos (excluidos del repo, ~1.3 GB)
│   ├── 01_calidad_de_vida_y_bienestar/
│   ├── 02_economia_y_costo_de_vida/
│   ├── 03_salud_publica/
│   ├── 04_vivienda_y_urbanismo/
│   ├── 05_medioambiente_y_sostenibilidad/
│   ├── 06_seguridad_y_criminalidad/
│   ├── 07_gobernanza_y_libertades/
│   ├── 08_migracion_y_movilidad/
│   └── 09_clima_y_desastres/
├── notebooks/
│   └── 01_analisis_mejor_lugar_para_vivir.ipynb   # Análisis principal
├── src/                                           # Pipeline de construcción de índices
│   ├── build_country_indices.py
│   └── country_aliases.json
├── scripts/                                       # CLI entry points
│   └── download_datasets.py                       # Descarga automática desde Kaggle
├── outputs/                                       # Release artifacts (trackeados)
│   ├── country_category_indices.csv               # 208 países × 9 índices
│   ├── ranking_paises_clusters.csv                # País → cluster + score
│   ├── audit_category_coverage.csv
│   ├── audit_variable_scores.csv
│   ├── unmatched_country_names.csv
│   ├── maps/
│   │   ├── mapa_clusters.html                     # Choropleth coloreado por cluster
│   │   └── mapa_habitabilidad.html                # Choropleth por Índice Compuesto
│   └── figures/                                   # 13 figuras PNG generadas por el notebook
├── docs/
│   └── Revision_Datos_Mejor_Lugar_Para_Vivir.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Notebook Principal

### `notebooks/01_analisis_mejor_lugar_para_vivir.ipynb`

Análisis completo de habitabilidad a nivel país usando 9 índices temáticos construidos a partir de datos internacionales.

**Fuente de datos:** `outputs/country_category_indices.csv` — 208 países × 9 índices (escala 0–100)

**Índices analizados:**

| Índice | Descripción |
|--------|-------------|
| Bienestar | Felicidad, prosperidad, calidad de vida subjetiva |
| Economía | PIB per cápita, costo de vida, asequibilidad |
| Salud | Esperanza de vida, mortalidad infantil, acceso sanitario |
| Vivienda y urbanismo | Calidad habitacional, ratio asequibilidad, mercado inmobiliario |
| Medio ambiente | Calidad del aire, emisiones, índices SDG |
| Seguridad | Índice de crimen, seguridad percibida |
| Gobernanza | Libertad política, libertad de prensa, estado de derecho |
| Movilidad | Índice de pasaporte, facilidad de migración |
| Clima | Confort climático, riesgo de desastres naturales |

**Metodología:**
- Exploración de distribuciones, valores faltantes y matriz de correlaciones entre índices
- Construcción de un Índice Compuesto de Habitabilidad (promedio ponderado de los 9 índices)
- Imputación de valores faltantes con mediana, estandarización z-score
- K-Means con k=4 (validado con método del codo y coeficiente de silueta)
- Reducción dimensional con PCA para visualización
- Choropleths interactivos con Plotly

---

## Resultados

### Top 5 países (Índice Compuesto de Habitabilidad)

1. Luxemburgo — **79.3**
2. Dinamarca — **78.7**
3. Finlandia — **78.5**
4. Suiza — **78.2**
5. Noruega — **77.4**

### Clusters identificados (k=4)

| Cluster | Países | Score medio | Perfil |
|---------|-------:|------------:|--------|
| 2 | 42 | 72.4 | **Alto desarrollo** — Europa Occidental, Oceanía, Norteamérica |
| 0 | 86 | 55.7 | **Intermedios globales** — gran parte de Latinoamérica, Europa del Este |
| 3 | 13 | 55.4 | **Economías ricas no-democráticas** — Golfo, Singapur, perfil con alta economía/seguridad pero baja gobernanza |
| 1 | 67 | 38.7 | **Bajo desempeño** — dominado por África subsahariana |

### Patrones geográficos

| Continente | Cluster dominante | % en cluster | Score medio |
|---|---|---:|---:|
| Europa | Cluster 2 (alto desarrollo) | 74.4% | 69.0 |
| África | Cluster 1 (bajo desempeño) | 85.2% | 41.3 |
| Sudamérica | Cluster 0 (intermedios) | 91.7% | 54.6 |
| Norteamérica | Cluster 0 (intermedios) | 72.0% | 55.0 |
| Oceanía | Cluster 0 (intermedios) | 78.6% | 57.0 |
| Asia | Distribuido en los 4 clusters | — | 50.2 |

Asia es el continente con mayor diversidad: se reparte entre el Cluster 0 (36%), Cluster 1 (32%), Cluster 3 (22%) y Cluster 2 (10%).

---

## Pipeline de Datos

El proyecto incluye un pipeline reproducible para construir los índices a nivel país desde cero.

### `scripts/download_datasets.py`

Descarga automática desde Kaggle API y los organiza en `data_external/`:

```bash
python scripts/download_datasets.py
```

Requiere credenciales configuradas en `~/.kaggle/kaggle.json`.

### `src/build_country_indices.py`

Construye `outputs/country_category_indices.csv` a partir de los datasets en `data_external/`:

```bash
python src/build_country_indices.py
```

**Proceso interno:**
1. Normalización de nombres de país (maneja variaciones ortográficas, abreviaciones, subdivisiones)
2. Extracción de variables por categoría, normalización a escala 0–100 (winsorized minmax)
3. Ponderación de variables primarias vs. secundarias
4. Filtro de cobertura: país incluido sólo si tiene ≥30% cobertura en la categoría o tiene fuente primaria

**Salidas en `outputs/`:**

| Archivo | Descripción |
|---|---|
| `country_category_indices.csv` | Tabla de índices final (208 países × 9 categorías) |
| `audit_variable_scores.csv` | Desglose de cada variable y su score |
| `audit_category_coverage.csv` | Auditoría de completitud por categoría |
| `unmatched_country_names.csv` | Países sin mapeo exitoso (diagnóstico) |

---

## Outputs Visuales

### Figuras estáticas (`outputs/figures/`)

13 PNGs generados al ejecutar el notebook:

| Archivo | Contenido |
|---|---|
| `01_valores_faltantes.png` | % de países sin dato por índice |
| `02_distribucion_indices.png` | Histogramas + KDE de los 9 índices |
| `03_boxplot_indices.png` | Boxplot comparativo de los 9 índices |
| `04_matriz_correlacion.png` | Heatmap de correlaciones entre índices |
| `05_top_bottom_15.png` | Top 15 / Bottom 15 países por Índice Compuesto |
| `06_elbow_silhouette.png` | Selección de k: método del codo + silueta |
| `07_pca_clusters.png` | Países proyectados en 2D (PCA) coloreados por cluster |
| `08_radar_clusters.png` | Perfil promedio normalizado de cada cluster |
| `09_habitabilidad_por_cluster.png` | Boxplot del Índice de Habitabilidad por cluster |
| `10_heatmap_perfil_clusters.png` | Heatmap cluster × índice |
| `11_silueta.png` | Análisis de silueta por punto |
| `12_clusters_por_continente.png` | Composición de clusters por continente (stacked bar) |
| `13_habitabilidad_por_continente.png` | Boxplot del Índice por continente |

### Mapas interactivos (`outputs/maps/`)

| Archivo | Descripción |
|---|---|
| `mapa_clusters.html` | Choropleth mundial coloreado por cluster K-Means (interactivo) |
| `mapa_habitabilidad.html` | Choropleth mundial con gradiente del Índice Compuesto (0–100) |

Se abren directamente en cualquier navegador.

---

## Tecnologías y Librerías

| Herramienta | Uso |
|-------------|-----|
| **Python 3.8+** | Lenguaje principal |
| **Jupyter Notebook** | Entorno de análisis interactivo |
| **Pandas / NumPy** | Manipulación de datos y operaciones numéricas |
| **Scikit-learn** | KMeans, PCA, Silhouette, StandardScaler, SimpleImputer |
| **Matplotlib / Seaborn** | Visualizaciones estáticas |
| **Plotly + Kaleido** | Mapas coropletos interactivos + exportación PNG |
| **Kneed** | Detección automática del punto de codo |
| **pycountry-convert** | Mapeo ISO3 → continente |
| **Kaggle API** | Descarga automática de datasets |

---

## Instalación y Uso

### Requisitos previos

- Python 3.8 o superior
- pip

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Uso rápido (con datos ya generados)

```bash
git clone <url-del-repositorio>
cd Proyecto_BigData
jupyter notebook notebooks/01_analisis_mejor_lugar_para_vivir.ipynb
```

Los archivos en `outputs/` ya están incluidos en el repositorio como release artifacts, por lo que el notebook se puede ejecutar sin reproducir el pipeline ni configurar Kaggle.

### Reproducción completa del pipeline

```bash
# 1. Configurar Kaggle API (token en ~/.kaggle/kaggle.json)
# 2. Descargar datasets crudos a data_external/
python scripts/download_datasets.py

# 3. Construir índices por país → outputs/
python src/build_country_indices.py

# 4. Ejecutar el análisis
jupyter notebook notebooks/01_analisis_mejor_lugar_para_vivir.ipynb
```

---

## Flujo de Trabajo

```
Datasets internacionales (Kaggle, ONU, World Bank, RSF, Numbeo…)
        ↓
scripts/download_datasets.py  →  data_external/ (9 carpetas temáticas)
        ↓
src/build_country_indices.py  →  outputs/country_category_indices.csv
        ↓
notebooks/01_analisis_mejor_lugar_para_vivir.ipynb
  ├── EDA: distribuciones, correlaciones, valores faltantes
  ├── Índice Compuesto de Habitabilidad
  ├── Preprocesamiento: imputación + z-score
  ├── K-Means (k=4, validado con Elbow + Silhouette)
  ├── PCA 2D para visualización
  └── Mapas mundiales interactivos (Plotly)
        ↓
outputs/ranking_paises_clusters.csv
outputs/figures/ (13 PNGs)
outputs/maps/{mapa_clusters,mapa_habitabilidad}.html
```

---

## Conceptos Teóricos

### K-Means

Asigna cada punto al centroide más cercano e itera hasta convergencia. Minimiza la varianza intra-clúster (SSE/Inercia).

- **Ventajas:** eficiente y escalable, centroides interpretables, determinista con `random_state`
- **Limitaciones:** requiere k conocido de antemano, sensible a outliers, asume clusters esféricos

### Métricas de Evaluación

| Métrica | Descripción | Valor ideal |
|---------|-------------|-------------|
| **Inercia (SSE)** | Suma de distancias al cuadrado a los centroides | Minimizar |
| **Silhouette Score** | Cohesión intra-clúster vs. separación inter-clúster | Maximizar (rango −1 a 1) |

---

## Autor

Proyecto desarrollado por Miguel Salvador Calata Rodríguez como parte de un curso de Big Data Impartido por la Doctora Liliana Ibeth Barbosa Santillan.

---

## Licencia

Uso educativo. Los datasets utilizados son de dominio público.
