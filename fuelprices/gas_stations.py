import json
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


def get_kool_prices() -> list[FuelPrice]:
    # kool.lv is a Readymag site rendered client side. The page HTML embeds the
    # project JSON, which links a pre-rendered HTML snapshot of each page. The
    # snapshot URL changes whenever the site is republished, so look it up.
    url = "https://kool.lv/degviela/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    snapshot_url = _find_kool_snapshot_url(response.text, page_path="degviela")

    response = requests.get(snapshot_url, headers=headers, timeout=30)
    response.raise_for_status()
    # The CDN omits the charset, so requests would fall back to ISO-8859-1.
    response.encoding = "utf-8"
    return parse_kool_prices(response.text)


def _find_kool_snapshot_url(html: str, page_path: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.select("script[data-content]"):
        try:
            data = json.loads(script["data-content"])
        except json.JSONDecodeError:
            continue
        pages = data.get("project", {}).get("pages", [])
        for page in pages:
            if page.get("pagePath") == page_path and page.get("htmlUrl"):
                return page["htmlUrl"]
    raise ValueError(f"No Readymag snapshot found for Kool page '{page_path}'")


def _widget_position(widget) -> tuple[float, float]:
    style = widget.get("style", "")
    left = re.search(r"left:\s*(-?[\d.]+)px", style)
    top = re.search(r"top:\s*(-?[\d.]+)px", style)
    if not left or not top:
        return float("nan"), float("nan")
    return float(left.group(1)), float(top.group(1))


def parse_kool_prices(html: str) -> list[FuelPrice]:
    # Readymag places each text as a free-floating absolutely positioned widget,
    # so labels and prices aren't nested together. Pair each fuel label with the
    # nearest price widget below it in the same column.
    fuel_mapping = {
        "95e": FuelType.PETROL_95,
        "98": FuelType.PETROL_98,
        "dd": FuelType.DIESEL,
        "kool premium diesel": FuelType.PRO_DIESEL,
    }
    column_tolerance_px = 20

    soup = BeautifulSoup(html, "html.parser")
    widgets = []
    for widget in soup.select(".rmwidget.widget-text-v3"):
        text = _normalize_whitespace(widget.get_text(" "))
        if text:
            widgets.append((text, *_widget_position(widget)))

    prices = [
        (text, left, top)
        for text, left, top in widgets
        if re.fullmatch(r"\d+[.,]\d+(\s+\d+)?", text)
    ]

    rows = []
    for text, left, top in widgets:
        # Labels may carry footnote markers, e.g. "98*".
        name = text.rstrip("* ").lower()
        if name not in fuel_mapping:
            continue
        below = [
            p for p in prices if abs(p[1] - left) <= column_tolerance_px and p[2] > top
        ]
        if not below:
            logger.error(f"No price found below Kool label {text!r}")
            continue
        price = min(below, key=lambda p: p[2])[0]
        rows.append({"fuel_type": name, "price": price, "location": ""})

    return _parse_fuel_rows(
        pd.DataFrame(rows, columns=["fuel_type", "price", "location"]),
        station_name="Kool",
        fuel_mapping=fuel_mapping,
    )
