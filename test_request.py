import requests


file_path = "sample.txt"
url = "http://localhost:5000/generate"

with open(file_path, "rb") as f:
    files = {"transcript": f}
    response = requests.post(url, files=files)

print("✅ Response status:", response.status_code)
print("📝 Response JSON:", response.json())
