import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = os.environ['INFLUXDB_BUCKET']
url = os.environ['INFLUXDB_URL']
org = os.environ['INFLUXDB_ORG']
token = os.environ['INFLUXDB_TOKEN']

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


record = influxdb_client.Point("fuel_95_price").tag("fuel_station", "pepega").time(circlek_prices.timestamp).field("price", circlek_prices.fuel_95_price)
write_api.write(bucket=bucket, org=org, record=record)
