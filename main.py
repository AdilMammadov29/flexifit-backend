import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# BU SATIR: Dünyadaki her yerin (Vercel dahil) senin API'ne bağlanmasına izin verir.
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

MONGO_URI ="mongodb+srv://mamedoff2910_db_user:Adil291006@adilmammadov.vjv3p8n.mongodb.net/?appName=AdilMammadov"
client = MongoClient(MONGO_URI)
db = client.FlexiFitDatabase
users_collection = db.users

@app.route('/')
def home():
    return "Adil'in FlexiFit API'si Calisiyor!", 200

@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        if users_collection.find_one({"email": data['email']}):
            return jsonify({"error": "Bu email zaten kayitli!"}), 400
        users_collection.insert_one(data)
        return jsonify({"message": "Kayit basarili!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = users_collection.find_one({"email": data['email'], "password": data['password']})
        if user:
            return jsonify({"message": "Giris basarili!"}), 200
        return jsonify({"error": "Hatali email veya sifre!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
