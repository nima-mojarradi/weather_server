import requests
import json
import http.server
from database import WeatherDatabase
import datetime


def get_city_weather(city_name: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    key = "0da42fc97e00bbde9fae47f103a71ca6"
    try:
        # city_name = get_city_name()

        # param = {"q": city_name, "appid": key}
        # res = requests.get(url, param)
        
        
        final_url = url + "?q=" + city_name + "&appid=" + key + "&units=metric"
        response = requests.get(final_url)
        data = response.json()
        temperature = data["main"]["temp"]
        feeling = data["main"]["feels_like"]
        last_update = datetime.datetime.fromtimestamp(data['dt'])
        print(
            f"city: {city_name}, temp: {temperature}^c, feeling:{feeling}^c")
        print(f"last update at: " ,last_update)           
        return {"cityname": {city_name}, "temp": {temperature}, "feeling": {feeling}}
    except KeyError:
        print("error: city does not exist")
    except ValueError:
        print("error:city does not exist")



def start_server() -> None:
    server_address = ('127.0.0.1', 8000)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    httpd.serve_forever()


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        city_name = post_data.decode()

        # request to the weather API and get the response data
        response_data = get_city_weather(city_name)

        db = WeatherDatabase()
        db.save_request_data(city_name, datetime.datetime.now().isoformat())
        db.save_response_data(city_name, response_data)
        #back to client
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

if __name__ == '__main__':
    start_server()

