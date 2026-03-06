# Proyecto BigData — Clustering No Supervisado

Proyecto de aprendizaje automático no supervisado que aplica técnicas de **K-Means** y **Clustering Jerárquico** sobre distintos conjuntos de datos reales. El objetivo es segmentar datos sin etiquetas previas y evaluar la calidad de los agrupamientos obtenidos.

---

## Contenido

- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Datasets](#datasets)
- [Algoritmos y Técnicas](#algoritmos-y-técnicas)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Resultados](#resultados)

---

## Descripción

Este proyecto cubre el flujo completo de clustering no supervisado:

1. **Preprocesamiento**: carga de datos, estandarización de características con `StandardScaler`.
2. **Reducción de dimensionalidad**: Análisis de Componentes Principales (PCA) para visualización y mejora de rendimiento.
3. **K-Means Clustering**: agrupamiento basado en centroides con selección óptima de `k`.
4. **Clustering Jerárquico Aglomerativo**: construcción de dendrogramas y análisis de la jerarquía de clusters.
5. **Evaluación**: método del codo (*Elbow Method*) y puntuación de silueta (*Silhouette Score*).

El proyecto incluye un notebook educativo (Clase 16) y un notebook de aplicación práctica sobre datos propios.

---

## Estructura del Proyecto

```
Proyecto_BigData/
├── data/
│   ├── customers_large_dataset.csv          # Dataset de clientes (10 000 registros)
│   └── uaScoresDataFrame-csv-2.csv          # Puntuaciones de calidad de vida urbana (266 ciudades)
├── Clase_16_Clustering_K_means_y_Jerárquico.ipynb   # Notebook educativo principal
├── Clustering_k_means_mi_data.ipynb                  # Notebook de análisis con datos propios
├── .gitignore
└── README.md
```

---

## Datasets

### 1. Urban Areas — Calidad de Vida (`uaScoresDataFrame-csv-2.csv`)

| Campo | Descripción |
|-------|-------------|
| `UA_Name` | Nombre del área urbana |
| `UA_Country` | País |
| `UA_Continent` | Continente |
| `Housing` | Puntuación de vivienda (0–10) |
| `Cost of Living` | Costo de vida (0–10) |
| `Startups` | Ecosistema de startups (0–10) |
| `Venture Capital` | Acceso a capital de riesgo (0–10) |
| `Travel Connectivity` | Conectividad de transporte (0–10) |
| `Commute` | Tiempos de desplazamiento (0–10) |
| `Business Freedom` | Libertad de negocios (0–10) |
| `Safety` | Seguridad (0–10) |
| `Healthcare` | Salud (0–10) |
| `Education` | Educación (0–10) |
| `Environmental Quality` | Calidad ambiental (0–10) |
| `Economy` | Economía (0–10) |
| `Taxation` | Fiscalidad (0–10) |
| `Internet Access` | Acceso a internet (0–10) |
| `Leisure & Culture` | Ocio y cultura (0–10) |
| `Tolerance` | Tolerancia (0–10) |
| `Outdoors` | Espacios al aire libre (0–10) |

- **Filas**: 266 áreas urbanas de distintos países y continentes.
- **Objetivo**: segmentar ciudades por su perfil de calidad de vida.

---

### 2. Clientes — Segmentación (`customers_large_dataset.csv`)

| Campo | Descripción |
|-------|-------------|
| `CustomerID` | Identificador único del cliente |
| `Genre` | Género (Male / Female) |
| `Age` | Edad en años |
| `Annual Income (k$)` | Ingreso anual en miles de dólares |
| `Spending Score (1-100)` | Puntuación de comportamiento de gasto |

- **Filas**: 10 000 registros de clientes.
- **Objetivo**: identificar segmentos de clientes con perfiles de compra similares.

---

### 3. Olivetti Faces Dataset (integrado en scikit-learn)

- 400 imágenes en escala de grises (64×64 px) de 40 personas distintas (10 fotos por persona).
- Utilizado para demostrar K-Means sobre datos de alta dimensionalidad con reducción PCA.

---

## Algoritmos y Técnicas

### K-Means Clustering
- Agrupamiento iterativo basado en la minimización de la distancia euclidiana a los centroides.
- Selección del número óptimo de clusters `k` mediante:
  - **Método del Codo**: se grafica la SSE (*Sum of Squared Errors*) vs. `k` y se localiza el punto de inflexión con `KneeLocator`.
  - **Silhouette Score**: mide qué tan similar es un punto a su propio cluster comparado con los demás.

### Clustering Jerárquico Aglomerativo
- Construye una jerarquía de clusters de abajo hacia arriba.
- Visualización mediante **dendrogramas** (`scipy.cluster.hierarchy`).
- Métodos de enlace disponibles: `ward`, `complete`, `average`, `single`.

### PCA (Análisis de Componentes Principales)
- Reducción de dimensionalidad para visualización 2D/3D de clusters.
- Retención de varianza explicada configurable (`n_components`).

---

## Requisitos

- Python 3.8+
- Jupyter Notebook o JupyterLab

### Dependencias principales

```
numpy
pandas
matplotlib
scikit-learn
scipy
kneed
```

---

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd Proyecto_BigData
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Instalar las dependencias:

```bash
pip install numpy pandas matplotlib scikit-learn scipy kneed
```

---

## Uso

Lanzar Jupyter y abrir el notebook deseado:

```bash
jupyter notebook
```

### Notebooks disponibles

| Notebook | Descripción |
|----------|-------------|
| `Clase_16_Clustering_K_means_y_Jerárquico.ipynb` | Notebook educativo: K-Means sobre Olivetti Faces, selección de `k`, Clustering Jerárquico y dendrogramas. |
| `Clustering_k_means_mi_data.ipynb` | Aplicación práctica: segmentación de áreas urbanas y clientes con los datasets propios. |

Ejecutar las celdas de forma secuencial en cada notebook.

---

## Resultados

### Áreas Urbanas
- Se identificaron **8 clusters** de ciudades con perfiles de calidad de vida similares mediante K-Means.
- La reducción PCA permite visualizar la separación entre grupos en 2D.
- El clustering jerárquico valida los agrupamientos obtenidos.

### Olivetti Faces
- K-Means con **k=40** clusters agrupa correctamente las imágenes por identidad facial.
- PCA con 100 componentes retiene suficiente varianza para una segmentación de calidad.

### Clientes
- El dataset de 10 000 clientes permite identificar segmentos diferenciados por edad, ingreso y puntuación de gasto, útiles para estrategias de marketing.

---

## Stack Tecnológico

| Categoría | Librería |
|-----------|----------|
| Manipulación de datos | `pandas`, `numpy` |
| Visualización | `matplotlib` |
| Machine Learning | `scikit-learn` |
| Jerarquía / Dendrogramas | `scipy` |
| Detección del codo | `kneed` |
| Entorno interactivo | Jupyter Notebook |
