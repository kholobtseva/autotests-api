import httpx
from tools.fakers import get_random_email

payload = {
  "email": get_random_email(),
  "password": "string",
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}

response = httpx.post("http://localhost:8000/api/v1/users", json = payload)

print("Status_code: ", response.status_code)
print("User Response: ", response.json())
