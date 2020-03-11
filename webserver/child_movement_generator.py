import requests
import pandas as pd
import time
import random


url = "http://localhost:8080/check?cid="
filename = 'child_info.csv'
data = pd.read_csv(filename)


min_sleep = 1
max_sleep = 3

day_length = 5

is_simulation_running = False

def generate_random_timestamps():
    global data
    ids = data["id"].tolist()
    random.shuffle(ids)
    for _id in ids:
        update_child_statuses(_id)
        sleep_for_random_amount_of_time()
    sleep_for_a_day()

def sleep_for_a_day():
    global day_length
    time.sleep(day_length)

def update_child_statuses(_id):
    global url
    check_url = url + str(_id)
    requests.put(check_url).text


def sleep_for_random_amount_of_time():
    global min_sleep, max_sleep
    rd = random.uniform(min_sleep, max_sleep)
    time.sleep(rd)


def _run():
    global is_simulation_running
    if is_simulation_running:
        return

    is_simulation_running = True
    for _ in range(2):
        generate_random_timestamps()
    is_simulation_running = False



if __name__ == "__main__":
    _run()
