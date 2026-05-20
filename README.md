# Proyecto Big Data: Análisis del Mejor Lugar para Vivir

## Descripción General

Proyecto de análisis de datos que combina ingeniería de datos, aprendizaje no supervisado y visualización geoespacial para responder una pregunta práctica: **¿cuál es el mejor país o ciudad para vivir?**

El proyecto integra múltiples fuentes de datos internacionales, construye índices compuestos de habitabilidad por país, aplica clustering con K-Means y Clustering Jerárquico, y genera mapas mundiales interactivos con los resultados.

---

## Estructura del Proyecto

```
Proyecto_BigData/
├── data/                                          # Datasets de entrada (trackeados)
│   ├── customers_large_dataset.csv                # Clientes shopping (10,000 registros)
│   └── uaScoresDataFrame-csv-2.csv                # 266 ciudades del mundo
├── data_external/                                 # Datasets pesados (excluidos del repo, ~1.3 GB)
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
│   ├── 01_analisis_mejor_lugar_para_vivir.ipynb   # Análisis principal
│   ├── 02_clustering_ciudades.ipynb               # K-Means sobre 266 ciudades
│   └── 03_clustering_educativo.ipynb              # Clase teórico-práctica
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
│   │   ├── mapa_clusters.html
│   │   └── mapa_habitabilidad.html
│   └── figures/
│       └── output.png
├── docs/
│   ├── Gaps_y_Datos_Faltantes.md
│   ├── INSTRUCCIONES_DESCARGA.md                  # Configuración Kaggle API
│   └── Revision_Datos_Mejor_Lugar_Para_Vivir.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Notebooks

### 1. `notebooks/01_analisis_mejor_lugar_para_vivir.ipynb` — Análisis Principal

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
- Exploración de distribuciones y matriz de correlaciones entre índices
- Construcción de Índice Compuesto de Habitabilidad (promedio ponderado)
- Imputación de valores faltantes con mediana, estandarización z-score
- K-Means con k=4 (validado con método del codo y coeficiente de silueta)
- Reducción dimensional con PCA para visualización
- Mapas coropletos interactivos con Plotly

**Hallazgos principales:**

*Top 5 países (Índice Compuesto):*
1. Luxemburgo — 79.3
2. Dinamarca — 78.7
3. Finlandia — 78.5
4. Suiza — 78.2
5. Noruega — 77.4

*Clusters identificados (k=4):*

| Cluster | Países | Score medio | Perfil |
|---------|--------|-------------|--------|
| Cluster 2 | 42 | 72.4 | Alto desarrollo (Europa occidental, Oceanía) |
| Cluster 3 | 13 | 55.4 | Emergentes dinámicos (Corea del Sur, EAU, Qatar) |
| Cluster 0 | 86 | 48.1 | Intermedios globales (México, Perú, Bhutan) |
| Cluster 1 | 67 | 38.7 | Bajo desempeño (Yemen, Haití, Afganistán) |

*Patrones geográficos:* Europa concentra el 74.4% del Cluster 2; África concentra el 85.2% del Cluster 1. Asia presenta la mayor diversidad, distribuida en todos los clusters.

---

### 2. `notebooks/02_clustering_ciudades.ipynb` — Análisis de Ciudades

K-Means y Clustering Jerárquico sobre 266 ciudades del mundo con 17 métricas de calidad urbana.

**Preprocesamiento:** estandarización + PCA (10 componentes, 91.45% de varianza explicada)

**Resultado con k=6 clusters:**

| Cluster | Ciudades representativas | Perfil |
|---------|--------------------------|--------|
| 0 | Almaty, El Cairo, Karachi | Vivienda cara, bajo desarrollo |
| 1 | Bali, La Habana, Portland | Seguras y tolerantes, aisladas |
| 2 | Copenhague, Berlín, Auckland | Economías desarrolladas de primer mundo |
| 3 | Nueva York, Dubai, Boston | Hubs tecnológicos y financieros, alto costo |
| 4 | Atlanta, Phoenix, Charlotte | Ciudades estadounidenses de clase media |
| 5 | Barcelona, Estambul, Bangkok | Hubs globales con buen balance calidad/costo |

---

### 3. `notebooks/03_clustering_educativo.ipynb` — Notebook Educativo

Introducción teórico-práctica a los algoritmos de clustering.

**Contenidos:**
- K-Means sobre el dataset Olivetti Faces (400 imágenes, PCA a 100 componentes)
- Elección de k óptimo: método del codo con `KneeLocator` y coeficiente de silueta
- Clustering Jerárquico sobre datos de clientes de shopping (dendrograma, método Ward)
- Comparación entre ambos algoritmos

---

## Pipeline de Datos

El proyecto incluye un pipeline reproducible para construir los índices a nivel país desde cero.

### `scripts/download_datasets.py`

Descarga automática de 8 datasets desde Kaggle API y los organiza en `data_external/`:

```bash
python scripts/download_datasets.py
```

Requiere credenciales configuradas en `~/.kaggle/kaggle.json`. Ver `docs/INSTRUCCIONES_DESCARGA.md`.

### `src/build_country_indices.py`

Construye `outputs/country_category_indices.csv` a partir de los datasets en `data_external/`:

```bash
python src/build_country_indices.py
```

**Proceso interno:**
1. Normalización de nombres de país (maneja variaciones ortográficas y abreviaciones)
2. Extracción de variables por categoría, normalización a escala 0–100 (winsorized minmax)
3. Ponderación de variables primarias vs. secundarias
4. Filtro de cobertura: país incluido solo si tiene ≥30% cobertura en la categoría o fuente primaria

**Salidas en `outputs/`:**
- `country_category_indices.csv` — tabla de índices final
- `audit_variable_scores.csv` — desglose de cada variable y su score
- `audit_category_coverage.csv` — auditoría de completitud
- `unmatched_country_names.csv` — países sin mapeo exitoso

---

## Datasets

### `data/customers_large_dataset.csv`

10,000 registros de clientes con: `CustomerID`, `Genre`, `Age`, `Annual Income (k$)`, `Spending Score (1-100)`.
Usado en el notebook educativo para segmentación de clientes.

### `data/uaScoresDataFrame-csv-2.csv`

266 ciudades del mundo con 17 métricas de calidad urbana (escala 0–10): Housing, Cost of Living, Startups, Venture Capital, Travel Connectivity, Commute, Business Freedom, Safety, Healthcare, Education, Environmental Quality, Economy, Taxation, Internet Access, Leisure & Culture, Tolerance, Outdoors.

### `outputs/country_category_indices.csv` (generado)

208 países × 9 índices temáticos (escala 0–100). Entrada principal del análisis de habitabilidad. Generado por `src/build_country_indices.py`.

### Olivetti Faces (desde scikit-learn)

400 imágenes en escala de grises de 40 personas (64×64 px). Cargado directamente con `sklearn.datasets.fetch_olivetti_faces`.

---

## Resultados Generados

| Archivo | Descripción |
|---------|-------------|
| `ranking_paises_clusters.csv` | Tabla país → cluster asignado + score de habitabilidad |
| `outputs/maps/mapa_clusters.html` | Mapa mundial interactivo coloreado por cluster |
| `outputs/maps/mapa_habitabilidad.html` | Mapa mundial con gradiente por Índice Compuesto (0–100) |

Los archivos `.html` se pueden abrir directamente en cualquier navegador web.

---

## Tecnologías y Librerías

| Herramienta | Uso |
|-------------|-----|
| **Python 3.8+** | Lenguaje principal |
| **Jupyter Notebook** | Entorno de análisis interactivo |
| **Pandas** | Manipulación de datos tabulares |
| **NumPy** | Operaciones numéricas y matriciales |
| **Scikit-learn** | KMeans, PCA, Silhouette, StandardScaler |
| **SciPy** | Clustering jerárquico, dendrogramas |
| **Matplotlib / Seaborn** | Visualizaciones estáticas |
| **Plotly** | Mapas coropletos interactivos |
| **Kneed** | Detección automática del punto de codo |
| **pycountry_convert** | Mapeo ISO3 → continente |
| **openpyxl** | Lectura de archivos Excel |
| **Kaggle API** | Descarga de datasets |

---

## Instalación y Uso

### Requisitos previos

- Python 3.8 o superior
- pip

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy kneed plotly pycountry-convert openpyxl jupyter ipykernel
```

### Uso rápido (con datos ya generados)

```bash
git clone <url-del-repositorio>
cd Proyecto_BigData
jupyter notebook
```

Abrir `notebooks/01_analisis_mejor_lugar_para_vivir.ipynb` — los archivos en `outputs/` ya están incluidos en el repositorio como release artifacts, así que el notebook se puede ejecutar sin reproducir el pipeline.

### Reproducción completa del pipeline

```bash
# 1. Configurar Kaggle API (ver docs/INSTRUCCIONES_DESCARGA.md)
# 2. Descargar datasets a data_external/
python scripts/download_datasets.py

# 3. Construir índices por país → outputs/
python src/build_country_indices.py

# 4. Ejecutar el análisis
jupyter notebook notebooks/01_analisis_mejor_lugar_para_vivir.ipynb
```

---

## Flujo de Trabajo

```
Datasets internacionales (Kaggle, ONU, World Bank)
        ↓
scripts/download_datasets.py  →  data_external/ (9 carpetas temáticas)
        ↓
src/build_country_indices.py  →  outputs/country_category_indices.csv (208 países × 9 índices)
        ↓
notebooks/01_analisis_mejor_lugar_para_vivir.ipynb
  ├── EDA: distribuciones, correlaciones, valores faltantes
  ├── Índice Compuesto de Habitabilidad
  ├── Preprocesamiento: imputación + z-score
  ├── K-Means (k=4, validado con Elbow + Silhouette)
  ├── PCA 2D para visualización
  └── Mapas mundiales interactivos (Plotly)
        ↓
outputs/ranking_paises_clusters.csv + outputs/maps/mapa_clusters.html + outputs/maps/mapa_habitabilidad.html
```

---

## Conceptos Teóricos

### K-Means

Asigna cada punto al centroide más cercano e itera hasta convergencia. Minimiza la varianza intra-clúster (SSE/Inercia).

- **Ventajas:** eficiente y escalable, centroides interpretables
- **Limitaciones:** requiere k conocido de antemano, sensible a outliers y forma esférica de clusters

### Clustering Jerárquico Aglomerativo

Construye una jerarquía de clusters fusionando pares de forma ascendente. Visualizado mediante dendrograma.

- **Ventajas:** no requiere k de antemano, estructura jerárquica interpretable
- **Limitaciones:** O(n²) en memoria y tiempo, no apto para datasets muy grandes

### Métricas de Evaluación

| Métrica | Descripción | Valor ideal |
|---------|-------------|-------------|
| **Inertia (SSE)** | Suma de distancias al cuadrado a los centroides | Minimizar |
| **Silhouette Score** | Cohesión intra-clúster vs. separación inter-clúster | Maximizar (–1 a 1) |

---

## Autor

Proyecto desarrollado como parte de un curso de Big Data y Machine Learning.

---

## Licencia

Uso educativo. Los datasets incluidos son de dominio público o de uso académico.