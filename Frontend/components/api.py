import requests

BASE_URL = "http://localhost:8000"

def upload_resume(file):
    files = {"file": file}
    response = requests.post(f"{BASE_URL}/upload-resume", files=files)
    return response.json()

def get_skill_gap(user_id):
    response = requests.get(f"{BASE_URL}/skill-gap/{user_id}")
    return response.json()

def get_roadmap(user_id):
    response = requests.get(f"{BASE_URL}/roadmap/{user_id}")
    return response.json()

def chat_with_ai(message):
    response = requests.post(f"{BASE_URL}/chat", json={"message": message})
    return response.json()