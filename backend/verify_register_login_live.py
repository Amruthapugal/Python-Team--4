import requests
import json
import random
import string

def verify_register_login_live():
    base_url = 'http://127.0.0.1:8000/api'
    
    # Generate random user
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    email = f'live_{rand_suffix}@test.com'
    password = 'password123'
    name = 'Live Tester'
    
    # 1. Register (Payload matching Register.jsx)
    register_url = f'{base_url}/users/'
    register_data = {
        'username': email,
        'email': email,
        'name': name,
        'password': password,
        'role': 'STUDENT'
    }
    
    print(f"1. Registering: {email}")
    try:
        resp = requests.post(register_url, json=register_data)
        print(f"Register Status: {resp.status_code}")
        print(f"Register Body: {resp.text}")
        
        if resp.status_code != 201:
            print("REGISTRATION FAILED. Aborting.")
            return
    except Exception as e:
        print(f"Register Exception: {e}")
        return

    # 2. Login (Payload matching Login.jsx)
    login_url = f'{base_url}/token/'
    login_data = {
        'email': email,
        'password': password
    }
    
    print(f"2. Logging in: {email}")
    try:
        resp = requests.post(login_url, json=login_data)
        print(f"Login Status: {resp.status_code}")
        print(f"Login Body: {resp.text}")
        
        if resp.status_code == 200:
            print("LOGIN SUCCESS!")
        else:
             print("LOGIN FAILED!")
             
    except Exception as e:
        print(f"Login Exception: {e}")

if __name__ == '__main__':
    verify_register_login_live()
