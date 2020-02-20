import requests

serv = input()
port = int(input())
a = int(input())
b = int(input())

response = requests.get(f"{serv}:{port}", params={"a": a, "b": b})
json_response = response.json()
print(*sorted(json_response["result"]))
print(json_response["check"])
