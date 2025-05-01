from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId  # needed to look up by application number

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["loanApplications"]
collection = db["applications"]

counters = db["counters"]

# Initialize counter if it doesn't exist
if counters.count_documents({"name": "application_counter"}) == 0:
    counters.insert_one({"name": "application_counter", "value": 0})

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API: Add new application and return application number
@app.route('/api/add_application', methods=['POST'])
def add_application():
    data = request.get_json()
    name = data.get("name")
    zipcode = data.get("zipcode")

    # Get and increment the application number
    counter_doc = counters.find_one_and_update(
        {"name": "application_counter"},
        {"$inc": {"value": 1}},
        return_document=True
    )
    application_number = counter_doc["value"]

    application = {
        "application_number": application_number,
        "name": name,
        "zipcode": zipcode,
        "status": "received",
        "notes": []
    }

    collection.insert_one(application)
    return jsonify({
        "message": "Application submitted.",
        "application_number": application_number
    })

# API: Check status using application number
@app.route('/api/check_status', methods=['POST'])
def check_status():
    data = request.get_json()
    try:
        app_id = int(data.get("application_number"))
    except:
        return jsonify({"status": "not found"})

    app_data = collection.find_one({"application_number": app_id})
    if app_data:
        return jsonify({"status": app_data["status"]})
    else:
        return jsonify({"status": "not found"})

# API: Update status using application number
@app.route('/api/update_status_by_id', methods=['POST'])
def update_status_by_id():
    data = request.get_json()
    try:
        app_id = int(data.get("application_number"))
        status = data.get("status")
    except:
        return jsonify({"message": "Invalid input."})

    result = collection.update_one(
        {"application_number": app_id},
        {"$set": {"status": status}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Status updated."})
    else:
        return jsonify({"message": "Application not found."})

# API: Update status by name (original method)
@app.route('/api/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    name = data.get("name")
    status = data.get("status")

    result = collection.update_one({"name": name}, {"$set": {"status": status}})
    return jsonify({"message": "Status updated." if result.modified_count > 0 else "Application not found."})

# API: Add a note by name
from datetime import datetime  # Add this at the top if it's not already there

@app.route('/api/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    name = data.get("name")
    subphase = data.get("subphase")
    message = data.get("message")

    note = {
        "subphase": subphase,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    result = collection.update_one(
        {"name": name},
        {"$push": {"notes": note}}
    )

    return jsonify({"message": "Note added." if result.modified_count > 0 else "Application not found."})

# API: View notes by name
@app.route('/api/notes', methods=['GET'])
def get_notes():
    name = request.args.get("name")
    app_data = collection.find_one({"name": name}, {"_id": 0})
    if app_data:
        return jsonify(app_data)
    return jsonify({"message": "Application not found."})

@app.route('/api/get_notes_by_id', methods=['POST'])
def get_notes_by_id():
    data = request.get_json()
    try:
        app_id = int(data.get("application_number"))
    except:
        return jsonify({"message": "Invalid application number."})

    app_data = collection.find_one({"application_number": app_id}, {"_id": 0, "notes": 1})
    if app_data:
        return jsonify(app_data)
    return jsonify({"message": "Application not found."})

if __name__ == "__main__":
    app.run(debug=True)
