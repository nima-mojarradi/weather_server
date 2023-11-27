import requests


def start_client():
    city_name = input("Enter a city name: ")
    res = requests.post("http://127.0.0.1:8000", city_name.encode())
    data = res.json()
    print(data)
    if data.get("error"):
        print("invalid")
    else:
        print(
            f'"cityname": {city_name}, "temp": {data["temperature"]}, "feeling": {data["feeling"]}')


if __name__ == "__main__":
    start_client()
