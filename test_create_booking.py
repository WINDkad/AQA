from conftest import invalid_booking_data
from constants import BASE_URL
import requests


class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, "Бронь не удалилась"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"


    def test_update_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        updated_data = booking_data.copy()
        updated_data["firstname"] = "UpdatedName"
        updated_data["lastname"] = "UpdatedLastName"
        updated_data["totalprice"] = 9999
        updated_data["depositpaid"] = False
        updated_data["bookingdates"] = {
            "checkin": "2025-12-01",
            "checkout": "2025-12-10"
        }
        updated_data["additionalneeds"] = "Dinner"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=updated_data)
        assert put_booking.status_code == 200, "Бронь обновлена"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["firstname"] == updated_data["firstname"]
        assert get_booking.json()["lastname"] == updated_data["lastname"]
        assert get_booking.json()["totalprice"] == updated_data["totalprice"]
        assert get_booking.json()["depositpaid"] == updated_data["depositpaid"]
        assert get_booking.json()["bookingdates"] == updated_data["bookingdates"]
        assert get_booking.json()["additionalneeds"] == updated_data["additionalneeds"]


    def test_patch_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        patch_data = {
            "firstname": "UpdatedName",
            "lastname": "UpdatedLastName"
        }

        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=patch_data)
        assert patch_booking.status_code == 200, "Бронь обновлена"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["firstname"] == patch_data["firstname"]
        assert get_booking.json()["lastname"] == patch_data["lastname"]
        assert get_booking.json()["totalprice"] == booking_data["totalprice"]

    def test_negative_scenarios_combined(self, auth_session, booking_data):
        get_response = auth_session.get(f"{BASE_URL}/booking/999999")
        assert get_response.status_code == 404, "GET: ожидался 404 для несуществующей брони"

        invalid_post_data = {"firstname": "John"}  # недостаточно полей
        post_response = auth_session.post(f"{BASE_URL}/booking", json=invalid_post_data)
        assert post_response.status_code == 400, "POST: ожидался 400 при невалидных данных"

        put_response = auth_session.put(f"{BASE_URL}/booking/999999", json=booking_data)
        assert put_response.status_code == 404, "PUT: ожидался 404 при обновлении несуществующей брони"

        patch_response = auth_session.patch(f"{BASE_URL}/booking/1", json={})
        assert patch_response.status_code == 400, "PATCH: ожидался 400 при пустом теле"

        delete_response = requests.delete(f"{BASE_URL}/booking/1")
        assert delete_response.status_code == 403, "DELETE: ожидалась ошибка авторизации"




