# FlexiFit Backend API 🏋️‍♂️

FlexiFit uygulaması için geliştirilmiş, yüksek performanslı ve önbellek destekli RESTful Web API projesi.

## 🚀 Özellikler
* **Hızlı Yanıt Süreleri:** Sık sorgulanan kullanıcı veya antrenman verileri **Redis** kullanılarak önbelleğe (cache) alınır ve veritabanı yükü hafifletilir.
* **Kullanıcı ve Veri Yönetimi:** Kullanıcı kayıtları, kimlik doğrulama (authentication) ve profil verileri **SQLite** üzerinde güvenli bir şekilde saklanır.
* **Modüler Mimari:** Flask ile ölçeklenebilir ve yönetilebilir REST uç noktaları (endpoints) tasarlanmıştır.

## 🛠️ Teknoloji Yığını
* **Backend:** Python, Flask
* **Veritabanı:** SQLite
* **Önbellekleme (Cache):** Redis

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/AdilMammadov29/flexifit-backend.git](https://github.com/AdilMammadov29/flexifit-backend.git)
   cd flexifit-backend
