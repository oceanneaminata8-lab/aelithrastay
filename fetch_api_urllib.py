import urllib.request
import json

try:
    with urllib.request.urlopen('http://127.0.0.1:8000/api/properties/1/') as response:
        data = response.read().decode('utf-8')
        print(json.dumps(json.loads(data), indent=2))
except Exception as e:
    print(f"Error: {e}")
