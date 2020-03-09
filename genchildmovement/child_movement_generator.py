import requests
import csv



url = "https://klevang.dk/ubicom"
data = open("child_info.csv", 'w')

print(data)



#def generate_random_timestamps():




def update_child_statuses():
    requests.put(url, data=data).text


