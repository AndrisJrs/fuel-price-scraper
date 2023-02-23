import requests
import re
import time
from bs4 import BeautifulSoup

class FuelPrices:
  def __init__(self, fuel_station_name, fuel_95_price, fuel_98_price, fuel_diesel_price, fuel_lpg_price):
    self.fuel_station_name = fuel_station_name
    self.fuel_95_price = fuel_95_price
    self.fuel_98_price = fuel_98_price
    self.fuel_diesel_price = fuel_diesel_price
    self.fuel_lpg_price = fuel_lpg_price
    self.timestamp = time.time()

  def get_fuel_prices(station_name, url, fuel_95_css_selector, fuel_98_css_selector, fuel_diesel_css_selector, fuel_lpg_css_selector):
    float_regex = r"\d+(?:\.\d+)?"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if fuel_95_css_selector is None:
      fuel_95_price = None
    else:
      fuel_95_price_object = soup.select(fuel_95_css_selector)[0].text
      fuel_95_price = float(re.findall(float_regex, fuel_95_price_object)[0])

    if fuel_98_css_selector is None:
      fuel_98_price = None
    else:
      fuel_98_price_object = soup.select(fuel_98_css_selector)[0].text
      fuel_98_price = float(re.findall(float_regex, fuel_98_price_object)[0])

    if fuel_diesel_css_selector is None:
      fuel_diesel_price = None
    else:
      fuel_diesel_price_object = soup.select(fuel_diesel_css_selector)[0].text
      fuel_diesel_price = float(re.findall(float_regex, fuel_diesel_price_object)[0])

    if fuel_lpg_css_selector is None:
      fuel_lpg_price = None
    else:
      fuel_lpg_price_object = soup.select(fuel_lpg_css_selector)[0].text
      fuel_lpg_price = float(re.findall(float_regex, fuel_lpg_price_object)[0])

    return FuelPrices(station_name, fuel_95_price, fuel_98_price, fuel_diesel_price, fuel_lpg_price)