from flask import Flask, request, jsonify, make_response
from child import Child
from datetime import datetime
from threading import Thread
from child_movement_generator import _run
import csv, json, time

app = Flask(__name__)
children = []
polling_addresses = []
poll_restricted_time = 10
has_update = True
#is_running_simulation = False

def get_default_response(message = ''):
    resp = make_response(message)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def run_function_in_new_thread(some_func):
    thread = Thread(target = some_func)
    thread.start()

'''
A list is maintained, containing all the IPs that are currently polling the webserver.
IPs that currently poll will be put into a waiting loop, waiting for updates.
IPs that ARE NOT polling will be served the current list of children, regardless of the variable "has_update"'s state.
'''
def addr_is_polling(rem_addr):
    for element in polling_addresses:
        if element[0] == rem_addr:
            return True
    return False

def remove_expired_polling_addresses():
    new_pollers = []
    for poller in polling_addresses:
        if poller[1] > time.time():
            new_pollers.append(poller)
    return new_pollers



def init_child_list():
    global children
    child_csv = open("child_info.csv", encoding="utf-8")
    csv_reader = csv.reader(child_csv)
    for row in csv_reader:
        new_child = Child(row[0], row[1], False)
        if new_child.name != "name":
            children.append(new_child)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/check", methods=["PUT", "GET"])
def check_child_in():
    global has_update
    child_id = request.args.get("cid")
    for child in children:
        if child.id == child_id:
            child.status = not child.status
            child.last_change = datetime.now().strftime("%d/%m %H:%M:%S")
            child.history.append((child.status, child.last_change))
            has_update = True
            return get_default_response("Status updated for " + child.name)
    return get_default_response("No child found with that ID...")


@app.route("/status", methods=["GET"])
def daycare_status():
    global children, has_update, polling_addresses
    polling_addresses = remove_expired_polling_addresses()

    if addr_is_polling(request.remote_addr):
        wait_counter = 0
        while wait_counter < 60: #one long-polling "session" lasts 1 minute
            if has_update:
                break
            time.sleep(1)
            wait_counter += 1
        
        if not has_update:
            return ('', 204)    # The HTTP 204 No Content success status response code indicates
                                # that the request has succeeded, but that the client 
                                # doesn't need to go away from its current page. 
                                # A 204 response is cacheable by default.
    else:
        polling_addresses.append((request.remote_addr, time.time()+poll_restricted_time))

    children_j = [child.__dict__ for child in children]
    children_json = {
        "children": children_j
    }
    has_update = False
    return get_default_response(jsonify(children_json))


@app.route("/reset", methods=["GET"])
def reset_daycare():
    global children, has_update
    for child in children:
        child.status = False
    has_update = True
    run_function_in_new_thread(_run)
    return get_default_response("Reset")

if __name__ == "__main__":
    init_child_list()
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
