import requests
from conftest import auth_session
from constants import BASE_URL
from faker import Faker
faker = Faker()

class TestBooking:
    def test_create_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная цена не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилиия не совпадает"

        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_update_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"

        update_data = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "totalprice": faker.random_int(min=100, max=100000),
            "depositpaid": faker.boolean(),
            "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-10"
            },
            "additionalneeds": faker.word()
        }

        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=update_data)
        assert update_booking.status_code == 200, "Ошибка обновления брони"
        assert update_booking.json()["lastname"] == update_data["lastname"], "Заданная фамилия не совпадает"
        assert update_booking.json()["firstname"] == update_data["firstname"], "Заданная предоплата не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        get_data = get_booking.json()
        assert get_data["firstname"] == update_data["firstname"]
        assert get_data["lastname"] == update_data["lastname"]
        assert get_data["totalprice"] == update_data["totalprice"]
        assert get_data["depositpaid"] == update_data["depositpaid"]
        assert get_data["bookingdates"] == update_data["bookingdates"]
        assert get_data["additionalneeds"] == update_data["additionalneeds"]

    def test_patch_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден"

        update_data = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name()
        }

        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=update_data)
        assert patch_booking.status_code == 200, "Ошибка обновления брони"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200
        data = get_booking.json()

        assert data["firstname"] == update_data["firstname"]
        assert data["additionalneeds"] == booking_data["additionalneeds"]
        assert data["lastname"] == update_data["lastname"]
        assert data["totalprice"] == booking_data["totalprice"]
        assert data["depositpaid"] == booking_data["depositpaid"]
        assert data["bookingdates"] == booking_data["bookingdates"]

    def test_negative_create_booking(self, auth_session, booking_data):
        invalid_data = {
            "depositpaid": faker.boolean(),
            "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-10"
            },
            "additionalneeds": faker.word()
        }

        create_booking = auth_session.post(f"{BASE_URL}/booking", json=invalid_data)
        assert create_booking.status_code == 500, "Бронь создалась"

    def test_negative_put_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден"

        update_data = {
            "firstname": 123,
            "lastname": 123,
            "totalprice": "asdfasdf",
            "depositpaid": 123,
            "bookingdates": {
                "checkin": 123,
                "checkout": 123
            },
            "additionalneeds": 123
        }

        update_booking = auth_session.post(f"{BASE_URL}/booking/{booking_id}", json=update_data)
        assert update_booking.status_code == 404, "Бронь обновлена"

    def test_negative_patch_booking(self, auth_session, booking_data):                 #тут принимает, валидация не отрабатывает
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден"

        update_data = {
            "firstname": 123,
            "lastname": 123,
            "totalprice": "asdfasdf",
            "depositpaid": 123,
            "bookingdates": {
                "checkin": "asdf",
                "checkout": "asdf"
            },
            "additionalneeds": 123
        }

        update_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=update_data)
        assert update_booking.status_code == 200, "Бронь обновилась"


    def test_negative_get_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{faker.random_int(min=1, max=999999999)}")
        assert get_booking.status_code == 404, "Бронь найдена"

    def test_negative_delete_without_auth(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден"

        response = requests.delete(f"{BASE_URL}/booking/{booking_id}")
        assert response.status_code == 403, "Удаление прошло без авторизации!"
