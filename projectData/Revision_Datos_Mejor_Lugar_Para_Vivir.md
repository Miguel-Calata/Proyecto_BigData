# Revisión de Datos: Análisis del Mejor Lugar para Vivir

**Fecha de revisión:** Abril 2026 (actualizado — incorpora nuevos datasets)
**Objetivo:** Evaluar desde múltiples aristas y variables el mejor lugar para vivir
**Resultado general:** ✅ Los datos disponibles son altamente adecuados para esta problemática

---

## Resumen Ejecutivo

Se tienen **28 datasets** en total (20 originales + 8 nuevos incorporados tras el análisis de brechas). De ellos, **21 son directamente útiles** para evaluar calidad de vida, cubriendo ahora de forma completa todas las dimensiones relevantes: económica, salud, seguridad, educación, vivienda, medioambiente, gobernanza, bienestar subjetivo, movilidad, clima y desastres — tanto a nivel de **ciudades** como de **países**. Las brechas identificadas en la revisión de febrero 2026 han sido cubiertas en su totalidad.

---

## Datasets ALTAMENTE Relevantes (Usar como núcleo del análisis)

### 1. `city-quality-of-life-dataset/uaScoresDataFrame.csv`
**Nivel:** Ciudad | **Registros:** 266 ciudades globales

Es el dataset más directamente alineado con la pregunta. Contiene puntajes de calidad de vida en **17 dimensiones** por ciudad:

| Dimensión | Dimensión | Dimensión |
|-----------|-----------|-----------|
| Housing (Vivienda) | Safety (Seguridad) | Healthcare (Salud) |
| Cost of Living (Costo de vida) | Education (Educación) | Environmental Quality (Medio ambiente) |
| Startups (Emprendimiento) | Economy (Economía) | Taxation (Impuestos) |
| Venture Capital | Tolerance (Tolerancia) | Internet Access |
| Travel Connectivity | Leisure & Culture | Outdoors |
| Commute (Transporte) | Business Freedom | |

✅ **Ideal como base de un índice compuesto del mejor lugar para vivir a nivel ciudad.**

---

### 2. `2023-global-prosperity-index-w-region-politics/global_prosperity_regions_politics.csv`
**Nivel:** País | **Registros:** ~159 países | **Año:** 2023

Índice de prosperidad con dimensiones macro:
- Seguridad y Gobernanza
- Libertad personal
- Capital social
- Entorno empresarial
- Infraestructura y mercado
- Calidad económica
- Condiciones de vida, Salud, Educación
- Medioambiente natural
- **Régimen político** (liberal, autocracia, etc.)

✅ **Excelente para el eje de libertades civiles y calidad institucional.**

---

### 3. `world-happiness/` (2015, 2016, 2017, 2018, 2019)
**Nivel:** País | **Registros:** ~150 países por año | **Serie temporal:** 5 años

Variables del World Happiness Report:
- Score global de felicidad
- PIB per cápita (logarítmico)
- Apoyo social
- Esperanza de vida saludable
- Libertad de elección de vida
- Generosidad
- Percepción de corrupción

✅ **Permite análisis de tendencia de bienestar subjetivo. Altamente citado internacionalmente.**

---

### 4. `countries-of-the-world-2023/world-data-2023.csv`
**Nivel:** País | **Registros:** 196 países | **Año:** 2023

Cobertura de variables muy amplia:
- Densidad poblacional, superficie
- Tasa de natalidad, fertilidad
- CO₂, precio de gasolina
- IPC e inflación
- PIB, participación laboral, desempleo
- Matrícula escolar (primaria y terciaria)
- Mortalidad infantil, esperanza de vida
- Médicos por mil habitantes
- Salario mínimo, tasa impositiva
- Población urbana, idioma oficial, coordenadas

✅ **Dataset "todo en uno" para comparación entre países. Muy rico para análisis multivariado.**

---

### 5. `global-cost-of-living/cost-of-living_v2.csv`
**Nivel:** Ciudad | **Registros:** Cientos de ciudades | **Variables:** 55 columnas (x1–x55)

Contiene precios detallados de vida cotidiana (aun sin etiquetas visibles en encabezado, incluye restaurantes, transporte, supermercados, alquiler, servicios, etc. basado en la fuente Numbeo).

✅ **Fundamental para dimensión económica y comparación del poder adquisitivo real por ciudad.**

---

### 6. `sustainable-development-data/sustainable_development_report_2023.csv`
**Nivel:** País | **Serie temporal:** 2000–2022 + reporte 2023

Puntaje de los 17 Objetivos de Desarrollo Sostenible (ODS):
- Sin pobreza, Hambre cero, Salud, Educación
- Agua limpia, Energía limpia, Trabajo digno
- Ciudades sostenibles, Producción responsable
- Acción climática, Vida submarina y terrestre
- Paz, justicia e instituciones

✅ **Cubre la dimensión de sostenibilidad a largo plazo, clave para una decisión de vida.**

---

### 7. `global-housing-market-analysis-2015-2024/global_housing_market_extended.csv`
**Nivel:** País | **Serie temporal:** 2015–2024

Variables: House Price Index, Rent Index, Affordability Ratio, Mortgage Rate, Inflation Rate, GDP Growth, Population Growth, Urbanization Rate, Construction Index.

✅ **Esencial para evaluar la viabilidad de comprar o rentar en cada lugar.**

---

### 8. `human-development-report-2015/` (varios CSVs)
**Nivel:** País | Múltiples archivos

- `human_development.csv` — Índice HDI, esperanza de vida, educación, GNI per cápita
- `gender_inequality.csv` — Desigualdad de género
- `gender_development.csv` — Desarrollo diferenciado por género
- `inequality_adjusted.csv` — HDI ajustado por desigualdad
- `multidimensional_poverty.csv` — Pobreza en salud, educación, estándares de vida
- `historical_index.csv` — Tendencia histórica del HDI

✅ **Añade dimensión de equidad y desarrollo humano real, no solo riqueza bruta.**

---

## Nuevos Datasets Incorporados (Abril 2026)

> Estos datasets cubren las brechas identificadas en la revisión anterior.

### 9. `world-crime-index-2023/crime-index-2023.csv` 🆕
**Carpeta:** `PRINCIPAL/06_seguridad_y_criminalidad/` | **Nivel:** Ciudad | **Registros:** 416 ciudades | **Año:** 2023 | **Fuente:** Numbeo

Columnas: `Rank`, `City`, `Country`, `Crime Index`, `Safety Index`

Ranking de crimen y seguridad a nivel ciudad. Crime Index alto = mayor inseguridad; Safety Index es su inverso.

✅ **Cubre la brecha de seguridad a nivel ciudad. Complementa los puntajes de city-QoL con datos crudos de crimen.**

---

### 10. `world-happiness-2024/World-happiness-report-2024.csv` 🆕
**Carpeta:** `PRINCIPAL/01_calidad_de_vida_y_bienestar/` | **Nivel:** País | **Registros:** 143 países | **Año:** 2024

También incluye `World-happiness-report-updated_2024.csv` (2363 registros con serie temporal).

Columnas: `Country name`, `Regional indicator`, `Ladder score`, `Log GDP per capita`, `Social support`, `Healthy life expectancy`, `Freedom to make life choices`, `Generosity`, `Perceptions of corruption`

✅ **Actualiza los datos de bienestar subjetivo hasta 2024. Cubre la brecha de felicidad post-2019.**

---

### 11. `world-air-quality-index/AQI and Lat Long of Countries.csv` 🆕
**Carpeta:** `PRINCIPAL/05_medioambiente_y_sostenibilidad/` | **Nivel:** Ciudad | **Registros:** 16,695 ciudades | **Coordenadas:** Sí

Columnas: `Country`, `City`, `AQI Value`, `AQI Category`, `CO AQI Value`, `Ozone AQI Value`, `NO2 AQI Value`, `PM2.5 AQI Value`, `lat`, `lng`

✅ **Cubre la brecha de calidad del aire a nivel ciudad. Permite visualizaciones cartográficas de contaminación.**

---

### 12. `global-air-pollution-dataset/global air pollution dataset.csv` 🆕
**Carpeta:** `PRINCIPAL/05_medioambiente_y_sostenibilidad/` | **Nivel:** Ciudad | **Registros:** 23,463 ciudades

Columnas: `Country`, `City`, `AQI Value`, `AQI Category`, `CO`, `Ozone`, `NO2`, `PM2.5` (sin coordenadas, mayor cobertura de ciudades)

🔶 **Complementa world-air-quality-index con más ciudades. Ideal para enriquecer con merge por ciudad/país.**

---

### 13. `press-freedom-index/` (2014–2023, 10 archivos XLSX) 🆕
**Carpeta:** `PRINCIPAL/07_gobernanza_y_libertades/` | **Nivel:** País | **Cobertura:** ~180 países/año | **Fuente:** RSF

Columnas por año: `ISO`, `Score`, `Rank`, `Political Context`, `Economic Context`, `Legal Context`, `Social Context`, `Safety`, `Zone`, `Country_EN`, etc.

✅ **Cubre la brecha de libertad de prensa. Serie temporal de 10 años con desglose por contexto político, económico, legal y social.**

---

### 14. `freedom-in-the-world/Freedom in the World 2013-2022 Dataset (Ver 2.18.23).csv` 🆕
**Carpeta:** `PRINCIPAL/07_gobernanza_y_libertades/` | **Nivel:** País | **Registros:** 2,095 (países × años) | **Fuente:** Freedom House

Columnas: `Country/Territory`, `Region`, `Status`, `PR rating`, `CL rating`, dimensiones A–G (derechos políticos y libertades civiles)

✅ **Mide libertades civiles y derechos políticos 2013–2022. Complementa el Press Freedom Index con evaluación de democracia.**

---

### 15. `henley-passport-index/henley-passport-index-2026-03-17.csv` 🆕
**Carpeta:** `PRINCIPAL/08_migracion_y_movilidad/` | **Nivel:** País–País | **Registros:** ~45,000 pares | **Año:** Marzo 2026

Columnas: `Origin`, `Destination`, `Requirement` (visa-free, visa-on-arrival, e-visa, visa required, etc.)

✅ **Cubre la brecha de visas e inmigración. Mide la libertad de movimiento global por país de origen.**

---

### 16. `2024-passport-index-dataset/passport-index-matrix.csv` 🆕
**Carpeta:** `PRINCIPAL/08_migracion_y_movilidad/` | **Nivel:** País | **Registros:** 199 países | **Año:** 2024

Matriz cuadrada país×país con el tipo de acceso visatorio (0, 1, 2, 3...). Incluye variantes ISO2 e ISO3.

🔶 **Formato matriz alternativo al Henley Index. Útil para cálculos matriciales de movilidad global.**

---

### 17. `daily-temperature-major-cities/city_temperature.csv` 🆕
**Carpeta:** `PRINCIPAL/09_clima_y_desastres/` | **Nivel:** Ciudad | **Registros:** ~2.9 millones | **Serie:** 1995–presente

Columnas: `Region`, `Country`, `State`, `City`, `Month`, `Day`, `Year`, `AvgTemperature`

✅ **Cubre la brecha de clima y meteorología. Dataset masivo con temperaturas diarias históricas por ciudad.**

---

### 18. `global-disaster-risk-index/world_risk_index.csv` 🆕
**Carpeta:** `PRINCIPAL/09_clima_y_desastres/` | **Nivel:** País | **Registros:** 1,917 (países × años) | **Fuente:** WorldRiskIndex

Columnas: `Region`, `WRI`, `Exposure`, `Vulnerability`, `Susceptibility`, `Lack of Coping Capabilities`, `Lack of Adaptive Capacities`, `Year`

✅ **Cubre el riesgo de desastres naturales. Mide exposición, vulnerabilidad y capacidad de respuesta por país.**

---

### 19. `all-natural-disasters-19002021-eosdis/` 🆕
**Carpeta:** `PRINCIPAL/09_clima_y_desastres/` | **Nivel:** País | **Serie:** 1900–2021 | **Fuente:** EMDAT / NASA EOSDIS

Archivos: `1900_2021_DISASTERS.xlsx - emdat data.csv` y `1970-2021_DISASTERS.xlsx - emdat data.csv`

Columnas: `Year`, `Disaster Type`, `Disaster Subtype`, `Country`, `Region`, `Continent`, `Latitude`, `Longitude`, `Aid Contribution`, etc.

✅ **Base de datos histórica de desastres naturales más completa disponible (120 años). Permite calcular frecuencia e intensidad de eventos por región.**

---

### 20. `global-daily-climate-data/` 🆕
**Carpeta:** `PRINCIPAL/09_clima_y_desastres/` | **Nivel:** Ciudad/País | **Registros:** 1,245 ciudades con clima diario

Archivos:
- `cities.csv` — metadatos de ciudades (lat, lng, iso2, iso3)
- `countries.csv` — metadatos de países (población, área, capital, región)
- `daily_weather.parquet` — datos climáticos diarios (gran volumen, formato parquet)

✅ **Complementa la temperatura histórica con datos climáticos estructurados y coordenadas geoespaciales. El formato parquet es ideal para análisis de alto rendimiento.**

---

## Datasets MODERADAMENTE Relevantes (Útiles como complemento)

### 21. `who-worldhealth-statistics-2020-complete/` (~35 archivos CSV)
**Nivel:** País | **Año:** 2020 | Fuente: OMS

Incluye: esperanza de vida, mortalidad infantil, maternas, suicidios, malaria, tuberculosis, VIH, saneamiento básico, agua potable, médicos, farmacéuticos, etc.

🔶 **Muy rico para la dimensión salud pública.** Ideal para profundizar en el eje sanitario.

---

### 22. `emissions-by-country/` (GCB 2022)
**Nivel:** País | **Serie histórica larga**

Emisiones de CO₂ totales y per cápita por fuente (carbón, petróleo, gas, cemento, etc.)

🔶 **Relevante para quienes valoran el impacto ambiental y huella de carbono del lugar donde viven.**

---

### 23. `food-security-indicator-for-the-world-2016-2020/`
**Nivel:** País | **Serie:** 2016–2020 | Fuente: FAO

Indicadores de suficiencia alimentaria, suministro calórico, acceso a proteínas.

🔶 **Pertinente para zonas de riesgo alimentario o para evaluaciones completas de desarrollo.**

---

### 24. `global-ai-job-market-salary-2025/ai_job_dataset.csv`
**Nivel:** Trabajo individual | **Año:** 2024–2025

Datos de salarios en empleos de IA por país, nivel de experiencia, modalidad remota, tamaño de empresa.

🔶 **Relevante si el análisis incluye la dimensión de oportunidades laborales en economías del conocimiento.**

---

### 25. `move-very-far/share-of-the-population-that-was-born-in-another-country.csv`
**Nivel:** País

Porcentaje de población nacida en otro país → proxy de apertura a migrantes e integración.

🔶 **Útil como indicador de tolerancia y facilidad de adaptación para quien se muda.**

---

## Datasets NO Relevantes para esta problemática

| Dataset | Carpeta | Razón |
|---------|---------|-------|
| `careerbuilder-job-listing-2020/` | `COMPLEMENTARIO/` | Solo EE.UU., datos de hace 5 años, muy sectorial |
| `employeeturnover/` | `NO_RELEVANTE/` | Datos de RRHH internos, sin relevancia geográfica de calidad de vida |
| `educational-geospatial-data/` | `COMPLEMENTARIO/` | Solo útil para visualizaciones cartográficas |
| `life-expectancy-dataset-real/impv/` | `PRINCIPAL/03_salud_publica/` | Dataset ML ya procesado (X_train, y_test), usar solo como referencia |
| `_duplicados_ya_clasificados/` | `NO_RELEVANTE/` | Copias descargadas manualmente, ya integradas en PRINCIPAL |

---

## Mapa de Dimensiones Cubiertas (Actualizado)

| Dimensión | Datasets que la cubren | Estado |
|-----------|----------------------|--------|
| 💰 Economía y costo de vida | city-QoL, global-cost-of-living, countries-2023, prosperity-index | ✅ Completo |
| 🏠 Vivienda | city-QoL, global-housing-market, global-cost-of-living | ✅ Completo |
| 🏥 Salud | WHO statistics, countries-2023, HDR-2015, happiness, prosperity | ✅ Completo |
| 🎓 Educación | city-QoL, countries-2023, HDR-2015, prosperity, SDG report | ✅ Completo |
| 🔒 Seguridad | city-QoL, prosperity-index, **world-crime-index-2023** 🆕 | ✅ Completo |
| 🌿 Calidad del aire | city-QoL, **world-air-quality-index** 🆕, **global-air-pollution** 🆕 | ✅ Completo |
| 🌱 Sostenibilidad | SDG report, emissions, prosperity | ✅ Completo |
| 🗳️ Gobernanza y libertades | prosperity-index, **press-freedom-index** 🆕, **freedom-in-the-world** 🆕 | ✅ Completo |
| 😊 Bienestar subjetivo | world-happiness 2015–2019, **world-happiness-2024** 🆕 | ✅ Completo |
| 🌍 Sostenibilidad ODS | SDG report 2000–2022 | ✅ Completo |
| 👫 Igualdad de género | HDR-2015 (gender equality, gender development) | ✅ Completo |
| 🍽️ Seguridad alimentaria | food-security FAO | ✅ Completo |
| 💻 Mercado laboral tech | global-AI-jobs-2025 | ✅ Completo |
| 🛂 Movilidad y visas | move-very-far, **henley-passport-index** 🆕, **2024-passport-index** 🆕 | ✅ Completo |
| 🏙️ Urbanización | countries-2023, global-housing | ✅ Completo |
| 🌡️ Clima y temperatura | **daily-temperature-major-cities** 🆕, **global-daily-climate-data** 🆕 | ✅ Completo |
| ⚡ Desastres naturales | **global-disaster-risk-index** 🆕, **all-natural-disasters-EMDAT** 🆕 | ✅ Completo |

---

## Brechas Resueltas (vs. Revisión Anterior)

| Brecha identificada (feb. 2026) | Dataset que la cubre | Estado |
|--------------------------------|---------------------|--------|
| Clima y meteorología | daily-temperature-major-cities, global-daily-climate-data | ✅ Resuelta |
| Seguridad a nivel ciudad | world-crime-index-2023 (416 ciudades) | ✅ Resuelta |
| Felicidad post-2019 | world-happiness-report-2024 (hasta 2024) | ✅ Resuelta |
| Visas e inmigración | henley-passport-index-2026, 2024-passport-index | ✅ Resuelta |
| Riesgo de desastres | global-disaster-risk-index, all-natural-disasters-EMDAT | ✅ Resuelta |

---

## Recomendación de Estrategia Analítica

### Nivel País (macro)
Cruzar: `countries-2023` + `prosperity-index` + `world-happiness-2024` + `SDG-report` + `HDR-2015` + `freedom-in-the-world` + `global-disaster-risk-index` usando código ISO de país como llave.

### Nivel Ciudad (micro)
Usar: `city-quality-of-life` como base, enriquecer con `global-cost-of-living` + `world-crime-index-2023` + `world-air-quality-index` + `daily-temperature-major-cities` usando ciudad+país como llave.

### Movilidad y acceso (para nómadas y migrantes)
Añadir: `henley-passport-index` + `press-freedom-index` + `freedom-in-the-world` para perfilar países por libertad de movimiento y derechos civiles.

### Análisis sugeridos
1. **Índice compuesto** ponderado por perfil de usuario (familia, nómada digital, jubilado, refugiado climático)
2. **Clustering K-Means** de países/ciudades por similitud multivariada (17+ dimensiones)
3. **Ranking filtrable** por región, tamaño de ciudad, régimen político, riesgo climático
4. **Análisis de correlación** entre felicidad, PIB, desigualdad, calidad ambiental y seguridad
5. **Visualización radar** por ciudad/país para comparar perfiles de calidad de vida
6. **Análisis temporal** de felicidad y libertades 2013–2024 por país
7. **Mapa de riesgo climático** cruzando disaster-risk-index con daily-temperature

---

*Revisión elaborada con base en inspección directa de headers, estructuras y contenidos de los 28 datasets disponibles.*
*Versión 2.0 — Actualizada en abril 2026 para incorporar 8 nuevos datasets del análisis de brechas.*
