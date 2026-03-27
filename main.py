import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi
from datetime import datetime

app = Flask(__name__)
CORS(app) # Güvenlik duvarını tüm domainler için açtık

# MongoDB Bağlantısı
MONGO_URI = "mongodb+srv://mamedoff2910_db_user:Adil291006@adilmammadov.vjv3p8n.mongodb.net/?appName=AdilMammadov"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.FlexiFitDatabase
users_collection = db.users

# ==========================================
# 1. ANA SİSTEM (Kayıt / Giriş)
# ==========================================

@app.route('/')
def home():
    return "Adil'in FlexiFit API'si Calisiyor!", 200

@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        if users_collection.find_one({"email": data['email']}):
            return jsonify({"error": "Bu email zaten kayitli!"}), 400
        
        data['theme'] = 'light'
        data['consumption_history'] = []
        data['current_weight'] = data.get('weight', 0)
        
        users_collection.insert_one(data)
        return jsonify({"message": "Kayit basarili!"}), 201
    except Exception as e:
        return jsonify({"error": "Veritabani hatasi: " + str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = users_collection.find_one({"email": data['email'], "password": data['password']})
        if user:
            return jsonify({
                "message": "Giris basarili!", 
                "user": {"email": user['email'], "full_name": user.get('full_name', '')}
            }), 200
        return jsonify({"error": "Hatali email veya sifre!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ==========================================

# Tüketim Ekle
@app.route('/api/consumption', methods=['POST'])
def add_consumption():
    data = request.json
    email = data.get('email')
    item = {
        "name": data.get('name'), 
        "calories": data.get('calories'), 
        "water_ml": data.get('water_ml', 0), 
        "date": str(datetime.now())
    }
    users_collection.update_one({"email": email}, {"$push": {"consumption_history": item}})
    return jsonify({"message": "Tuketim basariyla eklendi."}), 200

# Profil Görüntüle
@app.route('/api/profile/<email>', methods=['GET'])
def get_profile(email):
    user = users_collection.find_one({"email": email}, {"_id": 0, "password": 0})
    return jsonify(user) if user else (jsonify({"error": "Kullanici bulunamadi"}), 404)

# Geçmişi Görüntüle
@app.route('/api/history/<email>', methods=['GET'])
def get_history(email):
    user = users_collection.find_one({"email": email}, {"_id": 0, "consumption_history": 1})
    return jsonify(user.get("consumption_history", [])) if user else (jsonify({"error": "Kullanici bulunamadi"}), 404)

# HAFTALIK ÖZET (Grafik ve Çizelge İçin Eklenen Yeni Kod)
@app.route('/api/weekly-summary/<email>', methods=['GET'])
def get_weekly_summary(email):
    user = users_collection.find_one({"email": email})
    if not user: return jsonify({"error": "Kullanici bulunamadi"}), 404
    
    history = user.get("consumption_history", [])
    summary = {}
    for item in history:
        date_str = item['date'][:10] # Sadece YYYY-MM-DD kısmını al
        summary[date_str] = summary.get(date_str, 0) + item['calories']
    return jsonify(summary)

# Kilo Güncelle (PUT)
@app.route('/api/update-weight', methods=['PUT'])
def update_weight():
    data = request.json
    users_collection.update_one({"email": data['email']}, {"$set": {"current_weight": data['new_weight']}})
    return jsonify({"message": "Kilo guncellendi."}), 200

# Kaydı Sil (DELETE)
@app.route('/api/delete-food', methods=['DELETE'])
def delete_food():
    data = request.json
    users_collection.update_one({"email": data['email']}, {"$pull": {"consumption_history": {"name": data['food_name']}}})
    return jsonify({"message": "Kayit silindi."}), 200

# Hesabı Sil (DELETE)
@app.route('/api/delete-account', methods=['DELETE'])
def delete_account():
    data = request.json
    users_collection.delete_one({"email": data['email']})
    return jsonify({"message": "Hesap tamamen silindi."}), 200

# Öğün Önerisi (AI)
@app.route('/api/recommendation/<int:hour>', methods=['GET'])
def get_recommendation(hour):
    if 6 <= hour < 11:
        return jsonify({"meal": "Kahvalti", "suggestion": "Yulaf ezmesi ve 2 haslanmis yumurta"})
    elif 11 <= hour < 15:
        return jsonify({"meal": "Ogle Yemegi", "suggestion": "Izgara tavuk gogsu ve kinoa salatasi"})
    elif 15 <= hour < 19:
        return jsonify({"meal": "Ara Ogun", "suggestion": "1 porsiyon meyve ve 10 adet cig badem"})
    else:
        return jsonify({"meal": "Aksam Yemegi", "suggestion": "Firinda somon ve buharda brokoli"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
