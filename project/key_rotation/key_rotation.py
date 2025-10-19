import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv, set_key
from datetime import datetime
from db_connection import client
from logger import logger


db = client["BadBoys"]
dek_key_collection = db["3DES_DEKS"]
dek_key_logs_collection = db["3DES_DEKS_LOGS"]
oldest_dek_doc = dek_key_collection.find_one(sort=[("_id", -1)])
new_des_deks_id = oldest_dek_doc['3DES_DEK_ID'] +1

#To-Do: Tam path verme çalıştırmanın yollarını araştır.
dotenv_path = r"C:\Users\Mehme\Masaüstü\Projects\BadBoysProject\key_rotation\.env"
load_dotenv(dotenv_path)

MASTER_3DES_KEY = bytes.fromhex(os.getenv("MASTER_3DES_KEY"))


logger(new_des_deks_id,
       1, 
       "Başlangıç", 
       f"Başlangıç; {new_des_deks_id-1} 3DES_DEK_ID li eski dek key alındı. MASTER_3DES_KEY alındı.")
# --------------------------
# 3DES şifreleme fonksiyonu
# --------------------------
def des3_encrypt(key: bytes, data: bytes) -> bytes:

    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.encrypt(data)

# 🔹 Key unwrap (padding yok)
def des3_decrypt(key: bytes, data: bytes) -> bytes:

    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.decrypt(data)

# --------------------------
# Master Key Şifresini Çöz
# --------------------------
decrypted_master_key = des3_decrypt(bytes.fromhex(oldest_dek_doc["dek"]), MASTER_3DES_KEY)
print("Yeni çözülmüş MASTER_3DES_KEY:", decrypted_master_key.hex())
logger(new_des_deks_id,
       2, 
       "Master Key Şifresini Çöz", 
       f"Master Key Şifresini Çöz; Master key şifresi çözüldü. Ham Master Key: {decrypted_master_key.hex()}")

# --------------------------
# Master Key Şifrele
# --------------------------

new_dek = os.urandom(24)
encrypted_master_key = des3_encrypt(new_dek, decrypted_master_key)
print("Şifrelenmiş MASTER_3DES_KEY (yeni DEK ile):", encrypted_master_key.hex())
logger(new_des_deks_id,
       3, 
       "Master Key Şifrele", 
       f"Master Key Şifrele; Master key şifresi şifrelendi. \nŞifrelenmiş hali: {decrypted_master_key.hex()} \n Yeni Dek: {new_dek}")

# --------------------------
# Şifrelenmiş Master Keyi yaz
# --------------------------

# .env dosyasına yaz
set_key(dotenv_path, "MASTER_3DES_KEY", encrypted_master_key.hex())
logger(new_des_deks_id,
       4, 
       "Şifrelenmiş Master Keyi yaz", 
       f"Şifrelenmiş Master Keyi yaz; {encrypted_master_key.hex()}")


# --------------------------
# DEK ve encrypted master key'i kaydet
# --------------------------
dek_doc = {
    "dek": new_dek.hex(),
    "create_date": datetime.now(),
    "status": "A",
    "rotate_date": None,
    "3DES_DEK_ID": oldest_dek_doc['3DES_DEK_ID']+1
}
dek_key_collection.insert_one(dek_doc)

dek_log_doc = {
    "dek": new_dek.hex(),
    "encrypted_master_key": encrypted_master_key.hex(),
    "create_date": datetime.now()
}
dek_key_logs_collection.insert_one(dek_log_doc)

print("DEK ve encrypted MASTER key başarıyla kaydedildi.")

# Yeni şifrelenmiş master key
encrypted_master_key = encrypted_master_key.hex()


# .env dosyasına yaz
set_key(dotenv_path, "MASTER_3DES_KEY", encrypted_master_key)
print(".env dosyası güncellendi: MASTER_3DES_KEY")

print('yeni master key ', encrypted_master_key)
print('yeni dek, ', new_dek.hex())

