import requests
import json

def verify_admin_resource_mgmt():
    base_url = 'http://127.0.0.1:8000/api'
    admin_creds = {'email': 'admin@test.com', 'password': 'password123'}
    
    # 1. Login as Admin
    print("\n[Step 1] Login as Admin")
    try:
        resp = requests.post(f'{base_url}/token/', json=admin_creds)
        if resp.status_code != 200:
            print(f"Admin login failed: {resp.status_code}")
            return
        token = resp.json()['access']
        print("Admin logged in successfully.")
        headers = {'Authorization': f'Bearer {token}'}
    except Exception as e:
        print(f"Login error: {e}")
        return

    # 2. Create Resource
    print("\n[Step 2] Create Resource")
    new_resource = {
        'name': 'Test Admin Lab',
        'type': 'LAB',
        'capacity': 50,
        'status': 'AVAILABLE'
    }
    try:
        resp = requests.post(f'{base_url}/resources/', json=new_resource, headers=headers)
        print(f"Create Status: {resp.status_code}")
        if resp.status_code == 201:
            resource_id = resp.json()['id']
            print(f"Resource created: ID {resource_id}")
        else:
            print(f"Failed to create resource: {resp.text}")
            return
    except Exception as e:
        print(f"Create error: {e}")
        return

    # 3. Verify Resource Exists
    print("\n[Step 3] Verify Resource")
    resp = requests.get(f'{base_url}/resources/{resource_id}/', headers=headers)
    if resp.status_code == 200:
        print("Resource verified in DB.")
    else:
        print("Resource not found!")

    # 4. Delete Resource
    print("\n[Step 4] Delete Resource")
    try:
        resp = requests.delete(f'{base_url}/resources/{resource_id}/', headers=headers)
        print(f"Delete Status: {resp.status_code}")
        if resp.status_code == 204:
            print("Resource deleted successfully.")
        else:
            print(f"Failed to delete: {resp.text}")
    except Exception as e:
        print(f"Delete error: {e}")

if __name__ == '__main__':
    verify_admin_resource_mgmt()
