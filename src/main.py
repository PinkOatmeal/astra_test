from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.controllers.geolite_controller import GeoliteController
from src.db.database import Base, engine, SessionLocal
from src.schemas.Geo import GeoSchemaCountry, GeoSchemaCity, GeoSchemaFull

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/country/{ip}", response_model=GeoSchemaCountry)
def get_country_info(ip: str, db: Session = Depends(get_db)):
    controller = GeoliteController(db)
    return controller.fetch_country_info(ip)


@app.get("/city/{ip}", response_model=GeoSchemaCity)
def get_city_info(ip: str, db: Session = Depends(get_db)):
    controller = GeoliteController(db)
    return controller.fetch_city_info(ip)


@app.get("/full/{ip}", response_model=GeoSchemaFull)
def get_full_info(ip: str, db: Session = Depends(get_db)):
    controller = GeoliteController(db)
    return controller.fetch_city_info(ip)
