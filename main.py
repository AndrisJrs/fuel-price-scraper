import logging
import os

from fuelprices.gas_stations import (
    get_circlek_prices,
    get_viada_prices,
    get_virsi_prices,
)
from fuelprices.influx_db import InfluxDb

logger = logging.getLogger(__name__)


def main():
    bucket = os.environ["INFLUXDB_BUCKET"]
    url = os.environ["INFLUXDB_URL"]
    org = os.environ["INFLUXDB_ORG"]
    token = os.environ["INFLUXDB_TOKEN"]

    influxdb = InfluxDb(url, token, org, bucket)

    try:
        circlek_prices = get_circlek_prices()
        influxdb.write_fuel_prices(circlek_prices)
    except Exception:
        logger.exception("Failed to retrieve CircleK prices")

    try:
        virsi_prices = get_virsi_prices()
        influxdb.write_fuel_prices(virsi_prices)
    except Exception:
        logger.exception("Failed to retrieve Virsi prices")

    try:
        viada_prices = get_viada_prices()
        influxdb.write_fuel_prices(viada_prices)
    except Exception:
        logger.exception("Failed to retrieve Viada prices")


if __name__ == "__main__":
    main()
