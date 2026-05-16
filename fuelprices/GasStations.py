import requests
import re
import logging
import pandas as pd
from fuelprices.FuelPrice import FuelPrice
from bs4 import BeautifulSoup

from fuelprices.FuelType import FuelType
from fuelprices.StationParameters import StationParameters

price_regex = r"\d+(?:\.\d+)?"

def get_circlek_prices() -> list[FuelPrice]:
    station_name = "CircleK"
    url = "https://www.circlek.lv/degviela-miles/degvielas-cenas"
    fuel_prices = []

    tables = pd.read_html(url, skiprows=1)

    df = tables[0]
    df.columns = ["fuel_type", "price", "location"]

    fuel_mapping = {
        "95miles": FuelType.PETROL_95,
        "98miles+": FuelType.PETROL_98,
        "Dmiles": FuelType.DIESEL,
        "miles+\xa0XTL": FuelType.RENEWABLE_DIESEL,
        "Dmiles+": FuelType.PRO_DIESEL,
        "Autogāze": FuelType.LPG,
    }

    df["fuel_enum"] = df["fuel_type"].map(fuel_mapping)

    for index, row in df.iterrows():
        logging.debug(f"Processing row: {row["fuel_type"]}, {row["price"]}, {row["location"]}")
        if pd.isna(row["fuel_enum"]):
            logging.debug(f"Skipping unknown fuel type: {row["fuel_type"]}")
            continue
        fuel_price = FuelPrice(
            fuel_station_name=station_name,
            fuel_key=row["fuel_enum"],
            price=float(re.findall(price_regex, str(row["price"]))[0]),
            location=row["location"]
        )
        fuel_prices.append(fuel_price)

    return fuel_prices


def get_neste_prices() -> list[FuelPrice]:
    station_name = "Neste"
    url = "https://www.neste.lv/lv/content/degvielas-cenas"
    fuel_prices = []

    tables = pd.read_html(url, skiprows=1)

    df = tables[0]
    df.columns = ["fuel_type", "price", "location"]

    fuel_mapping = {
        "Neste Futura\xa095": FuelType.PETROL_95,
        "Neste Futura 98": FuelType.PETROL_98,
        "Neste Futura D": FuelType.DIESEL,
        "Neste Pro Diesel": FuelType.PRO_DIESEL,
        "Neste MY Renewable Diesel": FuelType.RENEWABLE_DIESEL
    }

    df["fuel_enum"] = df["fuel_type"].map(fuel_mapping)

    for index, row in df.iterrows():
        logging.debug(f"Processing row: {row["fuel_type"]}, {row["price"]}, {row["location"]}")
        if pd.isna(row["fuel_enum"]):
            logging.debug(f"Skipping unknown fuel type: {row["fuel_type"]}")
            continue
        fuel_price = FuelPrice(
            fuel_station_name=station_name,
            fuel_key=row["fuel_enum"],
            price=float(re.findall(price_regex, str(row["price"]))[0]),
            location=row["location"]
        )
        fuel_prices.append(fuel_price)

    return fuel_prices


def get_virsi_prices() -> list[FuelPrice]:
    virsi_parameters = StationParameters(
        station_name="Virši",
        url="https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas",
        petrol_95_price_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)"
        ),
        petrol_95_location_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(2) > p:nth-child(2)"
        ),
        petrol_98_price_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)"
        ),
        petrol_98_location_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(3) > p:nth-child(2)"
        ),
        diesel_price_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)"
        ),
        diesel_location_css_selector=(
            "div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > p:nth-child(2)"
        ),
        lpg_price_css_selector=(
            "div.price-card:nth-child(5) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)"
        ),
        lpg_location_css_selector=("div.price-card:nth-child(5) > p:nth-child(2)"),
    )

    fuel_prices = __get_station_prices(station_parameters=virsi_parameters)
    return fuel_prices


def get_viada_prices() -> list[FuelPrice]:
    viada_parameters = StationParameters(
        station_name="Viada",
        url="https://www.viada.lv/zemakas-degvielas-cenas/",
        petrol_95_price_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)"
        ),
        petrol_95_location_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)"
        ),
        petrol_98_price_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)"
        ),
        petrol_98_location_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)"
        ),
        diesel_price_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)"
        ),
        diesel_location_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)"
        ),
        lpg_price_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)"
        ),
        lpg_location_css_selector=(
            ".the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(3)"
        ),
    )

    fuel_prices = __get_station_prices(station_parameters=viada_parameters)
    return fuel_prices


def __extract_fuel_price(
    response_text: str,
    station_name: str,
    fuel_css_selector: str,
    fuel_location_css_selector: str,
    fuel_key: FuelType,
):
    logging.debug("Parsing " + fuel_key.value + " for " + station_name)
    soup = BeautifulSoup(response_text, "html.parser")
    float_regex = r"\d+(?:\.\d+)?"
    price_string = soup.select_one(fuel_css_selector).text
    price_float = float(re.findall(float_regex, price_string)[0])
    location = soup.select_one(fuel_location_css_selector).text

    return FuelPrice(station_name, fuel_key, price_float, location)


def __get_station_prices(station_parameters: StationParameters) -> list[FuelPrice]:
    fuel_prices = []

    logging.info("Retrieving fuel prices for " + station_parameters.station_name)

    logging.debug("Getting URL " + station_parameters.url)
    response = requests.get(station_parameters.url)

    if (
        station_parameters.petrol_95_price_css_selector
        and station_parameters.petrol_95_location_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.PETROL_95} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.petrol_95_price_css_selector,
                fuel_location_css_selector=station_parameters.petrol_95_location_css_selector,
                fuel_key=FuelType.PETROL_95,
            )
            fuel_prices.append(fuel_price)
        except Exception as e:
            logging.error(
                f"Failed to retrieve {FuelType.PETROL_95} price for {station_parameters.station_name} station"
            )
            logging.exception(e)

    if (
        station_parameters.petrol_98_price_css_selector
        and station_parameters.petrol_98_location_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.PETROL_98} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.petrol_98_price_css_selector,
                fuel_location_css_selector=station_parameters.petrol_98_location_css_selector,
                fuel_key=FuelType.PETROL_98,
            )
            fuel_prices.append(fuel_price)
        except Exception as e:
            logging.error(
                f"Failed to retrieve {FuelType.PETROL_98} price for {station_parameters.station_name} station"
            )
            logging.exception(e)

    if (
        station_parameters.diesel_price_css_selector
        and station_parameters.diesel_location_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.DIESEL} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.diesel_price_css_selector,
                fuel_location_css_selector=station_parameters.diesel_location_css_selector,
                fuel_key=FuelType.DIESEL,
            )
            fuel_prices.append(fuel_price)
        except Exception as e:
            logging.error(
                f"Failed to retrieve {FuelType.DIESEL} price for {station_parameters.station_name} station"
            )
            logging.exception(e)

    if (
        station_parameters.renewable_diesel_price_css_selector
        and station_parameters.renewable_diesel_location_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.RENEWABLE_DIESEL} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.renewable_diesel_price_css_selector,
                fuel_location_css_selector=station_parameters.renewable_diesel_location_css_selector,
                fuel_key=FuelType.RENEWABLE_DIESEL,
            )
            fuel_prices.append(fuel_price)
        except Exception as e:
            logging.error(
                f"Failed to retrieve {FuelType.RENEWABLE_DIESEL} price for {station_parameters.station_name} station"
            )
            logging.exception(e)

    if (
        station_parameters.lpg_price_css_selector
        and station_parameters.lpg_location_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.LPG} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.lpg_price_css_selector,
                fuel_location_css_selector=station_parameters.lpg_location_css_selector,
                fuel_key=FuelType.LPG,
            )
            fuel_prices.append(fuel_price)
        except Exception as e:
            logging.error(
                f"Failed to retrieve {FuelType.LPG} price for {station_parameters.station_name} station"
            )
            logging.exception(e)
    return fuel_prices
