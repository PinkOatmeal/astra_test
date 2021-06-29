from base64 import b64encode

import requests
from sqlalchemy.orm import Session

from src.db.crud.geo.geo_crud import GeoCrud
from src.db.models.Geo import Geo
from src.schemas.Geo import GeoSchemaFromCountryJson, GeoSchemaFull


class GeoliteController:
    auth_str: str
    crud: GeoCrud

    def __init__(self, user_id: str, api_key: str, db: Session) -> None:
        self.auth_str = b64encode(bytes(f"{user_id}:{api_key}", "utf-8")).decode("utf-8")
        self.crud = GeoCrud(db)

    def fetch_country_info(self, ip: str) -> Geo:
        url = f"https://geolite.info/geoip/v2.1/country/{ip}"

        response = requests.get(url, headers={"Authorization": f"Basic {self.auth_str}"})
        response_json: dict[str, any] = response.json()

        geo_to_db: GeoSchemaFromCountryJson = GeoSchemaFromCountryJson(
            ip=ip,
            continent=response_json["continent"]["names"]["en"],
            continent_code=response_json["continent"]["code"],
            country=response_json["country"]["names"]["en"],
            country_iso=response_json["country"]["iso_code"]
        )

        return self.crud.create_with_country(geo_to_db)

    def fetch_city_info(self, ip: str) -> Geo:
        url = f"https://geolite.info/geoip/v2.1/city/{ip}"

        response = requests.get(url, headers={"Authorization": f"Basic {self.auth_str}"})
        response_json: dict[str, any] = response.json()

        geo_to_db: GeoSchemaFull = GeoSchemaFull(
            ip=ip,
            continent=response_json["continent"]["names"]["en"],
            continent_code=response_json["continent"]["code"],
            country=response_json["country"]["names"]["en"],
            country_iso=response_json["country"]["iso_code"],
            city=response_json["city"]["names"]["en"] if "city" in response_json.keys() else None,
            latitude=response_json["location"]["latitude"],
            longitude=response_json["location"]["longitude"],
            time_zone=response_json["location"]["time_zone"],
            postal=response_json["postal"]["code"] if "postal" in response_json.keys() else None,
            metro_code=response_json["location"].get("metro_code")
        )

        return self.crud.create_with_full_info(geo_to_db)
