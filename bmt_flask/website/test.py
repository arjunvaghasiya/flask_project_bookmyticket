import unittest
import requests
from flask_jwt_extended import create_access_token
from base64 import b64encode


def basic_auth_for_user(username, password):
    data = {"username": username, "password": password}
    headers = {}
    headers["Authorization"] = "Basic " + b64encode(
        (data["username"] + ":" + data["password"]).encode("utf-8")
    ).decode("utf-8")
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    return headers


def user_data_(var_username, var_email, var_password, var_password_verify):
    dict1 = {}
    dict1 = {
        "username": var_username,
        "email": var_email,
        "password": var_password,
        "password_verify": var_password_verify,
    }
    return dict1


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"
    data = {
        "username": "user-2476",
        "email": "mauxebruttoibeu-2476@yopmail.com",
        "password": "abc123",
        "password_verify": "abc123",
        "first_name": "maux",
        "last_name": "oibeu",
        "gender": "male",
        "passport_number": "hsd976ogvsdg",
        "nationality": "indian",
        "age": "32",
        "address": "surat",
        "phone": "9367692476",
    }

    flight_data = {
        "flight_id": "fl-int-arbemt-0001",
        "flight_name": "CDF-3122",
        "flight_airline": "arabemirates",
        "flight_from": "delhi",
        "flight_to": "singapore",
        "business_class_total": "80",
        "economy_class_total": "150",
        "bus_cls_avl_seets": "50",
        "ecn_cls_avl_seets": "50",
        "dpt_date": "2022-11-25",
        "eta_date": "2022-11-25",
        "dpt_time": "12:20:00",
        "eta_time": "03:20:00",
        "business_class_price": 90000,
        "economy_class_price": 80000,
    }

    booking_data = {
        "flight_id": "fl-int-airind-0001",
        "coupan_code": "zief30c4xBOtUXh",
        "b_class": 1,
        "e_class": 1,
    }
    user_data = {"email": "test_update@gmail.com"}

    admin_user_data = {
        "email": "test_admin_@gmail.com",
        "is_admin": True,
        "is_superuser": False,
    }

    def test1_register_user(self):
        resp = requests.post("http://127.0.0.1:5000/", json=self.data)
        self.assertNotEqual(resp.status_code, 200)

    def test2_get_users(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/admin/all_users/", headers=headers)
        self.assertEqual(resp.status_code, 200)
        print("test 2 is completed")

    def test3_get_flights(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/flights/1", headers=headers)
        self.assertEqual(resp.status_code, 200)
        print("test 3 is completed")

    def test4_get_flights_acoding_to_location_date(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get(
            "http://127.0.0.1:5000/flights/date/rajkot/london/2022/12/06/1"
        )
        self.assertEqual(resp.status_code, 200)
        print("test 4 is completed")

    def test5_get_flights_acoding_to_location_price(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/flights/rajkot/london/50000.0/1")
        self.assertEqual(resp.status_code, 200)
        print("test 5 is completed")

    def test6_get_flights_acoding_to_location(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/flights/rajkot/london/1")
        self.assertEqual(resp.status_code, 200)
        print("test 6 is completed")

    def test7_add_flight(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.post(
            "http://127.0.0.1:5000/admin/flight_add/",
            json=self.flight_data,
            headers=headers,
        )
        self.assertNotEqual(resp.status_code, 200)
        print("test 7 is completed")

    def test8_add_flight(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.put(
            "http://127.0.0.1:5000/admin/flight_update/fl-int-arbemt-0001",
            json=self.flight_data,
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 8 is completed")

    def test9_allotmnet_coupan(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.post(
            "http://127.0.0.1:5000/allot_coupan/3",
            json={"coupan_code_valid_upto": "2023-01-06"},
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 9 is completed")

    def test10_get_alloted_coupan(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/allot_coupan/3", headers=headers)
        self.assertEqual(resp.status_code, 200)
        print("test 10 is completed")

    def test11_login(self):
        headers = basic_auth_for_user("user-2476", "abc123")
        resp = requests.get("http://127.0.0.1:5000/login/", headers=headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        access_token = list(data.items())[0][1]
        print("test 10 is completed")

    def test12_get_alloted_coupan(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp1 = requests.get("http://127.0.0.1:5000/login/", headers=headers)
        self.assertEqual(resp1.status_code, 200)
        data = resp1.json()
        access_token = list(data.items())[0][1]
        headers1 = {"Authorization": "Bearer {}".format(access_token)}
        resp = requests.post(
            "http://127.0.0.1:5000/book", json=self.booking_data, headers=headers1
        )
        self.assertEqual(resp.status_code, 200)
        print("test 12 is completed")

    def test13_get_coupan(self):
        headers = basic_auth_for_user("user-2476", "abc123")
        resp1 = requests.get("http://127.0.0.1:5000/login/", headers=headers)
        self.assertEqual(resp1.status_code, 200)
        data = resp1.json()
        access_token = list(data.items())[0][1]
        headers1 = {"Authorization": "Bearer {}".format(access_token)}
        resp = requests.get("http://127.0.0.1:5000/coupan", headers=headers1)
        self.assertEqual(resp.status_code, 200)
        print("test 13 is completed")

    def test14_upadate_self(self):
        headers = basic_auth_for_user("user-2476", "abc123")
        resp1 = requests.get("http://127.0.0.1:5000/login/", headers=headers)
        self.assertEqual(resp1.status_code, 200)
        data = resp1.json()
        access_token = list(data.items())[0][1]
        headers1 = {"Authorization": "Bearer {}".format(access_token)}
        resp = requests.post("http://127.0.0.1:5000/update/user/",json=self.data ,headers=headers1)
        self.assertEqual(resp.status_code, 200)
        print("test 14 is completed")

    def test15_get_self_tickets(self):
        headers = basic_auth_for_user("user-2476", "abc123")
        resp1 = requests.get("http://127.0.0.1:5000/my_tickets", headers=headers)
        self.assertEqual(resp1.status_code, 200)
        print("test 15 is completed")



if __name__ == "__main__":
    tester = TestAPI()
    tester.test1_register_user()
