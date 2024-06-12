import requests
import re
import logging
from fuelprices.FuelPrices import FuelPrice
from bs4 import BeautifulSoup

class GasStations:
    fuel_95_key = 'fuel_95_price'
    fuel_98_key = 'fuel_98_price'
    fuel_diesel_key = 'fuel_diesel_price'
    fuel_lpg_key = 'fuel_lpg_price'

    def __get_fuel_price(response_text, station_name, fuel_css_selector, fuel_location_css_selector, fuel_key):
        logging.debug("Parsing " + fuel_key + " for " + station_name)
        soup = BeautifulSoup(response_text, 'html.parser')
        float_regex = r"\d+(?:\.\d+)?"
        price_string = soup.select(fuel_css_selector)[0].text
        price_float = float(re.findall(float_regex, price_string)[0])
        location = soup.select(fuel_location_css_selector)[0].text 

        return FuelPrice(station_name, fuel_key, price_float, location)

    def get_circlek_prices() -> list:
        station_name = "CircleK"
        url = "https://www.circlek.lv/priv%C4%81tperson%C4%81m/degvielas-cenas"
        fuel_95_price_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)'
        fuel_95_location_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3)'
        fuel_98_price_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)'
        fuel_98_location_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(3)'
        fuel_diesel_price_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)'
        fuel_diesel_location_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(3)'
        fuel_lpg_price_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)'
        fuel_lpg_location_css_selector = '.uk-table > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(3)'
        logging.info("Retrieving fuel prices for " + station_name)

        logging.debug("Getting URL " + url)
        response = requests.get(url)
        
        fuel_prices = []
        
        fuel_95_price = GasStations.__get_fuel_price(response.text, station_name, fuel_95_price_css_selector, fuel_95_location_css_selector, GasStations.fuel_95_key)
        fuel_prices.append(fuel_95_price)
        fuel_98_price = GasStations.__get_fuel_price(response.text, station_name, fuel_98_price_css_selector, fuel_98_location_css_selector, GasStations.fuel_98_key)
        fuel_prices.append(fuel_98_price)
        fuel_diesel_price = GasStations.__get_fuel_price(response.text, station_name, fuel_diesel_price_css_selector, fuel_diesel_location_css_selector, GasStations.fuel_diesel_key)
        fuel_prices.append(fuel_diesel_price)
        fuel_lpg_price = GasStations.__get_fuel_price(response.text, station_name, fuel_lpg_price_css_selector, fuel_lpg_location_css_selector, GasStations.fuel_lpg_key)
        fuel_prices.append(fuel_lpg_price)

        logging.info("Successfully retrieve fuel prices for " + station_name)        
        return fuel_prices

    def get_neste_prices() -> list:
        station_name = "Neste"
        url = "https://www.neste.lv/lv/content/degvielas-cenas"
        fuel_95_price_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_95_location_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)'
        fuel_98_price_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_98_location_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3)'
        fuel_diesel_price_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_diesel_location_css_selector = '.field__item > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)'
        logging.info("Retrieving fuel prices for " + station_name)

        logging.debug("Getting URL " + url)
        response = requests.get(url)

        fuel_prices = []

        fuel_95_price = GasStations.__get_fuel_price(response.text, station_name, fuel_95_price_css_selector, fuel_95_location_css_selector, GasStations.fuel_95_key)
        fuel_prices.append(fuel_95_price)
        fuel_98_price = GasStations.__get_fuel_price(response.text, station_name, fuel_98_price_css_selector, fuel_98_location_css_selector, GasStations.fuel_98_key)
        fuel_prices.append(fuel_98_price)
        fuel_diesel_price = GasStations.__get_fuel_price(response.text, station_name, fuel_diesel_price_css_selector, fuel_diesel_location_css_selector, GasStations.fuel_diesel_key)
        fuel_prices.append(fuel_diesel_price)
        return fuel_prices

    def get_virsi_prices() -> list:
        station_name = "Virši"
        url = "https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas"
        fuel_95_price_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_95_location_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(2) > p:nth-child(2)'
        fuel_98_price_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_98_location_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(3) > p:nth-child(2)'
        fuel_diesel_price_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_diesel_location_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > p:nth-child(2)'
        fuel_lpg_price_css_selector = 'div.price-card:nth-child(5) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_lpg_location_css_selector = 'div.price-card:nth-child(5) > p:nth-child(2)'
        logging.info("Retrieving fuel prices for " + station_name)

        logging.debug("Getting URL " + url)
        response = requests.get(url)

        fuel_prices = []

        fuel_95_price = GasStations.__get_fuel_price(response.text, station_name, fuel_95_price_css_selector, fuel_95_location_css_selector, GasStations.fuel_95_key)
        fuel_prices.append(fuel_95_price)
        fuel_98_price = GasStations.__get_fuel_price(response.text, station_name, fuel_98_price_css_selector, fuel_98_location_css_selector, GasStations.fuel_98_key)
        fuel_prices.append(fuel_98_price)
        fuel_diesel_price = GasStations.__get_fuel_price(response.text, station_name, fuel_diesel_price_css_selector, fuel_diesel_location_css_selector, GasStations.fuel_diesel_key)
        fuel_prices.append(fuel_diesel_price)
        fuel_lpg_price = GasStations.__get_fuel_price(response.text, station_name, fuel_lpg_price_css_selector, fuel_lpg_location_css_selector, GasStations.fuel_lpg_key)
        fuel_prices.append(fuel_lpg_price)

        logging.info("Successfully retrieve fuel prices for " + station_name)        
        return fuel_prices
    
    def get_viada_prices() -> list:
        station_name = "Viada"
        url = "https://www.viada.lv/zemakas-degvielas-cenas/"
        fuel_95_price_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)'
        fuel_95_location_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)'
        fuel_98_price_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)'
        fuel_98_location_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3)'
        fuel_diesel_price_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)'
        fuel_diesel_location_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)'
        fuel_lpg_price_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)'
        fuel_lpg_location_css_selector = '.the_content_wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(3)'

        logging.info("Retrieving fuel prices for " + station_name)

        logging.debug("Getting URL " + url)
        response = requests.get(url, verify=False)

        fuel_prices = []

        fuel_95_price = GasStations.__get_fuel_price(response.text, station_name, fuel_95_price_css_selector, fuel_95_location_css_selector, GasStations.fuel_95_key)
        fuel_prices.append(fuel_95_price)
        fuel_98_price = GasStations.__get_fuel_price(response.text, station_name, fuel_98_price_css_selector, fuel_98_location_css_selector, GasStations.fuel_98_key)
        fuel_prices.append(fuel_98_price)
        fuel_diesel_price = GasStations.__get_fuel_price(response.text, station_name, fuel_diesel_price_css_selector, fuel_diesel_location_css_selector, GasStations.fuel_diesel_key)
        fuel_prices.append(fuel_diesel_price)
        fuel_lpg_price = GasStations.__get_fuel_price(response.text, station_name, fuel_lpg_price_css_selector, fuel_lpg_location_css_selector, GasStations.fuel_lpg_key)
        fuel_prices.append(fuel_lpg_price)

        logging.info("Successfully retrieve fuel prices for " + station_name)        
        return fuel_prices