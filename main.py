import influxdb_client
from fuelprices.helpers import *
from influxdb_client.client.write_api import SYNCHRONOUS

def main():
    circlek_prices = get_circlek_prices()
    neste_prices = get_neste_prices()
    virsi_prices = get_virsi_prices()

    bucket = "fuel_prices"
    org = "primary"
    token = ""
    # Store the URL of your InfluxDB instance
    url="http://localhost:8086"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    record = influxdb_client.Point("fuel_95_price").tag("fuel_station", "pepega").time(circlek_prices.timestamp).field("price", circlek_prices.fuel_95_price)
    write_api.write(bucket=bucket, org=org, record=record)

if __name__ == '__main__':
    main()