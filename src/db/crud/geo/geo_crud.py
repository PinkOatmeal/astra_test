from typing import Optional

from sqlalchemy.orm import Session

from src.db.models.Geo import Geo
from src.schemas.Geo import GeoSchemaFull, GeoSchemaFromCountryJson


class GeoCrud:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_with_full_info(self, geo: GeoSchemaFull) -> Geo:
        geo_to_db: Geo = Geo(
            ip=geo.ip,
            continent=geo.continent,
            continent_code=geo.continent_code,
            country=geo.country,
            country_iso=geo.country_iso,
            city=geo.city,
            latitude=geo.latitude,
            longitude=geo.longitude,
            time_zone=geo.time_zone,
            postal=geo.postal,
            metro_code=geo.metro_code)
        self.db.add(geo_to_db)
        self.db.commit()
        self.db.refresh(geo_to_db)
        return geo_to_db

    def create_with_country(self, geo: GeoSchemaFromCountryJson) -> Geo:
        geo_to_db: Geo = Geo(
            ip=geo.ip,
            continent=geo.continent,
            continent_code=geo.continent_code,
            country=geo.country,
            country_iso=geo.country_iso)

        self.db.add(geo_to_db)
        self.db.commit()
        self.db.refresh(geo_to_db)
        return geo_to_db

    def read_by_id(self, _id: int) -> Optional[Geo]:
        return self.db.query(Geo).filter(Geo.id == _id).first()

    def update_with_full_info(self, geo: GeoSchemaFull) -> Geo:
        geo_from_db: Geo = self.db.query(Geo).filter(Geo.ip == geo.ip).first()

        geo_from_db.ip = geo.ip,
        geo_from_db.continent = geo.continent,
        geo_from_db.continent_code = geo.continent_code,
        geo_from_db.country = geo.country,
        geo_from_db.country_iso = geo.country_iso,
        geo_from_db.city = geo.city,
        geo_from_db.latitude = geo.latitude,
        geo_from_db.longitude = geo.longitude,
        geo_from_db.time_zone = geo.time_zone,
        geo_from_db.postal = geo.postal,
        geo_from_db.metro_code = geo.metro_code

        self.db.commit()
        self.db.refresh(geo_from_db)

        return geo_from_db

    def update_with_country(self, geo: GeoSchemaFromCountryJson) -> Geo:
        geo_from_db: Geo = self.db.query(Geo).filter(Geo.ip == geo.ip).first()

        geo_from_db.ip = geo.ip,
        geo_from_db.continent = geo.continent,
        geo_from_db.continent_code = geo.continent_code,
        geo_from_db.country = geo.country,
        geo_from_db.country_iso = geo.country_iso

        self.db.commit()
        self.db.refresh(geo_from_db)

        return geo_from_db

    def ip_entry_exists(self, ip: str) -> bool:
        return self.db.query(Geo).filter(Geo.ip == ip).first() is not None
