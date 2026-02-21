import requests
import sys

BASE_URL = 'http://localhost:8000/api'

def get_token(username, password):
    response = requests.post(f"{BASE_URL}/accounts/token/", data={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json()['access']
    return None

def main():
    print("--- 1. Setup Data ---")
    # Login as Instructor
    inst_token = get_token('instructor1', 'pass123')
    if not inst_token:
        print("Error: instructor1 not found. Please register users first via verify.py or web UI.")
        return

    # Create Course & Assignment
    headers_inst = {'Authorization': f'Bearer {inst_token}'}
    c_resp = requests.post(f"{BASE_URL}/courses/", json={'title': 'CLI Course', 'description': 'Test'}, headers=headers_inst)
    course_id = c_resp.json().get('id')
    print(f"Course Created: ID {course_id}")

    a_resp = requests.post(f"{BASE_URL}/courses/assignments/", json={
        'course': course_id, 'title': 'CLI Assignment', 'description': 'Accept me!', 'due_date': '2025-01-01T12:00:00Z'
    }, headers=headers_inst)
    if a_resp.status_code != 201:
        print("Failed to create assignment")
        return
    assignment_id = a_resp.json()['id']
    print(f"Assignment Created: ID {assignment_id}")

    print("\n--- 2. Student Flow ---")
    stud_token = get_token('student1', 'pass123')
    if not stud_token:
         print("Error: student1 not found.")
         return
    headers_stud = {'Authorization': f'Bearer {stud_token}'}

    # Verify initial status (should be null)
    # Note: The API I built requires fetching assignment details to see 'current_user_status' 
    # OR the specific track endpoint via GET if I implemented it?
    # I implemented POST /track/. I also implemented GET /track/ in the view!
    
    track_resp = requests.get(f"{BASE_URL}/courses/assignments/{assignment_id}/track/", headers=headers_stud)
    print(f"Initial Status: {track_resp.json().get('status')}")

    # ACCEPT Assignment
    print(">> Student Accepting Assignment...")
    accept_resp = requests.post(f"{BASE_URL}/courses/assignments/{assignment_id}/track/", json={'status': 'accepted'}, headers=headers_stud)
    print(f"New Status: {accept_resp.json().get('status')}")

    # SUBMIT Assignment
    print(">> Student Submitting Work...")
    sub_resp = requests.post(f"{BASE_URL}/courses/submissions/", json={'assignment': assignment_id, 'content': 'CLI Submission'}, headers=headers_stud)
    if sub_resp.status_code == 201:
        print("Submission Successful!")
    else:
        print(f"Submission Failed: {sub_resp.text}")

    print("\n--- 3. Instructor Grading ---")
    # Get submission ID
    # Instructor views submissions
    subs_resp = requests.get(f"{BASE_URL}/courses/submissions/", headers=headers_inst)
    # Find our submission
    submission = next((s for s in subs_resp.json() if s['assignment'] == assignment_id), None)
    
    if submission:
        sub_id = submission['id']
        print(f"Found Submission ID: {sub_id}")
        grade_resp = requests.patch(f"{BASE_URL}/courses/submissions/{sub_id}/", json={'grade': 'A+'}, headers=headers_inst)
        print(f"Grading Response: {grade_resp.status_code} - Grade: {grade_resp.json().get('grade')}")
    else:
        print("Submission not found for instructor.")

if __name__ == "__main__":
    main()
