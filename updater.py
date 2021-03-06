from config import GEOLITE_USER_ID, GEOLITE_API_KEY
from src.controllers.geolite_controller import GeoliteController
from src.db.database import Base, engine, SessionLocal
from src.exceptions.exceptions import InvalidIPProvided, IPNotFound, ReservedIPProvided


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    controller: GeoliteController = GeoliteController(db, user_id=GEOLITE_USER_ID, api_key=GEOLITE_API_KEY)

    print("Введите ip-адрес для обновления конкретной записи")
    print("`all` для обновления всех записей")
    print("`exit` для завершения консольного приложения")

    while True:
        answer: str = str(input("> "))
        if answer == "exit":
            return
        if answer == "all":
            controller.update_all()
            print(f"База IP-адресов успешно обновлена")
            continue
        if len(answer) != 0:
            try:
                controller.fetch_city_info(answer)
                print(f"Данные о адресе {answer} успешно обновлены")
            except InvalidIPProvided:
                print("Введен не правильный ip-адрес, повторите ввод")
            except ReservedIPProvided:
                print("Введен зарезервированный ip-адрес (приватный, многоадресный и т.д.)")
            except IPNotFound:
                print("Введенный ip-адрес не найден в базе geolite")
        else:
            print("Неправильная команда, повторите ввод")


if __name__ == '__main__':
    main()
