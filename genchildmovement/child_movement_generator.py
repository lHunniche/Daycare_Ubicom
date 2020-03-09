import requests
import pandas as pd
import time
import random

url = "http://klevang.dk:8080/check?cid="
filename = 'genchildmovement/child_info.csv'
data = pd.read_csv(filename)
min_sleep = 5
max_sleep = 20

day_length = 80


def generate_random_timestamps():
    global data
    for i in range(len(data)):
        _id = data.loc[i, "id"]
        child = {
            "name": data.loc[i, "name"],
            "id": _id
        }
        update_child_statuses(_id)
        sleep_for_random_amount_of_time()
    sleep_for_a_day()

def sleep_for_a_day():
    global day_length
    time.sleep(day_length)

def update_child_statuses(_id, child):
    global url
    check_url = url + _id
    requests.put(check_url, data=data).text


def sleep_for_random_amount_of_time():
    global min_sleep
    global max_sleep
    rd = random.randint(min_sleep, max_sleep)
    time.sleep(rd)


def _run():
    while True:
        generate_random_timestamps()

_run()
