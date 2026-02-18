import requests
import json

def verify_robustness():
    base_url = 'http://127.0.0.1:8000/api'
    email = 'student@test.com'
    password = 'password123'
    
    # Test 1: Login with trailing spaces
    login_url = f'{base_url}/token/'
    login_data = {
        'email': f' {email} ',  # Note the spaces
        'password': f'{password} ' # Note the space
    }
    
    print(f"Testing Login with Whitespace: '{login_data['email']}'")
    try:
        resp = requests.post(login_url, json=login_data)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print("SUCCESS: Backend correctly trimmed whitespace and logged in.")
        else:
            print(f"FAILURE: Backend rejected whitespace. Body: {resp.text}")
             
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == '__main__':
    verify_robustness()
