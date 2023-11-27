import unittest
import weather_server

city = input("enter the name of city: ")
class GetCityWeatherTest(unittest.TestCase):
    def test_get_city_weather(self):
        self.assertIsInstance(weather_server.get_city_weather(city),dict)

if __name__=="__main__":
    unittest.main()