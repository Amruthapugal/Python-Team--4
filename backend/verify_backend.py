import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'
AUTH_URL = f'{BASE_URL}/token/'

def run_verification():
    print("--- Starting Backend Verification ---")

    # 1. Login
    print("1. Logging in as test user...")
    try:
        response = requests.post(AUTH_URL, json={'email': 'test@example.com', 'password': 'password123'})
        if response.status_code != 200:
            print(f"FAILED: Login failed. Status: {response.status_code}, Body: {response.text}")
            return
        tokens = response.json()
        access_token = tokens['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        print("SUCCESS: Logged in.")
    except Exception as e:
        print(f"FAILED: Could not connect to backend. {e}")
        return

    # 2. Create Resource
    print("\n2. Creating a Resource (Computer Lab)...")
    resource_data = {
        'name': 'Innovation Lab',
        'type': 'LAB',
        'capacity': 30,
        'status': 'AVAILABLE'
    }
    res_response = requests.post(f'{BASE_URL}/resources/', json=resource_data, headers=headers)
    if res_response.status_code != 201:
        print(f"FAILED: Resource creation failed. Status: {res_response.status_code}, Body: {res_response.text}")
        return
    resource = res_response.json()
    resource_id = resource['id']
    print(f"SUCCESS: Resource created. ID: {resource_id}")

    # 3. Create First Booking
    print("\n3. Creating First Booking (10:00-11:00)...")
    booking_data = {
        'resource': resource_id,
        'booking_date': '2025-10-25',
        'time_slot': '10:00-11:00'
    }
    book1_response = requests.post(f'{BASE_URL}/bookings/', json=booking_data, headers=headers)
    if book1_response.status_code != 201:
        print(f"FAILED: Booking 1 failed. Status: {book1_response.status_code}, Body: {book1_response.text}")
        return
    print("SUCCESS: First booking created.")

    # 4. Attempt Double Booking
    print("\n4. Attempting Double Booking (Same Resource/Time)...")
    book2_response = requests.post(f'{BASE_URL}/bookings/', json=booking_data, headers=headers)
    if book2_response.status_code == 400:
        print("SUCCESS: Double booking rejected (Expected behavior).")
        print(f"Error Message: {book2_response.text}")
    else:
        print(f"FAILED: Double booking was ALLOWED! Status: {book2_response.status_code}")

if __name__ == "__main__":
    run_verification()
