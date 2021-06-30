from typing import Optional

from pydantic import BaseModel


class BaseGeoSchema(BaseModel):
    ip: str


class GeoSchemaCreate(BaseModel):
    pass


class GeoSchemaCountry(BaseGeoSchema):
    country: str
    country_iso: str

    class Config:
        orm_mode = True


class GeoSchemaCity(BaseGeoSchema):
    country: str
    country_iso: str
    city: Optional[str]

    class Config:
        orm_mode = True


class GeoSchemaFull(BaseGeoSchema):
    continent: str
    continent_code: str
    country: str
    country_iso: str
    city: Optional[str]
    latitude: float
    longitude: float
    time_zone: str
    postal: Optional[str]
    metro_code: Optional[int]

    class Config:
        orm_mode = True


class GeoSchemaFromCountryJson(BaseGeoSchema):
    continent: str
    continent_code: str
    country: str
    country_iso: str

    class Config:
        orm_mode = True
