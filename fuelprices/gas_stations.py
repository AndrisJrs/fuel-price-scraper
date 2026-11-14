import logging
import re
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from fuelprices.fuel_price import FuelPrice
from fuelprices.fuel_type import FuelType

logger = logging.getLogger(__name__)

price_regex = r"\d+(?:\.\d+)?"


def _normalize_whitespace(text) -> str:
    return " ".join(str(text).split())


def _parse_fuel_rows(
    df: pd.DataFrame, station_name: str, fuel_mapping: dict[str, FuelType]
) -> list[FuelPrice]:
    """Turn a DataFrame with fuel_type, price and location columns into FuelPrices.

    Rows whose fuel_type isn't in fuel_mapping, or whose price can't be parsed,
    are logged and skipped.
    """
    if df.empty:
        raise ValueError(
            f"No fuel rows found on {station_name} page; layout may have changed"
        )

    df = df[["fuel_type", "price", "location"]].fillna("")
    df = df.map(_normalize_whitespace)
    df["fuel_enum"] = df["fuel_type"].map(fuel_mapping)

    fuel_prices = []
    for row in df.itertuples(index=False):
        logger.debug(f"Processing row: {row.fuel_type}, {row.price}, {row.location}")
        if pd.isna(row.fuel_enum):
            logger.debug(f"Skipping unknown fuel type: {row.fuel_type}")
            continue
        prices = re.findall(price_regex, row.price.replace(",", "."))
        if not prices:
            logger.error(
                f"No price found for {station_name} {row.fuel_type}: {row.price!r}"
            )
            continue
        fuel_prices.append(
            FuelPrice(
                fuel_station_name=station_name,
                fuel_key=row.fuel_enum,
                price=float(prices[0]),
                location=row.location,
            )
        )

    return fuel_prices


def get_circlek_prices() -> list[FuelPrice]:
    url = "https://www.circlek.lv/degviela-miles/degvielas-cenas"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    return parse_circlek_prices(response.text)


def parse_circlek_prices(html: str) -> list[FuelPrice]:
    tables = pd.read_html(StringIO(html), match="Degviela", skiprows=1)

    df = tables[0].iloc[:, :3]
    df.columns = ["fuel_type", "price", "location"]

    return _parse_fuel_rows(
        df,
        station_name="CircleK",
        fuel_mapping={
            "95miles": FuelType.PETROL_95,
            "98miles+": FuelType.PETROL_98,
            "Dmiles": FuelType.DIESEL,
            "miles+ XTL": FuelType.RENEWABLE_DIESEL,
            "Dmiles+": FuelType.PRO_DIESEL,
            "Autogāze": FuelType.LPG,
        },
    )


def get_virsi_prices() -> list[FuelPrice]:
    url = "https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return parse_virsi_prices(response.text)


def parse_virsi_prices(html: str) -> list[FuelPrice]:
    soup = BeautifulSoup(html, "html.parser")

    rows = []
    for card in soup.select(".fuel-block .price-card"):
        price = card.select_one(".price")
        address = card.select_one(".address")
        if price is None:
            continue
        spans = price.find_all("span")
        rows.append(
            {
                "fuel_type": card.get("data-type", "").lower(),
                "price": spans[-1].get_text() if spans else "",
                "location": address.get_text() if address else "",
            }
        )

    return _parse_fuel_rows(
        pd.DataFrame(rows, columns=["fuel_type", "price", "location"]),
        station_name="Virši",
        fuel_mapping={
            "95e": FuelType.PETROL_95,
            "98e": FuelType.PETROL_98,
            "dd": FuelType.DIESEL,
            "lpg": FuelType.LPG,
        },
    )


def get_viada_prices() -> list[FuelPrice]:
    url = "https://www.viada.lv/zemakas-degvielas-cenas/"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return parse_viada_prices(response.text)


def parse_viada_prices(html: str) -> list[FuelPrice]:
    soup = BeautifulSoup(html, "html.parser")

    rows = []
    for row in soup.select(".fuel-table__row"):
        fuel = row.select_one(".fuel-table__fuel")
        price = row.select_one(".fuel-table__price")
        if fuel is None or price is None:
            continue
        stations = [s.get_text() for s in row.select(".fuel-table__station")]
        rows.append(
            {
                "fuel_type": fuel.get_text(),
                "price": price.get_text(" "),
                "location": ", ".join(s.strip() for s in stations),
            }
        )

    return _parse_fuel_rows(
        pd.DataFrame(rows, columns=["fuel_type", "price", "location"]),
        station_name="Viada",
        fuel_mapping={
            "95 Multi FX": FuelType.PETROL_95,
            "98 Multi FX": FuelType.PETROL_98,
            "D": FuelType.DIESEL,
            "D Multi FX": FuelType.PRO_DIESEL,
            "Gāze": FuelType.LPG,
        },
    )
