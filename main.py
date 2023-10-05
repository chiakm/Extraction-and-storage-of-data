# Use https://www.wunderground.com/weather/se/borlänge for Assignment
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
import requests 
import csv
import json


class HomeScreen(Screen):
    firebase_url = 'https://firstone-398d9-default-rtdb.firebaseio.com/.json'
    weather = StringProperty()
    description = StringProperty()
    humidity = StringProperty()
    pressure = StringProperty()
    visibility = StringProperty()
    city_name = StringProperty()
    country_name = StringProperty()

    def search(self):
    
        
        city_name = self.ids.city_name.text
        country_name = self.ids.country_name.text
    
        # Try scraping from the first URL
        url1 = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'
        try:
            response = requests.get(url=url1)
            print(response.status_code)
    
            soup = BeautifulSoup(response.text,'html.parser')
            mainclass = soup.find(class_='bk-focus__qlook')
            secondclass = soup.find(class_='bk-focus__info')
            self.weather = mainclass.find(class_='h2').get_text()
            self.visibility = secondclass.findAll('td')[3].get_text()  # can also try slicing
            self.pressure = secondclass.findAll('td')[4].get_text()
            self.humidity = secondclass.findAll('td')[5].get_text()
        except:
            # If the first URL fails, try scraping from the second URL
            url2 = f'https://www.wunderground.com/weather/se/borlänge'
            response = requests.get(url=url2)
            print(response.status_code)
    
            soup = BeautifulSoup(response.text,'html.parser')
            mainclass = soup.find(class_='small-12 medium-6 columns')
            secondclass = soup.find(class_= 'small-12 medium-6 columns large-6')
            self.weather = mainclass.find(class_ ='current-temp').get_text()
            self.visibility = secondclass.findAll(class_='wu-value wu-value-to')[1].get_text()  # can also try slicing
            self.pressure = secondclass.findAll(class_='wu-value wu-value-to')[0].get_text()
            self.humidity = secondclass.findAll(class_='wu-value wu-value-to')[3].get_text()

        # Save the extracted weather data in a CSV file
        with open('weather_data.csv', 'a', newline='') as csvfile:
            headers = ['City','Country','Weather', 'Visibility', 'Pressure', 'Humidity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            writer.writerow({'City': city_name , 'Country':country_name ,'Weather': self.weather, 'Visibility': self.visibility,
                            'Pressure': self.pressure, 'Humidity': self.humidity})



            weather = self.weather
            visibility = self.visibility
            pressure = self.pressure
            humidity = self.humidity

            json_data = '{"ExtractedData":{"City": "' + city_name + '", "Country": "' + country_name + '", "Weather": "' + weather + '", "Visibility": "' + visibility + '", "Pressure": "' + pressure + '", "Humidity": "' + humidity + '"}}'
            res = requests.post(url=self.firebase_url, json=json.loads(json_data))
            print(response.status_code)
            print(res)
    
    

class MainApp(MDApp):
    def build(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        Window.size = (400, 600)

MainApp().run()