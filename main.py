from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
import requests
import pandas
import json

GUI = Builder.load_file("screen.kv")

class MyApp(App):
    def build(self):
        return GUI
    
    def on_start(self): 
        codes = []
        coins = []
        for keys, values in self.get_coins().items():
            for value in values.values():
                if keys == 'Code':
                    codes.append(value)
                else:
                    coins.append(value)

        for i in range(len(codes) - 1):
            label = self.create_label(codes[i], coins[i])
            if label != None:
                self.root.add_widget(label)
        
    def create_label(self, code, coin):
        quote = self.get_currency_quote_rate(code)
        if quote != None:
            return Label(text = f"{coin} R$ {quote}")
        else:
            return None

    def get_currency_quote_rate(self, code):
        link = f"https://economia.awesomeapi.com.br/last/{code}-BRL"
        print(link)
        request = requests.get(link) 

        if request.status_code == 200:
            request_json = request.json()
            quote = request_json[f"{code}BRL"]["bid"]
            return quote

    def get_coins(self):
        coins_excel = pandas.read_excel('coins.xlsx', sheet_name='Coins to BRL')
        coins_json_str = coins_excel.to_json()
        coins_json = json.loads(coins_json_str)
        return coins_json

MyApp().run()