from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pymongo import MongoClient
# from bson import ObjectId

# Connect to MongoDB (modify connection string as needed)
client = MongoClient("mongodb+srv://rohith123:1.....m@cluster0.qttl3mr.mongodb.net/CAD?retryWrites=true&w=majority")
db = client["CAD"]  # Database name
 # Collection name

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

modules = [
    {"title": "React", "content": "ReactJS is a component-based JavaScript library used to build dynamic and interactive user interfaces. It simplifies the creation of single-page applications (SPAs) with a focus on performance and maintainability.It is developed and maintained by Facebook.Uses a virtual DOM for faster updates."},
    {"title": "Flask", "content": "Flask is a micro web framework that helps developers build web applications. It's a collection of libraries and modules that use the Python programming language. Flask is lightweight and flexible, and is often used to create dynamic websites, APIs, and microservices. "}
]

mcqs = [
    {"question": "What is Flask?", "options": ["A Python framework", "A JavaScript library", "A database"], "answer": "A Python framework"},
    {"question": "What is React?", "options": ["A Python framework", "A JavaScript library", "A database"], "answer": "A JavaScript library"}
]

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

tasks = [
    {"id": 1, "title": "Task 1", "status": "Pending"},
    {"id": 2, "title": "Task 2", "status": "Completed"}
]

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/modules", methods=["GET"])
def get_modules():
    collection = db["learning"] 
    doc = collection.find_one({"employeeId": 10}, {"React", "Flask"})

    return jsonify(modules)

@app.route("/mcqs", methods=["GET"])
def get_mcqs():
    return jsonify(mcqs)

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)
