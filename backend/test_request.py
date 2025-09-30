import requests


url = "http://127.0.0.1:8000/predict/"


image_path = "images/example.jpg"

with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Status code:", response.status_code)
print("Resposta JSON:", response.json())
