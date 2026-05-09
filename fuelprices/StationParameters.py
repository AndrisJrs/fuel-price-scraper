from typing import Optional


class StationParameters:
    def __init__(
        self,
        station_name: str,
        url: str,
        petrol_95_price_css_selector: Optional[str] = None,
        petrol_95_location_css_selector: Optional[str] = None,
        petrol_98_price_css_selector: Optional[str] = None,
        petrol_98_location_css_selector: Optional[str] = None,
        diesel_price_css_selector: Optional[str] = None,
        diesel_location_css_selector: Optional[str] = None,
        renewable_diesel_price_css_selector: Optional[str] = None,
        renewable_diesel_location_css_selector: Optional[str] = None,
        lpg_price_css_selector: Optional[str] = None,
        lpg_location_css_selector: Optional[str] = None,
    ):
        self.station_name = station_name
        self.url = url
        self.petrol_95_price_css_selector = petrol_95_price_css_selector
        self.petrol_95_location_css_selector = petrol_95_location_css_selector
        self.petrol_98_price_css_selector = petrol_98_price_css_selector
        self.petrol_98_location_css_selector = petrol_98_location_css_selector
        self.diesel_price_css_selector = diesel_price_css_selector
        self.diesel_location_css_selector = diesel_location_css_selector
        self.renewable_diesel_price_css_selector = renewable_diesel_price_css_selector
        self.renewable_diesel_location_css_selector = (
            renewable_diesel_location_css_selector
        )
        self.lpg_price_css_selector = lpg_price_css_selector
        self.lpg_location_css_selector = lpg_location_css_selector
