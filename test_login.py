import requests
import json

# 测试登录
def test_login(username, password):
    url = "http://localhost:8000/api/v1/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# 测试不同账号
print("Testing admin login...")
test_login("admin", "admin123")

print("\nTesting alice login...")
test_login("alice", "alice123")

print("\nTesting bob login...")
test_login("bob", "bob123")
