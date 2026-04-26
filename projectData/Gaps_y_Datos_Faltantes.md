# Datos Faltantes: Qué Descargar para Completar el Análisis

**Problemática:** Evaluar el mejor lugar para vivir desde múltiples aristas
**Fecha:** Febrero 2026

---

## Diagnóstico de Brechas

Los datasets actuales cubren bien las dimensiones económica, salud, educación, gobernanza y bienestar subjetivo. Sin embargo, **6 dimensiones críticas están ausentes o incompletas** y hay **datos desactualizados** que conviene reemplazar.

---

## PRIORIDAD ALTA — Gaps que afectan directamente la decisión de vivir en un lugar

### 🔴 1. Crimen y Seguridad (datos crudos)

**¿Por qué falta?** El dataset de calidad de vida tiene un puntaje de "Safety" por ciudad, pero es un índice agregado. No hay estadísticas crudas de homicidios, robos, crimen organizado, etc.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [World Crime Index 2023](https://www.kaggle.com/datasets/arsalanrehman/world-crime-index-2023) | Kaggle (Numbeo) | País/ciudad — índice de crimen y seguridad |
| [Crime Rate by Country 2023](https://www.kaggle.com/datasets/zabihullah18/crime-rate-by-country-2023) | Kaggle | País — tasa de crimen 2023 |
| [Global Organized Crime Index](https://www.kaggle.com/datasets/oscaryezfeijo/global-organized-crime-index-dataset) | Kaggle | País — crimen organizado |

**Variables que aportan:** Índice de crimen, índice de seguridad, tasa de homicidios, crimen organizado por país/ciudad.

---

### 🔴 2. Clima y Condiciones Meteorológicas

**¿Por qué falta?** Cero datos de temperatura, lluvia, humedad, horas de sol o riesgo climático. El clima es uno de los factores más subjetivos pero más determinantes en calidad de vida.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [Daily Temperature of Major Cities](https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities) | Kaggle | Ciudades principales — temperatura diaria histórica |
| [World Weather Repository (Daily)](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository) | Kaggle | Global — clima actualizado diariamente |
| [Global Daily Climate Data](https://www.kaggle.com/datasets/guillemservera/global-daily-climate-data) | Kaggle | Global — temperatura, precipitación, humedad |

**Variables que aportan:** Temperatura promedio/máx/mín, precipitación, humedad, horas de sol, velocidad del viento.

---

### 🔴 3. Calidad del Aire (AQI / PM2.5)

**¿Por qué falta?** Hay datos de emisiones de CO₂ por país (fuente de energía), pero no hay datos de **calidad del aire respirable** a nivel ciudad. El PM2.5 y AQI son indicadores directos de salud pública.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [World Air Quality Index by City](https://www.kaggle.com/datasets/adityaramachandran27/world-air-quality-index-by-city-and-coordinates) | Kaggle | Ciudad + coordenadas — AQI, CO, PM2.5, PM10, NO2 |
| [Global Air Pollution Dataset](https://www.kaggle.com/datasets/hasibalmuzdadid/global-air-pollution-dataset) | Kaggle | País — AQI categorías, múltiples contaminantes |
| [PM2.5 Air Pollution Dataset](https://www.kaggle.com/datasets/ineubytes/pm25-airpolution-dataset) | Kaggle | PM2.5 específicamente por país |

**Variables que aportan:** AQI global, PM2.5, PM10, NO₂, CO, SO₂ — esenciales para la dimensión salud ambiental.

---

### 🔴 4. Riesgo de Desastres Naturales

**¿Por qué falta?** No hay ningún dataset que cuantifique el riesgo de terremotos, huracanes, inundaciones o sequías por país/región. Fundamental para evaluar estabilidad a largo plazo.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [Global Disaster Risk Index (Time Series)](https://www.kaggle.com/datasets/tr1gg3rtrash/global-disaster-risk-index-time-series-dataset) | Kaggle | País — índice compuesto de riesgo por desastre |
| [WorldRiskIndex](https://data.humdata.org/dataset/worldriskindex) | HDX/ONU | 193 países — exposición + vulnerabilidad + capacidad de respuesta |
| [Natural Disasters 1900–2021](https://www.kaggle.com/datasets/brsdincer/all-natural-disasters-19002021-eosdis) | Kaggle | Histórico global — tipo de desastre, muertes, afectados |

**Variables que aportan:** Exposición a terremotos, tsunamis, ciclones, inundaciones, sequías; vulnerabilidad social; historial de eventos.

---

## PRIORIDAD MEDIA — Mejoran significativamente la calidad del análisis

### 🟡 5. World Happiness Report Actualizado (2020–2024)

**¿Por qué está desactualizado?** Los datos de felicidad en la carpeta solo llegan a 2019. Hay 5 años de datos nuevos que incluyen el impacto de la pandemia, guerra en Europa, etc.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [World Happiness Report 2024 (Yearly Updated)](https://www.kaggle.com/datasets/jainaru/world-happiness-report-2024-yearly-updated) | Kaggle | 2005–2024 — todos los años en un solo archivo |
| [World Happiness Report till 2023](https://www.kaggle.com/datasets/sazidthe1/global-happiness-scores-and-factors) | Kaggle | Hasta 2023 con factores detallados |

**Reemplaza:** `world-happiness/2015.csv` ... `2019.csv`

---

### 🟡 6. Libertad de Prensa e Índice de Democracia

**¿Por qué importa?** Los datos de régimen político del Prosperity Index son categóricos (liberal, autocracia, etc.). Hace falta un score continuo que capture matices de libertad civil, censura y pluralismo mediático.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [Press Freedom Index 2014–2023](https://www.kaggle.com/datasets/yajuvendrasinh/press-freedom-index-2014-to-2023) | Kaggle (RSF) | 180 países — score de libertad de prensa, serie temporal |
| [Freedom Rankings Per Country 2013–2022](https://www.kaggle.com/datasets/justin2028/freedom-in-the-world-2013-2022) | Kaggle (Freedom House) | País — libertades políticas y civiles |

**Variables que aportan:** Score RSF, ranking de libertad de prensa, derechos políticos, libertades civiles.

---

### 🟡 7. Movilidad y Acceso con Pasaporte (Visa/Inmigración)

**¿Por qué importa?** Para quien evalúa moverse, es esencial saber qué tan fácil es entrar, vivir legalmente y moverse desde ese país. También cuán bienvenidos son los extranjeros.

**Qué descargar:**

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| [Henley Passport Index Dataset](https://www.kaggle.com/datasets/joebeachcapital/henley-passport-index-dataset) | Kaggle | 199 países — score de movilidad del pasaporte |
| [2024 Passport Index Dataset](https://www.kaggle.com/datasets/mexwell/2024-passport-index-dataset) | Kaggle | Matriz completa de requisitos de visa entre países |

**Variables que aportan:** Destinos sin visa, mobility score, visa on arrival, facilidad de movimiento internacional.

---

### 🟡 8. Velocidad de Internet / Infraestructura Digital

**¿Por qué importa?** El dataset actual tiene "Internet Access" como un score subjetivo en el city-QoL, pero no hay datos de velocidad real medida (Mbps) ni cobertura de fibra. Crítico para nómadas digitales y trabajo remoto.

**Fuentes recomendadas:**
- [Ookla Speedtest Global Index](https://www.speedtest.net/global-index) — descargable desde su sitio oficial o Kaggle con búsqueda "ookla internet speed country"
- [Worldwide Internet Speed (Kaggle búsqueda)](https://www.kaggle.com/search?q=internet+speed+by+country) — varios datasets disponibles

**Variables que aportan:** Velocidad de descarga/subida fija y móvil por país (Mbps), ranking global.

---

## PRIORIDAD BAJA — Enriquecen análisis de perfiles específicos

### 🟢 9. Derechos LGBTQ+ por País

Para personas de esta comunidad, el marco legal y social es determinante. No existe ningún dataset que lo cubra en la carpeta actual.

**Fuente:** [ILGA World — Homophobia State-Sponsored (CSV)](https://ilga.org/state-sponsored-homophobia-report) o buscar en Kaggle "LGBTQ rights by country".

---

### 🟢 10. Costo del Sistema de Salud (desembolso real)

Existe data de mortalidad y cobertura, pero no de cuánto cuesta efectivamente recibir atención médica. El dato de "out of pocket health expenditure" en countries-2023 es parcial.

**Fuente:** [WHO Global Health Expenditure Database](https://apps.who.int/nha/database) — exportable en CSV.

---

### 🟢 11. Igualdad Salarial y Mercado Laboral Reciente

El dataset de AI jobs es sectorial (solo IA). Falta un dataset más amplio de salarios por profesión y país, especialmente post-pandemia.

**Fuente:** [Kaggle — "global salary dataset 2023"](https://www.kaggle.com/search?q=global+salary+by+country+2023) — varios datasets disponibles.

---

### 🟢 12. Caminabilidad y Transporte Urbano (Walkability)

No hay datos de Walk Score, acceso a transporte público o infraestructura peatonal por ciudad. Solo existe el puntaje de "Commute" en city-QoL como indicador agregado.

**Fuente:** [Walk Score Open Data](https://www.walkscore.com/cities-and-neighborhoods/) — parcialmente disponible; buscar en Kaggle "walkability score city".

---

## Resumen de Prioridades de Descarga

| Prioridad | Dataset a descargar | Dimensión que cubre |
|-----------|--------------------|--------------------|
| 🔴 Alta | World Crime Index 2023 | Seguridad real |
| 🔴 Alta | Daily Temperature of Major Cities | Clima |
| 🔴 Alta | World Air Quality Index by City | Calidad del aire |
| 🔴 Alta | Global Disaster Risk Index | Riesgo de desastres |
| 🟡 Media | World Happiness Report 2024 | Bienestar actualizado |
| 🟡 Media | Press Freedom Index 2014–2023 | Libertades civiles |
| 🟡 Media | Henley Passport Index 2024 | Movilidad / inmigración |
| 🟡 Media | Internet Speed by Country | Infraestructura digital |
| 🟢 Baja | LGBTQ+ Rights by Country | Inclusión social |
| 🟢 Baja | Global Health Expenditure | Costo real de salud |
| 🟢 Baja | Global Salary Dataset 2023 | Mercado laboral amplio |
| 🟢 Baja | Walkability Score by City | Movilidad urbana |

---

## Cobertura Proyectada con Datos Completos

```
Economía y costo de vida    ████████████ 95%
Vivienda                    ██████████░░ 85%
Salud pública               █████████░░░ 80%  → mejora con AQI y salud expenditure
Seguridad                   ██████░░░░░░ 50%  → requiere crime index
Clima y medioambiente        ████░░░░░░░░ 35%  → requiere clima + AQI + desastres
Libertades civiles          ████████░░░░ 70%  → mejora con press freedom
Bienestar subjetivo         ███████████░ 90%  → con happiness 2024
Infraestructura digital     ██████░░░░░░ 50%  → requiere internet speed
Movilidad internacional     ░░░░░░░░░░░░ 0%   → requiere passport index
Inclusión (LGBTQ+)          ░░░░░░░░░░░░ 0%   → requiere dataset específico
```

---

*Análisis elaborado con base en revisión del inventario existente y búsqueda de fuentes disponibles en Kaggle, HDX y organismos internacionales.*
