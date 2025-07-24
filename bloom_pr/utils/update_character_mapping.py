import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("STARTGG_API_KEY")

url = "https://api.start.gg/gql/alpha"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

query = """
query Characters {
  videogame(id: 1386) {
    characters {
      id
      name
    }
  }
}
"""

response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()

if "errors" in data:
    print("Erreur:", data["errors"])
else:
    chars = data["data"]["videogame"]["characters"]
    for char in chars:
        print(f"{char['id']}: \"{char['name']}\",")
