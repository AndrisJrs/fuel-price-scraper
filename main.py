import os

from fuelprices.gas_stations import (
    get_circlek_prices,
    get_kool_prices,
    get_viada_prices,
    get_virsi_prices,
)
from fuelprices.influx_db import InfluxDb


def main():
    bucket = os.environ["INFLUXDB_BUCKET"]
    url = os.environ["INFLUXDB_URL"]
    org = os.environ["INFLUXDB_ORG"]
    token = os.environ["INFLUXDB_TOKEN"]

    influxdb = InfluxDb(url, token, org, bucket)

    scrapers = {
        "CircleK": get_circlek_prices,
        "Virsi": get_virsi_prices,
        "Viada": get_viada_prices,
        "Kool": get_kool_prices,
    }
    # Collect every station before failing, so one broken site doesn't stop
    # the others from being written.
    errors = []
    for name, get_prices in scrapers.items():
        try:
            influxdb.write_fuel_prices(get_prices())
        except Exception as e:  # noqa: BLE001 - re-raised below in the group
            e.add_note(f"Failed to retrieve {name} prices")
            errors.append(e)

    if errors:
        raise ExceptionGroup(
            f"Failed to retrieve prices for {len(errors)} station(s)", errors
        )


if __name__ == "__main__":
    main()
