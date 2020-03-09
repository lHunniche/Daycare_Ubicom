from flask import Flask, request, jsonify, make_response
from child import Child
import csv
import json

app = Flask(__name__)
children = []

def init_child_list():
    global children
    child_csv = open("../genchildmovement/child_info.csv", encoding="utf-8")
    csv_reader = csv.reader(child_csv)
    for row in csv_reader:
        new_child = Child(row[0], row[1], False)
        children.append(new_child)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/check", methods=["POST", "GET"])
def check_child_in():
    child_id = request.args.get("cid")
    for child in children:
        if child.id == child_id:
            if child.status:
                child.status = not child.status
                return "Checking " + child.name + " out."
            else:
                child.status = not child.status
                return "Checking " + child.name + " in."
    return "No child found with that ID..."


@app.route("/status", methods=["GET"])
def daycare_status():
    global children
    children_j = [child.__dict__ for child in children]
    children_json = {
        "children": children_j
    }
    return jsonify(children_json), 200

if __name__ == "__main__":
    init_child_list()
    app.run(debug=True, host='127.0.0.1', port=8080)
