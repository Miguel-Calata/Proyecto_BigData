# Proyecto Big Data: Clustering con K-Means y Clustering Jerárquico

## Descripcion General

Este proyecto educativo implementa y compara dos de los algoritmos de clustering más importantes del aprendizaje no supervisado:

- **K-Means** (agrupamiento por centroides)
- **Clustering Jerárquico Aglomerativo**

A través de notebooks interactivos en Python, se aplican ambos algoritmos a distintos conjuntos de datos reales para analizar patrones, segmentar poblaciones y extraer conocimiento útil sin necesidad de etiquetas previas.

---

## Estructura del Proyecto

```
Proyecto_BigData/
├── data/
│   ├── customers_large_dataset.csv       # Dataset de clientes (10,000 registros)
│   └── uaScoresDataFrame-csv-2.csv       # Dataset de ciudades del mundo (266 ciudades)
├── Clase_16_Clustering_K_means_y_Jerárquico.ipynb   # Notebook educativo principal
├── Clustering_k_means_mi_data.ipynb                 # Notebook con análisis propio
├── .gitignore
└── README.md
```

---

## Contenido de los Notebooks

### 1. `Clase_16_Clustering_K_means_y_Jerárquico.ipynb`

Notebook educativo con explicaciones teóricas y ejemplos prácticos:

- **K-Means sobre el dataset Olivetti Faces**
  - Carga y preprocesamiento de 400 imágenes de rostros (64×64 píxeles)
  - Reducción de dimensionalidad con PCA (100 componentes)
  - Agrupamiento y visualización de clústeres
  - Selección del número óptimo de clústeres con el método del codo y el coeficiente de silueta

- **Clustering Jerárquico sobre datos de clientes de un shopping**
  - Segmentación de clientes según ingreso anual y puntuación de gasto
  - Generación e interpretación de dendrogramas
  - Comparación con resultados de K-Means

**Conceptos clave cubiertos:**
- Varianza intra-clúster e inter-clúster
- Método del codo (Elbow Method) con detección automática mediante `KneeLocator`
- Coeficiente de silueta (Silhouette Score)
- Métodos de enlace en clustering jerárquico: `ward`, `complete`, `average`, `single`

---

### 2. `Clustering_k_means_mi_data.ipynb`

Notebook de aplicación propia con análisis avanzado:

- **K-Means sobre datos de áreas urbanas del mundo**
  - Análisis de 266 ciudades con 17 métricas de calidad de vida
  - Preprocesamiento: estandarización z-score + PCA (10 componentes)
  - Identificación de grupos de ciudades con características similares
  - Interpretación de los clústeres resultantes

- **Clustering Jerárquico sobre el mismo dataset**
  - Comparación de resultados entre ambos métodos
  - Análisis de la estabilidad de los grupos obtenidos

---

## Datasets

### Dataset 1: Clientes de Shopping (`customers_large_dataset.csv`)

| Columna | Descripcion |
|---|---|
| `CustomerID` | Identificador único del cliente |
| `Genre` | Género (Male / Female) |
| `Age` | Edad del cliente |
| `Annual Income (k$)` | Ingreso anual en miles de dólares |
| `Spending Score (1-100)` | Puntuación de gasto (1 = poco, 100 = mucho) |

- **Registros:** 10,000 clientes
- **Caso de uso:** Segmentación de clientes para estrategias de marketing personalizadas

---

### Dataset 2: Áreas Urbanas del Mundo (`uaScoresDataFrame-csv-2.csv`)

Contiene puntuaciones (escala 0–10) para 266 ciudades del mundo en 17 dimensiones:

| Métrica | Descripcion |
|---|---|
| `Housing` | Calidad y disponibilidad de vivienda |
| `Cost of Living` | Índice de costo de vida general |
| `Startups` | Ecosistema emprendedor |
| `Venture Capital` | Acceso a capital de inversión |
| `Travel Connectivity` | Conectividad internacional |
| `Commute` | Calidad del transporte y movilidad urbana |
| `Business Freedom` | Libertad regulatoria para negocios |
| `Safety` | Seguridad y tasas de criminalidad |
| `Healthcare` | Calidad de los servicios de salud |
| `Education` | Calidad del sistema educativo |
| `Environmental Quality` | Calidad ambiental (aire, agua, verde urbano) |
| `Economy` | Estabilidad económica |
| `Taxation` | Nivel de carga impositiva |
| `Internet Access` | Disponibilidad de banda ancha |
| `Leisure & Culture` | Actividades culturales y de ocio |
| `Tolerance` | Tolerancia y diversidad social |
| `Outdoors` | Espacios verdes y actividades al aire libre |

- **Registros:** 266 ciudades
- **Metadatos adicionales:** nombre de ciudad, país, continente
- **Caso de uso:** Análisis comparativo de ciudades para planificación urbana o decisiones de reubicación

---

### Dataset 3: Olivetti Faces (desde `sklearn`)

- **Fuente:** `sklearn.datasets.fetch_olivetti_faces`
- **Registros:** 400 imágenes (10 fotos × 40 personas distintas)
- **Formato:** Imágenes en escala de grises de 64×64 píxeles (4,096 características por imagen)
- **Caso de uso:** Clustering de alta dimensionalidad para identificación de personas

---

## Tecnologías y Librerías

| Herramienta | Uso |
|---|---|
| **Python 3.x** | Lenguaje principal |
| **Jupyter Notebook** | Entorno de desarrollo interactivo |
| **NumPy** | Operaciones numéricas y matriciales |
| **Pandas** | Carga y manipulación de datos tabulares |
| **Matplotlib** | Visualización de datos y gráficos |
| **Scikit-learn** | Algoritmos de clustering, PCA, métricas |
| **SciPy** | Dendrogramas y clustering jerárquico avanzado |
| **Kneed** | Detección automática del punto de codo |

---

## Instalacion y Uso

### Requisitos previos

- Python 3.8 o superior
- pip

### Instalacion de dependencias

```bash
pip install numpy pandas matplotlib scikit-learn scipy kneed jupyter
```

### Ejecucion

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Proyecto_BigData

# Iniciar Jupyter Notebook
jupyter notebook
```

Luego abrir desde el navegador el notebook deseado:
- `Clase_16_Clustering_K_means_y_Jerárquico.ipynb` para la clase educativa
- `Clustering_k_means_mi_data.ipynb` para el análisis con datos propios

---

## Flujo de Trabajo

```
1. Carga y Exploracion de Datos
        ↓
2. Preprocesamiento
   - Estandarizacion (z-score)
   - Reduccion de dimensionalidad (PCA)
        ↓
3. Visualizacion Exploratoria
   - Scatter plots en espacio PCA
        ↓
4. Aplicacion de Clustering
   - K-Means
   - Clustering Jerarquico
        ↓
5. Seleccion del Numero Optimo de Clusters (k)
   - Metodo del Codo
   - Coeficiente de Silueta
   - Inspeccion del Dendrograma
        ↓
6. Interpretacion y Analisis de Resultados
   - Estadisticas por cluster
   - Identificacion de patrones
```

---

## Conceptos Teoricos Clave

### K-Means

Algoritmo iterativo que asigna cada punto al centroide más cercano y actualiza los centroides hasta convergencia. Minimiza la **varianza intra-clúster (SSE/Inertia)**.

**Ventajas:**
- Rápido y escalable a grandes datasets
- Fácil de interpretar mediante centroides
- Determinista con semilla fija (`random_state`)

**Limitaciones:**
- Requiere especificar `k` de antemano
- Sensible a la inicialización y a valores atípicos
- Asume clústeres de forma esférica

---

### Clustering Jerárquico Aglomerativo

Construye una jerarquía de clústeres fusionando pares de grupos similares de abajo hacia arriba. El resultado se visualiza como un **dendrograma**.

**Ventajas:**
- No requiere especificar `k` con anticipación
- Produce una jerarquía interpretable
- Captura estructuras a múltiples escalas

**Limitaciones:**
- Mayor costo computacional O(n²)
- No apto para datasets muy grandes sin optimizaciones

---

### Métricas de Evaluacion

| Métrica | Descripcion | Valor ideal |
|---|---|---|
| **Inertia (SSE)** | Suma de distancias al cuadrado a los centroides | Minimizar |
| **Silhouette Score** | Cohesión intra-clúster vs. separación inter-clúster | Maximizar (rango: -1 a 1) |

---

## Ejercicios Propuestos

Los notebooks incluyen ejercicios para reforzar los conceptos:

1. Aplicar K-Means con diferentes valores de `k` y comparar la inercia
2. Probar distintos métodos de enlace (`ward`, `complete`, `average`) en el clustering jerárquico
3. Evaluar el impacto del número de componentes PCA en los resultados del clustering
4. Identificar y analizar las características de cada clúster resultante
5. Comparar los resultados de ambos algoritmos sobre el mismo dataset

---

## Resultados Destacados

- La segmentacion de clientes del shopping permite identificar grupos con comportamientos de gasto diferenciados, facilitando estrategias de marketing personalizadas.
- El análisis de ciudades del mundo revela agrupaciones coherentes por región geográfica y nivel de desarrollo, con ciudades de características similares agrupadas independientemente del continente.
- El dataset Olivetti Faces demuestra la capacidad de K-Means para agrupar imágenes en alta dimensionalidad tras aplicar PCA.

---

## Autor

Proyecto desarrollado como parte de un curso de Big Data y Machine Learning.

---

## Licencia

Este proyecto es de uso educativo. Los datasets utilizados son de dominio público o para fines académicos.
