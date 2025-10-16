"""
Simple script to test the authentication API endpoints
Run this after starting the server with: uvicorn app.main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def print_response(response):
    """Pretty print response"""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print("-" * 80)


def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing Health Check")
    print("-" * 80)
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)


def test_register():
    """Test user registration"""
    print("\n2. Testing User Registration")
    print("-" * 80)

    user_data = {
        "email": "john.doe@example.com",
        "phone": "0241234567",  # Will be normalized to 233241234567
        "password": "SecurePass123",
        "full_name": "John Doe",
        "user_type": "individual",
        "location": {
            "lat": 5.6037,
            "lng": -0.1870,
            "address": "Accra, Ghana"
        }
    }

    response = requests.post(f"{API_URL}/auth/register", json=user_data)
    print_response(response)
    return response.json() if response.status_code == 201 else None


def test_login(email, password):
    """Test user login"""
    print("\n3. Testing User Login")
    print("-" * 80)

    login_data = {
        "email": email,
        "password": password
    }

    response = requests.post(f"{API_URL}/auth/login", json=login_data)
    print_response(response)
    return response.json() if response.status_code == 200 else None


def test_get_profile(access_token):
    """Test getting user profile"""
    print("\n4. Testing Get User Profile (Protected Route)")
    print("-" * 80)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{API_URL}/users/me", headers=headers)
    print_response(response)


def test_update_profile(access_token):
    """Test updating user profile"""
    print("\n5. Testing Update User Profile")
    print("-" * 80)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    update_data = {
        "full_name": "John Doe Updated",
        "language_preference": "en"
    }

    response = requests.put(f"{API_URL}/users/me", json=update_data, headers=headers)
    print_response(response)


def test_get_stats(access_token):
    """Test getting user stats"""
    print("\n6. Testing Get User Stats")
    print("-" * 80)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{API_URL}/users/me/stats", headers=headers)
    print_response(response)


def test_refresh_token(refresh_token):
    """Test refreshing access token"""
    print("\n7. Testing Refresh Token")
    print("-" * 80)

    refresh_data = {
        "refresh_token": refresh_token
    }

    response = requests.post(f"{API_URL}/auth/refresh", json=refresh_data)
    print_response(response)
    return response.json() if response.status_code == 200 else None


def test_unauthorized_access():
    """Test accessing protected route without token"""
    print("\n8. Testing Unauthorized Access (Should Fail)")
    print("-" * 80)

    response = requests.get(f"{API_URL}/users/me")
    print_response(response)


def main():
    """Run all tests"""
    print("=" * 80)
    print("ZIP Platform API - Authentication Test Suite")
    print("=" * 80)

    # Test health check
    test_health_check()

    # Test unauthorized access first
    test_unauthorized_access()

    # Register a new user
    user = test_register()
    if not user:
        print("\n❌ Registration failed. User might already exist.")
        print("Trying to login with existing credentials...")
        tokens = test_login("john.doe@example.com", "SecurePass123")
    else:
        print(f"\n✅ User registered successfully! ID: {user.get('id')}")
        # Login with the new user
        tokens = test_login("john.doe@example.com", "SecurePass123")

    if not tokens:
        print("\n❌ Login failed. Exiting tests.")
        return

    print(f"\n✅ Login successful!")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    # Test protected routes
    test_get_profile(access_token)
    test_update_profile(access_token)
    test_get_stats(access_token)

    # Test token refresh
    new_tokens = test_refresh_token(refresh_token)
    if new_tokens:
        print("\n✅ Token refresh successful!")

    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
