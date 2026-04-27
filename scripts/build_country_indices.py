#!/usr/bin/env python3
"""
Build a reproducible country-level index table for the "mejor lugar para vivir"
project.

Outputs:
  - projectData/processed/country_category_indices.csv
  - projectData/processed/audit_variable_scores.csv
  - projectData/processed/audit_category_coverage.csv
  - projectData/processed/unmatched_country_names.csv
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRINCIPAL = PROJECT_ROOT / "projectData" / "PRINCIPAL"
OUTPUT_DIR = PROJECT_ROOT / "projectData" / "processed"
ALIASES_PATH = Path(__file__).resolve().with_name("country_aliases.json")

CATEGORY_COLUMNS = [
    "calidad_de_vida_y_bienestar",
    "economia_y_costo_de_vida",
    "salud_publica",
    "vivienda_y_urbanismo",
    "medioambiente_y_sostenibilidad",
    "seguridad_y_criminalidad",
    "gobernanza_y_libertades",
    "migracion_y_movilidad",
    "clima_y_desastres",
]

PRIMARY_DIRECT_WEIGHT = 0.30
COVERAGE_THRESHOLD = 0.30


@dataclass(frozen=True)
class CountryInfo:
    country: str
    iso3: str


class CountryNormalizer:
    def __init__(self, path: Path):
        config = json.loads(path.read_text(encoding="utf-8"))
        self.aliases = {self._tidy(k): self._tidy(v) for k, v in config["aliases"].items()}
        self.iso3 = {self._tidy(k): v for k, v in config["iso3"].items()}
        self.exclude = {self._tidy(v) for v in config["exclude"]}
        self.us_states = {self._tidy(v) for v in config["us_states"]}
        self.subnational_codes = {
            "AB": "Canada",
            "AK": "United States",
            "AZ": "United States",
            "BC": "Canada",
            "CA": "United States",
            "CO": "United States",
            "DC": "United States",
            "FL": "United States",
            "GA": "United States",
            "HI": "United States",
            "ID": "United States",
            "IL": "United States",
            "IN": "United States",
            "KY": "United States",
            "LA": "United States",
            "MA": "United States",
            "MD": "United States",
            "MI": "United States",
            "MN": "United States",
            "MO": "United States",
            "NC": "United States",
            "NM": "United States",
            "NV": "United States",
            "NY": "United States",
            "OH": "United States",
            "OR": "United States",
            "PA": "United States",
            "QC": "Canada",
            "TX": "United States",
            "VA": "United States",
            "WA": "United States",
        }
        self.raw_to_normalized: dict[str, str] = {}
        self.unmatched: set[tuple[str, str, str]] = set()

    @staticmethod
    def _tidy(value: object) -> str:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        text = str(value).replace("\ufeff", "").strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def normalize(
        self,
        raw_value: object,
        source: str,
        *,
        map_us_states: bool = False,
        iso_hint: str | None = None,
    ) -> CountryInfo | None:
        raw = self._tidy(raw_value)
        if not raw:
            return None

        country = raw
        if map_us_states and country in self.us_states:
            country = "United States"
        if map_us_states and country in self.subnational_codes:
            country = self.subnational_codes[country]
        country = self.aliases.get(country, country)

        if not country or country in self.exclude:
            return None

        iso_hint = self._tidy(iso_hint)
        if iso_hint and re.fullmatch(r"[A-Z]{3}", iso_hint):
            self.iso3.setdefault(country, iso_hint)

        iso3 = self.iso3.get(country, "")
        if not iso3:
            self.unmatched.add((source, raw, country))

        self.raw_to_normalized[raw] = country
        return CountryInfo(country=country, iso3=iso3)

    def write_unmatched(self, output_path: Path) -> None:
        rows = [
            {"source": source, "raw_country": raw, "normalized_country": normalized}
            for source, raw, normalized in sorted(self.unmatched)
        ]
        pd.DataFrame(rows).to_csv(output_path, index=False)


class MetricRegistry:
    def __init__(self, normalizer: CountryNormalizer):
        self.normalizer = normalizer
        self.metric_rows: list[dict[str, object]] = []
        self.country_iso: dict[str, str] = {}

    def _register_country(self, info: CountryInfo) -> None:
        if info.iso3:
            self.country_iso[info.country] = info.iso3
        else:
            self.country_iso.setdefault(info.country, "")

    @staticmethod
    def _winsorized_minmax(values: pd.Series, higher_is_better: bool) -> pd.Series:
        numeric = pd.to_numeric(values, errors="coerce")
        valid = numeric.dropna()
        if valid.empty:
            return pd.Series(np.nan, index=values.index)
        if valid.nunique() == 1:
            return pd.Series(50.0, index=values.index).where(numeric.notna(), np.nan)

        low = valid.quantile(0.05)
        high = valid.quantile(0.95)
        if pd.isna(low) or pd.isna(high) or low == high:
            low = valid.min()
            high = valid.max()
        clipped = numeric.clip(lower=low, upper=high)
        score = (clipped - low) / (high - low) * 100.0
        if not higher_is_better:
            score = 100.0 - score
        return score.clip(0, 100)

    @staticmethod
    def _clip_0_100(values: pd.Series) -> pd.Series:
        return pd.to_numeric(values, errors="coerce").clip(0, 100)

    def add_metric(
        self,
        *,
        category: str,
        variable: str,
        source: str,
        data: pd.DataFrame,
        country_col: str,
        value_col: str,
        weight: float,
        higher_is_better: bool = True,
        score_mode: str = "minmax",
        map_us_states: bool = False,
        iso_col: str | None = None,
        primary: bool = False,
        aggregate: str = "median",
    ) -> None:
        if data.empty or country_col not in data.columns or value_col not in data.columns:
            return

        rows: list[dict[str, object]] = []
        for _, row in data[[c for c in [country_col, value_col, iso_col] if c]].iterrows():
            info = self.normalizer.normalize(
                row[country_col],
                source,
                map_us_states=map_us_states,
                iso_hint=row[iso_col] if iso_col else None,
            )
            if info is None:
                continue
            value = parse_numeric(row[value_col])
            if pd.isna(value):
                continue
            self._register_country(info)
            rows.append({"country": info.country, "raw_value": value})

        if not rows:
            return

        metric = pd.DataFrame(rows)
        if aggregate == "mean":
            metric = metric.groupby("country", as_index=False)["raw_value"].mean()
        elif aggregate == "sum":
            metric = metric.groupby("country", as_index=False)["raw_value"].sum()
        else:
            metric = metric.groupby("country", as_index=False)["raw_value"].median()

        if score_mode == "score_0_100":
            metric["normalized_score"] = self._clip_0_100(metric["raw_value"])
        elif score_mode == "score_0_10":
            metric["normalized_score"] = self._clip_0_100(metric["raw_value"] * 10.0)
        else:
            metric["normalized_score"] = self._winsorized_minmax(
                metric["raw_value"],
                higher_is_better=higher_is_better,
            )

        for _, row in metric.iterrows():
            if pd.isna(row["normalized_score"]):
                continue
            self.metric_rows.append(
                {
                    "country": row["country"],
                    "country_iso3": self.country_iso.get(row["country"], ""),
                    "category": category,
                    "variable": variable,
                    "source": source,
                    "raw_value": float(row["raw_value"]),
                    "normalized_score": round(float(row["normalized_score"]), 4),
                    "weight": weight,
                    "primary": bool(primary),
                }
            )

    def add_pre_scored_series(
        self,
        *,
        category: str,
        variable: str,
        source: str,
        series: pd.Series,
        weight: float,
        primary: bool = False,
    ) -> None:
        data = series.dropna().reset_index()
        data.columns = ["country", "score"]
        self.add_metric(
            category=category,
            variable=variable,
            source=source,
            data=data,
            country_col="country",
            value_col="score",
            weight=weight,
            score_mode="score_0_100",
            primary=primary,
        )

    def to_frame(self) -> pd.DataFrame:
        if not self.metric_rows:
            return pd.DataFrame()
        return pd.DataFrame(self.metric_rows)


def parse_numeric(value: object) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return np.nan
    if isinstance(value, (int, float, np.number)):
        return float(value)
    text = str(value).strip()
    if not text:
        return np.nan
    text = text.replace("\u2212", "-").replace("%", "")
    if re.search(r"\d{1,3}(,\d{3})+(?:\D|$)", text):
        text = text.replace(",", "")
    elif "," in text and "." not in text:
        text = text.replace(",", ".")
    else:
        text = text.replace(",", "")
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    if not match:
        return np.nan
    try:
        return float(match.group(0))
    except ValueError:
        return np.nan


def read_csv(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False, **kwargs)


def latest_per_country(
    df: pd.DataFrame,
    country_col: str,
    year_col: str,
    value_cols: Iterable[str],
    *,
    last_n_years: int = 5,
) -> pd.DataFrame:
    value_cols = list(value_cols)
    work = df[[country_col, year_col, *value_cols]].copy()
    work[year_col] = pd.to_numeric(work[year_col], errors="coerce")
    for col in value_cols:
        work[col] = work[col].map(parse_numeric)
    work = work.dropna(subset=[country_col, year_col])
    if work.empty:
        return work
    latest = work.groupby(country_col)[year_col].transform("max")
    recent = work[work[year_col] >= latest - (last_n_years - 1)]
    return recent.groupby(country_col, as_index=False)[value_cols].median()


def minmax_score_series(values: pd.Series, *, higher_is_better: bool = True) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    valid = numeric.dropna()
    if valid.empty:
        return pd.Series(np.nan, index=values.index)
    if valid.nunique() == 1:
        return pd.Series(50.0, index=values.index).where(numeric.notna(), np.nan)
    low = valid.quantile(0.05)
    high = valid.quantile(0.95)
    if pd.isna(low) or pd.isna(high) or low == high:
        low = valid.min()
        high = valid.max()
    score = (numeric.clip(low, high) - low) / (high - low) * 100.0
    if not higher_is_better:
        score = 100.0 - score
    return score.clip(0, 100)


def add_quality_of_life(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "01_calidad_de_vida_y_bienestar"

    happiness = read_csv(base / "world-happiness-2024" / "World-happiness-report-2024.csv")
    registry.add_metric(
        category="calidad_de_vida_y_bienestar",
        variable="world_happiness_ladder_score_2024",
        source="world-happiness-2024/World-happiness-report-2024.csv",
        data=happiness,
        country_col="Country name",
        value_col="Ladder score",
        weight=0.45,
        score_mode="score_0_10",
        primary=True,
    )

    city = read_csv(base / "city-quality-of-life-dataset" / "uaScoresDataFrame.csv")
    city_cols = [
        "Housing",
        "Cost of Living",
        "Safety",
        "Healthcare",
        "Education",
        "Environmental Quality",
        "Economy",
        "Internet Access",
        "Leisure & Culture",
        "Tolerance",
        "Outdoors",
    ]
    city["city_qol_composite"] = city[city_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    registry.add_metric(
        category="calidad_de_vida_y_bienestar",
        variable="city_quality_of_life_composite",
        source="city-quality-of-life-dataset/uaScoresDataFrame.csv",
        data=city,
        country_col="UA_Country",
        value_col="city_qol_composite",
        weight=0.30,
        score_mode="score_0_10",
        map_us_states=True,
        primary=True,
    )

    prosperity = read_csv(base / "2023-global-prosperity-index-w-region-politics" / "global_prosperity_regions_politics.csv")
    registry.add_metric(
        category="calidad_de_vida_y_bienestar",
        variable="global_prosperity_average_rank_inverted",
        source="2023-global-prosperity-index-w-region-politics/global_prosperity_regions_politics.csv",
        data=prosperity,
        country_col="country",
        value_col="average_score",
        weight=0.25,
        higher_is_better=False,
        iso_col="code",
    )


def add_economy(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "02_economia_y_costo_de_vida"
    world = read_csv(base / "countries-of-the-world-2023" / "world-data-2023.csv")
    world["GDP_numeric"] = world["GDP"].map(parse_numeric)
    world["Population_numeric"] = world["Population"].map(parse_numeric)
    world["GDP_per_capita"] = world["GDP_numeric"] / world["Population_numeric"]

    metrics = [
        ("gdp_per_capita", "GDP_per_capita", 0.25, True, "minmax"),
        ("unemployment_rate_inverted", "Unemployment rate", 0.20, False, "minmax"),
        ("cpi_change_inverted", "CPI Change (%)", 0.15, False, "minmax"),
        ("labor_force_participation", "Population: Labor force participation (%)", 0.15, True, "minmax"),
        ("total_tax_rate_inverted", "Total tax rate", 0.10, False, "minmax"),
    ]
    for variable, column, weight, higher, mode in metrics:
        registry.add_metric(
            category="economia_y_costo_de_vida",
            variable=variable,
            source="countries-of-the-world-2023/world-data-2023.csv",
            data=world,
            country_col="Country",
            value_col=column,
            weight=weight,
            higher_is_better=higher,
            score_mode=mode,
        )

    cost = read_csv(base / "global-cost-of-living" / "cost-of-living_v2.csv")
    for col in ["x1", "x2", "x8", "x9", "x10", "x18", "x20", "x26", "x28", "x38"]:
        cost[col] = cost[col].map(parse_numeric)
    monthly_basics = (
        cost["x1"] * 8
        + cost["x2"] * 2
        + cost["x8"] * 12
        + cost["x9"] * 8
        + cost["x10"] * 4
        + cost["x18"] * 6
        + cost["x20"] * 40
        + cost["x26"]
        + cost["x28"]
    )
    cost["cost_affordability_ratio"] = cost["x38"] / monthly_basics.replace(0, np.nan)
    registry.add_metric(
        category="economia_y_costo_de_vida",
        variable="cost_of_living_affordability_salary_vs_basics",
        source="global-cost-of-living/cost-of-living_v2.csv",
        data=cost,
        country_col="country",
        value_col="cost_affordability_ratio",
        weight=0.15,
        higher_is_better=True,
        primary=True,
    )


def add_health(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "03_salud_publica"
    health = read_csv(base / "life-expectancy-dataset-real" / "impv" / "final.csv")
    recent = latest_per_country(
        health,
        "Country",
        "Year",
        [
            "Life expectancy",
            "Infant Mortality",
            "Clean fuels and cooking technologies",
            "Mortality caused by road traffic injury",
            "Tuberculosis Incidence",
            "DPT Immunization",
            "Hospital beds",
            "Basic sanitation services",
            "Non-communicable Mortality",
            "Sucide Rate",
        ],
    )
    for variable, column, weight, higher in [
        ("life_expectancy", "Life expectancy", 0.25, True),
        ("infant_mortality_inverted", "Infant Mortality", 0.15, False),
        ("clean_fuels", "Clean fuels and cooking technologies", 0.10, True),
        ("dpt_immunization", "DPT Immunization", 0.10, True),
        ("hospital_beds", "Hospital beds", 0.10, True),
        ("basic_sanitation_services", "Basic sanitation services", 0.10, True),
    ]:
        registry.add_metric(
            category="salud_publica",
            variable=variable,
            source="life-expectancy-dataset-real/impv/final.csv",
            data=recent,
            country_col="Country",
            value_col=column,
            weight=weight,
            higher_is_better=higher,
            primary=variable == "life_expectancy",
        )

    recent["mortality_disease_risk"] = recent[
        ["Non-communicable Mortality", "Tuberculosis Incidence", "Mortality caused by road traffic injury"]
    ].mean(axis=1)
    registry.add_metric(
        category="salud_publica",
        variable="ncd_tb_road_mortality_inverted",
        source="life-expectancy-dataset-real/impv/final.csv",
        data=recent,
        country_col="Country",
        value_col="mortality_disease_risk",
        weight=0.10,
        higher_is_better=False,
    )

    uhc = read_csv(base / "who-worldhealth-statistics-2020-complete" / "uhcCoverage.csv")
    uhc_recent = latest_per_country(uhc, "Location", "Period", ["First Tooltip"])
    registry.add_metric(
        category="salud_publica",
        variable="uhc_coverage",
        source="who-worldhealth-statistics-2020-complete/uhcCoverage.csv",
        data=uhc_recent,
        country_col="Location",
        value_col="First Tooltip",
        weight=0.10,
        score_mode="score_0_100",
    )


def add_housing(registry: MetricRegistry) -> None:
    city = read_csv(
        PRINCIPAL
        / "01_calidad_de_vida_y_bienestar"
        / "city-quality-of-life-dataset"
        / "uaScoresDataFrame.csv"
    )
    registry.add_metric(
        category="vivienda_y_urbanismo",
        variable="city_qol_housing",
        source="city-quality-of-life-dataset/uaScoresDataFrame.csv",
        data=city,
        country_col="UA_Country",
        value_col="Housing",
        weight=0.30,
        score_mode="score_0_10",
        map_us_states=True,
        primary=True,
    )

    cost = read_csv(PRINCIPAL / "02_economia_y_costo_de_vida" / "global-cost-of-living" / "cost-of-living_v2.csv")
    for col in ["x22", "x23", "x36", "x37", "x38"]:
        cost[col] = cost[col].map(parse_numeric)
    cost["monthly_rent_to_salary"] = cost[["x22", "x23"]].median(axis=1) / cost["x38"].replace(0, np.nan)
    cost["buy_price_to_salary"] = cost[["x36", "x37"]].median(axis=1) / cost["x38"].replace(0, np.nan)
    registry.add_metric(
        category="vivienda_y_urbanismo",
        variable="rent_to_salary_inverted",
        source="global-cost-of-living/cost-of-living_v2.csv",
        data=cost,
        country_col="country",
        value_col="monthly_rent_to_salary",
        weight=0.30,
        higher_is_better=False,
        primary=True,
    )
    registry.add_metric(
        category="vivienda_y_urbanismo",
        variable="buy_price_to_salary_inverted",
        source="global-cost-of-living/cost-of-living_v2.csv",
        data=cost,
        country_col="country",
        value_col="buy_price_to_salary",
        weight=0.20,
        higher_is_better=False,
    )

    housing = read_csv(
        PRINCIPAL
        / "04_vivienda_y_urbanismo"
        / "global-housing-market-analysis-2015-2024"
        / "global_housing_market_extended.csv"
    )
    latest = latest_per_country(
        housing,
        "Country",
        "Year",
        ["Affordability Ratio", "Mortgage Rate (%)", "Construction Index"],
    )
    for variable, column, weight, higher in [
        ("affordability_ratio_inverted", "Affordability Ratio", 0.10, False),
        ("mortgage_rate_inverted", "Mortgage Rate (%)", 0.05, False),
        ("construction_index", "Construction Index", 0.05, True),
    ]:
        registry.add_metric(
            category="vivienda_y_urbanismo",
            variable=variable,
            source="global-housing-market-analysis-2015-2024/global_housing_market_extended.csv",
            data=latest,
            country_col="Country",
            value_col=column,
            weight=weight,
            higher_is_better=higher,
        )


def add_environment(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "05_medioambiente_y_sostenibilidad"
    sdg = read_csv(base / "sustainable-development-data" / "sustainable_development_report_2023.csv")
    sdg_cols = [
        "overall_score",
        "goal_6_score",
        "goal_7_score",
        "goal_11_score",
        "goal_12_score",
        "goal_13_score",
        "goal_15_score",
    ]
    sdg["sdg_environment_composite"] = sdg[sdg_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    registry.add_metric(
        category="medioambiente_y_sostenibilidad",
        variable="sdg_environment_sustainability_composite",
        source="sustainable-development-data/sustainable_development_report_2023.csv",
        data=sdg,
        country_col="country",
        value_col="sdg_environment_composite",
        weight=0.35,
        score_mode="score_0_100",
        iso_col="country_code",
        primary=True,
    )

    air = read_csv(base / "world-air-quality-index" / "AQI and Lat Long of Countries.csv")
    air["air_pollution_composite"] = air[["AQI Value", "PM2.5 AQI Value"]].map(parse_numeric).mean(axis=1)
    registry.add_metric(
        category="medioambiente_y_sostenibilidad",
        variable="aqi_pm25_country_median_inverted",
        source="world-air-quality-index/AQI and Lat Long of Countries.csv",
        data=air,
        country_col="Country",
        value_col="air_pollution_composite",
        weight=0.35,
        higher_is_better=False,
        primary=True,
    )

    co2 = read_csv(base / "emissions-by-country" / "GCB2022v27_percapita_flat.csv")
    co2_latest = latest_per_country(co2, "Country", "Year", ["Total"])
    registry.add_metric(
        category="medioambiente_y_sostenibilidad",
        variable="co2_per_capita_latest_inverted",
        source="emissions-by-country/GCB2022v27_percapita_flat.csv",
        data=co2_latest,
        country_col="Country",
        value_col="Total",
        weight=0.15,
        higher_is_better=False,
    )

    city = read_csv(
        PRINCIPAL
        / "01_calidad_de_vida_y_bienestar"
        / "city-quality-of-life-dataset"
        / "uaScoresDataFrame.csv"
    )
    city["city_environment_outdoors"] = city[["Environmental Quality", "Outdoors"]].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    registry.add_metric(
        category="medioambiente_y_sostenibilidad",
        variable="city_qol_environment_outdoors",
        source="city-quality-of-life-dataset/uaScoresDataFrame.csv",
        data=city,
        country_col="UA_Country",
        value_col="city_environment_outdoors",
        weight=0.15,
        score_mode="score_0_10",
        map_us_states=True,
    )


def add_safety(registry: MetricRegistry) -> None:
    crime = read_csv(PRINCIPAL / "06_seguridad_y_criminalidad" / "world-crime-index-2023" / "crime-index-2023.csv")
    registry.add_metric(
        category="seguridad_y_criminalidad",
        variable="crime_dataset_safety_index",
        source="world-crime-index-2023/crime-index-2023.csv",
        data=crime,
        country_col="Country",
        value_col="Safety Index",
        weight=0.60,
        score_mode="score_0_100",
        map_us_states=True,
        primary=True,
    )

    city = read_csv(
        PRINCIPAL
        / "01_calidad_de_vida_y_bienestar"
        / "city-quality-of-life-dataset"
        / "uaScoresDataFrame.csv"
    )
    registry.add_metric(
        category="seguridad_y_criminalidad",
        variable="city_qol_safety",
        source="city-quality-of-life-dataset/uaScoresDataFrame.csv",
        data=city,
        country_col="UA_Country",
        value_col="Safety",
        weight=0.25,
        score_mode="score_0_10",
        map_us_states=True,
        primary=True,
    )

    prosperity = read_csv(
        PRINCIPAL
        / "01_calidad_de_vida_y_bienestar"
        / "2023-global-prosperity-index-w-region-politics"
        / "global_prosperity_regions_politics.csv"
    )
    registry.add_metric(
        category="seguridad_y_criminalidad",
        variable="global_prosperity_safety_rank_inverted",
        source="2023-global-prosperity-index-w-region-politics/global_prosperity_regions_politics.csv",
        data=prosperity,
        country_col="country",
        value_col="safety_and_security",
        weight=0.15,
        higher_is_better=False,
        iso_col="code",
    )


def add_governance(registry: MetricRegistry) -> None:
    freedom = read_csv(
        PRINCIPAL
        / "07_gobernanza_y_libertades"
        / "freedom-in-the-world"
        / "Freedom in the World 2013-2022 Dataset (Ver 2.18.23).csv"
    )
    freedom_latest = latest_per_country(freedom, "Country/Territory", "Edition", ["Total"])
    registry.add_metric(
        category="gobernanza_y_libertades",
        variable="freedom_house_latest_total",
        source="freedom-in-the-world/Freedom in the World 2013-2022 Dataset (Ver 2.18.23).csv",
        data=freedom_latest,
        country_col="Country/Territory",
        value_col="Total",
        weight=0.40,
        score_mode="score_0_100",
        primary=True,
    )

    press = pd.read_excel(PRINCIPAL / "07_gobernanza_y_libertades" / "press-freedom-index" / "2023.xlsx")
    press["Score_numeric"] = press["Score"].map(parse_numeric)
    registry.add_metric(
        category="gobernanza_y_libertades",
        variable="press_freedom_2023_score",
        source="press-freedom-index/2023.xlsx",
        data=press,
        country_col="Country_EN",
        value_col="Score_numeric",
        weight=0.35,
        score_mode="score_0_100",
        iso_col="ISO",
        primary=True,
    )

    prosperity = read_csv(
        PRINCIPAL
        / "01_calidad_de_vida_y_bienestar"
        / "2023-global-prosperity-index-w-region-politics"
        / "global_prosperity_regions_politics.csv"
    )
    prosperity["governance_personal_freedom_rank"] = prosperity[["governance", "personal_freedom"]].map(parse_numeric).mean(axis=1)
    registry.add_metric(
        category="gobernanza_y_libertades",
        variable="global_prosperity_governance_personal_freedom_rank_inverted",
        source="2023-global-prosperity-index-w-region-politics/global_prosperity_regions_politics.csv",
        data=prosperity,
        country_col="country",
        value_col="governance_personal_freedom_rank",
        weight=0.25,
        higher_is_better=False,
        iso_col="code",
    )


def add_migration(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "08_migracion_y_movilidad"
    henley = read_csv(base / "henley-passport-index" / "henley-passport-index-count-2026-03-17.csv")
    registry.add_metric(
        category="migracion_y_movilidad",
        variable="henley_visa_free_destinations",
        source="henley-passport-index/henley-passport-index-count-2026-03-17.csv",
        data=henley,
        country_col="Origin",
        value_col="Visa Free",
        weight=0.60,
        higher_is_better=True,
        primary=True,
    )

    passport = read_csv(base / "2024-passport-index-dataset" / "passport-index-tidy.csv")
    requirement_score = {
        "visa free": 1.00,
        "visa-free": 1.00,
        "visa on arrival": 0.80,
        "visa on arrival / evisa": 0.70,
        "e-visa": 0.60,
        "eta": 0.60,
        "visa required": 0.00,
        "covid ban": 0.00,
        "no admission": 0.00,
        "n/a": np.nan,
    }
    passport["requirement_score"] = (
        passport["Requirement"].astype(str).str.strip().str.lower().map(requirement_score)
    )
    passport_country = passport.groupby("Passport", as_index=False)["requirement_score"].mean()
    passport_country["requirement_score"] *= 100.0
    registry.add_metric(
        category="migracion_y_movilidad",
        variable="passport_index_requirement_score",
        source="2024-passport-index-dataset/passport-index-tidy.csv",
        data=passport_country,
        country_col="Passport",
        value_col="requirement_score",
        weight=0.25,
        score_mode="score_0_100",
        primary=True,
    )

    foreign = read_csv(base / "move-very-far" / "share-of-the-population-that-was-born-in-another-country.csv")
    foreign_latest = latest_per_country(
        foreign,
        "Entity",
        "Year",
        ["Share of the population that was born in another country"],
    )
    registry.add_metric(
        category="migracion_y_movilidad",
        variable="foreign_born_population_share",
        source="move-very-far/share-of-the-population-that-was-born-in-another-country.csv",
        data=foreign_latest,
        country_col="Entity",
        value_col="Share of the population that was born in another country",
        weight=0.15,
        higher_is_better=True,
    )


def add_climate(registry: MetricRegistry) -> None:
    base = PRINCIPAL / "09_clima_y_desastres"
    risk = read_csv(base / "global-disaster-risk-index" / "world_risk_index.csv")
    risk_latest = latest_per_country(risk, "Region", "Year", ["WRI"])
    registry.add_metric(
        category="clima_y_desastres",
        variable="world_risk_index_inverted",
        source="global-disaster-risk-index/world_risk_index.csv",
        data=risk_latest,
        country_col="Region",
        value_col="WRI",
        weight=0.45,
        higher_is_better=False,
        primary=True,
    )

    temp_path = base / "daily-temperature-major-cities" / "city_temperature.csv"
    temp_chunks: list[pd.DataFrame] = []
    usecols = ["Country", "Year", "AvgTemperature"]
    for chunk in pd.read_csv(temp_path, usecols=usecols, chunksize=500_000, low_memory=False):
        chunk["AvgTemperature"] = pd.to_numeric(chunk["AvgTemperature"], errors="coerce")
        chunk = chunk[chunk["AvgTemperature"].notna() & (chunk["AvgTemperature"] != -99)]
        chunk["Year"] = pd.to_numeric(chunk["Year"], errors="coerce")
        max_year = chunk["Year"].max()
        if pd.isna(max_year):
            continue
        chunk = chunk[chunk["Year"] >= max_year - 4]
        temp_chunks.append(chunk)
    if temp_chunks:
        temp = pd.concat(temp_chunks, ignore_index=True)
        temp["temp_c"] = (temp["AvgTemperature"] - 32.0) * 5.0 / 9.0
        temp_country = temp.groupby("Country", as_index=False)["temp_c"].mean()
        # 20C is the comfort target; scores taper toward 0 by about 20C away.
        temp_country["temperature_comfort_score"] = (100.0 - (temp_country["temp_c"] - 20.0).abs() * 5.0).clip(0, 100)
        registry.add_metric(
            category="clima_y_desastres",
            variable="temperature_comfort_score",
            source="daily-temperature-major-cities/city_temperature.csv",
            data=temp_country,
            country_col="Country",
            value_col="temperature_comfort_score",
            weight=0.35,
            score_mode="score_0_100",
            primary=True,
        )

    disasters = read_csv(
        base
        / "all-natural-disasters-19002021-eosdis"
        / "DISASTERS"
        / "1970-2021_DISASTERS.xlsx - emdat data.csv"
    )
    recent = disasters[pd.to_numeric(disasters["Year"], errors="coerce") >= 2000].copy()
    for col in ["Total Deaths", "Total Affected", "Total Damages ('000 US$)"]:
        if col in recent.columns:
            recent[col] = recent[col].map(parse_numeric).fillna(0)
        else:
            recent[col] = 0
    disaster_country = recent.groupby("Country", as_index=False).agg(
        events=("Year", "count"),
        deaths=("Total Deaths", "sum"),
        affected=("Total Affected", "sum"),
        damages=("Total Damages ('000 US$)", "sum"),
    )
    disaster_country["historical_disaster_impact"] = (
        disaster_country["events"]
        + np.log1p(disaster_country["deaths"])
        + np.log1p(disaster_country["affected"])
        + np.log1p(disaster_country["damages"])
    )
    registry.add_metric(
        category="clima_y_desastres",
        variable="historical_disaster_frequency_impact_inverted",
        source="all-natural-disasters-19002021-eosdis/DISASTERS/1970-2021_DISASTERS.xlsx - emdat data.csv",
        data=disaster_country,
        country_col="Country",
        value_col="historical_disaster_impact",
        weight=0.20,
        higher_is_better=False,
    )


def build_outputs(registry: MetricRegistry) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    audit = registry.to_frame()
    if audit.empty:
        raise RuntimeError("No metric scores were produced.")

    # The final product is country-level. Unresolved names are kept in the
    # unmatched audit file, but excluded here until mapped deliberately.
    all_countries = sorted(
        country for country in audit["country"].unique() if registry.country_iso.get(country, "")
    )
    final = pd.DataFrame({"country": all_countries})
    final["country_iso3"] = final["country"].map(lambda c: registry.country_iso.get(c, ""))

    coverage_rows: list[dict[str, object]] = []
    for category in CATEGORY_COLUMNS:
        cat = audit[audit["category"] == category].copy()
        cat_weight_total = cat[["variable", "weight"]].drop_duplicates()["weight"].sum()
        country_scores: dict[str, float] = {}
        for country in all_countries:
            rows = cat[cat["country"] == country]
            if rows.empty:
                country_scores[country] = -1.0
                coverage_rows.append(
                    coverage_row(country, registry, category, 0.0, cat_weight_total, 0, False, -1.0)
                )
                continue
            available_weight = rows[["variable", "weight"]].drop_duplicates()["weight"].sum()
            has_primary = bool(rows.loc[rows["primary"], "weight"].max() >= PRIMARY_DIRECT_WEIGHT) if rows["primary"].any() else False
            coverage_ratio = available_weight / cat_weight_total if cat_weight_total else 0.0
            if coverage_ratio < COVERAGE_THRESHOLD and not has_primary:
                score = -1.0
            else:
                score = np.average(rows["normalized_score"], weights=rows["weight"])
                score = round(float(np.clip(score, 0, 100)), 2)
            country_scores[country] = score
            coverage_rows.append(
                coverage_row(
                    country,
                    registry,
                    category,
                    available_weight,
                    cat_weight_total,
                    rows["variable"].nunique(),
                    has_primary,
                    score,
                )
            )

        final[category] = final["country"].map(country_scores)

    coverage = pd.DataFrame(coverage_rows)
    final = final.sort_values("country").reset_index(drop=True)
    audit = audit.sort_values(["category", "country", "variable"]).reset_index(drop=True)
    coverage = coverage.sort_values(["category", "country"]).reset_index(drop=True)
    return final, audit, coverage


def coverage_row(
    country: str,
    registry: MetricRegistry,
    category: str,
    available_weight: float,
    total_weight: float,
    variable_count: int,
    has_primary: bool,
    category_score: float,
) -> dict[str, object]:
    if category_score == -1:
        if available_weight == 0:
            reason = "no_data"
        elif available_weight / total_weight < COVERAGE_THRESHOLD and not has_primary:
            reason = "insufficient_coverage"
        else:
            reason = "not_conclusive"
    else:
        reason = "ok"
    return {
        "country": country,
        "country_iso3": registry.country_iso.get(country, ""),
        "category": category,
        "available_weight": round(float(available_weight), 4),
        "total_category_weight": round(float(total_weight), 4),
        "coverage_ratio": round(float(available_weight / total_weight), 4) if total_weight else 0.0,
        "variable_count": int(variable_count),
        "has_primary_source": bool(has_primary),
        "category_score": category_score,
        "reason": reason,
    }


def validate_final(final: pd.DataFrame) -> None:
    required = ["country", "country_iso3", *CATEGORY_COLUMNS]
    missing = [col for col in required if col not in final.columns]
    if missing:
        raise RuntimeError(f"Final output missing columns: {missing}")
    if final["country"].isna().any() or (final["country"].astype(str).str.strip() == "").any():
        raise RuntimeError("Final output contains empty countries.")
    for col in CATEGORY_COLUMNS:
        numeric = pd.to_numeric(final[col], errors="coerce")
        if numeric.isna().any():
            raise RuntimeError(f"Column {col} contains non-numeric values.")
        invalid = ~((numeric == -1) | ((numeric >= 0) & (numeric <= 100)))
        if invalid.any():
            raise RuntimeError(f"Column {col} has values outside 0-100 or -1.")


def main() -> None:
    normalizer = CountryNormalizer(ALIASES_PATH)
    registry = MetricRegistry(normalizer)

    add_quality_of_life(registry)
    add_economy(registry)
    add_health(registry)
    add_housing(registry)
    add_environment(registry)
    add_safety(registry)
    add_governance(registry)
    add_migration(registry)
    add_climate(registry)

    final, audit, coverage = build_outputs(registry)
    validate_final(final)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    final.to_csv(OUTPUT_DIR / "country_category_indices.csv", index=False)
    audit.to_csv(OUTPUT_DIR / "audit_variable_scores.csv", index=False)
    coverage.to_csv(OUTPUT_DIR / "audit_category_coverage.csv", index=False)
    normalizer.write_unmatched(OUTPUT_DIR / "unmatched_country_names.csv")

    print(f"Wrote {len(final)} countries to {OUTPUT_DIR / 'country_category_indices.csv'}")
    print(f"Wrote {len(audit)} audit metric rows")
    print(f"Wrote {len(coverage)} category coverage rows")


if __name__ == "__main__":
    main()
