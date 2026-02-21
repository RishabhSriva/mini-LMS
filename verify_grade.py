import requests
import sys

BASE_URL = 'http://localhost:8001/api'

def login(username, password):
    url = f"{BASE_URL}/accounts/token/"
    data = {'username': username, 'password': password}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()['access']
    except:
        pass
    return None

def get_submissions(token):
    url = f"{BASE_URL}/courses/submissions/"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def grade_submission(token, submission_id, grade):
    url = f"{BASE_URL}/courses/submissions/{submission_id}/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'grade': grade}
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Graded submission {submission_id} with {grade}")
        return True
    else:
        print(f"Failed to grade submission {submission_id}: {response.text}")
        return False

def main():
    # Login as instructor
    token_inst = login('instructor1', 'pass123')
    if not token_inst:
        print("Failed to login as instructor")
        return

    # Get submissions
    submissions = get_submissions(token_inst)
    if not submissions:
        print("No submissions found to grade")
        # Creating one if needed? Assuming verify.py ran before and created one.
        return

    submission_id = submissions[0]['id']
    
    # Grade it
    if grade_submission(token_inst, submission_id, 'A+'):
        print("Grading Verification SUCCESS!")
    else:
        print("Grading Verification FAILED!")

if __name__ == '__main__':
    main()
