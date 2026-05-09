import requests
import re
import logging
from fuelprices.FuelPrice import FuelPrice
from bs4 import BeautifulSoup

from fuelprices.FuelType import FuelType
from fuelprices.StationParameters import StationParameters


def get_circlek_prices() -> list[FuelPrice]:
    cirlek_parameters = StationParameters(
        station_name="CircleK",
        url="https://www.circlek.lv/degviela-miles/degvielas-cenas",
        petrol_95_price_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
        ),
        petrol_95_location_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3)"
        ),
        petrol_98_price_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)"
        ),
        petrol_98_location_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(3)"
        ),
        diesel_price_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)"
        ),
        diesel_location_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(3)"
        ),
        renewable_diesel_price_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)"
        ),
        renewable_diesel_location_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3)"
        ),
        lpg_price_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)"
        ),
        lpg_location_css_selector=(
            ".table > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(3)"
        ),
    )

    fuel_prices = __get_station_prices(station_parameters=cirlek_parameters)
    return fuel_prices


def get_neste_prices() -> list[FuelPrice]:
    neste_parameters = StationParameters(
        station_name="Neste",
        url="https://www.neste.lv/lv/content/degvielas-cenas",
        petrol_95_price_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > span:nth-child(1) > strong:nth-child(1)"
        ),
        petrol_95_location_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > p:nth-child(2)"
        ),
        petrol_98_price_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > span:nth-child(1) > strong:nth-child(1)"
        ),
        petrol_98_location_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)"
        ),
        diesel_price_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > span:nth-child(1) > strong:nth-child(1)"
        ),
        diesel_location_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)"
        ),
        renewable_diesel_price_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > span:nth-child(1) > span:nth-child(1) > strong:nth-child(1)"
        ),
        renewable_diesel_location_css_selector=(
            ".field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3) > p:nth-child(1) > span:nth-child(1)"
        ),
    )

    fuel_prices = __get_station_prices(station_parameters=neste_parameters)
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
        and station_parameters.petrol_98_price_css_selector
    ):
        try:
            logging.debug(
                f"Retrieving {FuelType.PETROL_98} prices for {station_parameters.station_name}"
            )
            fuel_price = __extract_fuel_price(
                response_text=response.text,
                station_name=station_parameters.station_name,
                fuel_css_selector=station_parameters.petrol_98_price_css_selector,
                fuel_location_css_selector=station_parameters.petrol_98_price_css_selector,
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
