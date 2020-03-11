import requests
import pandas as pd
import time
import random

url = "http://klevang.dk:8080/check?cid="
filename = 'child_info.csv'
data = pd.read_csv(filename)


min_sleep = 0.2
max_sleep = 1

day_length = 5

def generate_random_timestamps():
    global data
    ids = data["id"].tolist()
    shuf_ids = random.shuffle(ids)
    print(ids)
    for _id in ids:
        print("updating: ", _id)
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
    global min_sleep
    global max_sleep
    rd = random.uniform(min_sleep, max_sleep)
    print("sleeping for: ", rd, " seconds")
    time.sleep(rd)


def _run():
    requests.get("http://klevang.dk:8080/reset").text
    while True:
        generate_random_timestamps()


if __name__ == "__main__":
    _run()
