import requests
import json

def verify_live_login():
    url = 'http://127.0.0.1:8000/api/token/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'email': 'student@test.com',
        'password': 'password123'
    }
    
    print(f"Attempting login to: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("LOGIN SUCCESS!")
            tokens = response.json()
            access_token = tokens.get('access')
            if access_token:
                print("Access Token received.")
                # Try accessing a protected resource
                bookings_url = 'http://127.0.0.1:8000/api/bookings/'
                auth_headers = {'Authorization': f'Bearer {access_token}'}
                print(f"Attempting to fetch bookings from: {bookings_url}")
                resp2 = requests.get(bookings_url, headers=auth_headers)
                print(f"Bookings Status: {resp2.status_code}")
                print(f"Bookings Body: {resp2.text}")
        else:
            print("LOGIN FAILED!")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Is it running?")

if __name__ == '__main__':
    verify_live_login()
