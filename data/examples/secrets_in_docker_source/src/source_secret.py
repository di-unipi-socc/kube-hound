import requests

api_key = "d91f05e4a2334882d52a6580d851334c"

url = "https://api.example.com/resource"

headers = {
    "Authorization": f"Bearer {api_key}",
}

response = requests.get(url, headers=headers)

print(response.json())