# Fuel Price Scraper

## Abstract

This is scraper written in Python 3.10 that collects data from most popular fuel stations in Latvia and writes them into InfluxDB time series database that can later be used to visualize data in Graphana or other tools. This script must be configured with CRON to retrieve data in automated and repeated manner.

## Configuration

This script requires provisioned InfluxDB database version 2.0 or newer. Connection configuration is is provided through environment variables:

    INFLUXDB_BUCKET
    INFLUXDB_URL
    INFLUXDB_ORG
    INFLUXDB_TOKEN

In addition log level can be configured using following environment variable

    LOG_LEVEL

## Docker

Dockerfile is provided to run this script in a portable fashion with all dependencies configured. Docker image are also provided in this repository. \
Docker build and run example:

    docker build -t fuel-price-scraper .

    docker run -e LOG_LEVEL="DEBUG" -e INFLUXDB_BUCKET="fuel_prices" -e INFLUXDB_URL="http://infuxdb:8086" -e INFLUXDB_ORG="primary" -e INFLUXDB_TOKEN="token" --name fuel-price-scraper fuel-price-scraper