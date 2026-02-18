import requests
import time

def verify_admin_full_flow():
    base_url = 'http://127.0.0.1:8000/api'
    
    # 1. Login as Admin
    print("\n[Step 1] Login as Admin")
    admin_creds = {'email': 'admin@test.com', 'password': 'password123'}
    try:
        resp = requests.post(f'{base_url}/token/', json=admin_creds)
        if resp.status_code != 200:
            print("Admin login failed")
            return
        admin_token = resp.json()['access']
        print("Admin logged in.")
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
    except Exception as e:
        print(f"Login error: {e}")
        return

    # 2. Check Bookings as Admin
    print("\n[Step 2] Admin fetching bookings (Should be allowed)")
    resp = requests.get(f'{base_url}/bookings/', headers=admin_headers)
    if resp.status_code == 200:
        bookings = resp.json()
        print(f"Admin sees {len(bookings)} bookings.")
    else:
        print(f"FAILED: Admin could not fetch bookings. Status: {resp.status_code}")
        return

    # 3. Create a Booking as Student (to have something to approve)
    print("\n[Step 3] Student creating booking")
    student_creds = {'email': 'student@test.com', 'password': 'password123'}
    resp = requests.post(f'{base_url}/token/', json=student_creds)
    student_token = resp.json()['access']
    student_headers = {'Authorization': f'Bearer {student_token}'}
    
    # Get a resource
    resources = requests.get(f'{base_url}/resources/', headers=student_headers).json()
    if resources:
        res_id = resources[0]['id']
        booking_data = {
            'resource': res_id,
            'booking_date': '2026-04-01',
            'time_slot': '09:00-10:00'
        }
        resp = requests.post(f'{base_url}/bookings/', json=booking_data, headers=student_headers)
        if resp.status_code == 201:
            new_booking_id = resp.json()['id']
            print(f"Student created booking {new_booking_id}")
        else:
            print(f"Booking failed/exists: {resp.text}")
            # Try to grab an existing pending one
            all_bookings = requests.get(f'{base_url}/bookings/', headers=student_headers).json()
            pending = [b for b in all_bookings if b['status'] == 'PENDING']
            if pending:
                new_booking_id = pending[0]['id']
                print(f"Using existing pending booking {new_booking_id}")
            else:
                print("No pending bookings to test with.")
                return

        # 4. Admin Approves Booking
        print(f"\n[Step 4] Admin approving booking {new_booking_id}")
        resp = requests.post(f'{base_url}/bookings/{new_booking_id}/approve/', headers=admin_headers)
        if resp.status_code == 200:
            print("Admin successfully approved booking.")
        else:
            print(f"FAILED to approve: {resp.status_code} {resp.text}")

    else:
        print("No resources found.")

if __name__ == '__main__':
    verify_admin_full_flow()
