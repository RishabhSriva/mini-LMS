import requests
import sys

BASE_URL = 'http://localhost:8001/api'

def register(username, password, role):
    url = f"{BASE_URL}/accounts/register/"
    data = {'username': username, 'email': f'{username}@example.com', 'password': password, 'role': role}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print(f"Registered {username} ({role})")
        return True
    else:
        print(f"Failed to register {username}: {response.text}")
        return False

def login(username, password):
    url = f"{BASE_URL}/accounts/token/"
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Logged in {username}")
        return response.json()['access']
    else:
        print(f"Failed to login {username}: {response.text}")
        return None

def create_course(token, title):
    url = f"{BASE_URL}/courses/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'title': title, 'description': 'Test Description'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Created course '{title}'")
        return response.json()['id']
    else:
        print(f"Failed to create course: {response.text}")
        return None

def create_assignment(token, course_id, title):
    url = f"{BASE_URL}/courses/assignments/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'course': course_id, 'title': title, 'description': 'Test Assignment', 'due_date': '2025-12-31T23:59:59Z'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Created assignment '{title}'")
        return response.json()['id']
    else:
        print(f"Failed to create assignment: {response.text}")
        return None

def submit_assignment(token, assignment_id, content):
    url = f"{BASE_URL}/courses/submissions/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'assignment': assignment_id, 'content': content}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Submitted assignment {assignment_id}")
        return True
    else:
        print(f"Failed to submit assignment: {response.text}")
        return False

def main():
    # Instructor Flow
    register('instructor1', 'pass123', 'instructor')
    token_inst = login('instructor1', 'pass123')
    if not token_inst: return

    course_id = create_course(token_inst, 'Python 101')
    if not course_id: return

    assignment_id = create_assignment(token_inst, course_id, 'Homework 1')
    if not assignment_id: return

    # Student Flow
    register('student1', 'pass123', 'student')
    token_stud = login('student1', 'pass123')
    if not token_stud: return

    # Verify student can see course (optional check, skipping for brevity)
    
    # Submit assignment
    if submit_assignment(token_stud, assignment_id, 'My submission content'):
        print("Verification SUCCESS!")
    else:
        print("Verification FAILED!")

if __name__ == '__main__':
    main()
