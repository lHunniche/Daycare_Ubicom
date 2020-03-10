from flask import Flask, request, jsonify, make_response
from child import Child
from datetime import datetime
import csv, json, time

app = Flask(__name__)
children = []
has_update = True

def get_default_response(message = ''):
    resp = make_response(message)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def init_child_list():
    global children
    child_csv = open("../genchildmovement/child_info.csv", encoding="utf-8")
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
            has_update = True
            return get_default_response("Status updated for " + child.name)
    return get_default_response("No child found with that ID...")


@app.route("/status", methods=["GET"])
def daycare_status():
    global children, has_update
    wait_counter = 0
    while not has_update and wait_counter < 30: #one long-polling "session" lasts 1 minute
        time.sleep(2)
        wait_counter += 1
        #print(request.remote_addr, "is Long polling, and waiting for updates...")
    
    if not has_update:
        get_default_response()

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
    return get_default_response("Reset")

if __name__ == "__main__":
    init_child_list()
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
