import base64
from urllib.parse import urlencode

import requests
import os

BASIQ_API_KEY = "ZTE1NmVhZTEtNzhmYi00NzQ0LTlhN2ItMWQ4NTU0ZjRkOGE3OjFhOTcyZGJmLTgyYmQtNDM4Yi04OWMyLTdlMWY4M2Q0YjFhMg=="
BASE_URL = "https://au-api.basiq.io"


def authenticate():
    headers = {
        "Authorization": f"Basic {BASIQ_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded",
        "basiq-version": "3.0",
    }
    response = requests.post(f"{BASE_URL}/token", data="scope=SERVER_ACCESS", headers=headers, verify=False)
    print('response ----> ', response.reason)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def create_user(token, email, mobile, first_name, middle_name, last_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    request_data = {
        "email": email,
        "mobile": mobile,
        "firstName": first_name,
        "lastName": last_name,
        "middleName": middle_name
    }
    response = requests.post(f"{BASE_URL}/users", headers=headers, verify=False, json=request_data)
    return response.json()


def get_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users", headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to retrieve user")


def get_user(token, user_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to retrieve user")


def get_accounts(token, user_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/{user_id}/accounts", headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to retrieve accounts")


def generate_consent_url(token, user_id: str, institution_id: str) -> str:
    # Retrieve auth link
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    print('user_id ---> ', user_id)
    print('token ---> ', token)
    print('url --> ', f"{BASE_URL}/users/{user_id}/auth_link")
    auth_link_response = requests.get(f"{BASE_URL}/users/{user_id}/auth_link", headers=headers, verify=False)
    print('auth_link_response --> ', auth_link_response.reason)
    response_json = auth_link_response.json()

    connect_link = response_json['links']["public"]

    return f"{connect_link}?institutionId={institution_id}"


def get_institutions(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/institutions", headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to retrieve accounts")