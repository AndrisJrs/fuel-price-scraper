import os
import logging
from fuelprices.GasStations import (
    get_circlek_prices,
    get_neste_prices,
    get_virsi_prices,
    get_viada_prices,
)
from fuelprices.InfluxDb import InfluxDb


def main():
    bucket = os.environ["INFLUXDB_BUCKET"]
    url = os.environ["INFLUXDB_URL"]
    org = os.environ["INFLUXDB_ORG"]
    token = os.environ["INFLUXDB_TOKEN"]

    influxdb = InfluxDb(url, token, org, bucket)

    try:
        circlek_prices = get_circlek_prices()
        influxdb.write_fuel_prices(circlek_prices)
    except Exception as e:
        logging.error("Failed to retrieve CircleK prices")
        logging.exception(e)

    try:
        neste_prices = get_neste_prices()
        influxdb.write_fuel_prices(neste_prices)
    except Exception as e:
        logging.error("Failed to retrieve Neste prices")
        logging.exception(e)

    try:
        virsi_prices = get_virsi_prices()
        influxdb.write_fuel_prices(virsi_prices)
    except Exception as e:
        logging.error("Failed to retrieve Virsi prices")
        logging.exception(e)

    try:
        viada_prices = get_viada_prices()
        influxdb.write_fuel_prices(viada_prices)
    except Exception as e:
        logging.error("Failed to retrieve Viada prices")
        logging.exception(e)


if __name__ == "__main__":
    main()
