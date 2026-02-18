import requests
import json

def verify_staff_approval():
    base_url = 'http://127.0.0.1:8000/api'
    
    # 1. Login as Student and create a booking
    print("\n[Step 1] Student Logic")
    student_creds = {'email': 'student@test.com', 'password': 'password123'}
    try:
        resp = requests.post(f'{base_url}/token/', json=student_creds)
        if resp.status_code != 200:
            print("Student login failed")
            return
        student_token = resp.json()['access']
        print("Student logged in.")
        
        # Create booking
        headers = {'Authorization': f'Bearer {student_token}'}
        resources = requests.get(f'{base_url}/resources/', headers=headers).json()
        if not resources:
            print("No resources found to book.")
            return
        res_id = resources[0]['id']
        
        booking_data = {
            'resource': res_id,
            'booking_date': '2026-03-01',
            'time_slot': '10:00-11:00'
        }
        resp = requests.post(f'{base_url}/bookings/', json=booking_data, headers=headers)
        if resp.status_code == 201:
            booking_id = resp.json()['id']
            print(f"Student created booking {booking_id} (PENDING)")
        else:
            # Maybe already exists
            print(f"Booking creation msg: {resp.text}")
            # Try to find an existing one
            bookings = requests.get(f'{base_url}/bookings/', headers=headers).json()
            if bookings:
                booking_id = bookings[0]['id']
                print(f"Using existing booking {booking_id}")
            else:
                print("Could not get a booking ID")
                return
    except Exception as e:
        print(f"Student steps failed: {e}")
        return

    # 2. Login as Staff
    print("\n[Step 2] Staff Logic")
    staff_creds = {'email': 'staff@test.com', 'password': 'password123'}
    try:
        resp = requests.post(f'{base_url}/token/', json=staff_creds)
        if resp.status_code != 200:
             # Try creating staff if fails (maybe reset wiped it?)
             # Assuming staff exists from reset_system.py
             print(f"Staff login failed: {resp.status_code} {resp.text}")
             return
             
        staff_token = resp.json()['access']
        print("Staff logged in.")
        staff_headers = {'Authorization': f'Bearer {staff_token}'}
        
        # 3. View All Bookings
        resp = requests.get(f'{base_url}/bookings/', headers=staff_headers)
        bookings = resp.json()
        print(f"Staff sees {len(bookings)} bookings.")
        
        # Verify specific booking is visible
        target_booking = next((b for b in bookings if b['id'] == booking_id), None)
        if target_booking:
            print("Target booking is visible to Staff.")
        else:
            print("ERROR: Staff cannot see the student booking!")
            return

        # 4. Approve Booking
        print(f"Approving booking {booking_id}...")
        resp = requests.post(f'{base_url}/bookings/{booking_id}/approve/', headers=staff_headers)
        print(f"Approve Status: {resp.status_code}")
        print(f"Approve Body: {resp.text}")
        
        if resp.status_code == 200:
            print("SUCCESS: Booking Approved!")
            
            # Verify status changed
            resp = requests.get(f'{base_url}/bookings/{booking_id}/', headers=staff_headers)
            print(f"Final Status: {resp.json()['status']}")
        else:
            print("FAILURE: Could not approve.")

    except Exception as e:
        print(f"Staff steps failed: {e}")

if __name__ == '__main__':
    verify_staff_approval()
