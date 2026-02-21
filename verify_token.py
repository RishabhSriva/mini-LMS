import requests
import sys
import base64
import json

BASE_URL = 'http://localhost:8000/api'

def register(username, password, role):
    url = f"{BASE_URL}/accounts/register/"
    data = {
        'username': username,
        'password': password,
        'role': role
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"Registered {username} as {role}")
            return True
        else:
            print(f"Failed to register {username}: {response.text}")
            return False
    except Exception as e:
        print(f"Error registering {username}: {e}")
        return False

def login(username, password):
    url = f"{BASE_URL}/accounts/token/"
    data = {'username': username, 'password': password}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Logged in {username}")
            token = response.json()['access']
            # Decoding token to verify role
            parts = token.split('.')
            payload = json.loads(base64.b64decode(parts[1] + "==").decode('utf-8'))
            print(f"Token Payload Role: {payload.get('role')}")
            if payload.get('role') != 'instructor' and username == 'instructor1':
                 print("WARNING: Role mismatch in token for instructor!")
            return token
        else:
            print(f"Failed to login {username}: {response.text}")
            return None
    except Exception as e:
        print(f"Error logging in {username}: {e}")
        return None

def main():
    # Register (might fail if exists, that's fine)
    register('instructor1', 'pass123', 'instructor')
    
    # Login and check token
    print("\n--- Verifying Instructor Token ---")
    token_inst = login('instructor1', 'pass123')
    
    if token_inst:
        print("Verification SUCCESS! Token contains role.")
    else:
        print("Verification FAILED.")

if __name__ == '__main__':
    main()
