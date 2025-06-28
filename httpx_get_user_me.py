import httpx

login_payload = {
  "email": "xxxxx@gmail.com",
  "password": '12345'
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json = login_payload)
login_response_data = login_response.json()
print("Login response: ", login_response_data)
print("Status_code: ", login_response.status_code)

access_payload = {"accessToken": login_response_data["token"]["accessToken"]}

headers = {"Authorization" : f'Bearer {login_response_data["token"]["accessToken"]}'}
user_response = httpx.get("http://localhost:8000/api/v1/users/me", headers = headers)
user_response_data = user_response.json()
print("User Response: ", user_response_data)
print("Status_code: ", user_response.status_code)
